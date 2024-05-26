from fastapi import FastAPI, HTTPException, requests
from sqlalchemy.engine import row
from sqlalchemy.orm import Session
from models import Base, Pokemon, Type, engine
from pydantic import BaseModel
import requests

from query import find_by_type, find_pokemons_of_trainer

app = FastAPI()


# Pydantic models to validate data


class PokemonCreate(BaseModel):
    name: str


def fetch_pokemon_types(pokemon_name):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
    if response.status_code == 200:
        types = [type_info['type']['name'] for type_info in response.json()['types']]
        return types
    else:
        return None


def fetch_pokemon_details(pokemon_name):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
    if response.status_code == 200:
        data = response.json()
        details = {
            'height': data['height'],  # Height in decimeters
            'weight': data['weight']  # Weight in hectograms
        }
        return details
    else:
        print(f"Failed to fetch data for {pokemon_name}. Status code: {response.status_code}")
        return None


"""
# Example usage
pokemon_name = "igglybuff" #"pikachu"
pokemon_details = fetch_pokemon_details(pokemon_name)
if pokemon_details:
    print(f"Height: {pokemon_details['height']}, Weight: {pokemon_details['weight']}")
    print(str(fetch_pokemon_types(pokemon_name)))
"""


@app.post("/pokemon/")
def add_pokemon(pokemon: PokemonCreate):
    db = Session(bind=engine)
    db_pokemon = db.query(Pokemon).filter(Pokemon.name == pokemon.name).first()
    if db_pokemon:
        db.close()
        raise HTTPException(status_code=400, detail="Pokemon already exists")

    types = fetch_pokemon_types(pokemon.name)
    details = fetch_pokemon_details(pokemon.name)
    if types is None or details is None:
        db.close()
        raise HTTPException(status_code=400, detail="Pokemon does not exist")

    new_pokemon = Pokemon(name=pokemon.name, height=details["height"], weight=details["weight"])
    db.add(new_pokemon)

    for pt in types:
        type_instance = db.query(Type).filter(Type.type == pt).first()
        if not type_instance:
            type_instance = Type(type=pt)
            db.add(type_instance)
        new_pokemon.types.append(type_instance)

    db.commit()
    db.close()
    return {"status": "Pokemon added successfully"}


@app.get("/pokemon/by_type")
def get_pokemon_by_type(type):
    return find_by_type(type)


@app.get("/pokemon/by_trainer")
def get_pokemon_by_trainer(trainer_name):
    return find_pokemons_of_trainer(trainer_name)

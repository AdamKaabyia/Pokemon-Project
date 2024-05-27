from fastapi import APIRouter, HTTPException, requests
from sqlalchemy.orm import Session
from models import Base, Pokemon, Type, engine, Trainer, Type_Enrollment

from query import find_by_type, find_pokemons_of_trainer, find_owners
from utils import fetch_pokemon_types, fetch_pokemon_details

router = APIRouter()


@router.post("/")
def add_pokemon(pokemon_name: str):
    with Session(bind=engine) as session:
        db_pokemon = session.query(Pokemon).filter(Pokemon.name == pokemon_name).first()
        if db_pokemon:
            raise HTTPException(status_code=400, detail="Pokemon already exists")

        types = fetch_pokemon_types(pokemon_name)
        details = fetch_pokemon_details(pokemon_name)
        if not types or not details:
            raise HTTPException(status_code=404, detail="Pokemon data not found")

        new_pokemon = Pokemon(name=pokemon_name, height=details["height"], weight=details["weight"])
        session.add(new_pokemon)
        session.flush()  # Flush to assign an ID to new_pokemon

        for pt in types:
            type_instance = session.query(Type).filter(Type.type == pt).first()
            if not type_instance:
                type_instance = Type(type=pt)
                session.add(type_instance)
                session.flush()  # Ensuring type_instance.id is available for relationship

            new_type_enrollment=Type_Enrollment(type_id=type_instance.id,poke_id=new_pokemon.id)
            session.add(new_type_enrollment)
            session.flush()
        session.commit()
        return {"status": "success", "message": "Pokemon added successfully"}



@router.get("/by_type")
def get_pokemon_by_type(type):
    return find_by_type(type)


@router.get("/by_trainer")
def get_pokemon_by_trainer(trainer_name):
    return find_pokemons_of_trainer(trainer_name)


@router.get("/by_pokemon")
def get_trainers_by_pokemons(pokemon_name):
    return find_owners(pokemon_name)


@router.delete("/")
def delete_pokemon_of_trainer(poke_name, trainer_name):
    db = Session(bind=engine)
    db_pokemon = db.query(Pokemon).filter(Pokemon.name == poke_name).first()
    if not db_pokemon:
        db.close()
        raise HTTPException(status_code=400, detail="Pokemon does not exist")
    db_trainer = db.query(Trainer).filter(Trainer.name == trainer_name).filter(Trainer.poke_id == db_pokemon.id).first()
    if not db_trainer:
        db.close()
        raise HTTPException(status_code=400, detail="Pokemon does not exist")

    db.delete(db_trainer)
    db.commit()
    db.close()

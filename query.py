from load_data import Session
from models import Pokemon, Type, Trainer, engine


#query 1
def find_by_type(pokemon_type):
    session = Session()
    try:
        # Query to find all Pokemon of a given type
        results = session.query(Pokemon). \
            join(Type, Pokemon.id == Type.poke_id). \
            filter(Type.type == pokemon_type). \
            all()

        # Extracting Pokemon names from the query results and removing duplicates
        pokemon_names = list(set(pokemon.name for pokemon in results))
        return pokemon_names
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        session.close()


# Example usage
"""
pokemon_names = find_by_type('grass')
print(pokemon_names)
"""


def find_owners(pokemon_name):
    session = Session()
    try:
        # Query to find all trainers of a given Pokemon by name
        results = session.query(Trainer.name). \
            join(Pokemon, Trainer.poke_id == Pokemon.id). \
            filter(Pokemon.name == pokemon_name). \
            all()

        # Extracting trainer names from the query results
        trainer_names = [result[0] for result in results]  # result[0] because query returns a list of tuples
        return trainer_names if trainer_names else []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        session.close()


# Example usage
"""owner_names = find_owners('gengar')
print(owner_names)
"""


def find_pokemons_of_trainer(trainer_name):
    session = Session(bind=engine)
    try:
        # Query to find the trainer by name and get the associated Pokémon
        trainer_pokemons = session.query(Pokemon).\
            join(Trainer, Trainer.poke_id == Pokemon.id).\
            filter(Trainer.name == trainer_name).\
            all()

        if not trainer_pokemons:
            print(f"No Pokémon found for trainer named {trainer_name}.")
            return []

        # Extracting Pokemon names owned by the trainer
        pokemon_names = [pokemon.name for pokemon in trainer_pokemons]
        return pokemon_names

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        session.close()

# Example usage
pokemon_names = find_pokemons_of_trainer('Loga')
print(pokemon_names)

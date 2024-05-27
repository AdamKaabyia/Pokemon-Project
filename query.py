from load_data import Session
from models import Pokemon, Type, Trainer, engine, Type_Enrollment, Trainer_Enrollment


#query 1
def find_by_type(pokemon_type):
    session = Session()
    try:
        # Query to find all Pokemon of a given type using the Type_Enrollment table for many-to-many relationship
        results = session.query(Pokemon).join(Type_Enrollment).join(Type).filter(Type.type == pokemon_type).all()
        # Extracting Pokemon names from the query results and removing duplicates
        pokemon_names = list(set(pokemon.name for pokemon in results))
        return pokemon_names
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        session.close()


# Example usage
""""
pokemon_names = find_by_type('grass')
print(pokemon_names)
"""


def find_owners(pokemon_name):
    session = Session()
    try:
        # This query should now properly get the trainers associated with the given Pokemon name
        results = session.query(Pokemon).join(Trainer_Enrollment, Pokemon.trainers).join(Trainer, Trainer_Enrollment.trainer).filter(Pokemon.name == pokemon_name).all()

        # Extracting trainer names from the query results
        trainer_names = []
        for pokemon in results:
            # Check and extract trainers properly
            if pokemon.trainers:  # Making sure there are trainers associated
                for enrollment in pokemon.trainers:
                    trainer_names.append(enrollment.trainer.name)

        return trainer_names if trainer_names else []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        session.close()


# Example usage
"""
owner_names = find_owners('gengar')
print(owner_names)
"""


def find_pokemons_of_trainer(trainer_name):
    session = Session(bind=engine)
    try:
        trainer_pokemons = session.query(Pokemon).join(Trainer_Enrollment).join(Trainer).filter(Trainer.name == trainer_name).all()

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
"""
pokemon_names = find_pokemons_of_trainer('Loga')
print(pokemon_names)
"""
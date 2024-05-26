import json
from sqlalchemy.orm import sessionmaker
from models import Pokemon, Trainer, Trainer_Enrollment, Type, Type_Enrollment, engine

# Create a Session
Session = sessionmaker(bind=engine)
session = Session()


def loadDB():
    # Load JSON data
    with open('pokemons_data.json', 'r') as file:
        data = json.load(file)

    # Insert data into database
    for entry in data:
        # Insert Pokemon
        pokemon = Pokemon(id=entry['id'], name=entry['name'], height=entry['height'], weight=entry['weight'])
        session.add(pokemon)

        # Insert Trainers and Trainer_Enrollments
        for trainer_data in entry.get('ownedBy', []):
            # Check if the trainer already exists
            trainer = session.query(Trainer).filter_by(name=trainer_data['name'], town=trainer_data['town']).first()
            if not trainer:
                trainer = Trainer(name=trainer_data['name'], town=trainer_data['town'])
                session.add(trainer)
                session.flush()  # Ensures trainer.id is available

            trainer_enrollment = Trainer_Enrollment(trainer_id=trainer.id, poke_id=pokemon.id)
            session.add(trainer_enrollment)

        # Insert Types and Type_Enrollments
        for type_name in entry.get('types', []):
            # Check if the type already exists
            type_instance = session.query(Type).filter_by(type=type_name).first()
            if not type_instance:
                type_instance = Type(type=type_name)
                session.add(type_instance)
                session.flush()  # Ensures type_instance.id is available

            type_enrollment = Type_Enrollment(type_id=type_instance.id, poke_id=pokemon.id)
            session.add(type_enrollment)

    # Commit the transaction
    session.commit()
    # Close the session
    session.close()

    print("Database has been populated with SQLAlchemy.")


# Call loadDB to populate the database with data from JSON file
loadDB()

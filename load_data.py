import json

from sqlalchemy.orm import sessionmaker

from models import *

# Create a Session
Session = sessionmaker(bind=engine)
session = Session()

# Load JSON data
with open('pokemons_data.json', 'r') as file:
    data = json.load(file)

# Insert data into database
for entry in data:
    pokemon = Pokemon(id=entry['id'], name=entry['name'], height=entry['height'], weight=entry['weight'])
    session.add(pokemon)

    # Insert trainers
    for trainer in entry.get('ownedBy', []):
        new_trainer = Trainer(name=trainer['name'], town=trainer['town'], pokemon=pokemon)
        session.add(new_trainer)

    # Insert types
    for type_name in entry.get('types', []):
        new_type = Type(type=type_name, pokemon=pokemon)
        session.add(new_type)

session.commit()
session.close()

print("Database has been populated with SQLAlchemy.")

import json
import requests


def fetch_pokemon_types(pokemon_name):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
    if response.status_code == 200:
        types = [type_info['type']['name'] for type_info in response.json()['types']]
        return types
    else:
        return None


with open('pokemons_data.json', 'r') as file:
    pokemon_data = json.load(file)

for pokemon in pokemon_data:
    correct_types = fetch_pokemon_types(pokemon['name'])
    if correct_types:
        pokemon['types'] = correct_types  # Add the new 'types' field
        if 'type' in pokemon:
            del pokemon['type']  # Remove the old 'type' field

# Save the updated JSON data
with open('pokemons_data.json', 'w') as file:
    json.dump(pokemon_data, file, indent=4)

print("JSON file has been updated with correct Pokémon types.")

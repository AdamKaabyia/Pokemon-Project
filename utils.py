import requests

URL = "https://pokeapi.co/api/v2/pokemon/"


def fetch_pokemon_types(pokemon_name):
    response = requests.get(f"{URL}{pokemon_name.lower()}")
    if response.status_code == 200:
        types = [type_info['type']['name'] for type_info in response.json()['types']]
        return types
    else:
        return None


def fetch_pokemon_details(pokemon_name):
    response = requests.get(f"{URL}{pokemon_name.lower()}")
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

# Title

3 tables

1. pokemon:
     id | name | height | weight


2. trainer:
     name | town | poke_id


3. types:
     type | poke_id


____________________________________________
APIsupports the following operations:
1.	Add new pokemon species: adds a new pokemon species with the following information: id, name, height, weight, types (all of them).
    * add a new row in pokemon with { id | name | height | weight }the given id, name, height, weight
    * add new rows in types {type | poke_id } each row includes a single type
      
2.	Get pokemons by type: returns all pokemons with the specific type
    * iterate over the types table and take all the poke_id such that match type  
  	   
4.	Get pokemons by trainer: get all the pokemons of a given owner
6.	Get trainers of a pokemon: get all the trainers of a given pokemon
7.	delete pokemon of trainer
8.	add pokemon to a trainer: when a trainer catches a pokemon and train it the pokemon become his.
9.	Evolve (pokemon x of trainer y)

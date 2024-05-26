from fastapi import FastAPI
from routes import pokemones_router, catch_router, evolve_router

app = FastAPI()

# Include routers from separate files
app.include_router(pokemones_router.router, prefix="/pokemon")
app.include_router(catch_router.router, prefix="/catching")
app.include_router(evolve_router.router, prefix="/evolve")


# post: add new pokemon
# git: pokemons names by type
# git: trainer names by poke_name
# delete pokemon
# post: add pokemon to trainer - catching

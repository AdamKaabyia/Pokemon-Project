from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from models import Pokemon, engine, Trainer
from routes.pokemones_router import add_pokemon

router = APIRouter()

@router.post("/add")
def add_pokemon_to_trainer(poke_name, trainer_name,town):
    db = Session(bind=engine)
    db_pokemon = db.query(Pokemon).filter(Pokemon.name == poke_name).first()
    if not db_pokemon:
        db.close()
        add_pokemon(poke_name)
        db = Session(bind=engine)

    db_trainer = db.query(Trainer).filter(Trainer.name == trainer_name).all()
    if db_trainer:
        db_trainer = db_trainer.filter(Trainer.poke_id == db_pokemon.id)
        db.close()
        raise HTTPException(status_code=400, detail="Pokemon already exists")
    new_pair = Trainer(name=trainer_name, town=town,poke_id=db_pokemon.id)
    db.add(new_pair)

    db.commit()
    db.close()

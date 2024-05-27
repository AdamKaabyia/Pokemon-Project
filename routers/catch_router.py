from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from models import Pokemon, engine, Trainer, Trainer_Enrollment
from routers.pokemones_router import add_pokemon

router = APIRouter()

from fastapi import HTTPException


@router.post("/catch-pokemon")
def add_pokemon_to_trainer(poke_name: str, trainer_name: str, town: str):
    try:
        add_pokemon(poke_name)
    except HTTPException as e:
        if e.status_code==407:
            return e.detail


    session = Session(bind=engine)
    try:

        db_pokemon = session.query(Pokemon).filter(Pokemon.name == poke_name).first()
        if not db_pokemon:
            raise HTTPException(status_code=404, detail="Pokemon data not found")
        db_trainer = session.query(Trainer).filter(Trainer.name == trainer_name).first()
        if db_trainer:
            existing_pair = session.query(Trainer_Enrollment).filter_by(trainer_id=db_trainer.id,
                                                                        poke_id=db_pokemon.id).first()
            if existing_pair:
                raise HTTPException(status_code=404, detail="This trainer already has this Pokémon.")
        else:
            db_trainer = Trainer(name=trainer_name, town=town)
            session.add(db_trainer)
            session.flush()

        new_pair = Trainer_Enrollment(trainer_id=db_trainer.id, poke_id=db_pokemon.id)
        session.add(new_pair)
        session.commit()

        return "Pokemon added to trainer successfully"

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=406, detail="shit happened")
    finally:
        session.close()

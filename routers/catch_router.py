from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from models import Pokemon, engine, Trainer, Trainer_Enrollment
from routers.pokemones_router import add_pokemon

router = APIRouter()


@router.post("/add")
def add_pokemon_to_trainer(poke_name: str, trainer_name: str, town: str):
    session = Session(bind=engine)
    try:
        db_pokemon = session.query(Pokemon).filter(Pokemon.name == poke_name).first()
        if not db_pokemon:
            result = add_pokemon(poke_name)
            if result["status"] != "success":
                raise HTTPException(status_code=400, detail="Could not add Pokemon")
            db_pokemon = session.query(Pokemon).filter(Pokemon.name == poke_name).first()

        db_trainer = session.query(Trainer).filter(Trainer.name == trainer_name, Trainer.town == town).first()
        if db_trainer:
            existing_pair = session.query(Trainer_Enrollment).filter_by(trainer_id=db_trainer.id,
                                                                        poke_id=db_pokemon.id).first()
            if existing_pair:
                raise HTTPException(status_code=400, detail="This trainer already has this Pokémon.")

        if not db_trainer:
            db_trainer = Trainer(name=trainer_name, town=town)
            session.add(db_trainer)
            session.flush()

        new_pair = Trainer_Enrollment(trainer_id=db_trainer.id, poke_id=db_pokemon.id)
        session.add(new_pair)
        session.commit()

        return {"status": "success", "message": "Pokemon added to trainer successfully"}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

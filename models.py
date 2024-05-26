from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()


class Pokemon(Base):
    __tablename__ = 'pokemon'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    height = Column(Integer)
    weight = Column(Integer)
    trainers = relationship('Trainer_Enrollment', back_populates='pokemon')
    types = relationship('Type', back_populates='pokemon')


class Trainer(Base):
    __tablename__ = 'trainers'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    town = Column(String(255))


class Trainer_Enrollment(Base):
    __tablename__ = 'trainer_enrollment'
    id = Column(Integer, primary_key=True)
    trainer_id = Column(Integer)
    poke_id = Column(Integer, ForeignKey('pokemon.id'))
    trainer = relationship(Trainer, back_populates='pokemons')
    pokemon = relationship(Pokemon, back_populates='trainers')

class Type(Base):
    __tablename__ = 'types'
    id = Column(Integer, primary_key=True)
    type = Column(String(255))

class Type_Enrollment(Base):
    __tablename__ = 'types_enrollment'
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer)
    poke_id = Column(Integer, ForeignKey('pokemon.id'))
    pokemon = relationship('Pokemon', back_populates='types')
    type = relationship('Type', back_populates='types')


# Database connection setup
engine = create_engine('mysql+pymysql://root:@localhost/pokemons_db')
Base.metadata.create_all(engine)  # Creates the tables

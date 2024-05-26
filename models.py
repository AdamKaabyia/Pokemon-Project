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
    trainers = relationship('Trainer', back_populates='pokemon')
    types = relationship('Type', back_populates='pokemon')


class Trainer(Base):
    __tablename__ = 'trainer'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    town = Column(String(255))
    poke_id = Column(Integer, ForeignKey('pokemon.id'))
    pokemon = relationship('Pokemon', back_populates='trainers')


class Type(Base):
    __tablename__ = 'types'
    id = Column(Integer, primary_key=True)
    type = Column(String(255))
    poke_id = Column(Integer, ForeignKey('pokemon.id'))
    pokemon = relationship('Pokemon', back_populates='types')


# Database connection setup
engine = create_engine('mysql+pymysql://root:@localhost/pokemonsdb')
Base.metadata.create_all(engine)  # Creates the tables

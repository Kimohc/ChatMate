from sqlalchemy import Boolean, Column, Integer, String
from db import Base
from uuid import UUID


class Gebruiker(Base):
    __tablename__ = 'gebruikers'
    gebruiker_id = Column(String(100), primary_key=True)
    e_mail = Column(String(100))
    gebruikersnaam = Column(String(50))
    wachtwoord = Column(String(100))
    foto = Column(String(1000))
    beschrijving = Column(String(1000))


class Bots(Base):
    __tablename__ = 'bots'
    bot_id = Column(String(100), primary_key=True)
    bot_naam = Column(String(50))
    bot_foto = Column(String(1000))
    bot_beschrijving = Column(String(1000))
    bot_oud = Column(String(100))
    bot_geslacht = Column(String(50))
    bot_land = Column(String(100))


class Berichten(Base):
    __tablename__ = 'berichten'
    bericht_id = Column(Integer, primary_key=True, index=True)
    gesprek_id = Column(Integer)
    verstuurder_id = Column(String(100))
    bericht = Column(String(1000))


class Gesprekken(Base):
    __tablename__ = 'gesprekken'
    gesprek_id = Column(Integer, primary_key=True, index=True)
    gebruiker_id = Column(String(100))
    bot_id = Column(String(100))

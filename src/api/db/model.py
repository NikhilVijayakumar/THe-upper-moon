from datetime import datetime

from graphene import Float
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SlayerDB(Base):
    """Stores user profiles."""
    __tablename__ = "slayers"
    id = Column(String(), primary_key=True, index=True) # <-- Added ()
    name = Column(String(), index=True) # <-- Added ()
    breathing_style = Column(String()) # <-- Added ()
    level = Column(Integer()) # <-- Added ()
    strength = Column(String()) # <-- FIX: Added ()
    dexterity = Column(String()) # <-- FIX: Added ()
    stamina = Column(String()) # <-- FIX: Added ()


class WeaponDB(Base):
    """Weapon inventory and attributes."""
    __tablename__ = "weapons"
    id = Column(String(), primary_key=True, index=True) # <-- Added ()
    name = Column(String(), index=True) # <-- Added ()
    type = Column(String())  # e.g., Katana, Axe, Whip # <-- Added ()
    weight = Column(String()) # <-- FIX: Added ()
    sharpness = Column(String()) # <-- FIX: Added ()
    price = Column(Integer()) # <-- Added ()
    breathing_compatibility = Column(String()) # <-- Added ()


class InteractionDB(Base):
    """Battle outcomes for training data."""
    __tablename__ = "interactions"
    id = Column(Integer(), primary_key=True, index=True) # <-- Added ()
    slayer_id = Column(String()) # <-- Added ()
    weapon_id = Column(String()) # <-- Added ()
    battle_outcome = Column(Boolean()) # <-- Added ()
    timestamp = Column(DateTime(), default=datetime.utcnow) # <-- FIX: Added ()


class GamificationDB(Base):
    """Points and ranks (Reflects Section 8)."""
    __tablename__ = "gamification"
    slayer_id = Column(String(), primary_key=True, index=True) # <-- Added ()
    nichirin_points = Column(Integer(), default=0) # <-- Added ()
    rank = Column(String(), default='Apprentice') # <-- Added ()
    last_login = Column(DateTime(), default=datetime.utcnow) # <-- FIX: Added ()
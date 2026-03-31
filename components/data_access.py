# -*- coding: utf-8 -*-
"""
Created on Wed May 21 22:05:03 2025

@author: Cameron-n

Functions to load and save data to and from the database.
"""

#%% Imports

# Standard
import os
from dotenv import load_dotenv

# Pandas
import pandas as pd

# Flask
from flask import Flask

# SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, mapped_column


#%% Environment Variables

path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(path)

# Seemingly used. Could replace URI with these components
database_password = os.environ.get('PA_DATABASE_PASSWORD')
username = os.environ.get('PA_USER')
host_name = os.environ.get('PA_HOST')
database_name = os.environ.get('PA_DATABASE_NAME')


#%% Boilerplate

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

server = Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URI')
server.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 280}
db.init_app(server)


#%% Classes

# For new effects, add them:
    # Here
    # In `Ingredient` in the database (as a column)
    # In `Effects` in the database (as a row)
class Ingredient(db.Model):
    __tablename__ = "Ingredient"

    ID = mapped_column(String(50), primary_key=True)
    Icon = mapped_column(String(50))
    Value = mapped_column(Float)
    Weight = mapped_column(Float)
    Ingredient = mapped_column(String(50))
    Origin = mapped_column("Origin", String(50))
    First_Effect = mapped_column("First Effect", String(50))
    Weakness_to_Fire = mapped_column("Weakness to Fire", Integer)
    Blind = mapped_column(Integer)
    Burden = mapped_column(Integer)
    Chameleon = mapped_column(Integer)
    Paralyze = mapped_column(Integer)
    Poison = mapped_column(Integer)
    Frost_Damage = mapped_column("Frost Damage", Integer)
    Damage_Agility = mapped_column("Damage Agility", Integer)
    Damage_Endurance = mapped_column("Damage Endurance", Integer)
    Damage_Fatigue = mapped_column("Damage Fatigue", Integer)
    Damage_Health = mapped_column("Damage Health", Integer)
    Damage_Intelligence = mapped_column("Damage Intelligence", Integer)
    Damage_Luck = mapped_column("Damage Luck", Integer)
    Damage_Magicka = mapped_column("Damage Magicka", Integer)
    Damage_Personality = mapped_column("Damage Personality", Integer)
    Damage_Speed = mapped_column("Damage Speed", Integer)
    Damage_Strength = mapped_column("Damage Strength", Integer)
    Damage_Willpower = mapped_column("Damage Willpower", Integer)
    Disintegrate_Armor = mapped_column("Disintegrate Armor", Integer)
    Disintegrate_Weapon = mapped_column("Disintegrate Weapon", Integer)
    Divine_Intervention = mapped_column("Divine Intervention", Integer)
    Drain_Agility = mapped_column("Drain Agility", Integer)
    Drain_Alteration = mapped_column("Drain Alteration", Integer)
    Drain_Fatigue = mapped_column("Drain Fatigue", Integer)
    Drain_Health = mapped_column("Drain Health", Integer)
    Drain_Fatigue = mapped_column("Drain Fatigue", Integer)
    Drain_Magicka = mapped_column("Drain Magicka", Integer)
    Drain_Mysticism = mapped_column("Drain Mysticism", Integer)
    Drain_Sneak = mapped_column("Drain Sneak", Integer)
    Drain_Strength = mapped_column("Drain Strength", Integer)
    Drain_Intelligence = mapped_column("Drain Intelligence", Integer)
    Drain_Willpower = mapped_column("Drain Willpower", Integer)
    Drain_Agility = mapped_column("Drain Agility", Integer)
    Drain_Speed = mapped_column("Drain Speed", Integer)
    Drain_Endurance = mapped_column("Drain Endurance", Integer)
    Drain_Personality = mapped_column("Drain Personality", Integer)
    Drain_Luck = mapped_column("Drain Luck", Integer)
    Fire_Damage = mapped_column("Fire Damage", Integer)
    Fortify_Acrobatics = mapped_column("Fortify Acrobatics", Integer)
    Fortify_Alchemy = mapped_column("Fortify Alchemy", Integer)
    Fortify_Health = mapped_column("Fortify Health", Integer)
    Fortify_Athletics = mapped_column("Fortify Athletics", Integer)
    Fortify_Blunt_Weapon = mapped_column("Fortify Blunt Weapon", Integer)
    Fortify_Conjuration = mapped_column("Fortify Conjuration", Integer)
    Fortify_Light_Armor = mapped_column("Fortify Light Armor", Integer)
    Fortify_Marksman = mapped_column("Fortify Marksman", Integer)
    Fortify_Maximum_Magicka = mapped_column("Fortify Maximum Magicka", Integer)
    Fortify_Mysticism = mapped_column("Fortify Mysticism", Integer)
    Fortify_Restoration = mapped_column("Fortify Restoration", Integer)
    Fortify_Speechcraft = mapped_column("Fortify Speechcraft", Integer)
    Fortify_Unarmored = mapped_column("Fortify Unarmored", Integer)
    Fortify_Fatigue = mapped_column("Fortify Fatigue", Integer)
    Fortify_Magicka = mapped_column("Fortify Magicka", Integer)
    Fortify_Strength = mapped_column("Fortify Strength", Integer)
    Fortify_Intelligence = mapped_column("Fortify Intelligence", Integer)
    Fortify_Willpower = mapped_column("Fortify Willpower", Integer)
    Fortify_Agility = mapped_column("Fortify Agility", Integer)
    Fortify_Speed = mapped_column("Fortify Speed", Integer)
    Fortify_Endurance = mapped_column("Fortify Endurance", Integer)
    Fortify_Personality = mapped_column("Fortify Personality", Integer)
    Fortify_Luck = mapped_column("Fortify Luck", Integer)
    Fortify_Attack = mapped_column("Fortify Attack", Integer)
    Restore_Athletics = mapped_column("Restore Athletics", Integer)
    Restore_Health = mapped_column("Restore Health", Integer)
    Restore_Destruction = mapped_column("Restore Destruction", Integer)
    Restore_Restoration = mapped_column("Restore Restoration", Integer)
    Restore_Speechcraft = mapped_column("Restore Speechcraft", Integer)
    Restore_Fatigue = mapped_column("Restore Fatigue", Integer)
    Restore_Magicka = mapped_column("Restore Magicka", Integer)
    Restore_Strength = mapped_column("Restore Strength", Integer)
    Restore_Intelligence = mapped_column("Restore Intelligence", Integer)
    Restore_Willpower = mapped_column("Restore Willpower", Integer)
    Restore_Agility = mapped_column("Restore Agility", Integer)
    Restore_Speed = mapped_column("Restore Speed", Integer)
    Restore_Endurance = mapped_column("Restore Endurance", Integer)
    Restore_Personality = mapped_column("Restore Personality", Integer)
    Restore_Luck = mapped_column("Restore Luck", Integer)
    Sanctuary = mapped_column(Integer)
    Shield = mapped_column(Integer)
    Shock_Damage = mapped_column("Shock Damage", Integer)
    Silence = mapped_column(Integer)
    Slowfall = mapped_column(Integer)
    Stunted_Magicka = mapped_column("Stunted Magicka", Integer)
    Summon_Scamp = mapped_column("Summon Scamp", Integer)
    Vampirism = mapped_column(Integer)
    Weakness_to_Common_Disease = mapped_column("Weakness to Common Disease", Integer)
    Weakness_to_Frost = mapped_column("Weakness to Frost", Integer)
    Weakness_to_Magicka = mapped_column("Weakness to Magicka", Integer)
    Weakness_to_Normal_Weapons = mapped_column("Weakness to Normal Weapons", Integer)
    Weakness_to_Poison = mapped_column("Weakness to Poison", Integer)
    Weakness_to_Shock = mapped_column("Weakness to Shock", Integer)
    Detect_Animal = mapped_column("Detect Animal", Integer)
    Detect_Enchantment = mapped_column("Detect Enchantment", Integer)
    Detect_Key = mapped_column("Detect Key", Integer)
    Dispel = mapped_column(Integer)
    Feather = mapped_column(Integer)
    Invisibility = mapped_column(Integer)
    Jump = mapped_column(Integer)
    Levitate = mapped_column(Integer)
    Light = mapped_column(Integer)
    Mark = mapped_column(Integer)
    Night_Eye = mapped_column("Night Eye", Integer)
    Recall = mapped_column(Integer)
    Cure_Blight_Disease = mapped_column("Cure Blight Disease", Integer)
    Cure_Common_Disease = mapped_column("Cure Common Disease", Integer)
    Resist_Blight_Disease = mapped_column("Resist Blight Disease", Integer)
    Resist_Common_Disease = mapped_column("Resist Common Disease", Integer)
    Resist_Common_Disease = mapped_column("Resist Common Disease", Integer)
    Cure_Paralyzation = mapped_column("Cure Paralyzation", Integer)
    Resist_Paralysis = mapped_column("Resist Paralysis", Integer)
    Cure_Poison = mapped_column("Cure Poison", Integer)
    Resist_Poison = mapped_column("Resist Poison", Integer)
    Resist_Fire = mapped_column("Resist Fire", Integer)
    Resist_Frost = mapped_column("Resist Frost", Integer)
    Resist_Shock = mapped_column("Resist Shock", Integer)
    Resist_Normal_Weapons = mapped_column("Resist Normal Weapons", Integer)
    Fire_Shield = mapped_column("Fire Shield", Integer)
    Frost_Shield = mapped_column("Frost Shield", Integer)
    Lightning_Shield = mapped_column("Lightning Shield", Integer)
    Resist_Magicka = mapped_column("Resist Magicka", Integer)
    Reflect = mapped_column(Integer)
    Spell_Absorption = mapped_column("Spell Absorption", Integer)
    Telekinesis = mapped_column(Integer)
    Swift_Swim = mapped_column("Swift Swim", Integer)
    Water_Breathing = mapped_column("Water Breathing", Integer)
    Water_Walking = mapped_column("Water Walking", Integer)
    Sound = mapped_column(Integer)
    Reflect_Damage = mapped_column("Reflect Damage", Integer)
    Insight = mapped_column(Integer)
    Fortify_Casting = mapped_column("Fortify Casting", Integer)
    Radiant_Shield = mapped_column("Radiant Shield", Integer)
    Detect_Invisibility = mapped_column("Detect Invisibility", Integer)
    Detect_Enemy = mapped_column("Detect Enemy", Integer)
    Detect_Humanoid = mapped_column("Detect Humanoid", Integer)
    Blink = mapped_column(Integer)

class Effect(db.Model):
    __tablename__ = "Effect"
    
    Spell_Effects = mapped_column("Spell Effects", String(50), primary_key=True)
    Base_Cost = mapped_column("Base Cost", Float)
    Positive = mapped_column(Integer)
    HasNoDuration = mapped_column(Integer)
    HasNoMagnitude = mapped_column(Integer)
    Icon = mapped_column(String(50))

class Tool(db.Model):
    __tablename__ = "Tool"
    
    Name = mapped_column(String(50), primary_key=True)
    Quality = mapped_column(Float)
    Type = mapped_column(String(50))
    Origin = mapped_column(String(50))
    Icon = mapped_column(String(50))

class NPCtoCell(db.Model):
    __tablename__ = "NPCtoCell"
    
    Name = mapped_column(String(50), primary_key=True)
    Origin = mapped_column(String(50))
    CellName = mapped_column(String(50))
    CellX = mapped_column(Integer)
    CellY = mapped_column(Integer)
    isInterior = mapped_column(Integer)

class IngtoNPC(db.Model):
    __tablename__ = "IngtoNPC"
    
    Name = mapped_column(String(50), primary_key=True)
    NPCName = mapped_column(String(50), primary_key=True)
    Count = mapped_column(Integer)

class ContainertoCell(db.Model):
    __tablename__ = "ContainertoCell"
    
    ID = mapped_column(String(50), primary_key=True)
    Origin = mapped_column(String(50))
    CellName = mapped_column(String(50), primary_key=True)
    CellX = mapped_column(Float, primary_key=True)
    CellY = mapped_column(Float, primary_key=True)
    IsInterior = mapped_column(Integer)
    Count = mapped_column(Integer)

class FloratoCell(db.Model):
    __tablename__ = "FloratoCell"
    
    ID = mapped_column(String(50), primary_key=True)
    Origin = mapped_column(String(50))
    CellName = mapped_column(String(60), primary_key=True)
    CellX = mapped_column(Float, primary_key=True)
    CellY = mapped_column(Float, primary_key=True)
    IsInterior = mapped_column(Integer)
    Count = mapped_column(Integer)

class IngtoContainer(db.Model):
    __tablename__ = "IngtoContainer"
    
    ID = mapped_column(String(50), primary_key=True)
    Name = mapped_column(String(50))
    Ingredient = mapped_column(String(50), primary_key=True)
    Count = mapped_column(Integer)

class IngtoFauna(db.Model):
    __tablename__ = "IngtoFauna"
    
    ID = mapped_column(String(50), primary_key=True)
    Name = mapped_column(String(50))
    Ingredient = mapped_column(String(50), primary_key=True)
    Count = mapped_column(Integer)

class IngtoFlora(db.Model):
    __tablename__ = "IngtoFlora"
    
    ID = mapped_column(String(50), primary_key=True)
    Name = mapped_column(String(50))
    Ingredient = mapped_column(String(50), primary_key=True)
    Count = mapped_column(Integer)

class IngtoLoose(db.Model):
    __tablename__ = "IngtoLoose"
    
    ID = mapped_column(String(50), primary_key=True)
    Origin = mapped_column(String(50))
    CellName = mapped_column(String(60), primary_key=True)
    CellX = mapped_column(Float, primary_key=True)
    CellY = mapped_column(Float, primary_key=True)
    IsInterior = mapped_column(Integer)
    Count = mapped_column(Integer)

class LvlcretoCell(db.Model):
    __tablename__ = "LvlcretoCell"
    
    ID = mapped_column(String(50), primary_key=True)
    Origin = mapped_column(String(50))
    CellName = mapped_column(String(60), primary_key=True)
    CellX = mapped_column(Float, primary_key=True)
    CellY = mapped_column(Float, primary_key=True)
    IsInterior = mapped_column(Integer)
    Count = mapped_column(Integer)

#%% Data download

with server.app_context():
    # Don't use `db.select(Ingredient)`. This returns sqlalchemy objects instead 
    # of the raw database columns
    DF_INGREDIENTS = pd.DataFrame(db.session.execute(db.select(*Ingredient.__table__.columns)))
    DF_EFFECTS = pd.DataFrame(db.session.execute(db.select(*Effect.__table__.columns)))
    DF_TOOLS = pd.DataFrame(db.session.execute(db.select(*Tool.__table__.columns).order_by(Tool.Quality)))

# -*- coding: utf-8 -*-
"""
Created on Wed May 21 22:05:03 2025

@author: camer

Functions to load and save database from and to the database.
"""
# Consider Flask-SQL-Alchemy

import os
import pandas as pd
from dotenv import load_dotenv
import MySQLdb

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, mapped_column

path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(path)
database_password = os.environ.get('PA_DATABASE_PASSWORD')
username = os.environ.get('PA_USER')
host_name = os.environ.get('PA_HOST')
database_name = os.environ.get('PA_DATABASE_NAME')

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Ingredient(db.Model):
    __tablename__ = "Ingredient"
    
    Weight = mapped_column(Float)
    Value = mapped_column(String(50))
    Ingredient = mapped_column(String(50), primary_key=True)
    Weakness_to_Fire = mapped_column("Weakness to Fire", String(50))
    Blind = mapped_column(String(50))
    Burden = mapped_column(String(50))
    Paralyze = mapped_column(String(50))
    Poison = mapped_column(String(50))
    Frost_Damage = mapped_column("Frost Damage", String(50))
    Damage_Health = mapped_column("Damage Health", String(50))
    Drain_Health = mapped_column("Drain Health", String(50))
    Drain_Fatigue = mapped_column("Drain Fatigue", String(50))
    Drain_Magicka = mapped_column("Drain Magicka", String(50))
    Drain_Strength = mapped_column("Drain Strength", String(50))
    Drain_Intelligence = mapped_column("Drain Intelligence", String(50))
    Drain_Willpower = mapped_column("Drain Willpower", String(50))
    Drain_Agility = mapped_column("Drain Agility", String(50))
    Drain_Speed = mapped_column("Drain Speed", String(50))
    Drain_Endurance = mapped_column("Drain Endurance", String(50))
    Drain_Personality = mapped_column("Drain Personality", String(50))
    Drain_Luck = mapped_column("Drain Luck", String(50))
    Fortify_Health = mapped_column("Fortify Health", String(50))
    Fortify_Fatigue = mapped_column("Fortify Fatigue", String(50))
    Fortify_Magicka = mapped_column("Fortify Magicka", String(50))
    Fortify_Strength = mapped_column("Fortify Strength", String(50))
    Fortify_Intelligence = mapped_column("Fortify Intelligence", String(50))
    Fortify_Willpower = mapped_column("Fortify Willpower", String(50))
    Fortify_Agility = mapped_column("Fortify Agility", String(50))
    Fortify_Speed = mapped_column("Fortify Speed", String(50))
    Fortify_Endurance = mapped_column("Fortify Endurance", String(50))
    Fortify_Personality = mapped_column("Fortify Personality", String(50))
    Fortify_Luck = mapped_column("Fortify Luck", String(50))
    Fortify_Attack = mapped_column("Fortify Attack", String(50))
    Restore_Health = mapped_column("Restore Health", String(50))
    Restore_Fatigue = mapped_column("Restore Fatigue", String(50))
    Restore_Magicka = mapped_column("Restore Magicka", String(50))
    Restore_Strength = mapped_column("Restore Strength", String(50))
    Restore_Intelligence = mapped_column("Restore Intelligence", String(50))
    Restore_Willpower = mapped_column("Restore Willpower", String(50))
    Restore_Agility = mapped_column("Restore Agility", String(50))
    Restore_Speed = mapped_column("Restore Speed", String(50))
    Restore_Endurance = mapped_column("Restore Endurance", String(50))
    Restore_Personality = mapped_column("Restore Personality", String(50))
    Restore_Luck = mapped_column("Restore Luck", String(50))
    Detect_Animal = mapped_column("Detect Animal", String(50))
    Detect_Enchantment = mapped_column("Detect Enchantment", String(50))
    Detect_Key = mapped_column("Detect Key", String(50))
    Dispel = mapped_column(String(50))
    Feather = mapped_column(String(50))
    Invisibility = mapped_column(String(50))
    Levitate = mapped_column(String(50))
    Light = mapped_column(String(50))
    Night_Eye = mapped_column("Night Eye", String(50))
    Cure_Blight_Disease = mapped_column("Cure Blight Disease", String(50))
    Cure_Common_Disease = mapped_column("Cure Common Disease", String(50))
    Resist_Common_Disease = mapped_column("Resist Common Disease", String(50))
    Cure_Paralyzation = mapped_column("Cure Paralyzation", String(50))
    Resist_Paralysis = mapped_column("Resist Paralysis", String(50))
    Cure_Poison = mapped_column("Cure Poison", String(50))
    Resist_Poison = mapped_column("ResistPoison", String(50))
    Resist_Fire = mapped_column("Resist Fire", String(50))
    Resist_Frost = mapped_column("Resist Frost", String(50))
    Resist_Shock = mapped_column("Resist Shock", String(50))
    Fire_Shield = mapped_column("Fire Shield", String(50))
    Frost_Shield = mapped_column("Frost Shield", String(50))
    Lightning_Shield = mapped_column("Lightning Shield", String(50))
    Resist_Magicka = mapped_column("Resist Magicka", String(50))
    Reflect = mapped_column(String(50))
    Spell_Absorption = mapped_column("Spell Absorption", String(50))
    Telekinesis = mapped_column(String(50))
    Swift_Swim = mapped_column("Swift Swim", String(50))
    Water_Breathing = mapped_column("Water Breathing", String(50))
    Water_Walking = mapped_column("Water Walking", String(50))
    Origin = mapped_column("Origin", String(50))
    First_Effect = mapped_column("First Effect", String(50))
    
class Effect(db.Model):
    __tablename__ = "Effect"
    
    Spell_Effects = mapped_column(String(50), primary_key=True)
    Base_Cost = mapped_column(Float)
    Positive = mapped_column(Integer)

class Tool(db.Model):
    __tablename__ = "Tool"
    
    Name = mapped_column(String(50), primary_key=True)
    Quality = mapped_column(Float)
    Type = mapped_column(String(50))

def database_connection():
    """ Connect to database."""
    connection = MySQLdb.connect(
        user=username,
        passwd=database_password,
        host=host_name,
        db=database_name,
    )
    return connection

def database_execute(sql_text):
    """ Execute SQL query. Does not return anything.
    Use for UPDATE/DELETE queries."""
    connection = database_connection()

    connection.cursor().execute(
        sql_text
        )
    connection.commit()
    connection.close()

def database_fetch(sql_text):
    """ Execute SQL query. Returns results.
    Use for SELECT queries."""
    connection = database_connection()

    connection.query(
        sql_text
        )
    r=connection.store_result()

    dummy_data = []
    for row in r.fetch_row(0):
        dummy_data.append(row)
    df = pd.DataFrame(dummy_data)

    connection.close()

    return df

# %% Data download

DF_INGREDIENTS = database_fetch("SELECT * FROM Ingredient")
DF_COLUMN_NAMES = database_fetch("DESCRIBE Ingredient")[0]
DF_INGREDIENTS.columns = DF_COLUMN_NAMES

DF_EFFECTS = database_fetch("SELECT * FROM Effect")
DF_COLUMN_NAMES = database_fetch("DESCRIBE Effect")[0]
DF_EFFECTS.columns = DF_COLUMN_NAMES

DF_TOOLS = database_fetch("SELECT * FROM Tool")
DF_COLUMN_NAMES = database_fetch("DESCRIBE Tool")[0]
DF_TOOLS.columns = DF_COLUMN_NAMES
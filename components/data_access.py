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

path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(path)
database_password = os.environ.get('PA_DATABASE_PASSWORD')
username = os.environ.get('PA_USER')
host_name = os.environ.get('PA_HOST')
database_name = os.environ.get('PA_DATABASE_NAME')

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

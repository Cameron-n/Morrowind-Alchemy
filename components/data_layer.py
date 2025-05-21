# -*- coding: utf-8 -*-
"""
Created on Wed May 21 22:05:03 2025

@author: camer
"""
# Consider Flask-SQL-Alchemy

import pandas as pd
import os
from dotenv import load_dotenv
import MySQLdb

path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(path)
database_password = os.environ.get('PA_DATABASE_PASSWORD')
papassword = os.environ.get('PA_PASSWORD')
username = os.environ.get('PA_USER')

def databaseQuery(sql_text):
    connection = MySQLdb.connect(
        user=username,
        passwd=database_password,
        host=f'{username}.mysql.eu.pythonanywhere-services.com',
        db=f'{username}$default',
    )
    
    connection.cursor().execute(
        sql_text
        )
    connection.commit()
    connection.close()
    
    # connection.query(
    #     query
    #     )
    # r=connection.store_result()
    
    # dummy_data = []
    # for row in r.fetch_row(0):
    #     dummy_data.append(row)
    # df = pd.DataFrame(dummy_data)
    
    # connection.close()
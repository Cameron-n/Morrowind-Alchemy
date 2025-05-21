# -*- coding: utf-8 -*-
"""
Created on Wed May 21 20:51:51 2025

@author: Cameron-n
"""


# A very simple Flask Hello World app for you to get started with...

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'


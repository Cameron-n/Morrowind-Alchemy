# -*- coding: utf-8 -*-
"""
Created on Sun May 25 20:40:32 2025

@author: Cameron-n

Contains the layout for the navbar used in app.py
"""

#%% Imports

# Dash
import dash_mantine_components as dmc


#%% Layout
def navbar():
    layout = dmc.Stack([
        dmc.Anchor(
            dmc.Button("Potion Database", fullWidth=True), 
            href="/potion-database", underline="never", c="myColors.9"
            ),
        dmc.Anchor(
            dmc.Button("Potion Maker", fullWidth=True), 
            href="/", underline="never", c="myColors.9"
            ),
        dmc.Anchor(
            dmc.Button("Add Ingredient", fullWidth=True), 
            href="/add-ingredient", underline="never", c="myColors.9"
            ),
        ])
    
    return layout

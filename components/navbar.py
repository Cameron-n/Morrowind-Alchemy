# -*- coding: utf-8 -*-
"""
Created on Sun May 25 20:40:32 2025

@author: camer
"""

#%% Imports
# Standard

# Dash
import dash
import dash_mantine_components as dmc

# Relative

#%% Layout
def navbar():
    layout = dmc.Stack([
        dmc.Button(
            dmc.Anchor(
                "Potion Maker", 
                href="/",
                underline="never",
                c="myColors.9"
                )
            ),
        dmc.Button(
            dmc.Anchor(
                "Add Ingredient", 
                href="/add-ingredient",
                underline="never",
                c="myColors.9"
                )
            )
        ])
    
    return layout
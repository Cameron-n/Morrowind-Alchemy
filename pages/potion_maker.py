# -*- coding: utf-8 -*-
"""
Created on Thu May 22 20:16:47 2025

@author: camer

Dash page for simulating Morrowinds potion making window.
Allows selection of:
    - Stats (Alchemy, Intelligence, and Luck)
    - Apparatuses (Mortal and Pestle, Alembic, Retort, and Calcinator)
    - Ingredients (Up to 4)
    
Outputs:
    - Potion Effect(s)
    - Magnitude and Duration
"""

# TODO

#%% Imports
# Standard

# Dash
import dash
import dash_mantine_components as dmc

# Relative
from components.data_access import DF_INGREDIENTS

#%% Boilerplate
if __name__ != '__main__':
    dash.register_page(__name__)

#%% Layout
alchemy_tools = dmc.Group([
    dmc.Select("hi"),
    dmc.Select("hi"),
    dmc.Select("hi"),
    dmc.Select("hi"),
    ],
    grow=True,
    wrap="nowrap",)

ingredients = dmc.Group([
    dmc.Select("Ingredient 1", data = DF_INGREDIENTS["Ingredient"]),
    dmc.Select("Ingredient 2", data = DF_INGREDIENTS["Ingredient"]),
    dmc.Select("Ingredient 3", data = DF_INGREDIENTS["Ingredient"]),
    dmc.Select("Ingredient 4", data = DF_INGREDIENTS["Ingredient"]),
    ],
    grow=True,
    wrap="nowrap",)

ingredient_effect_boxes = dmc.Group([
    dmc.Container([
        dmc.Text("Hi"),
        dmc.Text("Hi"),
        dmc.Text("Hi"),
        dmc.Text("Hi"),
        ]),
    dmc.Container([
        dmc.Text("Hi"),
        dmc.Text("Hi"),
        dmc.Text("Hi"),
        dmc.Text("Hi"),
        ]),
    dmc.Container([
        dmc.Text("Hi"),
        dmc.Text("Hi"),
        dmc.Text("Hi"),
        dmc.Text("Hi"),
        ]),
    dmc.Container([
        dmc.Text("Hi"),
        dmc.Text("Hi"),
        dmc.Text("Hi"),
        dmc.Text("Hi"),
        ]),
    ],
    #grow=True,
    wrap="nowrap",)

left_items = dmc.Stack([
    alchemy_tools,
    ingredients,
    ingredient_effect_boxes
    ])

right_items = dmc.Container([
    dmc.Text("Hi"),
    dmc.Text("Hi"),
    dmc.Text("Hi"),
    dmc.Text("Hi"),
    dmc.Text("Hi"),
    dmc.Text("Hi"),
    dmc.Text("Hi"),
    dmc.Text("Hi"),
    ])

whole_thing = dmc.Group([
    left_items,
    right_items,
    ])

stats = dmc.Container([
    dmc.NumberInput(label="Alchemy", min=0,max=100, allowDecimal=False),
    dmc.NumberInput(label="Intelligence", min=0,max=100, allowDecimal=False),
    dmc.NumberInput(label="Luck", min=0,max=100, allowDecimal=False),
    ])

layout = dmc.Stack([
    stats,
    whole_thing,
    ])

#%% Callbacks

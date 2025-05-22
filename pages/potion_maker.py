# -*- coding: utf-8 -*-
"""
Created on Thu May 22 20:16:47 2025

@author: camer
"""

# TODO

#%% Imports
# Standard

# Dash
import dash
import dash_mantine_components as dmc
# Relative


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
    dmc.Select("hi"),
    dmc.Select("hi"),
    dmc.Select("hi"),
    dmc.Select("hi"),
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

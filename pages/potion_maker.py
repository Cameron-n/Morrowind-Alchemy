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
from dash import callback, Input, Output
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
    dmc.Select(label = "Ingredient 1",
               data = DF_INGREDIENTS["Ingredient"],
               searchable = True,
               id="ing_1"),
    dmc.Select(label = "Ingredient 2",
               data = DF_INGREDIENTS["Ingredient"],
               searchable = True,
               id="ing_2"),
    dmc.Select(label = "Ingredient 3",
               data = DF_INGREDIENTS["Ingredient"],
               searchable = True,
               id="ing_3"),
    dmc.Select(label = "Ingredient 4",
               data = DF_INGREDIENTS["Ingredient"],
               searchable = True,
               id="ing_4"),
    ],
    grow=True,
    wrap="nowrap",)

ingredient_effect_boxes = dmc.Group([
    dmc.Container(id="ing_1_effects"),
    dmc.Container(id="ing_2_effects"),
    dmc.Container(id="ing_3_effects"),
    dmc.Container(id="ing_4_effects"),
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
@callback (
    Output("ing_1_effects","children"),
    Input("ing_1","children"),
)
def update_effect_1_list(child):
    # Get list of up to 4 effects from DF_INGREDIENTS
    ingredient_row = DF_INGREDIENTS[DF_INGREDIENTS["Ingredient"]==child]
    ingredient_row_not_nan = ingredient_row.notna().iloc[0]
    columns_not_nan = DF_INGREDIENTS.columns[ingredient_row_not_nan]
    
    effects = [i for i in columns_not_nan]
    
    # Add components
    content = [dmc.Text(i) for i in effects]
    
    return content

@callback (
    Output("ing_2_effects","children"),
    Input("ing_2","children"),
)
def update_effect_2_list(child):
    # Get list of up to 4 effects from DF_INGREDIENTS
    ingredient_row = DF_INGREDIENTS[DF_INGREDIENTS["Ingredient"]==child]
    ingredient_row_not_nan = ingredient_row.notna().iloc[0]
    columns_not_nan = DF_INGREDIENTS.columns[ingredient_row_not_nan]
    
    effects = [i for i in columns_not_nan]
    
    # Add components
    content = [dmc.Text(i) for i in effects]
    
    return content

@callback (
    Output("ing_3_effects","children"),
    Input("ing_3","children"),
)
def update_effect_3_list(child):
    # Get list of up to 4 effects from DF_INGREDIENTS
    ingredient_row = DF_INGREDIENTS[DF_INGREDIENTS["Ingredient"]==child]
    ingredient_row_not_nan = ingredient_row.notna().iloc[0]
    columns_not_nan = DF_INGREDIENTS.columns[ingredient_row_not_nan]
    
    effects = [i for i in columns_not_nan]
    
    # Add components
    content = [dmc.Text(i) for i in effects]
    
    return content

@callback (
    Output("ing_4_effects","children"),
    Input("ing_4","children"),
)
def update_effect_4_list(child):
    # Get list of up to 4 effects from DF_INGREDIENTS
    ingredient_row = DF_INGREDIENTS[DF_INGREDIENTS["Ingredient"]==child]
    ingredient_row_not_nan = ingredient_row.notna().iloc[0]
    columns_not_nan = DF_INGREDIENTS.columns[ingredient_row_not_nan]
    
    effects = [i for i in columns_not_nan]
    
    # Add components
    content = [dmc.Text(i) for i in effects]
    
    return content
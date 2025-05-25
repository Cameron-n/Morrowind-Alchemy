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
# Remove ability to select same ingredient more than once
# Add alchemy tools table to database
# Add effects table (base cost)
# Add space for duration and magnitude

#%% Imports
# Standard
from collections import Counter

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
               clearable=True,
               id="ing_1"),
    dmc.Select(label = "Ingredient 2",
               data = DF_INGREDIENTS["Ingredient"],
               searchable = True,
               clearable=True,
               id="ing_2"),
    dmc.Select(label = "Ingredient 3",
               data = DF_INGREDIENTS["Ingredient"],
               searchable = True,
               clearable=True,
               id="ing_3"),
    dmc.Select(label = "Ingredient 4",
               data = DF_INGREDIENTS["Ingredient"],
               searchable = True,
               clearable=True,
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

right_items = dmc.Container(id="potion_maker_effects")

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

#%% Functions
def potion_magnitude_and_duration():
    
    m_quality = 0
    alchemy = 0
    intelligence = 0
    luck = 0
    base_cost = 0
    
    magnitude_base = m_quality*(alchemy+intelligence/5+luck/10)/(3*base_cost)
    duration_base = 3*magnitude_base
    
    magnitude = magnitude_base # + stuff
    duration = duration_base # + stuff
    
    return magnitude, duration

def potion_effects(list_of_effect_lists):
    """
    WARNING: Code adapted from Chat GPT.
    Finds what effects are shared between the input ingredients.
    These are the effects a potion will have.
    """
    
    counter = Counter()
    for i in list_of_effect_lists:
        counter.update(i)
        
    effects = [string for string, count in counter.items() if count>=2]
    
    return effects

def update_effect_list(value):
    if value is None:
        return None
    # Get list of up to 4 effects from DF_INGREDIENTS
    ingredient_row = DF_INGREDIENTS[DF_INGREDIENTS["Ingredient"]==value]
    ingredient_row_not_nan = ingredient_row.notna().iloc[0]
    columns_not_nan = DF_INGREDIENTS.columns[ingredient_row_not_nan]
    
    effects = list(columns_not_nan)
    effects.remove("Value")
    effects.remove("Weight")
    effects.remove("Ingredient")
    
    # Add components
    content = [dmc.Text(i) for i in effects]
    
    return content

#%% Callbacks
@callback(
    Output("ing_1_effects","children"),
    Input("ing_1","value"),
)
def update_effect_1_list(value):
    return update_effect_list(value)

@callback(
    Output("ing_2_effects","children"),
    Input("ing_2","value"),
)
def update_effect_2_list(value):
    return update_effect_list(value)

@callback(
    Output("ing_3_effects","children"),
    Input("ing_3","value"),
)
def update_effect_3_list(value):
    return update_effect_list(value)

@callback(
    Output("ing_4_effects","children"),
    Input("ing_4","value"),
)
def update_effect_4_list(value):
    return update_effect_list(value)

@callback(
    Output("potion_maker_effects","children"),
    Input("ing_1_effects","children"),
    Input("ing_2_effects","children"),
    Input("ing_3_effects","children"),
    Input("ing_4_effects","children"),
)
def update_effect_list_final(ing_1, ing_2, ing_3, ing_4):
    if not ing_1:
        ing_1 = [{'props': {'children':'empty_1'}}]
    if not ing_2:
        ing_2 = [{'props': {'children':'empty_2'}}]
    if not ing_3:
        ing_3 = [{'props': {'children':'empty_3'}}]
    if not ing_4:
        ing_4 = [{'props': {'children':'empty_4'}}]
    
    list_1 = [i['props']['children'] for i in ing_1]
    list_2 = [i['props']['children'] for i in ing_2]
    list_3 = [i['props']['children'] for i in ing_3]
    list_4 = [i['props']['children'] for i in ing_4]
    
    list_of_lists = [list_1, list_2, list_3, list_4]
    
    content = [dmc.Text(i) for i in potion_effects(list_of_lists)]
    
    return content

@callback(
    Output("","children"),
    Input("",""), # alchemy
    Input("",""), # Intelligence
    Input("",""), # luck
    Input("",""), # mortar
    Input("",""), # alembic
    Input("",""), # retort
    Input("",""), # calcinator
    Input("potion_maker_effects","children")
)
def update_potion_mag_and_dur():
    pass
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
# Tools table specify tool type and weight, value
# Effect table specify +ve, -ve
# Ingredients table specify origin [base, bloodmoon, tribunal, tamriel data, other]
# Account for if inputs are empty

#%% Imports
# Standard
from collections import Counter

# Dash
import dash
from dash import callback, Input, Output
import dash_mantine_components as dmc

# Relative
from components.data_access import DF_INGREDIENTS, DF_EFFECTS, DF_TOOLS

#%% Boilerplate
if __name__ != '__main__':
    dash.register_page(__name__, path='/')

#%% Layout
alchemy_tools = dmc.Group([
    dmc.Select(label = "Mortar and Pestle",
               data = [i for i in DF_TOOLS["Name"] if i[-17:]=="Mortar and Pestle"],
               value = DF_TOOLS["Name"][2],
               allowDeselect=False,
               id="mortar"),
    dmc.Select(label = "Alembic",
               data = [i for i in DF_TOOLS["Name"] if i[-7:]=="Alembic"],
               value = DF_TOOLS["Name"][0],
               allowDeselect=False,
               id="alembic"),
    dmc.Select(label = "Calcinator",
               data = [i for i in DF_TOOLS["Name"] if i[-10:]=="Calcinator"],
               value = DF_TOOLS["Name"][1],
               allowDeselect=False,
               id="calcinator"),
    dmc.Select(label = "Retort",
               data = [i for i in DF_TOOLS["Name"] if i[-6:]=="Retort"],
               value = DF_TOOLS["Name"][3],
               allowDeselect=False,
               id="retort"),
    ],
    grow=True,
    wrap="nowrap",)

ingredients = dmc.Group([
    dmc.Select(label = "Ingredient 1",
               data = DF_INGREDIENTS["Ingredient"],
               searchable = True,
               clearable=True,
               id="ing_1",
               styles={
                   "dropdown":{"background":"blue"}
                   }),
    dmc.Select(label = "Ingredient 2",
               data = DF_INGREDIENTS["Ingredient"],
               searchable = True,
               clearable=True,
               id="ing_2",
               styles={
                   "dropdown":{"background":"blue"}
                   }),
    dmc.Select(label = "Ingredient 3",
               data = DF_INGREDIENTS["Ingredient"],
               searchable = True,
               clearable=True,
               id="ing_3",
               styles={
                   "dropdown":{"background":"blue"}
                   }),
    dmc.Select(label = "Ingredient 4",
               data = DF_INGREDIENTS["Ingredient"],
               searchable = True,
               clearable=True,
               id="ing_4",
               styles={
                   "dropdown":{"background":"blue"}
                   }),
    ],
    grow=True,
    wrap="nowrap",)

ingredient_effect_boxes = dmc.Group([
    dmc.Card(id="ing_1_effects"),
    dmc.Card(id="ing_2_effects"),
    dmc.Card(id="ing_3_effects"),
    dmc.Card(id="ing_4_effects"),
    ],
    grow=True,
    wrap="nowrap",)

left_items = dmc.Stack([
    alchemy_tools,
    ingredients,
    ingredient_effect_boxes
    ])

potion_effects_stack = dmc.Card(id="potion_maker_effects")

magnitude_and_duration = dmc.Card(id="mag_and_dur")

right_items = dmc.Group([
    potion_effects_stack,
    magnitude_and_duration,
    ])

whole_thing = dmc.Group([
    left_items,
    right_items,
    ])

stats = dmc.Container([
    dmc.NumberInput(label="Alchemy",
                    value=50,
                    min=0,
                    max=100,
                    allowDecimal=False,
                    id="alchemy"),
    dmc.NumberInput(label="Intelligence",
                    value=50,
                    min=0,
                    max=100,
                    allowDecimal=False,
                    id="intelligence"),
    dmc.NumberInput(label="Luck",
                    value=40,
                    min=0,
                    max=100,
                    allowDecimal=False,
                    id="luck"),
    ])

layout = dmc.Stack([
    stats,
    whole_thing,
    ])

#%% Functions
def potion_magnitude_and_duration(
            alchemy, 
            intelligence, 
            luck,
            mortar, 
            alembic,
            retort,
            calcinator,
            base_cost,
            positive=True
            ):
    
    magnitude_base = mortar*(alchemy+intelligence/5+luck/10)/(3*base_cost)
    duration_base = 3*magnitude_base
    
    extras = 0
    mult = 1
    if positive:
        if retort and calcinator:
            extras = round(calcinator) + 2*(round(retort))
        elif retort:
            extras = round(retort)
        elif calcinator:
            extras = round(calcinator)
    else:
        if alembic and calcinator:
            mult = (48/120)/(alembic + calcinator)
        elif alembic:
            mult = 1/(alembic + 1)
        elif calcinator:
            extras = round(calcinator)

    magnitude = magnitude_base*mult + extras
    duration = duration_base*mult + extras

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
    content = [dmc.Text(i, truncate="end") for i in effects]
    
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
    Output("mag_and_dur","children"),
    Input("alchemy","value"),
    Input("intelligence","value"),
    Input("luck","value"),
    Input("mortar","value"),
    Input("alembic","value"),
    Input("retort","value"),
    Input("calcinator","value"),
    Input("potion_maker_effects","children")
)
def update_potion_mag_and_dur(
        alchemy, 
        intelligence, 
        luck, 
        mortar, 
        alembic,
        retort,
        calcinator,
        children
        ):
    # get effect names
    if not children:
        return None
    
    effect_names = [i['props']['children'] for i in children]
    
    # get effect costs from names
    effect_costs = [DF_EFFECTS["Base Cost"][DF_EFFECTS["Spell Effects"]==i].iloc[0] for i in effect_names]
    
    # get tool quality
    mortar = DF_TOOLS["Quality"][DF_TOOLS["Name"]==mortar].iloc[0]
    alembic = DF_TOOLS["Quality"][DF_TOOLS["Name"]==alembic].iloc[0]
    retort = DF_TOOLS["Quality"][DF_TOOLS["Name"]==retort].iloc[0]
    calcinator = DF_TOOLS["Quality"][DF_TOOLS["Name"]==calcinator].iloc[0]
    
    # calculate mag and duration
    stack_list = []
    for cost in effect_costs:
        mag, dur = potion_magnitude_and_duration(
            alchemy, 
            intelligence, 
            luck,
            mortar, 
            alembic,
            retort,
            calcinator,
            cost
            )
        text = f"{round(mag)} points for {round(dur)} seconds"
        stack_list.append(dmc.Text(text))  
    
    return stack_list

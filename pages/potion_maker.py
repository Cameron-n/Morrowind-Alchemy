# -*- coding: utf-8 -*-
"""
Created on Thu May 22 20:16:47 2025

@author: Cameron-n

Page for simulating Morrowind's potion making window.
Inputs:
    - Stats (Alchemy, Intelligence, and Luck)
    - Apparatuses (Mortar and Pestle, Alembic, Retort, and Calcinator)
    - Ingredients (Up to 4)

Outputs:
    - Potion Effect(s)
    - Magnitude and Duration
"""

#TODO
# calculation for single ingredients [low-reward, high-effort]
# don't include magnitude/duration if effect not have [mid-reward, mid-effort]
# verify math in-game cause wiki conflicts with openmw research [high-reward, high-effort]
# Figure out how to expand Created Effects border box [mid-reward, mid-effort]
# Add ingredient images? (See render_option_select.js)
# Fix ingredient groupings [high-reward, low-effort]


#%% Imports

# Standard
from collections import Counter
from copy import deepcopy

# Dash
import dash
from dash import callback, Input, Output
import dash_mantine_components as dmc

# Relative
from components.data_access import DF_INGREDIENTS, DF_EFFECTS, DF_TOOLS

DF_EFFECTS.fillna(0, inplace=True)

data_origins = DF_INGREDIENTS["Origin"].unique()

grouped_data = [
    {
        "group": name,
        "items": DF_INGREDIENTS["Ingredient"][DF_INGREDIENTS["Origin"] == name]
    } for name in data_origins
]


#%% Boilerplate

if __name__ != '__main__':
    dash.register_page(__name__)


#%% Layout

alchemy_tools_title = dmc.Text("Apparatus")

alchemy_tools = dmc.Group([
    dmc.Select(label="Mortar and Pestle",
               data=[i for i in DF_TOOLS["Name"][DF_TOOLS["Type"]=="Mortar and Pestle"]],
               value=DF_TOOLS[DF_TOOLS["Type"]=="Mortar and Pestle"][DF_TOOLS["Quality"]==0.5]["Name"].iloc[0],
               allowDeselect=False,
               renderOption={"function": "renderOptionSelect"},
               id="mortar"),
    dmc.Select(label="Alembic",
               data=[i for i in DF_TOOLS["Name"][DF_TOOLS["Type"]=="Alembic"]],
               renderOption={"function": "renderOptionSelect"},
               id="alembic"),
    dmc.Select(label="Calcinator",
               data=[i for i in DF_TOOLS["Name"][DF_TOOLS["Type"]=="Calcinator"]],
               renderOption={"function": "renderOptionSelect"},
               id="calcinator"),
    dmc.Select(label="Retort",
               data=[i for i in DF_TOOLS["Name"][DF_TOOLS["Type"]=="Retort"]],
               renderOption={"function": "renderOptionSelect"},
               id="retort"),
    ],
    grow=True,
    wrap="nowrap",)

alchemy_tools = dmc.Stack([
    alchemy_tools_title,
    alchemy_tools,
    ], gap=0)

ingredients_title = dmc.Text("Ingredients")

ingredients = dmc.Group([
    dmc.Select(value=None,
               data=grouped_data,
               searchable=True,
               clearable=True,
               id="ing_1",
               styles={
                   }),
    dmc.Select(value=None,
               data=grouped_data,
               searchable=True,
               clearable=True,
               id="ing_2",
               styles={
                   }),
    dmc.Select(value=None,
               data=grouped_data,
               searchable=True,
               clearable=True,
               id="ing_3",
               styles={
                   }),
    dmc.Select(value=None,
               data=grouped_data,
               searchable=True,
               clearable=True,
               id="ing_4",
               styles={
                   }),
    ],
    grow=True,
    wrap="nowrap",)

ingredients = dmc.Stack([
    ingredients_title,
    ingredients,
    ], gap=0)

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

potion_effects_title = dmc.Text("Created Effects")

potion_effects_stack = dmc.Card(id="potion_maker_effects")

magnitude_and_duration = dmc.Card(id="mag_and_dur")

right_items = dmc.Group([
    potion_effects_stack,
    magnitude_and_duration,
],
    align="stretch",
    grow=True,
    className="potionmaker-border",
    style={"height": "100%"}
)

right_items = dmc.Stack([
    potion_effects_title,
    right_items,
],
    style={"height": "200px", "width": "530px"})

whole_thing = dmc.Group([
    left_items,
    right_items,
],
    align="flex-start",
    p="md",
    className="potionmaker-border"
)

text = """
1. Set the stats to see the effects on the magnitude and duration of potion effects
2. Select the appartuses. These also alter the magnitude and duration. Note, only a Mortar and Pestle is *required*
3. Select the ingredients. These determine the outcome of the potion
"""

explain_title = dmc.Title("Potion Maker", order=3)
explain_text = dmc.Text(text, style={"white-space": "pre-wrap"})
explain_stack = dmc.Stack([
    explain_title,
    explain_text,
],
    gap=0
)

stats = dmc.Group([
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
    ], wrap="nowrap")

stats = dmc.Stack([
    explain_stack,
    stats,
    ], align="center")

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
    
    magnitude_base = mortar*(alchemy+intelligence/10+luck/10)/(3*base_cost)
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
            mult = 1/(2*alembic + 3*calcinator)
        elif alembic:
            mult = 1/(alembic + 1)
        elif calcinator:
            extras = round(calcinator)

    magnitude = magnitude_base*mult + extras
    duration = duration_base*mult + extras

    return magnitude, duration

def potion_effects(list_of_effect_lists):
    """
    WARNING: Code adapted from ChatGPT.
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
    ingredient_row = DF_INGREDIENTS[DF_INGREDIENTS["Ingredient"] == value]
    ingredient_row_not_nan = ingredient_row.notna().iloc[0]
    columns_not_nan = DF_INGREDIENTS.columns[ingredient_row_not_nan]
    
    effects = list(columns_not_nan)
    effects.remove("Value")
    effects.remove("Weight")
    effects.remove("Ingredient")
    effects.remove("Origin")
    effects.remove("First Effect")
    
    # Add components
    content = [dmc.Text(i, truncate="end") for i in effects]
    
    return content


#%% Callbacks

@callback(
    Output("ing_1_effects","children"),
    Output("ing_2_effects","children"),
    Output("ing_3_effects","children"),
    Output("ing_4_effects","children"),
    Output("ing_1","data"),
    Output("ing_2","data"),
    Output("ing_3","data"),
    Output("ing_4","data"),
    Input("ing_1","value"),
    Input("ing_2","value"),
    Input("ing_3","value"),
    Input("ing_4","value"),
    prevent_initial_call=True
)
def update_effect_dropdowns(value_1, value_2, value_3, value_4):
    """
    Removes shared effects from dropdowns.
    
    E.g. if ingredient 1 is "adamantium ore", the other dropdowns
    will no longer show that ingredient
    """
    
    data_1 = deepcopy(DF_INGREDIENTS["Ingredient"])
    data_2 = deepcopy(DF_INGREDIENTS["Ingredient"])
    data_3 = deepcopy(DF_INGREDIENTS["Ingredient"])
    data_4 = deepcopy(DF_INGREDIENTS["Ingredient"])

    for i in [value_2,value_3,value_4]:
        if i:
            data_1 = data_1[data_1!=i]
    for i in [value_1,value_3,value_4]:
        if i:
            data_2 = data_2[data_2!=i]
    for i in [value_2,value_1,value_4]:
        if i:
            data_3 = data_3[data_3!=i]
    for i in [value_2,value_3,value_1]:
        if i:
            data_4 = data_4[data_4!=i]
    
    if dash.callback_context.triggered_id == "ing_1":
        return update_effect_list(value_1), dash.no_update, dash.no_update, dash.no_update, \
               data_1, data_2, data_3, data_4
    elif dash.callback_context.triggered_id == "ing_2":
        return dash.no_update, update_effect_list(value_2), dash.no_update, dash.no_update, \
               data_1, data_2, data_3, data_4
    elif dash.callback_context.triggered_id == "ing_3":
        return dash.no_update, dash.no_update, update_effect_list(value_3), dash.no_update, \
               data_1, data_2, data_3, data_4
    elif dash.callback_context.triggered_id == "ing_4":
        return dash.no_update, dash.no_update, dash.no_update, update_effect_list(value_4), \
               data_1, data_2, data_3, data_4

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
    effect_costs = [DF_EFFECTS["Base Cost"][DF_EFFECTS["Spell Effects"] == i].iloc[0] for i in effect_names]

    # get positive or negative
    pos_neg = [DF_EFFECTS["Positive"][DF_EFFECTS["Spell Effects"] == i].iloc[0] for i in effect_names]

    # get tool quality
    mortar = DF_TOOLS["Quality"][DF_TOOLS["Name"]==mortar].iloc[0]
    if alembic:
        alembic = DF_TOOLS["Quality"][DF_TOOLS["Name"]==alembic].iloc[0]
    if retort:
        retort = DF_TOOLS["Quality"][DF_TOOLS["Name"]==retort].iloc[0]
    if calcinator:
        calcinator = DF_TOOLS["Quality"][DF_TOOLS["Name"]==calcinator].iloc[0]
    
    # calculate mag and duration
    stack_list = []
    for cost, pos in zip(effect_costs, pos_neg):
        mag, dur = potion_magnitude_and_duration(
            alchemy,
            intelligence,
            luck,
            mortar,
            alembic,
            retort,
            calcinator,
            cost,
            positive=pos
            )
        text = f"{round(mag)} points for {round(dur)} seconds"
        stack_list.append(dmc.Text(text))
    
    return stack_list

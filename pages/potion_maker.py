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
# Save state of page change
# Display quality of tools


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
DF_INGREDIENTS = DF_INGREDIENTS.replace(-1, 1)
DF_INGREDIENTS = DF_INGREDIENTS.replace(-2, 0)

data_origins = DF_INGREDIENTS["Origin"].unique()

grouped_data = [
    {
        "group": name,
        "items": DF_INGREDIENTS["Ingredient"][DF_INGREDIENTS["Origin"] == name]
    } for name in data_origins
]

appa_ids = {
        name: icon for name, icon in zip(DF_TOOLS["Name"], DF_TOOLS["Icon"])
    }

ing_ids = {
        name: icon for name, icon in zip(DF_INGREDIENTS["Ingredient"], DF_INGREDIENTS["Icon"])
    }

def tools_grouped(types):
    return [
        {
            "group": name,
            "items": DF_TOOLS["Name"][DF_TOOLS["Type"] == types][DF_TOOLS["Origin"] == name]
        } for name in DF_TOOLS["Origin"].unique()
    ]

#%% Boilerplate

if __name__ != '__main__':
    dash.register_page(__name__)


#%% Layout

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

min_v = 0
max_v = 1000

stats = dmc.Group([
    dmc.NumberInput(label="Alchemy",
                    value=50,
                    min=min_v,
                    max=max_v,
                    allowDecimal=False,
                    clampBehavior="strict",
                    id="alchemy"),
    dmc.NumberInput(label="Intelligence",
                    value=50,
                    min=min_v,
                    max=max_v,
                    allowDecimal=False,
                    clampBehavior="strict",
                    id="intelligence"),
    dmc.NumberInput(label="Luck",
                    value=40,
                    min=min_v,
                    max=max_v,
                    allowDecimal=False,
                    clampBehavior="strict",
                    id="luck"),
    ], wrap="nowrap")

stats = dmc.Stack([
    explain_stack,
    stats,
    ], align="center")

alchemy_tools_title = dmc.Text("Apparatus")

renderOptionAppa = {
    "function": "renderOptionSelect",
    "options": {"appa_ids": appa_ids}
    }

renderOptionIng = {
    "function": "renderOptionSelect",
    "options": {"appa_ids": ing_ids}
    }

alchemy_tools = dmc.Group([
    dmc.Group([
        dmc.Select(label="Mortar and Pestle",
                   data=tools_grouped("Mortar and Pestle"),
                   value=DF_TOOLS[DF_TOOLS["Type"]=="Mortar and Pestle"][DF_TOOLS["Quality"]==0.5]["Name"].iloc[0],
                   allowDeselect=False,
                   renderOption=renderOptionAppa,
                   id="mortar"),
        dmc.Select(label="Alembic",
                   data=tools_grouped("Alembic"),
                   renderOption=renderOptionAppa,
                   id="alembic"),
    ],
        grow=True,
        wrap="nowrap",),
    dmc.Group([
        dmc.Select(label="Calcinator",
                   data=tools_grouped("Calcinator"),
                   renderOption=renderOptionAppa,
                   id="calcinator"),
        dmc.Select(label="Retort",
                   data=tools_grouped("Retort"),
                   renderOption=renderOptionAppa,
                   id="retort"),
    ],
        grow=True,
        wrap="nowrap",),
    ])

alchemy_tools = dmc.Stack([
    alchemy_tools_title,
    alchemy_tools,
    ], gap=0)

ingredients_title = dmc.Text("Ingredients")

ingredients = dmc.Group([
    dmc.Group([
        dmc.Select(value=None,
                   data=grouped_data,
                   searchable=True,
                   clearable=True,
                   #renderOption=renderOptionIng,
                   id="ing_1",
                   ),
        dmc.Select(value=None,
                   data=grouped_data,
                   searchable=True,
                   clearable=True,
                   #renderOption=renderOptionIng,
                   id="ing_2",
                   ),
    ],
        grow=True,
        wrap="nowrap",),
    dmc.Group([
    dmc.Select(value=None,
               data=grouped_data,
               searchable=True,
               clearable=True,
               #renderOption=renderOptionIng,
               id="ing_3",
               ),
    dmc.Select(value=None,
               data=grouped_data,
               searchable=True,
               clearable=True,
               #renderOption=renderOptionIng,
               id="ing_4",
               ),
    ],
        grow=True,
        wrap="nowrap",),
    ])

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
    wrap="nowrap",
    visibleFrom="md",)

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
    style={"height": "300px", "width": "530px"})

whole_thing = dmc.Group([
    left_items,
    right_items,
],
    align="flex-start",
    p="md",
    className="potionmaker-border"
)

layout = dmc.Stack([
    stats,
    whole_thing,
    ], style={"margin": "auto", "max-width": "1500px"})


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
    """Calculate potion effect magnitude and duration for each effect"""
    magnitude_base = mortar*(alchemy+intelligence/10+luck/10)/(3*base_cost)
    duration_base = 3 * magnitude_base

    extras = 0
    mult = 1
    if positive:
        if retort and calcinator:
            extras = round(calcinator) + 2 * (round(retort))
        elif retort:
            extras = round(retort)
        elif calcinator:
            extras = round(calcinator)
    else:
        if alembic and calcinator:
            mult = 1 / (2 * alembic + 3 * calcinator)
        elif alembic:
            mult = 1 / (alembic + 1)
        elif calcinator:
            extras = round(calcinator)

    magnitude = magnitude_base * mult + extras
    duration = duration_base * mult + extras

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

    effects = [string for string, count in counter.items() if count >= 2]

    return effects


def update_effect_list(value):
    """Get an ingredient's effects and return a list of dmc.Text objects"""
    if value is None:
        return None
    # Get list of up to 4 effects from DF_INGREDIENTS
    ingredient_row = DF_INGREDIENTS[DF_INGREDIENTS["Ingredient"] == value]
    ingredient_row_not_nan = ingredient_row[ingredient_row != 0].notna().iloc[0]
    columns_not_nan = DF_INGREDIENTS.columns[ingredient_row_not_nan]

    effects = list(columns_not_nan)
    try:
        effects.remove("Value")
    except ValueError:
        pass
    try:
        effects.remove("Weight")
    except ValueError:
        pass
    effects.remove("Ingredient")
    effects.remove("Origin")
    effects.remove("First Effect")
    effects.remove("ID")
    effects.remove("Icon")

    # Add components
    content = [dmc.Text(i, truncate="end") for i in effects]

    return content


#%% Callbacks

@callback(
    [Output(f"ing_{i+1}_effects", "children") for i in range(4)],
    [Output(f"ing_{i+1}", "data") for i in range(4)],
    [Input(f"ing_{i+1}", "value") for i in range(4)],
    prevent_initial_call=True
)
def update_effect_dropdowns(value_1, value_2, value_3, value_4):
    """
    Remove shared effects from dropdowns.

    E.g. if ingredient 1 is "adamantium ore", the other dropdowns
    will no longer show that ingredient
    """
    values = [value_1, value_2, value_3, value_4]
    data_list = []

    for value in values:
        data_1 = deepcopy(grouped_data)
        values_1 = deepcopy(values)

        values_1.remove(value)
        for i in values_1:
            if i:
                for j in range(len(data_origins)):
                    if i in list(data_1[j]["items"]):
                        data_1[j]["items"] = data_1[j]["items"][data_1[j]["items"] != i]
        data_list.append(data_1)

    i = int(dash.callback_context.triggered_id[-1])

    return_tuple = [dash.no_update] * 4
    return_tuple[i-1] = update_effect_list(values[i-1])
    return_tuple += data_list
    return_tuple = tuple(return_tuple)

    return return_tuple


@callback(
    Output("potion_maker_effects", "children"),
    [Input(f"ing_{i+1}_effects", "children") for i in range(4)]
)
def update_effect_list_final(ing_1, ing_2, ing_3, ing_4):
    """Get potion effects from ingredient effects"""
    values = [ing_1, ing_2, ing_3, ing_4]
    list_of_lists = []
    num = 0

    for i in values:
        if not i:
            i = [{'props': {'children': f'empty_{num}'}}]
        num += 1
        list_of_lists.append([j['props']['children'] for j in i])

    gray_or_black = ["black", "grey"]
    content = [dmc.Text("• "+i, c=gray_or_black[counter % 2]) for 
               counter, i in enumerate(potion_effects(list_of_lists))]

    return content


@callback(
    Output("mag_and_dur", "children"),
    Input("alchemy", "value"),
    Input("intelligence", "value"),
    Input("luck", "value"),
    Input("mortar", "value"),
    Input("alembic", "value"),
    Input("retort", "value"),
    Input("calcinator", "value"),
    Input("potion_maker_effects", "children")
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
    """Formats the visual element's data for potion_magnitude_and_duration"""
    # get effect names
    if not children:
        return None
    if type(alchemy)==str or type(intelligence)==str or type(luck)==str:
        return None

    # Each name starts with "• ", e.g. "• Drain Fatigue"
    effect_names = [i['props']['children'][2:] for i in children]

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
    gray_or_black = ["black", "grey"]
    counter = 0
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
        text = f"• {round(mag)} points for {round(dur)} seconds"
        stack_list.append(dmc.Text(text, c=gray_or_black[counter % 2]))
        counter += 1
    
    return stack_list

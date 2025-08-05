# -*- coding: utf-8 -*-
"""
Created on Thu May 22 20:17:48 2025

@author: Cameron-n

Page to search through all potion combinations

Features:
    - Get all potions with selected effects, sorted by
      number of +ve effects DESC, then number of -ve effects ASC
"""

# Maybe use dcc.datatable?

#%% Imports

# Standard
import pandas as pd

# Dash
import dash
from dash import callback, Input, Output, State
import dash_mantine_components as dmc

# Relative
from components.data_access import DF_INGREDIENTS
from components.combos import potion_combinations


#%% Boilerplate

if __name__ != '__main__':
    dash.register_page(__name__, path="/")


#%% Layout

# Add drop_columns to data_access?
drop_columns = ["Value", "Weight", "Ingredient", "Origin", "First Effect"]
effects_list = DF_INGREDIENTS.drop(drop_columns, axis=1).columns
effects_list = ["+", "-"] + list(effects_list)

effects = dmc.Stack([
    dmc.Group([
        dmc.Select(label="Effect 1",
                   data=effects_list,
                   value="",
                   id="Effect 1"),
        dmc.Select(label="Effect 2",
                   data=effects_list,
                   value="",
                   id="Effect 2"),
        dmc.Select(label="Effect 3",
                   data=effects_list,
                   value="",
                   id="Effect 3"),
        dmc.Select(label="Effect 4",
                   data=effects_list,
                   value="",
                   id="Effect 4"),
        ]),
    dmc.Group([
        dmc.Select(label="Effect 5",
                   data=effects_list,
                   value="",
                   id="Effect 5"),
        dmc.Select(label="Effect 6",
                   data=effects_list,
                   value="",
                   id="Effect 6"),
        dmc.Select(label="Effect 7",
                   data=effects_list,
                   value="",
                   id="Effect 7"),
        dmc.Select(label="Effect 8",
                   data=effects_list,
                   value="",
                   id="Effect 8"),
        ])
    ])

effects_with_button = dmc.Group([
    effects,
    dmc.Button("Calculate", id="Effect Button")
    ])

head = dmc.TableThead(
    dmc.TableTr(
        [
            dmc.TableTh("Ingredient 1"),
            dmc.TableTh("Ingredient 2"),
            dmc.TableTh("Ingredient 3"),
            dmc.TableTh("Ingredient 4"),
            dmc.TableTh("Effect 1"),
            dmc.TableTh("Effect 2"),
            dmc.TableTh("Effect 3"),
            dmc.TableTh("Effect 4"),
            dmc.TableTh("Effect 5"),
            dmc.TableTh("Effect 6"),
            dmc.TableTh("Effect 7"),
            dmc.TableTh("Effect 8"),
            ]
        )
    )

body = dmc.TableTbody(id="Effect Table")

caption = dmc.TableCaption("Testing test alchemy 123")

potions_table = dmc.Table([head, body, caption])
potions_table = dmc.TableScrollContainer(
    potions_table, minWidth=600, maxHeight=425
    )

layout=dmc.Stack([
    effects_with_button,
    potions_table,
    ])


#%% Callbacks

@callback(
    Output("Effect Table", "children"),
    Input("Effect Button", "n_clicks"),
    State("Effect 1", "value"),
    State("Effect 2", "value"),
    State("Effect 3", "value"),
    State("Effect 4", "value"),
    State("Effect 5", "value"),
    State("Effect 6", "value"),
    State("Effect 7", "value"),
    State("Effect 8", "value"),
    suppress_inital_callback=True
)
def calculate_potions(
        n_clicks,
        value_1,
        value_2,
        value_3,
        value_4,
        value_5,
        value_6,
        value_7,
        value_8
        ):
    """
    Get ingredient combinations from combos.py and
    formats the data for this page's table
    """

    restrictions = []
    for i in [value_1, value_2, value_3, value_4,
              value_5, value_6, value_7, value_8]:
        if i not in [None, "", []]:
            restrictions.append(i)
    
    # Get all possible potion combinations
    potions_1 = DF_INGREDIENTS.fillna(0)
    potions_2 = potion_combinations(potions_1, restrictions) # pairs
    potions_3 = potion_combinations(potions_2, restrictions) # triplets
    potions_4 = potion_combinations(potions_3, restrictions) # linked quads
    #potions_2_2 = potion_quads(potions_2, restrictions) # 2 unlinked pairs
    potions = pd.concat([potions_2, potions_3, potions_4])
    potions = potions.reset_index().drop("index", axis=1)
    
    # We remove the ingredients columns to do maths on
    # the effect columns. We'll save the ingredients to
    # add them back on later
    ingredients_columns = ["Ingredient", "Ingredient 2",
                           "Ingredient 3", "Ingredient 4"]
    potions_ingredients = potions[potions.columns.intersection(ingredients_columns)]
    potions = potions.drop(ingredients_columns, axis=1, errors='ignore')

    # potion_combinations returns all combinations where each 
    # ingredient has at least one of the restrictions. We need
    # to further limit this to combinations where every restriction
    # is included
    ingredients_restrictions = pd.Series([True for _ in range(len(potions))])
    for i in restrictions:
        ingredients_restrictions = ingredients_restrictions & (potions[i] == 2) 
    potions = potions[ingredients_restrictions]

    # A potion has an effect if at least 2 ingredients share that effect.
    # Here we replace the '2's in the dataframe with the actual effect names
    potions = potions.where(potions != 2, potions.columns.to_series(), axis=1)
    potions = potions.to_numpy()

    # Add the potion data to the dmc table
    potion_data = []
    for index, potion in enumerate(potions):

        # Remove effects not part of the ingredients (0)
        # or in only an ingredient but not the other (1)
        potion = potion[potion!=0]
        potion = potion[potion!=1]

        table_ingredients = []
        for j in range(4):
            try:
                table_ingredients.append(potions_ingredients.iloc[index][j])
            except IndexError:
                table_ingredients.append('')

        # We don't know ahead of time how many effects a
        # potion has. So, we have to act like all 8 are
        # possible and ignore if there are less
        table_effects = []
        for j in range(8):
            try:
                table_effects.append(potion[j])
            except IndexError:
                table_effects.append('')
        
        new_row = {
            "Ingredient 1":table_ingredients[0],
            "Ingredient 2":table_ingredients[1],
            "Ingredient 3":table_ingredients[2],
            "Ingredient 4":table_ingredients[3],
            "Effect 1":table_effects[0],
            "Effect 2":table_effects[1],
            "Effect 3":table_effects[2],
            "Effect 4":table_effects[3],
            "Effect 5":table_effects[4],
            "Effect 6":table_effects[5],
            "Effect 7":table_effects[6],
            "Effect 8":table_effects[7],
            }
        potion_data.append(new_row)
    
    rows = [
           dmc.TableTr([
               dmc.TableTd(potion_datum["Ingredient 1"]),
               dmc.TableTd(potion_datum["Ingredient 2"]),
               dmc.TableTd(potion_datum["Ingredient 3"]),
               dmc.TableTd(potion_datum["Ingredient 4"]),
               dmc.TableTd(potion_datum["Effect 1"]),
               dmc.TableTd(potion_datum["Effect 2"]),
               dmc.TableTd(potion_datum["Effect 3"]),
               dmc.TableTd(potion_datum["Effect 4"]),
               dmc.TableTd(potion_datum["Effect 5"]),
               dmc.TableTd(potion_datum["Effect 6"]),
               dmc.TableTd(potion_datum["Effect 7"]),
               dmc.TableTd(potion_datum["Effect 8"]),
               ])
           for potion_datum in potion_data
           ]
    
    return rows

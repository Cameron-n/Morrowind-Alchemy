# -*- coding: utf-8 -*-
"""
Created on Thu May 22 20:17:48 2025

@author: camer

Page to search through all potion combinations

Features:
    - Test
"""

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

effects_list = DF_INGREDIENTS.columns[3:] # Removes: Value, Weight, Ingredient
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
                   value="Test",
                   id="Effect 5"),
        dmc.Select(label="Effect 6",
                   data=effects_list,
                   value="Test",
                   id="Effect 6"),
        dmc.Select(label="Effect 7",
                   data=effects_list,
                   value="Test",
                   id="Effect 7"),
        dmc.Select(label="Effect 8",
                   data=effects_list,
                   value="Test",
                   id="Effect 8"),
        ])
    ])

potion_data = [
    {"Ingredient 1":1,"Ingredient 2":2,"Ingredient 3":3,"Ingredient 4":4}
    ]

row = [
       dmc.TableTr([
           dmc.TableTd(potion_datum["Ingredient 1"]),
           dmc.TableTd(potion_datum["Ingredient 2"]),
           dmc.TableTd(potion_datum["Ingredient 3"]),
           dmc.TableTd(potion_datum["Ingredient 4"]),
           ])
       for potion_datum in potion_data
       ]

head = dmc.TableThead(
    dmc.TableTr(
        [
            dmc.TableTh("Ingredient 1"),
            dmc.TableTh("Ingredient 2"),
            dmc.TableTh("Ingredient 3"),
            dmc.TableTh("Ingredient 4"),
            ]
        )
    )
body = dmc.TableTbody(row)
caption = dmc.TableCaption("Testing test alchemy 123")

potions_table = dmc.Table([head, body, caption])

layout=dmc.Stack([
    effects,
    potions_table,
    ])


#%% Functions




#%% Callbacks


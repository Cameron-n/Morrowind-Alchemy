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
import pandas as pd

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

def potion_combinations(ingredients, restrictions):
    """
    Find all 2 ingredient potion combinations with the particular effects
    chosen, i.e. the restrictions.

    """

    # Remove irrelevant columns. Store Ingredient names to add back later
    drop_columns = ["Value", "Weight", "Ingredient", "Origin"]
    ingredients_names = ingredients["Ingredient"]
    ingredients_matrix = ingredients.drop(drop_columns, axis=1)
    for j in restrictions:
        ingredients_matrix = ingredients_matrix[ingredients_matrix[j]==1]

    #TODO Remove duplicates. Currently, does AB BA | should do AB
    for i in ingredients_matrix.to_numpy():
        combos = ingredients_matrix*i
        combos = combos.dropna(how="all")
        combos = combos.dropna(how="all", axis=1)
        combos = combos.join(ingredients_names)
        print(combos)

    return combos

# ERROR
# Heartwood is labelled as "Resist Magicka" but should be "Restore Magicka"
# Deadra's Heart is labelled as "Resist Magicka" but should be "Restore Magicka"
# Wolf Pelt is labelled as "Burden" "Poison" "Restore Magicka" "Reflect" but is "Drain Fatigue" "Fortify Speed" "Resist Common Disease" "Night Eye"

# Notes on step-by-step process to calculate potion combos
# 1. User selects effects
    # Callback
# 2. Ingredients with those effects identified
    # e.g. a[a["Poison"]==1][a["Burden"]==1]
    # Need all ingredients with AT LEAST one effect from selection
# 3. Calculate all 2-potions
    # More than 4 effects => skip
    # Calculate all pairwise combos (use potion_combinations)
# 4. Calculate all 3-potions
    # More than 6 effects => skip
    # Calculate all minimal triplets by extending pairwise.
# 5. Calculate all 4-potions
    # Calculate all minimal quads by extending triplets
    # Calculate disjoint pairwise pairs by joining pairwise
# 6. Order potions by number of positive effects
# 7. Extend button. Adds more ingredient to minimal set based on +ve effects


#%% Callbacks


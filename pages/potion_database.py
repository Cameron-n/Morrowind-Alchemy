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
# green if +ve, red if -ve ?
# Limit by origin
# Send output to potion_maker?

#%% Imports

# Standard
import numpy as np
import pandas as pd

# Dash
import dash
from dash import callback, Input, Output, State
import dash_mantine_components as dmc

# Relative
from components.data_access import DF_INGREDIENTS, DF_EFFECTS
from components.combos import potion_combinations

DF_INGREDIENTS = DF_INGREDIENTS.fillna(0)
DF_EFFECTS = DF_EFFECTS.fillna(0)


#%% Boilerplate

if __name__ != '__main__':
    dash.register_page(__name__, path="/")


#%% Layout

drop_columns = ["Value", "Weight", "Ingredient", "Origin", "First Effect"]
effects_list = DF_INGREDIENTS.drop(drop_columns, axis=1).columns
effects_list = list(effects_list)

effects = dmc.Stack([
    dmc.Group([
        dmc.Select(label="Effect 1",
                   data=effects_list,
                   value="",
                   searchable=True,
                   id="Effect 1"),
        dmc.Select(label="Effect 2",
                   data=effects_list,
                   value="",
                   searchable=True,
                   id="Effect 2"),
        dmc.Select(label="Effect 3",
                   data=effects_list,
                   value="",
                   searchable=True,
                   id="Effect 3"),
        dmc.Select(label="Effect 4",
                   data=effects_list,
                   value="",
                   searchable=True,
                   id="Effect 4"),
    ]),
    dmc.Group([
        dmc.Select(label="Effect 5",
                   data=effects_list,
                   value="",
                   searchable=True,
                   id="Effect 5"),
        dmc.Select(label="Effect 6",
                   data=effects_list,
                   value="",
                   searchable=True,
                   id="Effect 6"),
        dmc.Select(label="Effect 7",
                   data=effects_list,
                   value="",
                   searchable=True,
                   id="Effect 7"),
        dmc.Select(label="Effect 8",
                   data=effects_list,
                   value="",
                   searchable=True,
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

layout = dmc.Stack([
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
    Get ingredient combinations and format the data in table form.

    Parameters
    ----------
    n_clicks : TYPE
        DESCRIPTION.
    value_1 : TYPE
        DESCRIPTION.
    value_2 : TYPE
        DESCRIPTION.
    value_3 : TYPE
        DESCRIPTION.
    value_4 : TYPE
        DESCRIPTION.
    value_5 : TYPE
        DESCRIPTION.
    value_6 : TYPE
        DESCRIPTION.
    value_7 : TYPE
        DESCRIPTION.
    value_8 : TYPE
        DESCRIPTION.

    Returns
    -------
    rows : TYPE
        DESCRIPTION.

    """
    restrictions = []
    for i in [value_1, value_2, value_3, value_4,
              value_5, value_6, value_7, value_8]:
        if i not in [None, "", []]:
            restrictions.append(i)

    # Get all possible potion combinations
    potions_1 = DF_INGREDIENTS
    potions_2 = potion_combinations(potions_1, restrictions)  # pairs
    potions_3 = potion_combinations(potions_2, restrictions)  # triplets
    potions_4 = potion_combinations(potions_3, restrictions)  # linked quads
    #potions_2_2 = potion_quads(potions_2, restrictions) # 2 unlinked pairs
    potions = pd.concat([potions_2, potions_3, potions_4])
    potions = potions.reset_index().drop("index", axis=1)

    # We remove the ingredients columns to do maths on
    # the effect columns. We'll save the ingredients to
    # add them back on later
    ingredients_columns = ["Ingredient", "Ingredient 2",
                           "Ingredient 3", "Ingredient 4"]
    shared_columns = potions.columns.intersection(ingredients_columns)
    potions_ingredients = potions[shared_columns]
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
    potions = potions.where(potions < 2, potions.columns.to_series(), axis=1)

    # Get the ingredient names indexed correctly after the .where operation
    potions_ingredients = potions.join(potions_ingredients)[shared_columns]
    potions = potions.to_numpy()

    # Add the potion data to the dmc table
    potion_as_words = []
    for index, potion in enumerate(potions):

        # Remove effects not part of the ingredients (0)
        # or in only an ingredient but not the other (1)
        potion = potion[potion != 0]
        potion = potion[potion != 1]
        potion_as_words.append(potion)
    
    # Sort by +ve effects descending, -ve effects ascending
    # BUG -> Does not reorder the ingredients
    potion_sorted = []
    for i in potion_as_words:
        total = len(i)
        num_pos = 0
        for j in i:
            num_pos -= DF_EFFECTS[DF_EFFECTS["Spell Effects"]==j]["Positive"].iloc[0]
        for j in range(8-len(i)):
            i=np.append(i, '')
        part_one = np.append(total+num_pos, i)
        potion_sorted.append(np.append(num_pos, part_one))
    
    dtype = [('pos', float),
             ('neg', float),
             ('e1', object),
             ('e2', object),
             ('e3', object),
             ('e4', object),
             ('e5', object),
             ('e6', object),
             ('e7', object),
             ('e8', object)]
    potion_sorted = [tuple(i) for i in potion_sorted]
    potion_sorted = np.array(potion_sorted, dtype=dtype)
    potion_sorted = np.sort(potion_sorted, order=['pos', 'neg'])
    
    potion_data = []
    for index, potion in enumerate(potion_sorted):

        table_ingredients = []
        for j in range(4):
            try:
                table_ingredients.append(potions_ingredients.iloc[index][j])
            except IndexError:
                table_ingredients.append('')

        new_row = {
            "Ingredient 1": table_ingredients[0],
            "Ingredient 2": table_ingredients[1],
            "Ingredient 3": table_ingredients[2],
            "Ingredient 4": table_ingredients[3],
            "Effect 1": potion[0+2],
            "Effect 2": potion[1+2],
            "Effect 3": potion[2+2],
            "Effect 4": potion[3+2],
            "Effect 5": potion[4+2],
            "Effect 6": potion[5+2],
            "Effect 7": potion[6+2],
            "Effect 8": potion[7+2],
        }
        potion_data.append(new_row)

    rows = [
        dmc.TableTr([
            dmc.TableTd(potion_datum["Ingredient 1"]),
            dmc.TableTd(potion_datum["Ingredient 2"]),
            dmc.TableTd(potion_datum["Ingredient 3"]),
            dmc.TableTd(potion_datum["Ingredient 4"]),
            dmc.TableTd(dmc.Text(potion_datum["Effect 1"], c="red" if DF_EFFECTS[DF_EFFECTS["Spell Effects"]==(potion_datum["Effect 1"] or "Drain Fatigue")]["Positive"].iloc[0]==0 else "green")),
            dmc.TableTd(dmc.Text(potion_datum["Effect 2"], c="red" if DF_EFFECTS[DF_EFFECTS["Spell Effects"]==(potion_datum["Effect 2"] or "Drain Fatigue")]["Positive"].iloc[0]==0 else "green")),
            dmc.TableTd(dmc.Text(potion_datum["Effect 3"], c="red" if DF_EFFECTS[DF_EFFECTS["Spell Effects"]==(potion_datum["Effect 3"] or "Drain Fatigue")]["Positive"].iloc[0]==0 else "green")),
            dmc.TableTd(dmc.Text(potion_datum["Effect 4"], c="red" if DF_EFFECTS[DF_EFFECTS["Spell Effects"]==(potion_datum["Effect 4"] or "Drain Fatigue")]["Positive"].iloc[0]==0 else "green")),
            dmc.TableTd(dmc.Text(potion_datum["Effect 5"], c="red" if DF_EFFECTS[DF_EFFECTS["Spell Effects"]==(potion_datum["Effect 5"] or "Drain Fatigue")]["Positive"].iloc[0]==0 else "green")),
            dmc.TableTd(dmc.Text(potion_datum["Effect 6"], c="red" if DF_EFFECTS[DF_EFFECTS["Spell Effects"]==(potion_datum["Effect 6"] or "Drain Fatigue")]["Positive"].iloc[0]==0 else "green")),
            dmc.TableTd(dmc.Text(potion_datum["Effect 7"], c="red" if DF_EFFECTS[DF_EFFECTS["Spell Effects"]==(potion_datum["Effect 7"] or "Drain Fatigue")]["Positive"].iloc[0]==0 else "green")),
            dmc.TableTd(dmc.Text(potion_datum["Effect 8"], c="red" if DF_EFFECTS[DF_EFFECTS["Spell Effects"]==(potion_datum["Effect 8"] or "Drain Fatigue")]["Positive"].iloc[0]==0 else "green")),
        ])
        for potion_datum in potion_data
    ]

    return rows

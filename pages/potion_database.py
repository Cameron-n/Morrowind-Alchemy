# -*- coding: utf-8 -*-
"""
Created on Thu May 22 20:17:48 2025

@author: Cameron-n

Page to search through all potion combinations

Features:
    - Get all potions with selected effects, sorted by
      number of +ve effects DESC, then number of -ve effects ASC
"""

# Send output to potion_maker? [high-reward, mid-effort]
# Sometimes loading overlay doesn't disappear

#%% Imports

# Standard
import time
import numpy as np
import pandas as pd

# Dash
import dash
from dash import callback, Input, Output, State, dcc, clientside_callback
import dash_mantine_components as dmc

# Relative
from components.data_access import DF_INGREDIENTS, DF_EFFECTS
from components.combos import potion_combinations, potion_quads

DF_INGREDIENTS = DF_INGREDIENTS.fillna(0)
DF_EFFECTS = DF_EFFECTS.fillna(0)


#%% Boilerplate

if __name__ != '__main__':
    dash.register_page(__name__)


#%% Layout

text = """
1. Select the effects you want to include in the resulting potions.
2. Press Calculate to find these potions.
3. Limit the origins of the ingredients to include or exclude mods, dlcs, or base game ingredients.
"""

explain_title = dmc.Title("Potion Database", order=3)
explain_text = dmc.Text(text, style={"white-space": "pre-wrap"})
explain_stack = dmc.Stack([
    explain_title,
    explain_text,
],
    gap=0
)

data_origin = DF_INGREDIENTS["Origin"].unique()
origin_selecter = dmc.MultiSelect(label="Origins", data=data_origin,
                                  w=200, id="data-origins")

effects_list = list(DF_EFFECTS["Spell Effects"])
effects = dmc.Stack([
    dmc.Group([
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
        ], justify="center", wrap="nowrap"),
        dmc.Group([
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
        ], justify="center", wrap="nowrap"),
    ], justify="center"),
    dmc.Group([
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
        ], justify="center", wrap="nowrap"),
        dmc.Group([
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
        ], justify="center", wrap="nowrap")
    ], justify="center")
])

calc_button = dmc.Button("Calculate", id="Effect Button")
down_button = dmc.Button("Download", id="Download Button")
buttons = dmc.Group([
    calc_button,
    down_button,
    dcc.Store(id="potion-database-store"),
    dcc.Download(id="potion-database-download"),
    ], wrap="nowrap")

effects_with_button = dmc.Stack([
    explain_stack,
    origin_selecter,
    effects,
    buttons,
],
    align="center"
)

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

caption = dmc.TableCaption("End of Table")

potions_table = dmc.Table([head, body, caption],
                          withTableBorder=True,
                          highlightOnHover=True,
                          highlightOnHoverColor="myColors.8",
                          striped=True,
                          )
potions_table = dmc.TableScrollContainer(
    potions_table, minWidth=0, maxHeight=425, type="native"
)

loading_overlay = dmc.LoadingOverlay(id="data-loader-overlay")

potions_table = dmc.Box([
    loading_overlay,
    potions_table,
], pos="relative")

layout = dmc.Stack([
    effects_with_button,
    potions_table,
])


#%% Callbacks

clientside_callback(
    """
    function updateLoadingState(n_clicks) {
        return true
    }
    """,
    Output("data-loader-overlay", "visible"),
    Input("Effect Button", "n_clicks"),
    prevent_initial_call=True,
)


@callback(
    Output("Effect Table", "children"),
    Output("data-loader-overlay", "visible", allow_duplicate=True),
    Output("potion-database-store", "data"),
    Input("Effect Button", "n_clicks"),
    State("data-origins", "value"),
    State("Effect 1", "value"),
    State("Effect 2", "value"),
    State("Effect 3", "value"),
    State("Effect 4", "value"),
    State("Effect 5", "value"),
    State("Effect 6", "value"),
    State("Effect 7", "value"),
    State("Effect 8", "value"),
    prevent_initial_call=True
)
def calculate_potions(
        n_clicks,
        origins,
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
    # Used to cause the callback to trigger *after* the
    # loader is set to visible. Otherwise, the loader may
    # be set to False here, *then* set to True afterwards.
    time.sleep(0.1)

    if not (value_1 or value_2 or value_3 or value_4 or
            value_5 or value_6 or value_7 or value_8):
        return [], False, dash.no_update

    restrictions = []
    for i in [value_1, value_2, value_3, value_4,
              value_5, value_6, value_7, value_8]:
        if i not in [None, "", []]:
            restrictions.append(i)

    # Limit to selected origins
    # BUG: see "Bloodmoon" -> "Weakness to Fire"
    origin_limited = DF_INGREDIENTS.copy()
    if origins:
        origin_limited = origin_limited[origin_limited["Origin"].isin(origins)]
        origin_limited = origin_limited.reset_index().drop("index", axis=1)

    # Get all possible potion combinations
    potions_1 = origin_limited
    potions_2 = potion_combinations(potions_1, origin_limited, restrictions)  # pairs
    potions_3 = potion_combinations(potions_2, origin_limited, restrictions)  # triplets
    potions_4 = potion_combinations(potions_3, origin_limited, restrictions)  # linked quads
    potions_2_2 = potion_quads(potions_2) # 2 unlinked pairs
    potions = pd.concat([potions_2, potions_3, potions_4, potions_2_2])
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
    if not potions.empty:
        ingredients_restrictions = pd.Series([True for _ in range(len(potions))])
        for i in restrictions:
            ingredients_restrictions = ingredients_restrictions & (potions[i] == 2)
        potions = potions[ingredients_restrictions]

    # A potion has an effect if at least 2 ingredients share that effect.
    # Here we replace the '2's in the dataframe with the actual effect names
    potions = potions.where(potions < 2, potions.columns.to_series(), axis=1)

    # Get the ingredient names indexed correctly after the .where operation
    potions_ingredients = potions.join(potions_ingredients)[shared_columns]
    potions_ingredients = potions_ingredients.fillna('')
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
    potion_sorted = []
    for i in potion_as_words:
        total = len(i)
        num_pos = 0
        for j in i:
            num_pos -= DF_EFFECTS[DF_EFFECTS["Spell Effects"] == j]["Positive"].iloc[0]
        for j in range(8 - len(i)):
            i = np.append(i, '')
        part_one = np.append(total+num_pos, i)
        potion_sorted.append(np.append(num_pos, part_one))

    ingredients_sorted = []
    potions_ingredients = potions_ingredients.to_numpy()
    for i in potions_ingredients:
        for j in range(4-len(i)):
            i = np.append(i, '')
        ingredients_sorted.append(i)

    if potion_sorted != []:
        potion_sorted = np.append(ingredients_sorted, potion_sorted, axis=1)

    dtype = [('ing 1', object),
             ('ing 2', object),
             ('ing 3', object),
             ('ing 4', object),
             ('pos', float),
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
        new_row = {
            "Ingredient 1": potion[0],
            "Ingredient 2": potion[1],
            "Ingredient 3": potion[2],
            "Ingredient 4": potion[3],
            "Effect 1": potion[4+2],
            "Effect 2": potion[5+2],
            "Effect 3": potion[6+2],
            "Effect 4": potion[7+2],
            "Effect 5": potion[8+2],
            "Effect 6": potion[9+2],
            "Effect 7": potion[10+2],
            "Effect 8": potion[11+2],
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

    potion_data = pd.DataFrame(potion_data).to_json(date_format='iso', orient='split')

    return rows, False, potion_data


@callback(
    Output("potion-database-download", "data"),
    State("potion-database-store", "data"),
    Input("Download Button", "n_clicks"),
    prevent_initial_call=True
    )
def download_table(data, n_clicks):
    if not data:
        data = pd.DataFrame([])
    else:
        data = pd.read_json(data, orient='split')
    return dcc.send_data_frame(data.to_csv, "morrowind-potions.csv", index=False)

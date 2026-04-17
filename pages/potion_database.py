# -*- coding: utf-8 -*-
"""
Created on Thu May 22 20:17:48 2025

@author: Cameron-n

Page to search through all potion combinations

Features:
    - Get all potions with selected effects, sorted by
      number of +ve effects DESC, then number of -ve effects ASC
"""

# Send output to potion_maker? [high-reward, mid-effort, stretch-goal]
# Reverse order (for poisons)
# Indicate if further effects are possible (no 4th ingredient in at least one column)

#%% Imports

# Standard
import numpy as np
import pandas as pd

# Dash
import dash
from dash import callback, Input, Output, State, dcc, clientside_callback
import dash_mantine_components as dmc

# Relative
from components.data_access import DF_INGREDIENTS, DF_EFFECTS
from components.combos import potion_combinations

DF_INGREDIENTS = DF_INGREDIENTS.fillna(0)
DF_EFFECTS = DF_EFFECTS.fillna(0)


#%% Boilerplate

if __name__ != '__main__':
    dash.register_page(__name__)


#%% Layout

text = """
1. Select the effects you want.
2. (Optional) Limit the origins of the ingredients.
3. Press Calculate.
"""

explain_stack = dmc.Stack([
    dmc.Title("Potion Database", order=3),
    dmc.Text(text, style={"white-space": "pre-wrap"}),
],
    gap=0
)

data_origin = DF_INGREDIENTS["Origin"].unique()
origin_selecter = dmc.Container(
    dmc.MultiSelect(
        label="Origins",
        value=["Base", "Tribunal", "Bloodmoon"],
        data=data_origin,
        w=200,
        id="data-origins",
        )
    )

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
        ], wrap="nowrap"),
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
        ], wrap="nowrap"),
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
        ], wrap="nowrap"),
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
        ], wrap="nowrap")
    ], justify="center")
])

calc_button = dmc.Button("Calculate", id="Effect Button")
down_button = dmc.Button("Download", id="Download Button")
mwse_button = dmc.Checkbox("MWSE", id="potion-database-MWSE")
pois_button = dmc.Checkbox("Poison", id="potion-database-poison")
buttons = dmc.Group([
    calc_button,
    down_button,
    mwse_button,
    pois_button,
    dcc.Store(id="potion-database-store", storage_type='session'),
    dcc.Download(id="potion-database-download"),
    ], justify="center", wrap="nowrap")

effects_with_button = dmc.Stack([
    explain_stack,
    origin_selecter,
    effects,
    buttons,
], align="center")

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
                          stickyHeader=True,
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
    dmc.Box(id="dummy-input"),
], style={"margin": "auto", "max-width": "1500px"})


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
    State("potion-database-MWSE", "checked"),
    State("potion-database-poison", "checked"),
    [State(f"Effect {i+1}", "value") for i in range(8)],
    prevent_initial_call=True
)
def calculate_potions(
        n_clicks,
        origins,
        mwse,
        poison,
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
    if not origins:
        return [], False, dash.no_update
    
    if not (value_1 or value_2 or value_3 or value_4 or
            value_5 or value_6 or value_7 or value_8):
        return [], False, dash.no_update

    restrictions = []
    for i in [value_1, value_2, value_3, value_4,
              value_5, value_6, value_7, value_8]:
        if i not in [None, "", []]:
            restrictions.append(i)

    # Limit to selected origins
    origin_limited = DF_INGREDIENTS.copy()
    if mwse:
        origin_limited = origin_limited.replace(-1, 0)
        origin_limited = origin_limited.replace(-2, 1)
    else:
        origin_limited = origin_limited.replace(-1, 1)
        origin_limited = origin_limited.replace(-2, 0)

    if origins:
        origin_limited = origin_limited[origin_limited["Origin"].isin(origins)]
        origin_limited = origin_limited.reset_index().drop("index", axis=1)

    # Get all possible potion combinations
    potions = potion_combinations(origin_limited, restrictions, poison)

    potion_data = []
    for i in potions.index:
        new_row = {
            "Ingredient 1": potions.iloc[i].get("ing1", ''),
            "Ingredient 2": potions.iloc[i].get("ing2", ''),
            "Ingredient 3": potions.iloc[i].get("ing3", ''),
            "Ingredient 4": potions.iloc[i].get("ing4", ''),
            "Effect 1": potions.iloc[i].get(0, '') if type(potions.iloc[i].get(0, ''))!=type(1.0) else '', # '' if missing on nan
            "Effect 2": potions.iloc[i].get(1, '') if type(potions.iloc[i].get(1, ''))!=type(1.0) else '',
            "Effect 3": potions.iloc[i].get(2, '') if type(potions.iloc[i].get(2, ''))!=type(1.0) else '',
            "Effect 4": potions.iloc[i].get(3, '') if type(potions.iloc[i].get(3, ''))!=type(1.0) else '',
            "Effect 5": potions.iloc[i].get(4, '') if type(potions.iloc[i].get(4, ''))!=type(1.0) else '',
            "Effect 6": potions.iloc[i].get(5, '') if type(potions.iloc[i].get(5, ''))!=type(1.0) else '',
            "Effect 7": potions.iloc[i].get(6, '') if type(potions.iloc[i].get(6, ''))!=type(1.0) else '',
            "Effect 8": potions.iloc[i].get(7, '') if type(potions.iloc[i].get(7, ''))!=type(1.0) else '',
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
    [State(f"Effect {i+1}", "value") for i in range(8)],
    Input("Download Button", "n_clicks"),
    prevent_initial_call=True
    )
def download_table(data, value_1, value_2, value_3, value_4, value_5, value_6, value_7, value_8, n_clicks):
    if not data:
        data = pd.DataFrame([])
    else:
        data = pd.read_json(data, orient='split')
        data.loc[-1] = ['Selected Effects', '', '', '', value_1, value_2, value_3, value_4, value_5, value_6, value_7, value_8]
        data.index = data.index + 1
        data = data.sort_index()
    return dcc.send_data_frame(data.to_csv, "morrowind-potions.csv", index=False)


@callback(
    Output("Effect Table", "children", allow_duplicate=True),
    State("potion-database-store", "data"),
    Input("dummy-input", "children"),
    prevent_initial_call="initial duplicate"
    )
def load_last_table(data, n_clicks):

    if data:
        data = pd.read_json(data, orient='split')
        data = [data.iloc[i].to_dict() for i in range(len(data))]
        
        rows = [dmc.TableTr([
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
            for potion_datum in data
            ]
        
        return rows
    else:
        return dash.no_update

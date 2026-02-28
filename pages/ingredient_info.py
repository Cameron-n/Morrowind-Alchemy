# -*- coding: utf-8 -*-
"""
Created on Thu May 22 20:17:00 2025

@author: camer
"""

# ingredients name icon location effects price weight

#%% Imports

# Standard

# Dash
import dash
from dash import callback, Input, Output
import dash_mantine_components as dmc
import dash_leaflet as dl

# Relative
from components.data_access import DF_INGREDIENTS, DF_EFFECTS


#%% Boilerplate

if __name__ != '__main__':
    dash.register_page(__name__)


#%% Layout

url = "https://github.com/Cameron-n/Cameron-n.github.io/raw/main/maps/TD25.05TR25.05Cyr21.21aSky24.12b/{z}/{x}/{y}.png"

DF_EFFECTS.fillna(0, inplace=True)

data_origins = DF_INGREDIENTS["Origin"].unique()

grouped_data = [
    {
        "group": name,
        "items": DF_INGREDIENTS["Ingredient"][DF_INGREDIENTS["Origin"] == name]
    } for name in data_origins
]

layout = dmc.Stack([
    dmc.Group([
        dmc.Stack([
            dmc.Title("Ingredient Info", order=3),
            dmc.Select(
                value="",
                data=grouped_data,
                searchable=True,
                clearable=True,
                w=250,
                id="ingredient_info_select_ing",
                ),
            ]),
        dmc.Image(w=100, id="ingredient_info_image"),
        ], justify="space-between"),
    dmc.Group([
        dmc.Group([
            dmc.Text(id="ingredient_info_price"),
            dmc.AspectRatio(dmc.Image(src="assets/misc_icons/MW-icon-Gold.png"), ratio=1/1),
            ]),
        dmc.Group([
            dmc.Text(id="ingredient_info_weight"),
            dmc.AspectRatio(dmc.Image(src="assets/misc_icons/MW-icon-Weight.png"), ratio=1/1),
            ]),
        ]),
    dmc.Stack([
        dmc.Title("Effects", order=4),
        dmc.Box(id="ingredient_info_effects"),
        ]),
    dmc.Stack([
        dmc.Title("Locations", order=4),
        dl.Map(
            dl.TileLayer(url=url, maxZoom=7, minZoom=0, noWrap=True),
            center=[70, -50], zoom=1, style={"height": "50vh", "background-color": "rgba(33,32,28,1.0)"}
            )
        ]),
    ], style={"margin": "auto", "max-width": "500px"})


#%% Functions


#%% Callbacks

@callback(
    Output("ingredient_info_effects", "children"),
    Output("ingredient_info_price", "children"),
    Output("ingredient_info_weight", "children"),
    Input("ingredient_info_select_ing", "value")
)
def update_effect_list(value):
    """Get an ingredient's effects and return a list of dmc.Text objects"""
    if value in [None,"",[]]:
        return None, dmc.Image(src="placeholder"), dmc.Image(src="placeholder")
    # Get list of up to 4 effects from DF_INGREDIENTS
    ingredient_row = DF_INGREDIENTS[DF_INGREDIENTS["Ingredient"] == value]
    ingredient_row_not_nan = ingredient_row.notna().iloc[0]
    columns_not_nan = DF_INGREDIENTS.columns[ingredient_row_not_nan]
    
    price = ingredient_row["Value"].iloc[0]
    price = f"{str(price):<6}" # Doesn't work (pad with spaces)
    weight = ingredient_row["Weight"].iloc[0]
    weight = f"{str(weight):<6}"

    effects = list(columns_not_nan)
    effects.remove("Value")
    effects.remove("Weight")
    effects.remove("Ingredient")
    effects.remove("Origin")
    effects.remove("First Effect")

    # Add components
    content = [dmc.Text(i, truncate="end") for i in effects]

    return content, price, weight


@callback(
    Output("ingredient_info_image", "src"),
    Input("ingredient_info_select_ing", "value")
)
def update_image(value):
    if value:
        value = value.replace(" ", "_")
        src = f"assets/ingredient_icons/MW-icon-ingredient-{value}.png"
    else:
        src= ""

    return src

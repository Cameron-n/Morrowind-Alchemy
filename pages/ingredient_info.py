# -*- coding: utf-8 -*-
"""
Created on Thu May 22 20:17:00 2025

@author: camer
"""

# ingredients name icon location effects price weight

#%% Imports

# Standard
import pandas as pd

# Dash
import dash
from dash import callback, Input, Output
import dash_mantine_components as dmc
import dash_leaflet as dl

# Relative
from components.data_access import db, DF_INGREDIENTS, DF_EFFECTS, NPCtoCell, IngtoNPC, Ingredient


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

crs = "Simple"

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
            dmc.AspectRatio(dmc.Image(src="assets/icons/gold.png"), ratio=1/1),
            ]),
        dmc.Group([
            dmc.Text(id="ingredient_info_weight"),
            dmc.AspectRatio(dmc.Image(src="assets/icons/weight.png"), ratio=1/1),
            ]),
        ]),
    dmc.Stack([
        dmc.Title("Effects", order=4),
        dmc.Box(id="ingredient_info_effects"),
        ]),
    dmc.Stack([
        dmc.Title("Locations", order=4),
        dl.Map([
            dl.TileLayer(url=url, maxZoom=8, minZoom=0, noWrap=True),
            ], #+ markerslist,
            center=[70, -50], zoom=1, style={"height": "50vh", "background-color": "rgba(33,32,28,1.0)"}, crs=crs,
            id="ingredient_info_markers"
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
    ingredient_row_not_nan = ingredient_row[ingredient_row != 0].notna().iloc[0]
    columns_not_nan = DF_INGREDIENTS.columns[ingredient_row_not_nan]
    
    price = ingredient_row["Value"].iloc[0]
    price = f"{str(price):<6}" # Doesn't work (pad with spaces)
    weight = ingredient_row["Weight"].iloc[0]
    weight = f"{str(weight):<6}"

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

    return content, price, weight


@callback(
    Output("ingredient_info_image", "src"),
    Input("ingredient_info_select_ing", "value")
)
def update_image(value):
    icon = db.session.execute(db.select(Ingredient.Icon)
                              .where(Ingredient.Ingredient == value))
    icon = icon.scalar()

    if value:
        value = value.replace(" ", "_")
        icon = icon.replace("\\", "/")
        src = f"assets/icons/{icon}.png"
    else:
        src= ""

    return src

@callback(
    Output("ingredient_info_markers", "children"),
    Input("ingredient_info_select_ing", "value")
)
def update_markers(value):
    #database request for npcs
    ids = db.session.execute(db.select(Ingredient.ID)
                             .where(Ingredient.Ingredient == value))
    ids = ids.scalar()
    
    if not ids:
        return dl.TileLayer(url=url, maxZoom=8, minZoom=0, noWrap=True)

    df_npc = pd.DataFrame(db.session.execute(db.select(
        NPCtoCell.Name, NPCtoCell.CellX, NPCtoCell.CellY)
        .join(IngtoNPC, NPCtoCell.Name == IngtoNPC.NPCName)
        .where(IngtoNPC.Name == ids)))

    markerslist = [
        dl.Marker(position=[y - 34, x + 139], children=[dl.Tooltip(content=content)]) for content, x, y in zip(df_npc["Name"], df_npc["CellX"], df_npc["CellY"])
        ]
    
    tile_and_markers = [dl.TileLayer(url=url, maxZoom=8, minZoom=0, noWrap=True)] + markerslist
    
    return tile_and_markers

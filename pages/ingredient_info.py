# -*- coding: utf-8 -*-
"""
Created on Thu May 22 20:17:00 2025

@author: camer
"""

# ingredients name icon location effects price weight


#%% Imports

# Standard
from random import random
import pandas as pd

# Dash
import dash
from dash import callback, Input, Output
import dash_mantine_components as dmc
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import Namespace

# Relative
from components.data_access import (
    db, DF_INGREDIENTS, DF_EFFECTS, NPCtoCell, IngtoNPC, ContainertoCell,
    FloratoCell, IngtoContainer, IngtoFauna, IngtoFlora, IngtoLoose,
    LvlcretoCell, Ingredient
    )


#%% Boilerplate

if __name__ != '__main__':
    dash.register_page(__name__)
    
ns = Namespace("myNamespace", "mySubNamespace")


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

info = dmc.Stack([
    dmc.Group([
        dmc.Stack([
            dmc.Title("Ingredient Info", order=3),
            dmc.Select(
                value="",
                data=grouped_data,
                searchable=True,
                clearable=True,
                w=250,
                comboboxProps={"zIndex": 1000}, # Otherwise map overlays it
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
    ])

leaf_map = dmc.Stack([
        dmc.Title("Locations", order=4),
        dl.Map([
            dl.TileLayer(url=url, maxZoom=8, minZoom=0, noWrap=True),
            dl.LayersControl([
                    dl.Overlay(dl.LayerGroup(id="ingredient_info_npcs"), name="NPCs", checked=True),
                    dl.Overlay(dl.LayerGroup(id="ingredient_info_fauna"), name="Fauna", checked=True),
                    dl.Overlay(dl.LayerGroup(id="ingredient_info_flora"), name="Flora", checked=True),
                    dl.Overlay(dl.LayerGroup(id="ingredient_info_containers"), name="Containers", checked=True),
                    dl.Overlay(dl.LayerGroup(id="ingredient_info_loose"), name="Loose", checked=True)
                ])
            ],
            center=[-50, 100], zoom=1, className="map-size", crs=crs,
            )
        ])

layout = dmc.Grid([
    dmc.GridCol(info, span=4),
    dmc.GridCol(leaf_map, span=8),
    ], 
    style={"margin": "auto", "max-width": "1000px"}, 
    grow=True,
    align="stretch"
    )

#%% Functions
def dataframe_to_geojson(df, icon, interior="{cellname}<br>Count: {count}", exterior="{cellname}"):
    df.head()
    if not df.empty:
        markerslist = dlx.dicts_to_geojson(
            [
                dict(
                    lat=y - 34,
                    lon=x + 139,
                    popup=interior
                    .format(name=name, cellname=cellname, count=count) 
                    if isInterior==1 else 
                    exterior
                    .format(name=name, cellname=cellname), icon=icon) 
                for name, isInterior, count, cellname, x, y in
                zip(df["Name"], df["IsInterior"], df["Count"], df["CellName"], df["CellX"], df["CellY"])
                ]
            )

        # BUG: GeoJSON uses Supercluster which uses mercator projection.
        # This causes points outside of LAT [-90, 90] and LNG [-90, 90]
        # to be 'clamped' at those values when clustering.
        markerslist = dl.GeoJSON(
            data=markerslist, 
            cluster=True,
            pointToLayer=ns("pointToLayer"),
            superClusterOptions={"maxZoom": 7},
            #spiderfyOnMaxZoom=False,
            )
    else:
        markerslist = None
    return markerslist

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
    
    mwse_effect = ingredient_row[ingredient_row == -2].notna().iloc[0]
    mwse_effect = DF_INGREDIENTS.columns[mwse_effect]
    mwse_effect = list(mwse_effect)
    
    not_mwse_effect = ingredient_row[ingredient_row == -1].notna().iloc[0]
    not_mwse_effect = DF_INGREDIENTS.columns[not_mwse_effect]
    not_mwse_effect = list(not_mwse_effect)
    
    price = ingredient_row["Value"].iloc[0]
    price = f"{str(price):<6}" # Doesn't work (pad with spaces)
    weight = ingredient_row["Weight"].iloc[0]
    weight = f"{str(weight):<6}"
    first = ingredient_row["First Effect"].iloc[0]

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
    effects.remove(first)

    if not_mwse_effect:
        if not_mwse_effect == [first]:
            first = not_mwse_effect[0] + '/' + mwse_effect[0]
        else:
            for k, v in enumerate(effects):
                if v == not_mwse_effect[0]:
                    effects[k] += '/' + mwse_effect[0]
        effects.remove(mwse_effect[0])

    # Add components
    content = [dmc.Text(i, truncate="end") for i in effects]
    content = [first] + content

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
        src = f"assets/icons/{icon.lower()}.png"
    else:
        src= ""

    return src


@callback(
    Output("ingredient_info_npcs", "children"),
    Output("ingredient_info_fauna", "children"),
    Output("ingredient_info_flora", "children"),
    Output("ingredient_info_containers", "children"),
    Output("ingredient_info_loose", "children"),
    Input("ingredient_info_select_ing", "value")
)
def update_markers(value):
    # Note: React calls updateMarker() instead of creating new markers
    # in some instances. This updates the position of markers, but
    # *not* their content. To circument this, the markers are given id's
    # that are hopefully unique. This is a 'quick' solution that may still
    # cause issues in the future.
    # Credit: https://github.com/emilhe/dash-leaflet/issues/229

    #database request for npcs
    ids = db.session.execute(db.select(Ingredient.ID)
                             .where(Ingredient.Ingredient == value))
    ids = ids.scalar()

    if not ids:
        return None, None, None, None, None

    icon = db.session.execute(db.select(Ingredient.Icon)
                              .where(Ingredient.Ingredient == value))
    icon = icon.scalar().lower()

    df_npc = pd.DataFrame(db.session.execute(db.select(
        IngtoNPC.Count, NPCtoCell.CellName, NPCtoCell.Name, NPCtoCell.CellX, NPCtoCell.CellY)
        .join(IngtoNPC, NPCtoCell.Name == IngtoNPC.NPCName)
        .where(IngtoNPC.Name == ids)))

    df_fauna = pd.DataFrame(db.session.execute(db.select(
        IngtoFauna.Name, IngtoFauna.CountC, LvlcretoCell.IsInterior, LvlcretoCell.CellName, LvlcretoCell.CellX, LvlcretoCell.CellY)
        .join(IngtoFauna, LvlcretoCell.ID == IngtoFauna.ID)
        .where(IngtoFauna.Ingredient == ids)))
    if not df_fauna.empty:
        df_fauna["Count"] = df_fauna["CountC"]

    df_flora = pd.DataFrame(db.session.execute(db.select(
        IngtoFlora.CountC, FloratoCell.IsInterior, FloratoCell.Count, FloratoCell.CellName, FloratoCell.CellX, FloratoCell.CellY)
        .join(IngtoFlora, FloratoCell.ID == IngtoFlora.ID)
        .where(IngtoFlora.Ingredient == ids)))
    if not df_flora.empty:
        df_flora["Count"] *= df_flora["CountC"]
        df_flora = df_flora.assign(Name='')
    
    df_cont = pd.DataFrame(db.session.execute(db.select(
        IngtoContainer.CountC, ContainertoCell.IsInterior, ContainertoCell.Count, ContainertoCell.CellName, ContainertoCell.CellX, ContainertoCell.CellY)
        .join(IngtoContainer, ContainertoCell.ID == IngtoContainer.ID)
        .where(IngtoContainer.Ingredient == ids)))
    if not df_cont.empty:
        df_cont["Count"] *= df_cont["CountC"]
        df_cont = df_cont.assign(Name='')

    df_loose = pd.DataFrame(db.session.execute(db.select(
        IngtoLoose.IsInterior, IngtoLoose.Count, IngtoLoose.CellName, IngtoLoose.CellX, IngtoLoose.CellY)
        .where(IngtoLoose.ID == ids)))
    if not df_loose.empty:
        df_loose = df_loose.assign(Name='')

    if not df_npc.empty:
        markerslist_npc = [
            dl.Marker(id=str([y - 34, x + 139 + random()]), position=[y - 34, x + 139], children=[dl.Tooltip(content=f"{cellname}<br>{name}<br>Count: {count}")]) 
            for count, cellname, name, x, y in 
            zip(df_npc["Count"], df_npc["CellName"], df_npc["Name"], df_npc["CellX"], df_npc["CellY"])
            ]
    else:
        markerslist_npc = None

    markerslist_fauna = dataframe_to_geojson(df_fauna, "m/tx_alembic_05", interior="{cellname}<br>Name: {name}", exterior="{cellname}<br>Name: {name}")
    markerslist_flora = dataframe_to_geojson(df_flora, icon)
    markerslist_cont = dataframe_to_geojson(df_cont, "m/tx_calcinator_05")
    markerslist_loose = dataframe_to_geojson(df_loose, "m/tx_retort_05")

    return markerslist_npc, markerslist_fauna, markerslist_flora, markerslist_cont, markerslist_loose

# -*- coding: utf-8 -*-
"""
Created on Wed May 21 21:41:23 2025

@author: Cameron-n

Page to add ingredients to the database. Password protected
"""

# TODO
# Error handling:
    # Property 1 empty
    # Any cells empty
    # Duplicate ingredient name (overwrite?)
    # Other database errors
# Password protect on server
# Feedback on success
# Boxes to dropdown/limit input type

#%% Imports

# Standard

# Dash
import dash
from dash import callback, Input, State
import dash_mantine_components as dmc

# Relative
from components.data_access import db, Ingredient, DF_INGREDIENTS

#%% Boilerplate

if __name__ != '__main__':
    dash.register_page(__name__)


#%% Layout

first_three = dmc.Group([
        dmc.NumberInput(label="Value", min=0, required=True, id="textinput_value"),
        dmc.NumberInput(label="Weight", min=0, required=True, id="textinput_weight"),
        dmc.TextInput(label="Ingredient", required=True, id="textinput_ingredient"),
        dmc.TextInput(label="Origin", required=True, id="textinput_origin"),
        ],
    grow=True,
    wrap="nowrap")

# Add drop_columns to data_access
drop_columns = ["Value", "Weight", "Ingredient", "Origin", "First Effect"]
data = DF_INGREDIENTS.drop(drop_columns, axis=1).columns

properties = dmc.Group([
        dmc.Select(label="Property 1", data=data, clearable=False, required=True, id="textinput_property_1"),
        dmc.Select(label="Property 2", data=data, clearable=True, id="textinput_property_2"),
        dmc.Select(label="Property 3", data=data, clearable=True, id="textinput_property_3"),
        dmc.Select(label="Property 4", data=data, clearable=True, id="textinput_property_4"),
        ],
    grow=True,
    wrap="nowrap")


button = dmc.Button("Add Ingredient", c="myColors.9", id="button_add_ingredient")

layout = dmc.Stack([
    first_three,
    properties,
    button,
    ])


#%% Callbacks

@callback(
    State("textinput_value", "value"),
    State("textinput_weight", "value"),
    State("textinput_ingredient", "value"),
    State("textinput_origin", "value"),
    State("textinput_property_1", "value"),
    State("textinput_property_2", "value"),
    State("textinput_property_3", "value"),
    State("textinput_property_4", "value"),
    Input("button_add_ingredient","n_clicks"),
    )
def on_add_ingredient_button_clicked(
        value_value, 
        value_weight, 
        value_ingredient,
        value_origin,
        value_property_1, 
        value_property_2, 
        value_property_3, 
        value_property_4,
        n_clicks
        ):
    """
    Adds ingredient and properties to database
    """

    properties = [value_property_1, value_property_2, 
                  value_property_3 , value_property_4]

    effects = {i.replace(" ","_") : '1' for i in properties if i is not None}

    new_ingredient = Ingredient(
        Value=value_value,
        Weight=value_weight,
        Ingredient=value_ingredient,
        Origin=value_origin,
        First_Effect=value_property_1,
        **effects,
        )
    
    db.session.add(new_ingredient)
    db.session.commit()

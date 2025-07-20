# -*- coding: utf-8 -*-
"""
Created on Wed May 21 21:41:23 2025

@author: camer

Page to add ingredients to the database. Password protected
"""

# TODO
# Not all ingredients have 4 effects.

#%% Imports

# Standard

# Dash
import dash
from dash import callback, Input, State
import dash_mantine_components as dmc

# Relative
from components.data_access import db, Ingredient


#%% Boilerplate

if __name__ != '__main__':
    dash.register_page(__name__)


#%% Layout

first_three = dmc.Group([
        dmc.TextInput(label="Value", id="textinput_value"),
        dmc.TextInput(label="Weight", id="textinput_weight"),
        dmc.TextInput(label="Ingredient", id="textinput_ingredient"),
        ],
    grow=True,
    wrap="nowrap")

properties = dmc.Group([
        dmc.TextInput(label="Property 1", id="textinput_property_1"),
        dmc.TextInput(label="Property 2", id="textinput_property_2"),
        dmc.TextInput(label="Property 3", id="textinput_property_3"),
        dmc.TextInput(label="Property 4", id="textinput_property_4"),
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
        value_property_1, 
        value_property_2, 
        value_property_3, 
        value_property_4,
        n_clicks
        ):
    """
    Adds ingredient and properties to database
    """

    effects = {
        value_property_1.replace(" ","_") : '1',
        value_property_2.replace(" ","_") : '1',
        value_property_3.replace(" ","_") : '1',
        value_property_4.replace(" ","_") : '1',
        }

    new_ingredient = Ingredient(
        Value=value_value,
        Weight=value_weight,
        Ingredient=value_ingredient,
        **effects,
        )
    
    db.session.add(new_ingredient)
    db.session.commit()

# -*- coding: utf-8 -*-
"""
Created on Wed May 21 21:41:23 2025

@author: camer
"""

# TODO
# Change sql access to stored procedure.
# Not all ingredients have 4 effects.
# Add column for source? e.g. base/bloodmoon/tamriel_rebuilt etc

#%% Imports
# Standard

# Dash
import dash
from dash import callback, Input, State
import dash_mantine_components as dmc

# Relative
from components.data_access import database_execute

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


button = dmc.Button("Add Ingredient", id="button_add_ingredient")

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
    sql_text = f"""
    INSERT INTO Ingredient (
    	`Value`, 
    	`Weight`, 
    	`Ingredient`, 
    	`{value_property_1}`, 
    	`{value_property_2}`, 
    	`{value_property_3}`, 
    	`{value_property_4}`
    	)
    VALUES (
    	"{value_value}", 
    	"{value_weight}", 
    	"{value_ingredient}", 
    	1, 
    	1, 
    	1, 
    	1
    	);
    """

    database_execute(sql_text)

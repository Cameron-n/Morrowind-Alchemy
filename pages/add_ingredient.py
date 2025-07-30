# -*- coding: utf-8 -*-
"""
Created on Wed May 21 21:41:23 2025

@author: Cameron-n

Page to add ingredients to the database. Password protected
"""

# TODO
# Error handling:
    # Duplicate ingredient name (overwrite?, remove if values empty?)
# Password protect on server
# Boxes to dropdown/limit input type
    # make properties not share the same properties
    # List of missing inputs if input is missing. Turn boxes red

#%% Imports

# Standard

# Dash
import dash
from dash import callback, Input, Output, State
import dash_mantine_components as dmc
from sqlalchemy.exc import IntegrityError, OperationalError

# Relative
from components.data_access import db, Ingredient, DF_INGREDIENTS, DF_EFFECTS

#%% Boilerplate

if __name__ != '__main__':
    dash.register_page(__name__)


#%% Layout

data_origin = DF_INGREDIENTS["Origin"].unique()

first_three = dmc.Group([
        dmc.NumberInput(label="Value", min=0, required=True, id="textinput_value"),
        dmc.NumberInput(label="Weight", min=0, required=True, id="textinput_weight"),
        dmc.TextInput(label="Ingredient", required=True, id="textinput_ingredient"),
        dmc.TagsInput(label="Origin", data=data_origin, maxTags=1, required=True, id="textinput_origin"),
        ],
    grow=True,
    wrap="nowrap")

data_effects = DF_EFFECTS["Spell Effects"]

properties = dmc.Group([
        dmc.Select(label="Property 1", data=data_effects, clearable=False, required=True, searchable=True, id="textinput_property_1"),
        dmc.Select(label="Property 2", data=data_effects, clearable=True, searchable=True, id="textinput_property_2"),
        dmc.Select(label="Property 3", data=data_effects, clearable=True, searchable=True, id="textinput_property_3"),
        dmc.Select(label="Property 4", data=data_effects, clearable=True, searchable=True, id="textinput_property_4"),
        ],
    grow=True,
    wrap="nowrap")


button = dmc.Button("Add Ingredient", c="myColors.9", id="button_add_ingredient")

success_fail_alert = dmc.Alert(hide=True, variant='outline',
                               withCloseButton=True, id="alert-success-fail")

layout = dmc.Stack([
    success_fail_alert,
    first_three,
    properties,
    button,
    ])


#%% Callbacks

@callback(
    Output("alert-success-fail", "children"),
    Output("alert-success-fail", "title"),
    Output("alert-success-fail", "color"),
    Output("alert-success-fail", "hide"),
    State("alert-success-fail", "hide"),
    State("textinput_value", "value"),
    State("textinput_weight", "value"),
    State("textinput_ingredient", "value"),
    State("textinput_origin", "value"),
    State("textinput_property_1", "value"),
    State("textinput_property_2", "value"),
    State("textinput_property_3", "value"),
    State("textinput_property_4", "value"),
    Input("button_add_ingredient","n_clicks"),
    prevent_initial_call=True
    )
def on_add_ingredient_button_clicked(
        hide,
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

    starred = [value_value, value_weight, value_ingredient,
               value_origin, value_property_1]
    if True in [i in [None, [], ""] for i in starred]:
        return f"Missing required inputs.", "Failed!", "red", False

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

    try:
        # db.session.add(new_ingredient)
        # db.session.commit()
        1+1
    except IntegrityError:
        return "Duplicate ingredient name.", "Failed!", "red", False
    except OperationalError:
       return "Database Error. Try again later.", "Failed!", "red", False

    return "Data successfully added!", "Success!", "green", False

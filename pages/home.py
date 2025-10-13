# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 14:24:33 2025

@author: Cameron-n
"""


#%% Imports

# Standard

# Dash
import dash
from dash import callback, Input, Output
import dash_mantine_components as dmc

# Relative
from components.data_access import DF_INGREDIENTS, DF_EFFECTS, DF_TOOLS


#%% Boilerplate

if __name__ != '__main__':
    dash.register_page(__name__, path="/")


#%% Layout

layout = dmc.Stack([
    dmc.Title("Morrowind Alchemy Calculator", order=3),
    dmc.Text([
        "Hello and welcome to this webapp! It is designed to explore Morrowind's ",
        "alchemy system. The game has hundreds of thousands of possible potions, ",
        "so exploring them all manually is not reasonable."
        ],
    ),
    dmc.Stack([
        dmc.Text("With this webapp, you can:"),
        dmc.Text("1. Potion Database - Search through all possible potion combinations by selecting the desired effects"),
        dmc.Text("2. Potion Maker - Emulate the alchemy process in-game, with the addition of more detailed stats on magnitude and duration"),
        dmc.Text("3. Ingredient Info - See each ingredients name, icon, location, effects, price, and weight"),
        ],
    ),
    dmc.Title("How Alchemy Works", order=3),
    dmc.Stack([
        dmc.Text([
            "In Morrowind, there are magical effects. Ingredients have a list ",
            "up to four effects associated with them. Potions are mixtures of ",
            "up to four ingredients. If two of more ingredients in a potion share ",
            "the same effect, the potion has that effect. Note, eating ingredients ",
            "directly is possible but you only get the first effect in the list ",
            "and the magnitude (strength) and duration are very low. Also ",
            "alchemy requires a 'Mortar and Pestle', and can additionally have ",
            "an 'alembic', 'calcinator', and 'retort' added. Lastly, a players ",
            "skills in Alchemy, Intelligence, and Luck affect the final result."
            ]),
        ],
    ),
])


#%% Functions


#%% Callbacks




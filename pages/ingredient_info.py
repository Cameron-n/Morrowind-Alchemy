# -*- coding: utf-8 -*-
"""
Created on Thu May 22 20:17:00 2025

@author: camer
"""

# ingredients name icon location effects price weight

#%% Imports

# Standard
from collections import Counter
from copy import deepcopy

# Dash
import dash
from dash import callback, Input, Output
import dash_mantine_components as dmc

# Relative
from components.data_access import DF_INGREDIENTS, DF_EFFECTS, DF_TOOLS


#%% Boilerplate

if __name__ != '__main__':
    dash.register_page(__name__)


#%% Layout

layout = dmc.Stack([
    dmc.Text(">>> Under Construction <<<"),
    dmc.Select("Placeholder", w=250),
    dmc.Image(src="Placeholder", w=100),
    dmc.Group([
        dmc.Group([dmc.Image(src="placeholder", w=10), "price"]),
        dmc.Group([dmc.Image(src="placeholder", w=10), "weight"]),
        ]),
    dmc.Stack([
        dmc.Title("Effects", order=4),
        dmc.Text("effect 1"),
        dmc.Text("effect 2"),
        dmc.Text("effect 3"),
        dmc.Text("effect 4"),
        ]),
    dmc.Stack([
        dmc.Title("Locations", order=4),
        dmc.Text("list"),
        dmc.Text("of"),
        dmc.Text("locations"),
        ]),
    ])


#%% Functions


#%% Callbacks




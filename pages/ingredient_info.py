# -*- coding: utf-8 -*-
"""
Created on Thu May 22 20:17:00 2025

@author: camer
"""


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

layout = dmc.Text("Ingredient/Location Page")


#%% Functions


#%% Callbacks




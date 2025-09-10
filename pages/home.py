# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 14:24:33 2025

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
    dash.register_page(__name__, path="/")


#%% Layout

layout = dmc.Text("HOME Page")


#%% Functions


#%% Callbacks




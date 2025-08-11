# -*- coding: utf-8 -*-
"""
Created on Sun May 25 20:40:32 2025

@author: Cameron-n

Contains the layout for the navbar used in app.py
"""

#%% Imports

# Dash
import dash_mantine_components as dmc


#%% Layout
def navbar():
    """
    Navbar component for the app shell.

    Returns
    -------
    layout : dmc.Stack
        The navbar components. A stack of buttons with
        hyperlinks to pages.

    """
    layout = dmc.Stack([
        dmc.Anchor(
            dmc.Button("Potion Database", fullWidth=True),
            href="/", underline="never", c="myColors.9"
        ),
        dmc.Anchor(
            dmc.Button("Potion Maker", fullWidth=True),
            href="/potion-maker", underline="never", c="myColors.9"
        ),
    ])

    return layout

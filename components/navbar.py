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
def Navbar():
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
            dmc.Button("Home", fullWidth=True, id="nav-btn-home",
                       className="media-navbar-button"),
            href="/", underline="never", c="myColors.9",
            className="media-navbar-anchor"
        ),
        dmc.Anchor(
            dmc.Button("Potion Database", fullWidth=True, id="nav-btn-data",
                       className="media-navbar-button"),
            href="/potion-database", underline="never", c="myColors.9",
            className="media-navbar-anchor"
        ),
        dmc.Anchor(
            dmc.Button("Potion Maker", fullWidth=True, id="nav-btn-maker",
                       className="media-navbar-button"),
            href="/potion-maker", underline="never", c="myColors.9",
            className="media-navbar-anchor"
        ),
        dmc.Anchor(
            dmc.Button("Ingredient Info", fullWidth=True, id="nav-btn-info",
                       className="media-navbar-button"),
            href="/ingredient-info", underline="never", c="myColors.9",
            className="media-navbar-anchor"
        ),
    ],
        style={"height": "100%"},
    )

    return layout

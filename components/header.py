# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 15:09:33 2025

@author: camer
"""

#%% Imports

# Dash
import dash_mantine_components as dmc


#%% Layout
def Header():
    """
    Header component for the app shell.

    Returns
    -------
    layout : dmc.Group
        The header components. A burger for mobile navigation,
        and a clickable title that links to the home page.

    """
    layout = dmc.Group([
        dmc.Burger(id="burger-mobile", size="sm",
                   hiddenFrom="xs", opened=False),
        dmc.Burger(id="burger-tablet", size="sm", visibleFrom="xs",
                   hiddenFrom="md", opened=False),
        dmc.Anchor(
            dmc.Title("Morrowind Alchemy", order=5, c="myColors.9"),
            href="/", underline="never", c="myColors.9"
        ),
    ])

    return layout

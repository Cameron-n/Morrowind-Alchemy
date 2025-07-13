# -*- coding: utf-8 -*-
"""
Created on Wed May 21 20:51:51 2025

@author: Cameron-n

Entrypoint for the dash app. Sets up some boilerplate code and
creates the AppShell: the header, navbar, and main content area.
"""

#%% Imports

# Standard

# Dash
import dash
from dash import Dash
import dash_mantine_components as dmc

# Relative
from components.navbar import navbar
from components.config import theme


#%% Boilerplate

# Needed for dmc to work
dash._dash_renderer._set_react_version("18.2.0")

app = Dash(__name__, use_pages=True)


#%% Layout

layout = dmc.AppShell([
    dmc.AppShellHeader(
        dmc.Text("Morrowind Alchemy", c="myColors.9"),
        bg="myColors.2"
        ),
    dmc.AppShellNavbar(
        navbar(),
        p="md",
        bg="myColors.1"
        ),
    dmc.AppShellMain(dash.page_container)
    ],
    header={"height":60},
    navbar={
        "width":200,
        "breakpoint":"sm",
        "collapsed": {"mobile": True},
        },
    padding="md",
    bg="myColors.0"
    )

app.layout = dmc.MantineProvider(
    layout,
    theme=theme
    )


#%% Boilerplate
if __name__ == '__main__':
    app.run(debug=True)

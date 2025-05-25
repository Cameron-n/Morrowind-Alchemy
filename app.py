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

#%% Boilerplate
dash._dash_renderer._set_react_version("18.2.0")

app = Dash(__name__, use_pages=True)

#%% Layout

layout = dmc.AppShell([
    dmc.AppShellHeader(
        "Hello"
        ),
    dmc.AppShellNavbar(
        "Hi",
        p="md"
        ),
    dmc.AppShellMain(dash.page_container)
    ],
    header={"height":60},
    footer={"height":60},
    navbar={
        "width":100,
        "breakpoint":"sm",
        "collapsed": {"mobile": True},
        },
    padding="md",
    )

app.layout = dmc.MantineProvider(layout)

#%% Boilerplate
if __name__ == '__main__':
    app.run(debug=True)

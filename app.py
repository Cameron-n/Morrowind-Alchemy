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

#%% Boilerplate
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
    theme={
        "colors" : {
            "myColors" : [
                "#fff8e7",
                "#fbefd5",
                "#f5dda7",
                "#f0c976",
                "#ecb94e",
                "#eaaf34",
                "#e9aa26",
                "#cf941a",
                "#b88312",
                "#9f7102",
                ],
            },
        "primaryColor" : "myColors",
        "primaryShade" : 3,
        },
    )


#%% Boilerplate
if __name__ == '__main__':
    app.run(debug=True)

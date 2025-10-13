# -*- coding: utf-8 -*-
"""
Created on Wed May 21 20:51:51 2025

@author: Cameron-n

Entrypoint for the dash app. Sets up some boilerplate code and
creates the AppShell: the header, navbar, and main content area.
"""

# Rewrite code with lists of components instead of many variables

#%% Imports

# Standard

# Dash
import dash
from dash import Dash, callback, Input, Output, State, ctx
import dash_mantine_components as dmc

# Relative
from components.navbar import Navbar
from components.header import Header
from components.config import theme
from components.data_access import server


#%% Boilerplate

app = Dash(__name__, server=server, use_pages=True)


#%% Layout

layout = dmc.AppShell([
    dmc.AppShellHeader(
        Header(),
        p="md",
        bg="myColors.2"
    ),
    dmc.AppShellNavbar(
        Navbar(),
        p="md",
        bg="myColors.1"
    ),
    dmc.AppShellMain(dash.page_container)
],
    header={"height": 60},
    navbar={
        "width": 200,
        "breakpoint": "xs",
        "collapsed": {"mobile": True, "desktop": False},
},
    p="md",
    bg="myColors.0",
    id="appshell"
)

app.layout = dmc.MantineProvider(layout, theme=theme)


#%% Callbacks

@callback(
    Output("appshell", "navbar"),
    Input("burger-mobile", "opened"),
    Input("burger-tablet", "opened"),
    State("appshell", "navbar"),
    prevent_initial_call=True
)
def toggle_navbar(opened_mobile, opened_tablet, navbar):
    """Toggle navbar opened or closed on mobile using burger"""
    if ctx.triggered_id == "burger-mobile":
        navbar["collapsed"]["mobile"] = not opened_mobile
    elif ctx.triggered_id == "burger-tablet":
        navbar["collapsed"]["desktop"] = not opened_tablet
    return navbar


@callback(
    Output("appshell", "navbar", allow_duplicate=True),
    Output("burger-mobile", "opened"),
    Input("nav-btn-home", "n_clicks"),
    Input("nav-btn-data", "n_clicks"),
    Input("nav-btn-maker", "n_clicks"),
    Input("nav-btn-info", "n_clicks"),
    State("appshell", "navbar"),
    prevent_initial_call=True
)
def close_navbar_on_click(btn_one, btn_two, btn_three, btn_four, navbar):
    """Close navbar after selection is made on mobile"""
    navbar["collapsed"] = {"mobile": True, "desktop": False}
    return navbar, False


#%% Boilerplate

if __name__ == '__main__':
    app.run(debug=True)

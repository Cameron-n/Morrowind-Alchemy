# -*- coding: utf-8 -*-
"""
Created on Wed May 21 20:51:51 2025

@author: Cameron-n
"""

import dash
from dash import Dash
import dash_mantine_components as dmc

dash._dash_renderer._set_react_version("18.2.0")

app = Dash(__name__, use_pages=True)

app.layout = dmc.MantineProvider(dmc.Container(dash.page_container))

if __name__ == '__main__':
    app.run(debug=True)
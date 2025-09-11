# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 15:47:51 2025

@author: Cameron-n

Contains the styling for the app
"""

myColors = [
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
]

theme = {
    "colors": {
        "myColors": myColors,
    },
    "primaryColor": "myColors",
    "primaryShade": 3,
    "breakpoints": {
        "xs": '30em',  # Default values for reference
        "sm": '48em',
        "md": '64em',
        "lg": '74em',
        "xl": '90em',
    },
    "components": {
        "Select": {
            "styles": {
                "dropdown": {"background": myColors[4]},
            }
        },
        "TagsInput": {
            "styles": {
                "dropdown": {"background": myColors[4]},
            }
        },
        "MultiSelect": {
            "styles": {
                "dropdown": {"background": myColors[4]},
            }
        },
    },
}

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 14:24:33 2025

@author: Cameron-n
"""

#%% Imports

# Standard
import os

# Dash
import dash
import dash_mantine_components as dmc


#%% Boilerplate

if __name__ != '__main__':
    dash.register_page(__name__, path="/")


#%% Layout

relative_loc = "../assets/home-txt.txt"
home_text_loc = os.path.join(os.path.dirname(__file__), relative_loc)

with open(home_text_loc) as f:
    home_text = [line for line in f]

layout = dmc.Stack([
    dmc.Title("Morrowind Alchemy Calculator", order=3),
    dmc.Text(home_text[0]),
    dmc.AspectRatio(
        dmc.Image(
            src="assets/home-1.jpg",
            radius="md",
            ),
        ratio=16 / 9,
        style={"max-width": "500px"}
        ),
    dmc.Stack([
        dmc.Title("With this webapp, you can:", order=3),
        dmc.Text([
            dmc.Anchor(dmc.Button("Potion Database"), href="/potion-database"),
            " - Search through all possible potion combinations"
            ]),
        dmc.Text([
            dmc.Anchor(dmc.Button("Potion Maker"), href="/potion-maker"),
            " - Emulate the alchemy process in-game"
            ]),
        dmc.Text([
            dmc.Anchor(dmc.Button("Ingredient Info"), href="/ingredient-info"),
            " - Contains names, icons, locations, effects, prices, and weights"
            ]),
        ],
    ),
    dmc.Title("How Alchemy Works", order=3),
    dmc.Stack([
        dmc.Text(home_text[1]),
        ],
    ),
    dmc.Title("Credits", order=3),
    dmc.Stack([
        dmc.Text([
            "- The game Morrowind belongs to Bethesda Studios\n",
            "- The original data is available ",
            dmc.Anchor("here", href="https://docs.google.com/spreadsheets/d/1JQ391ET9lkKRoAdzQnkyIly7XCg2fNmtJqhpqmJitaM/edit?gid=1565250262#gid=1565250262"),
            "\n- This application was made by ",
            dmc.Anchor("Cameron-n", href="https://github.com/Cameron-n"),
            dmc.Anchor(
                "\nhttps://github.com/Cameron-n/Morrowind-Alchemy",
                href="https://github.com/Cameron-n/Morrowind-Alchemy"
                )
            ], style={"white-space": "pre-wrap"}),
        ]),
])

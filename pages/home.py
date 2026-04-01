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
    home_text = [line.encode('utf-8').decode('unicode_escape') for line in f]

layout = dmc.Stack([
    dmc.Title("Morrowind Alchemy Calculator", order=3),
    dmc.Title("Purpose", order=4),
    dmc.Text(home_text[0], style={"white-space": "pre-wrap"}),
    dmc.Container(
        dmc.AspectRatio(
            dmc.Image(
                src="assets/home-1.png",
                radius="md",
                ),
            ratio=16 / 9,
            style={"max-width": "500px"}
            ),
    ),
    dmc.Title("How Alchemy Works", order=4),
    dmc.Text(home_text[1], style={"white-space": "pre-wrap"}),
    dmc.Title("Potion Database", order=4),
    dmc.Text(home_text[2], style={"white-space": "pre-wrap"}),
    dmc.Title("Potion Maker", order=4),
    dmc.Text(home_text[3], style={"white-space": "pre-wrap"}),
    dmc.Title("Ingredient Info", order=4),
    dmc.Text(home_text[4], style={"white-space": "pre-wrap"}),
    dmc.Title("Credits", order=4),
    dmc.Text([
        "- The game Morrowind belongs to Bethesda Studios\n",
        "- The ",
        dmc.Anchor("MWSE", href="https://mwse.github.io/MWSE/guides/introduction-to-lua/"),
        " Lua functionality used for data collection\n",
        "- ",
        dmc.Anchor("This", href="https://www.nexusmods.com/morrowind/mods/53963"),
        " mod by Kezyma for creating map tiles from the game\n",
        "- Some base game data used for prototyping is available ",
        dmc.Anchor("here", href="https://docs.google.com/spreadsheets/d/1JQ391ET9lkKRoAdzQnkyIly7XCg2fNmtJqhpqmJitaM/edit?gid=1565250262#gid=1565250262"),
        "\n- A big thank you to the ",
        dmc.Anchor("UESP", href="https://en.uesp.net/wiki/Morrowind:Morrowind"),
        " for compiling lots of useful information"
        "\n- This application was made by ",
        dmc.Anchor("Cameron-n", href="https://github.com/Cameron-n"),
        dmc.Anchor(
            "\nhttps://github.com/Cameron-n/Morrowind-Alchemy",
            href="https://github.com/Cameron-n/Morrowind-Alchemy"
            )
        ], style={"white-space": "pre-wrap"}),
], style={"margin": "auto", "max-width": "750px"})

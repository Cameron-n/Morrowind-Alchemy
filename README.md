# Morrowind-Alchemy

## Overview

A [Dash](https://dash.plotly.com/) app to display information about potions that can be created using alchemy in the 
game Morrowind.

Due to the enormous number of ingredient combinations available, it is not practical to investigate all of them in-game. 
This app allows the optimal potions to be found based on what effects you want, limiting the number of negative effect 
and finding potions with additional positive effects.

Features:
- Potion Maker: Mimics the in-game alchemy menu
- Potion Database: Search combinations and calculate the 'optimal' potions
- Tamriel Rebuilt: Ingredients included and can be filtered to exclude

[//]: # (Add Ingredient: Add new ingredients to the database)

## How to use?

### Location

The app is hosted on [PythonAnywhere](https://eu.pythonanywhere.com/).

To view the app, navigate to:
- <https://cameronn.eu.pythonanywhere.com/>

### Source code

If you want to look at the code, here's how it works.

1. The app starts from the `app.py` file. This contains the main layout, including the `dash.page_container`, and some 
setup. 
2. It is then divided into `page`'s. Each file contains its layout and logic.
3. The `database` folder contains sql for database construction, and the file containing the `Flask-SQLAlchemy` logic.
4. The `assets` folder contains non-code assets such as pictures. It also contains `.css` files which Dash loads 
automatically.
5. The `components` folder contains additional layouts/logic. It contains the config file for the theming, and the
navbar's layout.

#### Guidelines

Some tips and tricks to make working with the libraries easier. This is as much for my benefits as for any other
readers!

- Component IDs are in the form `<file_name>-<component_name>-<custom>`. This is because Dash does not allow duplicate
IDs and it's very easy to lose track of the names.
- Test

## External Docs

This project is built on:

- [Dash](https://dash.plotly.com/) - A webapp framework
    - Mainly using the [Mantine](https://www.dash-mantine-components.com/) react library
    - See [Plotly](https://plotly.com/python/) for graphs
- [Flask](https://flask.palletsprojects.com/en/stable/) - For the underlying server
- [SQLAlchemy](https://www.sqlalchemy.org/) - A database ORM
    - See also [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/quickstart/)

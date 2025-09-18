# Morrowind-Alchemy

**Note: See >[this](https://cameron-n.github.io/Alchemy/Python-Webapp/)< post for a more detailed look at this project.**

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

### Self-setup

**Note: This assumes some familiarity with Python and SQL.**

If you want to host a copy of the app yourself, here's how to do so:

Create a Python environment and install the modules in the `requirements.txt`.

```pip install -r requirements.txt```

Clone the repository:

```git clone https://github.com/Cameron-n/Morrowind-Alchemy.git```

Run the app by running `app.py` and navitgating to `localhost:8050` on a browser. The app should run but will not display any data as we have not loaded any in yet.

Create a database and load the data. Note, I am using MySQL so e.g. the backticks may need to be replaced:
Run `create_tables.sql` to create the tables.
Run `effect_data.sql`, `ingredient_data.sql`, and `tool.sql` to populate the tables.

Create a .env file in the root folder with the following information:
```
DATABASE_URI="mysql+mysqldb://<user>:<password>@<host>:<port>/<database name>"
ADD_INGREDIENT_TOKEN="<A secure token>"
```
The DATABASE_URI contains the connection string to your database. If you don't
want to use MySQL, here is where you need to change that.

The ADD_INGREDIENT_TOKEN is used to stop anyone adding ingredients to the database
using the `add-ingredient` page. You can set it to any valid string you like and
will need it for that page. You can navigate to this page by explicitly stating
the URL, e.g. `http://localhost:8050/add-ingredient`.

In case you want to add new spell effects, these must be added in three places:

1. create_tables.sql - In the `Ingredient` table in the format ``` `effect name` int DEFAULT NULL ```
2. effect_data.sql - In the format ``` ... VALUES ('effect name', 'base cost', 1 (if positive) or 0 (if negative) ) ```
3. data_access.py - In the format ``` effect_name = mapped_column("name without underscores", Integer) ```

### Source code

If you want to look at the code, here's how it works.

1. The app starts from the `app.py` file. This contains the main layout, including the `dash.page_container`, and some 
setup. 
2. It is then divided into `page`'s. Each file contains its layout and logic.
3. The `database` folder contains sql for database construction.
4. The `assets` folder contains non-code assets such as pictures. It also contains `.css` files which Dash loads 
automatically.
5. The `components` folder contains additional layouts/logic. It contains the config file for the theming, the
navbar's layout, and the `Flask-SQLAlchemy` logic.

#### Guidelines

Some tips and tricks to make working with the libraries easier. This is as much for my benefits as for any other
readers!

- Component IDs are in the form `<file_name>-<component_name>-<custom>`. This is because Dash does not allow duplicate
IDs and it's very easy to lose track of the names.
- Test

## External Docs and Credits

This project is built on:

- [Dash](https://dash.plotly.com/) - A webapp framework
    - Mainly using the [Mantine](https://www.dash-mantine-components.com/) react library
    - See [Plotly](https://plotly.com/python/) for graphs
- [Flask](https://flask.palletsprojects.com/en/stable/) - For the underlying server
- [SQLAlchemy](https://www.sqlalchemy.org/) - A database ORM
    - See also [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/quickstart/)

The original data is taken from [this spreadsheet](https://docs.google.com/spreadsheets/d/1JQ391ET9lkKRoAdzQnkyIly7XCg2fNmtJqhpqmJitaM/edit?gid=1565250262#gid=1565250262).
- Data cleaning steps:
    - Add columns
    - The original source has these errors
        - Heartwood is labelled as "Resist Magicka" but should be "Restore Magicka"
        - Deadra's Heart is labelled as "Resist Magicka" but should be "Restore Magicka"
        - Wolf Pelt is labelled as "Burden" "Poison" "Restore Magicka" "Reflect" but is "Drain Fatigue" "Fortify Speed" "Resist Common Disease" "Night Eye"

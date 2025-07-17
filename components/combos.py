import pandas as pd
from components.data_access import DF_INGREDIENTS

def potion_combinations(ingredients=DF_INGREDIENTS, restrictions=None):

    # Remove non-effect columns. Ingredient names need to be stored so they can be added back
    # after row multiplication.
    drop_columns = ["Value", "Weight", "Ingredient", "Ingredient 2", "Ingredient 3", "Ingredient 4", "Origin"]

    ingredients_columns = ingredients.columns
    ingredient_names = ingredients[ingredients.columns.intersection(["Ingredient", "Ingredient 2", "Ingredient 3", "Ingredient 4"])]

    # Unsure on how this will work. Part of optimising by removing unneeded ingredients/columns
    # if not restrictions:
    #     restrictions = [i for i in DF_INGREDIENTS.drop(drop_columns, axis=1, errors="ignore").columns]
    #
    # ingredients=ingredients[["Ingredient"] + restrictions]
    # ingredients.dropna(how="all", axis=1)

    potions = pd.DataFrame()

    for index, row in DF_INGREDIENTS.iterrows():

        # Removes duplicates and self-combinations
        # e.g. for combos of A and B it removes BA and AA. Only AB is valid.
        temp_ingredients = ingredients.copy()
        if "Ingredient 4" in temp_ingredients.columns:
            temp_ingredients = temp_ingredients[temp_ingredients["Ingredient 4"] < row["Ingredient"]]
        elif "Ingredient 3" in temp_ingredients.columns:
            temp_ingredients = temp_ingredients[temp_ingredients["Ingredient 3"] < row["Ingredient"]]
        elif "Ingredient 2" in temp_ingredients.columns:
            temp_ingredients = temp_ingredients[temp_ingredients["Ingredient 2"] < row["Ingredient"]]
        elif "Ingredient" in temp_ingredients.columns:
            temp_ingredients = temp_ingredients[temp_ingredients["Ingredient"] < row["Ingredient"]]

        # Creates all possible potion combos AB, AC, DFH, etc.
        # If a row has all NaNs, the ingredients share no effects.
        combos = temp_ingredients.drop(drop_columns, axis=1, errors="ignore")*row.drop(drop_columns, errors="ignore")
        combos = combos.dropna(how="all")
        combos = combos.join(ingredient_names)

        if "Ingredient 2" not in ingredients_columns:
            combos["Ingredient 2"] = row["Ingredient"]
        elif "Ingredient 3" not in ingredients_columns:
            combos["Ingredient 3"] = row["Ingredient"]
        elif "Ingredient 4" not in ingredients_columns: # Optimisation: change to "else"
            combos["Ingredient 4"] = row["Ingredient"]

        potions = pd.concat([potions, combos])

    potions = potions.reset_index().drop("index", axis=1)

    return potions

potions_1 = DF_INGREDIENTS
potions_2 = potion_combinations(potions_1)
potions_3 = potion_combinations(potions_2)
#potions_4 = potion_combinations(potions_3)

"""
ABCD

ABC
ABD
ACD
BCD



"""


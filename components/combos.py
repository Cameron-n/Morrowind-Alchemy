# -*- coding: utf-8 -*-
"""
Created on Sun Jul 20 18:10:49 2025

@author: Cameron-n

Contains the logic to calculate ingredient combinations
"""

# The original source has these errors:
    # Heartwood is labelled as "Resist Magicka" but should be "Restore Magicka"
    # Deadra's Heart is labelled as "Resist Magicka" but should be "Restore Magicka"
    # Wolf Pelt is labelled as "Burden" "Poison" "Restore Magicka" "Reflect" but is "Drain Fatigue" "Fortify Speed" "Resist Common Disease" "Night Eye"

#%% Imports

# Standard
import pandas as pd

# Relative
from components.data_access import DF_INGREDIENTS


#%% Functions

#DF_INGREDIENTS = DF_INGREDIENTS[0:10]
DF_INGREDIENTS = DF_INGREDIENTS.fillna(0)

# Notes on step-by-step process to calculate potion combos
    # 1. User selects effects
        # Callback
    # 2. Ingredients with those effects identified
        # e.g. a[a["Poison"]==1][a["Burden"]==1]
        # Need all ingredients with AT LEAST one effect from selection
    # 3. Calculate all 2-potions
        # More than 4 effects => skip
        # Calculate all pairwise combos (use potion_combinations)
    # 4. Calculate all 3-potions
        # More than 6 effects => skip
        # Calculate all minimal triplets by extending pairwise.
    # 5. Calculate all 4-potions
        # Calculate all minimal quads by extending triplets
        # Calculate disjoint pairwise pairs by joining pairwise
    # 6. Order potions by number of positive effects DESC, number of negative effects ASC
    # 7. Extend button. Adds more ingredient to minimal set based on +ve effects

def potion_combinations(ingredients=DF_INGREDIENTS, restrictions=None):

    # Remove non-effect columns. Ingredient names need to be stored so they can be added back
    # after row multiplication.
    drop_columns = ["Value", "Weight", "Ingredient", "Ingredient 2", "Ingredient 3", "Ingredient 4", "Origin", "First Effect"]

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
        #TODO Bug. Currently, does not remove ingredients that add no new effects to existing potions
        temp_ingredients = temp_ingredients.drop(drop_columns, axis=1, errors="ignore")

        number_of_twos_before = temp_ingredients[temp_ingredients==2].sum(axis=1)

        combos = temp_ingredients + row.drop(drop_columns, errors="ignore")

        number_of_twos_after = combos[combos==2].sum(axis=1)

        combos["Number of Two's"] = number_of_twos_after - number_of_twos_before
        combos = combos[combos["Number of Two's"] > 0]
        combos = combos.drop("Number of Two's", axis=1)

        combos = combos.loc[(combos!=0).any(axis=1)]
        combos = combos.join(ingredient_names)

        if "Ingredient 2" not in ingredients_columns:
            combos["Ingredient 2"] = row["Ingredient"]
        elif "Ingredient 3" not in ingredients_columns:
            combos["Ingredient 3"] = row["Ingredient"]
        elif "Ingredient 4" not in ingredients_columns: # Optimisation: change to "else"
            combos["Ingredient 4"] = row["Ingredient"]

        potions = pd.concat([potions, combos])

    #potions = potions.replace(1, 0)
    potions = potions.loc[(potions.drop(drop_columns, axis=1, errors="ignore")!=0).any(axis=1)]
    potions = potions.reset_index().drop("index", axis=1)

    return potions

potions_1 = DF_INGREDIENTS
potions_2 = potion_combinations(potions_1)
#potions_3 = potion_combinations(potions_2)
#potions_4 = potion_combinations(potions_3)

potions_2_ingredients = potions_2[["Ingredient", "Ingredient 2"]]
potions_2 = potions_2.drop(["Ingredient", "Ingredient 2"], axis=1)
potions_2 = potions_2.where(potions_2 != 2, potions_2.columns.to_series(), axis=1)
potions_2 = potions_2.to_numpy()

for index, i in enumerate(potions_2):
    a=i[i!=0]
    print(a[a!=1][0], [i for i in potions_2_ingredients.iloc[index]])

# Function for 2 disjoint pairs
# Combines potions_2
# Only valid if the pairs share NO effects with each other, including unmatched
# ingredient effects.
# Extend for arbitary disjoint i.e. 5 = 3+2, 6=4+2=3+3?

# -*- coding: utf-8 -*-
"""
Created on Sun Jul 20 18:10:49 2025

@author: Cameron-n

Contains the logic to calculate ingredient combinations (i.e. potions)
"""

# Function for 2 disjoint pairs
# Combines potions_2
# Only valid if the pairs share NO effects with each other, including unmatched
# ingredient effects.
# Extend for arbitary disjoint i.e. 5 = 3+2, 6=4+2=3+3?

#%% Imports

# Standard
import numpy as np
import pandas as pd

# Relative
from components.data_access import DF_INGREDIENTS


#%% Functions


def potion_combinations(ingredients, restrictions=[]):
    """
    Create all minimal valid potion combinations that are NOT disjoint.
    
    Explanation
    ------------
        - A *potion* is a combination of up to four ingredients.
        - A *valid* potion has each ingredient share at least one of it's effects
          with at least one of the other ingredients.
        - A *minimal* potion only has the ingredients necessary to produce
          the effects in `restrictions`.
        - A *disjoint* potion is made from two minimal potions' ingredients
          that don't share any effects between them. 
          [What about AB,CD,AB -> AB|CD]?

    Parameters
    ----------
    ingredients : dataframe
        The ingredients. Taken from the database.
    restrictions : list, optional
        What effects to include in the resulting potions. The default is [].

    Returns
    -------
    potions : dataframe
        The potions.

    """
    drop_columns = ["Value", "Weight", "Ingredient", "Ingredient 2",
                    "Ingredient 3", "Ingredient 4", "Origin", "First Effect"]
    potions = pd.DataFrame()
    
    # Store the ingredient names columns
    ingredient_columns = ["Ingredient", "Ingredient 2", 
                          "Ingredient 3", "Ingredient 4"]
    ingredient_columns = ingredients.columns.intersection(ingredient_columns)
    ingredient_names = ingredients[ingredient_columns]

    # Restrict ingredients based on `restrictions`
    ingredients_restrictions = pd.Series([False for _ in range(len(ingredients))])
    df_restrictions = pd.Series([False for _ in range(len(DF_INGREDIENTS))])
    for i in restrictions: # Brackets needed due to | coming before != or ==
        ingredients_restrictions = ingredients_restrictions | (ingredients[i] != 0)
        df_restrictions = df_restrictions | (DF_INGREDIENTS[i] != 0)
    ingredients = ingredients[ingredients_restrictions]

    # Calculate potions ingredient-wise
    for index, row in DF_INGREDIENTS[df_restrictions].iterrows():

        # Remove Self-combinations
        temp_ingredients = ingredients.copy() # ??? Unneeded?
        if "Ingredient 3" in temp_ingredients.columns:
            temp_ingredients = temp_ingredients[(temp_ingredients["Ingredient 3"] != row["Ingredient"]) & (temp_ingredients["Ingredient 2"] != row["Ingredient"]) & (temp_ingredients["Ingredient"] != row["Ingredient"])]
        elif "Ingredient 2" in temp_ingredients.columns:
            temp_ingredients = temp_ingredients[(temp_ingredients["Ingredient 2"] != row["Ingredient"]) & (temp_ingredients["Ingredient"] != row["Ingredient"])]
        elif "Ingredient" in temp_ingredients.columns: # else
            temp_ingredients = temp_ingredients[temp_ingredients["Ingredient"] != row["Ingredient"]]

        temp_ingredients = temp_ingredients.drop(drop_columns, axis=1, errors="ignore")
        row_effects = row.drop(drop_columns, errors="ignore")

        # Track which ingredients add *new* effects
        number_of_twos_before = temp_ingredients[temp_ingredients==2].sum(axis=1)

        # Combine ingredients
        combos = temp_ingredients + row_effects

        number_of_twos_after = combos[combos==2].sum(axis=1)

        # New effects are those that increase a '1' to a '2'
        combos["Number of Two's"] = number_of_twos_after - number_of_twos_before
        combos = combos[combos["Number of Two's"] > 0]
        combos = combos.drop("Number of Two's", axis=1)

        combos = combos.loc[(combos!=0).any(axis=1)] # ???
        
        # Add back in ingredient names
        combos = combos.join(ingredient_names)

        if "Ingredient 2" not in ingredients.columns:
            combos["Ingredient 2"] = row["Ingredient"]
        elif "Ingredient 3" not in ingredients.columns:
            combos["Ingredient 3"] = row["Ingredient"]
        elif "Ingredient 4" not in ingredients.columns: # else
            combos["Ingredient 4"] = row["Ingredient"]

        potions = pd.concat([potions, combos])

    # Remove duplicates
    potion_columns = ["Ingredient", "Ingredient 2", 
                          "Ingredient 3", "Ingredient 4"]
    potion_columns = potions.columns.intersection(potion_columns)
    duplicates = np.sort(potions[potion_columns].to_numpy())
    potions[potion_columns] = duplicates
    potions = potions.drop_duplicates(potion_columns)

    #potions = potions.loc[(potions.drop(drop_columns, axis=1, errors="ignore")!=0).any(axis=1)] # ???
    potions = potions.reset_index().drop("index", axis=1)

    return potions


def potion_quads():
    pass

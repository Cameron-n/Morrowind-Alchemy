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

# Consider calculator for optimal potions from available ingredients?

#%% Imports

# Standard
from itertools import combinations
import pandas as pd

# Relative
from components.data_access import DF_INGREDIENTS


#%% Functions

DF_INGREDIENTS=DF_INGREDIENTS.fillna(0)

# https://stackoverflow.com/questions/31865088/using-python-and-pandas-to-create-combinations-instead-of-permutations
def combos(df, n):
    columns = []
    for i in range(n):
        columns += [f"Ingredient {i+1}"]

    return pd.DataFrame(list(combinations(df.Ingredient, n)), columns=columns)

def joins(potions, ingredients, n):
    cols=ingredients.columns.drop("Ingredient")
    for i in range(n):
        potions = potions.merge(ingredients, 
                                left_on=f"Ingredient {i+1}", 
                                right_on="Ingredient",
                                suffixes=(" x", " y"),
                                )
        # combine cols together
        if i != 0:
            for col in cols:
                potions[col] = potions[col+" x"] + potions[col+" y"]
                potions = potions.drop([col+" x",col+" y"], axis=1)
        potions = potions.drop("Ingredient", axis=1)
    return potions


def potion_combinations(
        ingredients,
        n,
        restrictions=[],
        ):
    """
    Create all minimal valid potion combinations.
    
    Explanation
    ------------
        - A *potion* is a combination of up to four ingredients.
        - A *valid* potion has each ingredient share at least one of it's effects
          with at least one of the other ingredients.
        - A *minimal* potion only has the ingredients necessary to produce
          the effects in `restrictions`.

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
    drop_columns = ["ID", "Icon", "Value", "Weight", "Origin", "First Effect"]
    ingredients = ingredients.drop(drop_columns, axis=1, errors="ignore")

    rest = ingredients[restrictions[0]]!=0
    if len(restrictions) > 1:
        for i in restrictions[1:]:
            rest = rest | (ingredients[i]!=0)

    ingredients = ingredients[rest]

    if ingredients.empty:
        return pd.DataFrame()

    # https://stackoverflow.com/questions/21164910/how-do-i-delete-a-column-that-contains-only-zeros-in-pandas
    ingredients = ingredients.loc[:, (ingredients != 0).any(axis=0)] # Remove all zero cols

    potions = combos(ingredients, n)
    potions = joins(potions, ingredients, n)

    potions = potions.reset_index().drop("index", axis=1)

    if potions.empty:
        potions = pd.DataFrame()

    return potions

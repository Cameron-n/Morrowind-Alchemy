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
import numpy as np
import pandas as pd

# Relative
from components.data_access import DF_INGREDIENTS


#%% Functions

DF_INGREDIENTS=DF_INGREDIENTS.fillna(0)


def potion_combinations(potions, origin_limited_ings, restrictions=[], pairs=False):
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
    # If potion pair or triplet returns no potions, we know further
    # combinations (triplets/quadruplets) will also be empty
    if potions.empty:
        return pd.DataFrame()
    
    if pairs: # Temporary measure
        return pd.DataFrame()
    
    if pairs:
        potions = potions.rename(columns={
            "Ingredient 1": "Ingredient 3",
            "Ingredient 2": "Ingredient 4"
            })

    drop_columns = ["ID", "Icon", "Value", "Weight", "Origin", "First Effect"]
    potions = potions.drop(drop_columns, axis=1, errors="ignore")
    origin_limited_ings = origin_limited_ings.drop(drop_columns, axis=1, errors="ignore")

    rest = potions[restrictions[0]]!=0
    if len(restrictions) > 1:
        for i in restrictions[1:]:
            rest = rest | (potions[i]!=0)

    potions = potions[rest]

    rest = origin_limited_ings[restrictions[0]]!=0
    if len(restrictions) > 1:
        for i in restrictions[1:]:
            rest = rest | (origin_limited_ings[i]!=0)

    origin_limited_ings = origin_limited_ings[rest]
    origin_limited_ings

    potions = potions.loc[:, (potions != 0).any(axis=0)] # Remove all zero cols
    origin_limited_ings = origin_limited_ings.loc[:, (origin_limited_ings != 0).any(axis=0)]
    cols = origin_limited_ings.columns
    ing_cols = ["Ingredient 1", "Ingredient 2", "Ingredient 3", "Ingredient 4"]

    suffixes = [" 1", " 2"]

    potions = origin_limited_ings.merge(potions, how="cross", suffixes=suffixes)
    ing_cols = potions.columns.intersection(ing_cols)
    potions[ing_cols] = np.sort(potions[ing_cols].to_numpy())
    potions = potions.drop_duplicates(ing_cols)
    potions = potions.rename(columns={"Ingredient": f"Ingredient {str(len(ing_cols) + 1)}"}, errors="ignore")

    duplicates = (potions["Ingredient 1"] != potions["Ingredient 2"])
    if "Ingredient 3" in potions.columns:
        duplicates = duplicates & (potions["Ingredient 1"] != potions["Ingredient 3"])
        duplicates = duplicates & (potions["Ingredient 2"] != potions["Ingredient 3"])
    if "Ingredient 4" in potions.columns:
        duplicates = duplicates & (potions["Ingredient 1"] != potions["Ingredient 4"])
        duplicates = duplicates & (potions["Ingredient 2"] != potions["Ingredient 4"])
        duplicates = duplicates & (potions["Ingredient 3"] != potions["Ingredient 4"])

    potions = potions[duplicates].copy() # Avoids SettingWithCopyWarning

    potions["Total Effects"] = (potions==2).sum(axis=1)+(potions==3).sum(axis=1)+(potions==4).sum(axis=1) # No. of 2's per row
    for col in cols.drop(["Ingredient", "Ingredient 1", "Ingredient 2"], errors="ignore"):
        if col+" 1" not in potions.columns and col+" 2" not in potions.columns:
            pass
        elif col+" 1" in potions.columns and col+" 2" in potions.columns: 
            potions[col] = potions[col+" 1"] + potions[col+" 2"]
        elif col+" 1" in potions.columns:
            potions[col] = potions[col+" 1"]
        elif col+" 2" in potions.columns:
            potions[col] = potions[col+" 2"]
        potions = potions.drop([col+" 1", col+" 2"], axis=1, errors="ignore")
    potions["Total Effects"] = (potions==2).sum(axis=1)+(potions==3).sum(axis=1)+(potions==4).sum(axis=1) - potions["Total Effects"]
    potions = potions[potions["Total Effects"] > 0]
    potions = potions.reset_index().drop(["index", "Total Effects"], axis=1)
    
    if potions.empty:
        potions = pd.DataFrame()

    return potions


def potion_quads(ingredients):
    # If potion pair returns no potions, we know further
    # combinations (quadruplets) will also be empty
    if ingredients.empty:
        return pd.DataFrame()

    return pd.DataFrame()

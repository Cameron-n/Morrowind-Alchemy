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

# Idea's for efficiency
# - Calculate potion disjoint pairs after excluding 1 effect pairs
# - Calculate potion joint pairs seperately (how?)
# - Problem with selecting many effects? How to exclude combo's that won't work?

# Idea's for display
# - Paginate (kinda needed...)

# [combo] Find pairs combinations
# [minimal] store+remove minimal

# if n == 1 done

# if n == 2
# [extend] merge in parts using pairs connections
# [combo/extend] Find disjoint combinations with [1,1]

# if n == 3
# [extend] for 3's
# [minimal]
# [extend] for 4's
# [combo] [1,2] for 4d's

# if n == 4

# if n == 5

# if n == 6

# if n == 7

# if n == 8
# [combo] Find disjoint with [4,4]

# https://medium.com/@vamarnath/why-pandas-is-slower-than-you-think-and-how-to-optimize-your-dataframe-code-1c23b2bd4803
# USE .astype('category')
# remember positive

#%% Imports

# Standard
from itertools import combinations
import pandas as pd

# Relative
from components.data_access import DF_INGREDIENTS


#%% Functions

DF_INGREDIENTS=DF_INGREDIENTS.fillna(0)

def extend(left, right, n):
    """2-pairs -> 3-pairs -> joint 4-pairs"""
    if left.empty or right.empty:
        return pd.DataFrame()

    df = pd.DataFrame()
    for ing in right[0].unique(): # !!! Change if remapped strings to integers [or not???]
    # instead of n, may need to check all ing cols?    
        temp = left[left[n]==ing].merge(right[right[0]==ing].drop(0, axis=1), how='cross')
        df = pd.concat([df, temp])
    
    return df


def disjoint(df):
    """Calculate the disjoint 4-pair potions"""
    pass


def combos(ingredients):
    # https://stackoverflow.com/questions/31865088/using-python-and-pandas-to-create-combinations-instead-of-permutations
    df = pd.DataFrame(list(combinations(ingredients[0], 2)))
    df = df.merge(ingredients, left_on=0, right_on=0)
    # Match name of the merge columns to remove duplicate columns after merge
    df.columns=pd.RangeIndex(start=-1, stop=len(df.columns)-1, step=1)
    df = df.merge(ingredients, left_on=0, right_on=0)
    df.columns=pd.RangeIndex(start=0, stop=len(df.columns), step=1)
    return df


def formatting(df):
    df = df.where(df != 1, df.columns.to_series(), axis=1)
    temp = []
    for i in range(df.shape[0]):
        l=list(df.iloc[i][df.iloc[i]!=0])
        temp.append(l)
    return pd.DataFrame(temp)


def restrict(df, restrictions):
    drop_columns = ["ID", "Icon", "Value", "Weight", "Origin", "First Effect"]
    df = df.drop(drop_columns, axis=1, errors="ignore")

    rest = df[restrictions[0]]!=0
    if len(restrictions) > 1:
        for i in restrictions[1:]:
            rest = rest | (df[i]!=0)
    return df[rest]


def potion_combinations(ingredients, restrictions):
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
    if not restrictions:
        return pd.DataFrame()

    ingredients = restrict(ingredients, restrictions)

    # Order restrictions smallest first by number of ingredients with them
    restrictions = list(ingredients[restrictions].sum().sort_values().index)

    if ingredients.empty:
        return pd.DataFrame()

    ingredients = formatting(ingredients)

    # pe_x_y refers to the joint* potions with y number of ingredients
    # with all effects in restrictions[0:x].
    # For example, if restrictions=["Blind", "Drain Fatigue"],
    # pe22 means all pairs of potions that have Drain Fatigue and Blind.
    # ne_x_y refers to pe_(x-1)_y potions that are not in pe_x_y.
    # * disjoint potions are the same as pe_x_y except that they are
    # 4-ingredient potions made of 2 pairs of ingredients where neither 
    # pair shares any effects. These are labelled d_x.

    # 1
    has_0th_effect = (ingredients==restrictions[0]).any(axis=1) # ??? checks ingredient columns too?
    # https://stackoverflow.com/questions/31865088/using-python-and-pandas-to-create-combinations-instead-of-permutations
    pe12 = combos(ingredients[has_0th_effect])
    if len(restrictions) == 1:
        #https://stackoverflow.com/questions/60014754/value-counts-for-each-row-pandas-dataframe
        pe12 = pe12.mode(axis=1).assign(ing1=pe12[0], ing2=pe12[1]) # ??? checks ingredient columns too?
        return pe12

    # 2
    has_1st_effect = (ingredients==restrictions[1]).any(axis=1)
    all_effects = ingredients[has_0th_effect & has_1st_effect][0]
    is_minimal = pe12[[0,1]].isin(list(all_effects)).sum(axis=1)
    pe22 = pe12[is_minimal==2]
    ne22 = pe12[is_minimal==1]
    del pe12

    right = pd.DataFrame(all_effects).merge(ingredients[~has_0th_effect], how="cross")
    right.columns = pd.RangeIndex(start=0, stop=len(right.columns), step=1)
    pe23 = extend(ne22, right, 2) # 2 ings -> 3 ings
    d2 = disjoint([1, 1], restrictions[0:1]) # .mode before to calc highest num of effects
    if len(restrictions) == 2:
        return pd.concat([pe22, pe23, d2])
        
        

    # new stuff ^^^^^
    return pd.DataFrame()

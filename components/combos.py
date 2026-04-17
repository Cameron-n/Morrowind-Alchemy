# -*- coding: utf-8 -*-
"""
Created on Sun Jul 20 18:10:49 2025

@author: Cameron-n

Contains the logic to calculate ingredient combinations (i.e. potions)
"""

# Consider calculator for optimal potions from available ingredients?

# Idea's for efficiency
# - Calculate potion disjoint pairs after excluding 1 effect pairs
# - Calculate potion joint pairs seperately (how?)
# - Problem with selecting many effects? How to exclude combo's that won't work?

# Idea's for display
# - Paginate
# - headers for number of effects

# https://medium.com/@vamarnath/why-pandas-is-slower-than-you-think-and-how-to-optimize-your-dataframe-code-1c23b2bd4803
# USE .astype('category')

# Tasks
# - disjoint function
# - fix mode if effect occurs 3/4 times [mode of pairs + mode of triples + mode of quads???]

#%% Imports

# Standard
from itertools import combinations
import pandas as pd
from pandas.api.types import CategoricalDtype

# Relative
from components.data_access import DF_EFFECTS

DF_EFFECTS = DF_EFFECTS.fillna(0)


#%% Functions

def only_effects(df, n=2): #<-- UNFINISHED
    if df.empty:
        return pd.DataFrame()

    if n==2:
        #https://stackoverflow.com/questions/60014754/value-counts-for-each-row-pandas-dataframe
        df = df.mode(axis=1).assign(ing1=df[0], ing2=df[1]).astype("category")
    elif n==3:
        df2 = df.apply(lambda x: pd.DataFrame(list(x.value_counts()[x.value_counts()>1].index)).transpose(), axis=1)
        df2 = pd.concat(list(df2))
        df = df2.assign(ing1=df[0], ing2=df[1], ing3=df[2]).astype("category")
    elif n==4:
        df2 = df.apply(lambda x: pd.DataFrame(list(x.value_counts()[x.value_counts()>1].index)).transpose(), axis=1)
        df2 = pd.concat(list(df2))
        df = df2.assign(ing1=df[0], ing2=df[1], ing3=df[2], ing4=df[3]).astype("category")

    return df


def rank_potions(df, limit, poison):
    if df.empty:
        return pd.DataFrame()

    pos_effects = DF_EFFECTS["Spell Effects"][DF_EFFECTS["Positive"]==1]
    df["pos"] = df.isin(list(pos_effects)).sum(axis=1)
    # neg effects is total cols minus non-effect cols minus pos effects count
    df["neg"] = df.count(axis=1)-(~df.columns.isin([0,1,2,3,4,5,6,7])).sum()-df["pos"]
    
    if not df.empty:
        if poison:
            df = df.sort_values(by=["neg","pos"], ascending=[False, True]).reset_index().drop("index", axis=1)
        else:
            df = df.sort_values(by=["pos","neg"], ascending=[False, True]).reset_index().drop("index", axis=1)

    return df.iloc[:limit]


def extend(left, right, n):
    """2-pairs -> 3-pairs -> joint 4-pairs"""
    if left.empty or right.empty:
        return left

    df = pd.DataFrame()
    if n == 2:
        for ing in right[0].unique():   
            temp0 = left[left[0]==ing].merge(right[right[0]==ing].drop(0, axis=1), how='cross')
            temp1 = left[left[1]==ing].merge(right[right[0]==ing].drop(0, axis=1), how='cross')
            df = pd.concat([df, temp0, temp1])
    else:
        for ing in right[0].unique():
            temp = left[left[n-1]==ing].merge(right[right[0]==ing].drop(0, axis=1), how='cross')
            df = pd.concat([df, temp])
    if n == 2:
        df.columns = [0, 1, 3, 4, 5, 6, 7, 8, 9 ,10 ,2 , 11, 12, 13, 14]
    else:
        df.columns = [0, 1, 4, 5, 6, 7, 8, 9, 10 ,11 ,2 , 12, 13, 14, 15, 3, 16, 17, 18, 19]
    
    return df


def disjoint(ingredients, restrictions, poison):
    """Calculate the disjoint 4-pair potions"""
    n = len(restrictions)
    if n == 2:
        possibilities = [[1,1]]
    elif n == 3:
        possibilities = [[1,2]]
    elif n == 4:
        possibilities = [[1,3],[2,2]]
    elif n == 5:
        possibilities = [[1,4],[2,3]]
    elif n == 6:
        possibilities = [[2,4],[3,3]]
    elif n == 7:
        possibilities = [[3,4]]
    elif n == 8:
        possibilities = [[4,4]]

    # Get each list of effect combos where [x,y]==n
    temp = []
    for i in possibilities:
        effect_combos = list(combinations(restrictions, i[0]))
        if i[0] == i[1]:
            effect_combos = effect_combos[:len(effect_combos)//2]
        temp.append(effect_combos)

    # Calculate ings combos
    p4 = pd.DataFrame()
    for pair in temp:
        for comb in pair:
            rest = (ingredients!="False").any(axis=1)
            not_rest = (ingredients!="False").any(axis=1)
            right_rest = (ingredients!="False").any(axis=1)
            for effect in comb:
                rest = rest & ((ingredients==effect).any(axis=1))
            for not_effect in list(set(restrictions)-set(comb)):
                not_rest = not_rest & ~((ingredients==not_effect).any(axis=1))
                right_rest = right_rest & (ingredients==not_effect).any(axis=1)

            left_ings = ingredients[rest & not_rest]
            p2l = combos(left_ings)
            p2l = rank_potions(only_effects(p2l), 10, poison).drop(["pos","neg"], axis=1, errors="ignore")
            if not p2l.empty:
                p2l.columns = [i for i in range(len(p2l.columns)-2)] + ['ing1', 'ing2']
            
            right_ings = ingredients[~rest & right_rest]
            p2r = combos(right_ings)
            p2r = rank_potions(only_effects(p2r), 10, poison).drop(["pos","neg"], axis=1, errors="ignore")
            if not p2r.empty:
                p2r.columns = [i+4 for i in range(len(p2r.columns)-2)] + ['ing3', 'ing4']
            
            if not p2r.empty and not p2l.empty:
                p4 = pd.concat([p4, p2l.merge(p2r, how="cross")])

    return p4

 
def combos(ingredients):
    # https://stackoverflow.com/questions/31865088/using-python-and-pandas-to-create-combinations-instead-of-permutations
    df = pd.DataFrame(list(combinations(ingredients[0], 2)))
    if df.empty:
        return pd.DataFrame()

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
    temp.append(["REMOVE", 0, 0, 0, 0]) # ensure df has 5 columns
    df = pd.DataFrame(temp)
    df = df.drop(df.shape[0]-1)
    return df


def restrict(df, restrictions):
    drop_columns = ["ID", "Icon", "Value", "Weight", "Origin", "First Effect"]
    df = df.drop(drop_columns, axis=1, errors="ignore")

    rest = df[restrictions[0]]!=0
    if len(restrictions) > 1:
        for i in restrictions[1:]:
            rest = rest | (df[i]!=0)
    return df[rest]


def potion_combinations(ingredients, restrictions, poison):
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
    
    # Explicit categories but may not be needed
    # and is less space efficient (negligably)
    categories = pd.concat(
        [ingredients[1][ingredients[1].notna()],
         ingredients[2][ingredients[2].notna()],
         ingredients[3][ingredients[3].notna()],
         ingredients[4][ingredients[4].notna()]
         ]).unique()
    cat_type = CategoricalDtype(categories=categories)
    cat_type_ing = CategoricalDtype(categories=ingredients[0].unique())
    ingredients[0] = ingredients[0].astype(cat_type_ing)
    ingredients[1] = ingredients[1].astype(cat_type)
    ingredients[2] = ingredients[2].astype(cat_type)
    ingredients[3] = ingredients[3].astype(cat_type)
    ingredients[4] = ingredients[4].astype(cat_type)

    # pe_x_y refers to the joint* potions with y number of ingredients
    # with all effects in restrictions[0:x].
    # For example, if restrictions=["Blind", "Drain Fatigue"],
    # pe22 means all pairs of potions that have Drain Fatigue and Blind.
    # ne_x_y refers to pe_(x-1)_y potions that are not in pe_x_y.
    # * disjoint potions are the same as pe_x_y except that they are
    # 4-ingredient potions made of 2 pairs of ingredients where neither 
    # pair shares any effects. These are labelled d_x.

    #%% 1
    has_0th_effect = (ingredients==restrictions[0]).any(axis=1)
    # https://stackoverflow.com/questions/31865088/using-python-and-pandas-to-create-combinations-instead-of-permutations
    pe12 = combos(ingredients[has_0th_effect])
    if pe12.empty:
        return pe12
    pe12[0] = pe12[0].astype(cat_type_ing)
    pe12[1] = pe12[1].astype(cat_type_ing)
    if len(restrictions) == 1:
        #https://stackoverflow.com/questions/60014754/value-counts-for-each-row-pandas-dataframe
        pe12 = only_effects(pe12)
        potions = rank_potions(pe12, 100, poison)
        return potions

    #%% 2
    has_1st_effect = (ingredients==restrictions[1]).any(axis=1)
    all_effects = ingredients[has_0th_effect & has_1st_effect][0]
    is_minimal = pe12[[0,1]].isin(list(all_effects)).sum(axis=1)
    pe22 = pe12[is_minimal==2]
    ne22 = pe12[is_minimal==1].reset_index().drop("index", axis=1)
    del pe12

    right = pd.DataFrame(all_effects).merge(ingredients[~has_0th_effect], how="cross")
    right.columns = pd.RangeIndex(start=0, stop=len(right.columns), step=1)
    pe23 = extend(ne22, right, 2).reset_index().drop("index", axis=1)
    del ne22

    if len(restrictions) == 2:
        d2 = disjoint(ingredients, restrictions, poison) # .mode before to calc highest num of effects
        pe22 = only_effects(pe22)
        pe23 = only_effects(pe23, 3)
        potions = pd.concat([pe22, pe23, d2])
        potions = rank_potions(potions, 100, poison)        
        return potions

    #%% 3
    has_2nd_effect = (ingredients==restrictions[2]).any(axis=1)
    all_effects = ingredients[has_0th_effect & has_1st_effect & has_2nd_effect][0]
    is_minimal = pe22[[0,1]].isin(list(all_effects)).sum(axis=1)
    pe32 = pe22[is_minimal==2]
    ne32 = pe22[is_minimal==1].reset_index().drop("index", axis=1)
    del pe22

    right = pd.DataFrame(all_effects).merge(ingredients[~has_0th_effect][~has_1st_effect], how="cross")
    right.columns = pd.RangeIndex(start=0, stop=len(right.columns), step=1)
    pe33 = extend(ne32, right, 2).reset_index().drop("index", axis=1)
    del ne32

    is_minimal = pe23[[0,1,2]].isin(list(all_effects)).sum(axis=1)
    pe33 = pd.concat([pe33, pe23[is_minimal==3]])
    ne33 = pe23[is_minimal==2]
    
    if len(restrictions) == 3:
        pe34 = extend(ne33, right, 3).reset_index().drop("index", axis=1)
        d3 = disjoint(ingredients, restrictions, poison)
        pe32 = only_effects(pe32)
        pe33 = only_effects(pe33, 3)
        pe34 = only_effects(pe34, 4)
        potions = pd.concat([pe32, pe33, pe34, d3])
        potions = rank_potions(potions, 100, poison)        
        return potions
    #%% 4
    has_3rd_effect = (ingredients==restrictions[3]).any(axis=1)
    all_effects = ingredients[has_0th_effect & has_1st_effect & has_2nd_effect & has_3rd_effect][0]
    is_minimal = pe32[[0,1]].isin(list(all_effects)).sum(axis=1)
    pe42 = pe32[is_minimal==2]
    ne42 = pe32[is_minimal==1].reset_index().drop("index", axis=1)
    del pe32

    right = pd.DataFrame(all_effects).merge(ingredients[~has_0th_effect][~has_1st_effect][~has_2nd_effect], how="cross")
    right.columns = pd.RangeIndex(start=0, stop=len(right.columns), step=1)
    pe43 = extend(ne42, right, 2).reset_index().drop("index", axis=1)
    del ne42

    is_minimal = pe33[[0,1,2]].isin(list(all_effects)).sum(axis=1)
    pe43 = pd.concat([pe43, pe33[is_minimal==3]])
    ne43 = pe33[is_minimal==2]

    if len(restrictions) == 4:
        pe44 = extend(ne43, right, 3).reset_index().drop("index", axis=1)
        d4 = disjoint(ingredients, restrictions, poison)
        pe42 = only_effects(pe42)
        pe43 = only_effects(pe43, 3)
        pe44 = only_effects(pe44, 4)
        potions = pd.concat([pe42, pe43, pe44, d4])
        potions = rank_potions(potions, 100, poison)        
        return potions
    #%% 5
    has_4th_effect = (ingredients==restrictions[4]).any(axis=1)
    all_effects = ingredients[has_0th_effect & has_1st_effect & has_2nd_effect & has_3rd_effect & has_4th_effect][0]

    right = pd.DataFrame(all_effects).merge(ingredients[~has_0th_effect][~has_1st_effect][~has_2nd_effect][~has_3rd_effect], how="cross")
    right.columns = pd.RangeIndex(start=0, stop=len(right.columns), step=1)

    is_minimal = pe43[[0,1,2]].isin(list(all_effects)).sum(axis=1)
    pe53 = pe43[is_minimal==3]
    ne53 = pe43[is_minimal==2]
    
    if len(restrictions) == 5:
        pe54 = extend(ne53, right, 3).reset_index().drop("index", axis=1)
        d5 = disjoint(ingredients, restrictions, poison)
        pe53 = only_effects(pe53, 3)
        pe54 = only_effects(pe54, 4)
        potions = pd.concat([pe53, pe54, d5])
        potions = rank_potions(potions, 100, poison)        
        return potions
    #%% 6
    has_5th_effect = (ingredients==restrictions[5]).any(axis=1)
    all_effects = ingredients[has_0th_effect & has_1st_effect & has_2nd_effect & has_3rd_effect & has_4th_effect & has_5th_effect][0]

    right = pd.DataFrame(all_effects).merge(ingredients[~has_0th_effect][~has_1st_effect][~has_2nd_effect][~has_3rd_effect][~has_4th_effect], how="cross")
    right.columns = pd.RangeIndex(start=0, stop=len(right.columns), step=1)

    is_minimal = pe53[[0,1,2]].isin(list(all_effects)).sum(axis=1)
    pe63 = pe53[is_minimal==3]
    ne63 = pe53[is_minimal==2]

    if len(restrictions) == 6:
        pe64 = extend(ne63, right, 3).reset_index().drop("index", axis=1)
        d6 = disjoint(ingredients, restrictions, poison) # .mode before to calc highest num of effects
        pe63 = only_effects(pe63, 3)
        pe64 = only_effects(pe64, 4)
        potions = pd.concat([pe63, pe64, d6])
        potions = rank_potions(potions, 100, poison)        
        return potions
    #%% 7
    has_6th_effect = (ingredients==restrictions[6]).any(axis=1)
    all_effects = ingredients[has_0th_effect & has_1st_effect & has_2nd_effect & has_3rd_effect & has_4th_effect & has_5th_effect & has_6th_effect][0]

    if len(restrictions) == 7:
        is_minimal = pe64[[0,1,2,3]].isin(list(all_effects)).sum(axis=1)
        pe74 = pe64[is_minimal==4]
        d7 = disjoint(ingredients, restrictions, poison) # .mode before to calc highest num of effects
        pe74 = only_effects(pe74, 4)
        potions = pd.concat([pe74, d7])
        potions = rank_potions(potions, 100, poison)        
        return potions
    #%% 8
    if len(restrictions) == 8:
        d8 = disjoint(ingredients, restrictions, poison) # .mode before to calc highest num of effects
        potions = rank_potions(d8, 100, poison)        
        return potions

    return pd.DataFrame()

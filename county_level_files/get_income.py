import pandas as pd
import numpy as np
import re
import os
import preprocessing_income as pre

INCOME_PAIRS = [
    ('income_2009_5yr', 'RNGE'),
    ('income_2010_5yr', 'JOHE'),
    ('income_2011', 'L33E'),
    ('income_2012', 'O34E'),
    ('income_2013', 'SUYE'),
    ('income_2014', 'AAS5E'),
    ('income_2015', 'AC2YE'),
    ('income_2016', 'AFJ8E'),
    ('income_2017', 'AHFCE'),
    ('income_2018', 'AJCTE'),
    ('income_2019', 'ALAJE'),
    ('income_2020_5yr', 'AMR7E'),
    ('income_2021', 'ANY7E'),
    ('income_2022', 'AP2FE')
    ]

for fp, cp in INCOME_PAIRS:
    
    df_iter = pre.get_csv("household_income/" + fp, cp)
    
    if fp == 'income_2009_5yr':
        df_inc = df_iter
    else:
        df_inc = pd.concat([df_inc, df_iter])
df_inc = df_inc.reset_index()
df_inc = df_inc.drop(columns = ['index'])

def growth_def(df_input, n):
    for i in np.arange(1, n):
        new_col = f'''income_growth_last_{i}_years'''
        
        orig_income = df_input.groupby('place')['average_income'].shift(i)
        change_in_income = df_input['average_income'] - orig_income
        df_input[new_col] = change_in_income / orig_income
        
        df_comp = df_input[~df_input[new_col].isna()] #PULL NON-NULLS FOR IMPUTATION COMPUTATIONS
        
        if i > 1:
            df_comp['diff'] = df_comp[new_col] - df_comp[last_col] #CHANGE IN GROWTH RATE FROM YEAR i TO YEAR i+1
            mean_change = df_comp['diff'].mean() #MEAN
            df_input[new_col] = df_input[new_col].fillna(df_input[last_col] + mean_change) #IMPUTE YEAR i GROWTH + MEAN CHANGE
        else:
            #0 FILL IN FOR GROWTH - TUFF HAVING ALL 2009 NUMBERS AT 0 GROWTH OH WELL
            df_input[new_col] = df_input[new_col].fillna(0) 
            
            #ALTERNATIVE - SET BY USING FUTURE YEARS - 0 FILL IN NOT GREAT, BUT I LIKE IT BETTER THAN USING UNKNOWN INFO
            # mean_growth_last = df_comp[new_col].mean()
            # df_input[new_col] = df_input[new_col].fillna(mean_growth_last)
        last_col = new_col

growth_def(df_inc, 4)
df_inc['year'] = df_inc['year'].astype(int)
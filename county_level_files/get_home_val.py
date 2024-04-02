import pandas as pd
import numpy as np
import re
import preprocessing_home_val as pre
import os
import warnings
warnings.filterwarnings('ignore')

HOME_VAL_PAIRS = [
    ('home_value_2009_5yr', 'RR5E'),
    ('home_value_2010_5yr', 'JTGE'),
    ('home_value_2011', 'MGZE'),
    ('home_value_2012', 'PGYE'),
    ('home_value_2013', 'S50E'),
    ('home_value_2014', 'AA3VE'),
    ('home_value_2015', 'ADDPE'),
    ('home_value_2016', 'AFUZE'),
    ('home_value_2017', 'AHP5E'),
    ('home_value_2018', 'AJNQE'),
    ('home_value_2019', 'ALLGE'),
    ('home_value_2020_5yr', 'AMV9E'),
    ('home_value_2021', 'AN8XE'),
    ('home_value_2022', 'AQDXE')
    ]

for fp, cp in HOME_VAL_PAIRS:
    
    df_iter = pre.get_csv("home_value/" + fp, cp, 'home value')
    
    if fp == 'home_value_2009_5yr':
        df_home_val = df_iter.copy()
    else:
        df_home_val = pd.concat([df_home_val, df_iter])
        
df_home_val = df_home_val.dropna().reset_index().drop(columns = ['index'])

def growth_def(df_input, n):
    for i in np.arange(1, n):
        new_col = f'''home_val_growth_last_{i}_years'''
        
        orig_val = df_input.groupby('place')['average_home_value'].shift(i)
        change_in_val = df_input['average_home_value'] - orig_val
        df_input[new_col] = change_in_val / orig_val
        
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

growth_def(df_home_val, 4)

df_home_val['val_in_three'] = df_home_val.groupby('place')['average_home_value'].shift(-3)
df_home_val['three_year_growth'] = df_home_val['val_in_three'] - df_home_val['average_home_value']
df_home_val = df_home_val.drop(columns = ['val_in_three'])

df_home_val['year'] = df_home_val['year'].astype(int)
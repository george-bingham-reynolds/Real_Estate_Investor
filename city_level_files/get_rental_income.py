import pandas as pd
import numpy as np
import re
import preprocessing_rent as pre
import os

RENT_PAIRS = [
    ('rent_2009_5yr', 'RRME'),
    ('rent_2010_5yr', 'JSXE'),
    ('rent_2011_5yr', 'MUHE'),
    ('rent_2012_5yr', 'QZLE'),
    ('rent_2013_5yr', 'UL1E'),
    ('rent_2014_5yr', 'ABH9E'),
    ('rent_2015_5yr', 'ADRCE'),
    ('rent_2016_5yr', 'AF81E'),
    ('rent_2017_5yr', 'AH5JE'),
    ('rent_2018_5yr', 'AJ26E'),
    ('rent_2019_5yr', 'AL0XE'),
    ('rent_2020_5yr', 'AMVRE'),
    ('rent_2021_5yr', 'AOT1E'),
    ('rent_2022_5yr', 'AQUKE')
    ]

for fp, cp in RENT_PAIRS:
    
    df_iter = pre.get_csv("rental_costs/" + fp, cp)
    if fp == 'rent_2009_5yr':
        df_rent = df_iter
    else:
        df_rent = pd.concat([df_rent, df_iter])
        
df_rent = df_rent.reset_index()
df_rent = df_rent.drop(columns = ['index'])

def growth_def(df_input, n):
    for i in np.arange(1, n):
        new_col = f'''rent_growth_last_{i}_years'''
        
        orig_rent = df_input[df_input['average_annual_rent'] != 0].groupby('place')['average_annual_rent'].shift(i)
        change_in_rent = df_input['average_annual_rent'] - orig_rent
        df_input[new_col] = change_in_rent / orig_rent
        
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

growth_def(df_rent, 4)

df_rent['rent_trailing_three'] = df_rent.groupby('place')['average_annual_rent'].rolling(3).sum().reset_index(0, drop = True)
df_rent['rent_in_three'] = df_rent.groupby('place')['rent_trailing_three'].shift(-2)
df_rent = df_rent.drop(columns = ['rent_trailing_three'], axis = 1)

df_rent['year'] = df_rent['year'].astype(int)
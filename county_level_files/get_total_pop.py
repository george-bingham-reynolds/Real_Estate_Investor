import pandas as pd
import numpy as np
import re
import os
import preprocessing_total_pop as pre

POP_PAIRS = [
    ('population_2009_5yr', 'RK9E'),
    ('population_2010', 'IHXE'),
    ('population_2011', 'LJBE'),
    ('population_2012', 'OJEE'),
    ('population_2013', 'SBLE'),
    ('population_2014', 'AAA5E'),
    ('population_2015', 'ACK2E'),
    ('population_2016', 'AE2BE'),
    ('population_2017', 'AGXFE'),
    ('population_2018', 'AIUWE'),
    ('population_2019', 'AKSLE'),
    ('population_2020', 'U7H'),
    ('population_2021', 'ANLSE'),
    ('population_2022', 'APKFE')
    ]


for fp, cp in POP_PAIRS:
    
    df_iter = pre.get_csv("population/" + fp, cp)
    
    if fp == 'population_2009_5yr':
        df_pop = df_iter
    else:
        df_pop = pd.concat([df_pop, df_iter])

df_pop = df_pop.reset_index()
df_pop = df_pop.drop(columns = ['index'])

def growth_def(df_input, n):
    for i in np.arange(1, n):
        
        new_col = f'''growth_last_{i}_years'''
        
        orig_pop = df_input.groupby('place')['total_population'].shift(i)
        change_in_pop = df_input['total_population'] - orig_pop
        df_input[new_col] = change_in_pop / orig_pop
        
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

growth_def(df_pop, 4)
df_pop['year'] = df_pop['year'].astype(int)
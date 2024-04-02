import pandas as pd
import numpy as np
import re
import os
import preprocessing_vacancy as pre

VAC_PAIRS = [
    ('vacancy_2009_5yr', 'RP8E'),
    ('vacancy_2010_5yr', 'JRJE'),
    ('vacancy_2011_5yr', 'MS3E'),
    ('vacancy_2012_5yr', 'QX7E'),
    ('vacancy_2013_5yr', 'UKNE'),
    ('vacancy_2014_5yr', 'ABGWE'),
    ('vacancy_2015_5yr', 'ADPZE'),
    ('vacancy_2016_5yr', 'AF7OE'),
    ('vacancy_2017_5yr', 'AH36E'),
    ('vacancy_2018_5yr', 'AJ1TE'),
    ('vacancy_2019_5yr', 'ALZKE'),
    ('vacancy_2020_5yr', 'AMUEE'),
    ('vacancy_2021_5yr', 'AOSOE'),
    ('vacancy_2022_5yr', 'AQSPE')
    ]


for fp, cp in VAC_PAIRS:
    
    df_iter = pre.get_csv("vacancy/" + fp, cp)
    
    if fp == 'vacancy_2009_5yr':
        df_vac = df_iter
    else:
        df_vac = pd.concat([df_vac, df_iter])

df_vac = df_vac.reset_index()
df_vac = df_vac.drop(columns = ['index'])

def growth_def(df_input, n):
    for i in np.arange(1, n):
        
        new_col = f'''vacancy_growth_last_{i}_years'''
        
        orig_vac = df_input[df_input['vacancy_rate'] != 0].groupby('place')['vacancy_rate'].shift(i)
        change_in_vac = df_input['vacancy_rate'] - orig_vac
        df_input[new_col] = change_in_vac / orig_vac
        
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

growth_def(df_vac, 4)
df_vac['year'] = df_vac['year'].astype(int)
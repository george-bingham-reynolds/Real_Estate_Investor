import pandas as pd
import numpy as np
import re
import os
import preprocessing_vacancy as pre

VAC_PAIRS = [
    ('vacancy_2009_5yr', 'RP8E'),
    ('vacancy_2010_5yr', 'JRJE'),
    ('vacancy_2011', 'MDGE'),
    ('vacancy_2012', 'PDHE'),
    ('vacancy_2013', 'S25E'),
    ('vacancy_2014', 'AA02E'),
    ('vacancy_2015', 'ADAVE'),
    ('vacancy_2016', 'AFR5E'),
    ('vacancy_2017', 'AHNBE'),
    ('vacancy_2018', 'AJKWE'),
    ('vacancy_2019', 'ALIME'),
    ('vacancy_2020_5yr', 'AMUEE'),
    ('vacancy_2021', 'AN6BE'),
    ('vacancy_2022', 'AQALE')
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
        
        orig_vac = df_input.groupby('place')['vacancy_rate'].shift(i)
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
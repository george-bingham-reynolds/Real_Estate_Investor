import preprocessing_home_val as pre
import pandas as pd
import numpy as np
import re
import os
import warnings
warnings.filterwarnings('ignore')

# FILEPATH, CODE PATTERN PAIRS
HOME_VAL_PAIRS = [
    ('home_value_2009_5yr', 'RR5E'),
    ('home_value_2010_5yr', 'JTGE'),
    ('home_value_2011_5yr', 'MU0E'),
    ('home_value_2012_5yr', 'QZ4E'),
    ('home_value_2013_5yr', 'UMKE'),
    ('home_value_2014_5yr', 'ABIRE'),
    ('home_value_2015_5yr', 'ADRUE'),
    ('home_value_2016_5yr', 'AF9JE'),
    ('home_value_2017_5yr', 'AH51E'),
    ('home_value_2018_5yr', 'AJ3OE'),
    ('home_value_2019_5yr', 'AL1FE'),
    ('home_value_2020_5yr', 'AMV9E'),
    ('home_value_2021_5yr', 'AOUJE'),
    ('home_value_2022_5yr', 'AQU2E')]

for fp, cp in HOME_VAL_PAIRS:
    
    df_iter = pre.get_csv("home_value/" + fp, cp, 'home value')
    
    if fp == 'home_value_2009_5yr':
        df_home_val = df_iter.copy()
    else:
        df_home_val = pd.concat([df_home_val, df_iter])
        
df_home_val = df_home_val.dropna().reset_index().drop(columns = ['index'])

# SEE VACANCY FOR FULLER EXPLANATION
def growth_def(df_input, n):
    for i in np.arange(1, n):
        new_col = f'''home_val_growth_last_{i}_years'''
        
        orig_val = df_input[df_input['average_home_value'] != 0].groupby('place')['average_home_value'].shift(i)
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

# WE NEED HOME VALUE 3 YEARS INTO FUTURE FOR ROI DEFINITION LATER
df_home_val['val_in_three'] = df_home_val.groupby('place')['average_home_value'].shift(-3)
df_home_val['three_year_growth'] = df_home_val['val_in_three'] - df_home_val['average_home_value']
df_home_val = df_home_val.drop(columns = ['val_in_three'])

df_home_val['year'] = df_home_val['year'].astype(int)
import pandas as pd
import numpy as np
import re
import preprocessing_race as pre
import os
import warnings
warnings.filterwarnings('ignore')

always_keep = ['year', 'place']

# FILEPATH, CODE PATTERN PAIRS
RACE_PAIRS = [
    ('race_2009_5yr', 'RLAE'),
    ('race_2010_5yr', 'JMBE'),
    ('race_2011_5yr', 'MNUE'),
    ('race_2012_5yr', 'QSQE'),
    ('race_2013_5yr', 'UEQE'),
    ('race_2014_5yr', 'ABA2E'),
    ('race_2015_5yr', 'ADKXE'),
    ('race_2016_5yr', 'AF2ME'),
    ('race_2017_5yr', 'AHY2E'),
    ('race_2018_5yr', 'AJWNE'),
    ('race_2019_5yr', 'ALUCE'),
    ('race_2020_5yr', 'AMPWE'),
    ('race_2021_5yr', 'AON5E'),
    ('race_2022_5yr', 'AQNGE')
    ]

for fp, cp in RACE_PAIRS:
    
    df_iter = pre.get_csv("race/" + fp, cp)
    if fp == 'race_2009_5yr':
        df_race = df_iter
    else:
        df_race = pd.concat([df_race, df_iter])
        
df_race = df_race.reset_index()
df_race = df_race.drop(columns = ['index'])
df_race['year'] = df_race['year'].astype(int)
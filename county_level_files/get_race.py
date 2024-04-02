import pandas as pd
import numpy as np
import re
import preprocessing_race as pre
import os
import warnings
warnings.filterwarnings('ignore')

always_keep = ['year', 'place']

RACE_PAIRS = [
    ('race_2009_5yr', 'RLAE'),
    ('race_2010', 'H7X'),
    ('race_2011', 'LJCE'),
    ('race_2012', 'OJFE'),
    ('race_2013', 'SBME'),
    ('race_2014', 'AAA6E'),
    ('race_2015', 'ACK3E'),
    ('race_2016', 'AE2CE'),
    ('race_2017', 'AGXGE'),
    ('race_2018', 'AIUXE'),
    ('race_2019', 'AKSME'),
    ('race_2020', 'U7J0'),
    ('race_2021', 'ANLTE'),
    ('race_2022', 'APKGE')
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
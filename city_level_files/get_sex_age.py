import pandas as pd
import numpy as np
import re
import preprocessing_sex_age as pre
import os
import warnings
warnings.filterwarnings('ignore')
always_keep = [
    'year',
    'place']
SEX_AGE_PAIRS = [
    ('sex_by_age_2009_5yr', 'RKYE'),
    ('sex_by_age_2010_5yr', 'JLZE'),
    ('sex_by_age_2011_5yr', 'MNIE'),
    ('sex_by_age_2012_5yr', 'QSEE'),
    ('sex_by_age_2013_5yr', 'UEEE'),
    ('sex_by_age_2014_5yr', 'ABAQE'),
    ('sex_by_age_2015_5yr', 'ADKLE'),
    ('sex_by_age_2016_5yr', 'AF2AE'),
    ('sex_by_age_2017_5yr', 'AHYQE'),
    ('sex_by_age_2018_5yr', 'AJWBE'),
    ('sex_by_age_2019_5yr', 'ALT0E'),
    ('sex_by_age_2020_5yr', 'AMPKE'),
    ('sex_by_age_2021_5yr', 'AONTE'),
    ('sex_by_age_2022_5yr', 'AQM4E')
    ]

for fp, cp in SEX_AGE_PAIRS:
    
    df_iter = pre.get_csv("age_by_sex/" + fp, cp)
    
    if fp == 'sex_by_age_2009_5yr':
        df_sex_age = df_iter
    else: df_sex_age = pd.concat([df_sex_age, df_iter])
    
df_sex_age = df_sex_age.reset_index()
df_sex_age = df_sex_age.drop(columns = ['index'])
df_sex_age['year'] = df_sex_age['year'].astype(int)
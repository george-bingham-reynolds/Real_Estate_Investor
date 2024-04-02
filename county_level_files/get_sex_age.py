import pandas as pd
import numpy as np
import re
import preprocessing_sex_age as pre
import os
import warnings
warnings.filterwarnings('ignore')

always_keep = ['year', 'place']

SEX_AGE_PAIRS = [
    ('sex_age_2009_5yr', 'RKYE'),
    ('sex_age_2010_5yr', 'JLZE'),
    ('sex_age_2011', 'LIIE'),
    ('sex_age_2012', 'OILE'),
    ('sex_age_2013', 'SASE'),
    ('sex_age_2014', 'AAACE'),
    ('sex_age_2015', 'ACJ9E'),
    ('sex_age_2016', 'AE1IE'),
    ('sex_age_2017', 'AGWME'),
    ('sex_age_2018', 'AIT3E'),
    ('sex_age_2019', 'AKRSE'),
    ('sex_age_2020_5yr', 'AMPKE'),
    ('sex_age_2021', 'ANK8E'),
    ('sex_age_2022', 'APJME')
    ]

for fp, cp in SEX_AGE_PAIRS:
    
    df_iter = pre.get_csv("age_by_sex/" + fp, cp)
    
    if fp == 'sex_age_2009_5yr':
        df_sex_age = df_iter
    else: df_sex_age = pd.concat([df_sex_age, df_iter])
    
df_sex_age = df_sex_age.reset_index()
df_sex_age = df_sex_age.drop(columns = ['index'])
df_sex_age['year'] = df_sex_age['year'].astype(int)
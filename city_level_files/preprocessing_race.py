import pandas as pd
import numpy as np
import re
import os

always_keep = ['YEAR', 'STATE', 'PLACE']


# MAKING FUNCTION FOR RACE POPULATION CSV PREPROCESSING:
def get_csv(fp, cp):
    
    # GET RID OF NON CODE-LABEL INFO FROM TXT FILE
    lines_to_keep = []
    with open(f"{fp}.txt", "r") as f:

         for line in f.readlines():
             if cp in line:
                 lines_to_keep.append(line)

    # WRITE TRIMMED DOWN FILE
    with open(f"{fp}_trim.txt", "w") as f:

        for link in lines_to_keep:
            f.write(link)


    # DROP SUPERFLUOUS INFO FROM DF
    df = pd.read_csv(f"{fp}.csv", encoding = "ISO-8859-1")
    df = df.drop(columns = [x for x in df.columns if x not in always_keep and cp not in x])
    df['YEAR'] = df['YEAR'].astype(str)

    # RENAMING DICT
    col_label_dict = {}

    with open(f"{fp}_trim.txt", "r") as f:

        for line in f.readlines():


            code = line.split(":")[0].lstrip() #SPLIT STRING ON : THEN GET RID LEADING WHITE SPACE
    
            # SPECIAL FORMATTING TO CLEAN UP CODES FOR MORE THAN 1 RACE
            if '009' in code:
                label = line.split(":")[1].lstrip().rstrip() + ' - 2'
            elif '010' in code:
                label = line.split(":")[1].lstrip().rstrip() + ' - 3'
            else:
                label = line.split(":")[1].lstrip().rstrip()
                
            col_label_dict[code] = label.lower()

    def relabel(code):
        if code in col_label_dict.keys():
            label = col_label_dict[code]
            return label
        else:
            return code

    # RENAME
    df = df.rename(mapper = relabel, axis = 1)
    # FOR MULTI-YEAR JUST PULL LAST YEAR
    df['YEAR'] = df['YEAR'].apply(lambda x: x[-4:] if '-' in x else x)
    
    #THE CENSUS SOMETIMES HAS PRETTY NICHE MULTI-RACE DEFINITIONS; ONE OVERALL SEEMS SUFFISH TO ME
    if 'two or more races - 3' in df.columns:
        df['two or more races'] = df['two or more races'] + df['two or more races - 2'] + df['two or more races - 3']
        df = df.drop(columns = ['two or more races - 2', 'two or more races - 3'])
     
    df.columns = [re.sub(' ', '_', x) for x in df.columns]
    # POPULATION SIZE IS BEING CAPTURED ELSEWHERE; LET'S DO PERCENTAGES HERE
    for col in df.columns:
        if (col not in always_keep) and (col != 'total'):
            df[col] = df[col]/df['total']
            
            # LOTS OF NULLS - PROBS A 0 DIV/LACK OF PRESENCE ISSUE CUZ NOT SUPER DUPER PERVASIVE JUST ENOUGH TO NOTICE
            df[col] = df[col].fillna(0)
    
    

    # COMBINE STATE AND CITY (PLACE) FOR 'PLACE' KEY
    df['place'] = df['PLACE'] + ' - ' + df['STATE']
    df = df.drop(columns = ['PLACE', 'total']) #HAVE PLACE NOW AND DON'T NEED TOTAL - IN OTHER PROCESS
    df.rename(columns={'YEAR':'year'}, inplace=True) #OTHER ONES ARE ALL LOWER CASE - DON'T MESS UP JOIN
    df.rename(columns={'STATE':'state'}, inplace=True)
    
    return df
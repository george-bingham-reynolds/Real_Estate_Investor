import pandas as pd
import numpy as np
import re
import os

always_keep = ['YEAR', 'STATE', 'PLACE']

# MAKING FUNCTION FOR HOME VACANCY CSV PREPROCESSING:
def get_csv(fp, cp):

    
    # GET RID OF NON CODE-LABEL INFO FROM TXT FILE
    lines_to_keep = []
    with open(f"{fp}.txt", "r") as f:

         for line in f.readlines():
             if cp in line:
                 lines_to_keep.append(line)


    with open(f"{fp}_trim.txt", "w") as f:

        for link in lines_to_keep:
            f.write(link)
            
    
    # DROP SUPERFLUOUS INFO FROM DF
    df = pd.read_csv(f"{fp}.csv", encoding = "ISO-8859-1")
    df = df.drop(columns = [x for x in df.columns if x not in always_keep and cp not in x])
    df['YEAR'] = df['YEAR'].astype(str)

    
    # MAKE DICT WITH CODE-LABEL KEY-VALUE PAIRS TO RENAME DF COLUMNS
    col_label_dict = {}

    with open(f"{fp}_trim.txt", "r") as f:
        for line in f.readlines():

            code = line.split(":")[0].lstrip() #SPLIT STRING ON : THEN GET RID LEADING WHITE SPACE

            val = re.sub('/n', '', line.split(":")[1].lstrip().rstrip()) #ASSOCIATED VAL, TRIMMED

            col_label_dict[code] = val
                
    
    # FUNCTION TO REPLACE CODES WITH LABELS
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
       
    df['vacancy_rate'] = df['Vacant']/df['Total']


    # HAVE SUMMARY METRIC WE NEED, SO DROP COLS USED TO DEFINE
    df = df.drop(columns = ['Vacant', 'Total', 'Occupied'])

    # AND NAME THEM FOR EASE-OF-USE
    df.columns = ['year', 'state', 'place', 'vacancy_rate']

    # COMBINE STATE AND CITY (PLACE) FOR 'PLACE' KEY
    df['place'] = df['place'] + ' - ' + df['state']
    
    return df
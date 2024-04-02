import pandas as pd
import numpy as np
import re
import os

always_keep = ['YEAR', 'STATE', 'COUNTY']

# MAKING CLASS FOR HOME CSV PREPROCESSING:
def get_csv(fp, cp):
    lines_to_keep = []
    
    with open(f"{fp}.txt", "r") as f:
        for line in f.readlines():
            if cp in line:
                lines_to_keep.append(line)

    # Write all the links in our list to the file
    with open(f"{fp}_trim.txt", "w") as f:
        for link in lines_to_keep:
            f.write(link)


    # DROP SUPERFLUOUS INFO FROM DF
    df = pd.read_csv(f"{fp}.csv", encoding = "ISO-8859-1")
    df = df.drop(columns = [x for x in df.columns if x not in always_keep and cp not in x])
    df['YEAR'] = df['YEAR'].astype(str)
    
    col_label_dict = {}

    with open(f"{fp}_trim.txt", "r") as f:
        for line in f.readlines():

            code = line.split(":")[0].lstrip() #SPLIT STRING ON : THEN GET RID LEADING WHITE SPACE

            list_of_nums = [re.sub('Lessthan', '', #GET TRIMMED LIST OF NUMS IN LINE
                                   re.sub('ormore', '', 
                                      re.sub(' ', '',
                                          re.sub(',', '', 
                                              re.sub('\$', '', 
                                                 re.sub('\n', '', 
                                                    x.lstrip())))))) for x in line.split(":")[1].split("to") if '0' in x or '9' in x] #AND DROP NON-NUMERIC

            if len(list_of_nums) > 0: #DROP 'TOTAL' COLUMN
                midpoint = round(np.mean([int(x) for x in list_of_nums]))
                col_label_dict[code] = str(midpoint)
            else:
                col_label_dict[code] = 'Total' #TOTAL COL
                
    def relabel(code):
        if code in col_label_dict.keys():
            label = col_label_dict[code]
            return label
        else:
            return code

    # RENAME
    df = df.rename(mapper = relabel, axis = 1)
    df['YEAR'] = df['YEAR'].apply(lambda x: x[-4:] if '-' in x else x)
    
    df['place'] = df['COUNTY'] + ' - ' + df['STATE']
    df = df.drop(columns = ['COUNTY'])
    df.columns = ['year', 'state', 'total_population', 'place']
    
    return df
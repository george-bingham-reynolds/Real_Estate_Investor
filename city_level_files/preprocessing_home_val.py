import pandas as pd
import numpy as np
import re
import os

always_keep = ['YEAR', 'STATE', 'PLACE']

# MAKING FUNCTION FOR HOME CSV PREPROCESSING:
def get_csv(fp, cp, input_type):

    
    # GET RID OF NON CODE-LABEL INFO FROM TXT FILE
    lines_to_keep = []
    with open(f"{fp}.txt", "r") as f:

         for line in f.readlines():
             if cp in line:
                 lines_to_keep.append(line)

    # WRITE A TRIMMED DOWN FILE TO WORK WITH MOVING FORWARD
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
       
        
    # HOME VALUE SPECIFICALLY    
    if input_type == 'home value':
        # NEW COL FOR HOME VAL
        df['average_home_value'] = None

        for i in range(len(df)):
            for col in df.columns:
                if '0' in col: #ONLY LOOK AT VALUE COLUMNS
                    amt = int(col)

                    # AVERAGE PRICE IS SUM OF HOUSEHOLD COUNT * VALUE/TOTAL; 
                    # CAN DIVIDE BY TOTAL HERE AND GET SAME NUMBER
                    df.loc[i, col] = (df.loc[i, col] * amt)/df.loc[i, 'Total']

            # AND NOW SUM IT
            average_price = sum([x for x in df.loc[i].values.tolist() if type(x) == np.float64][1:])
            df.loc[i, 'average_home_value'] = round(average_price, 2) #AND STORE IT


        # HAVE SUMMARY METRIC WE NEED, SO DROP COLS USED TO DEFINE
        df = df.drop(columns = [x for x in df.columns if x == 'Total' or '0' in x])

        # AND NAME THEM FOR EASE-OF-USE
        df.columns = ['year', 'state', 'place', 'average_home_value']

        # COMBINE STATE AND CITY (PLACE) FOR 'PLACE' KEY
        df['place'] = df['place'] + ' - ' + df['state']
    
    return df
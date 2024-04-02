import pandas as pd
import numpy as np
import re
import os

always_keep = ['YEAR', 'STATE', 'COUNTY']


# MAKING CLASS FOR HOME CSV PREPROCESSING:
def get_csv(fp, cp):
    
    # PULL ACTUAL CSV FROM BUCKET
    # command1 = f"gsutil cp gs://pums-data/population/{fp}.csv {fp}.csv"
    # command2 = f"gsutil cp gs://pums-data/population/{fp}.txt {fp}.txt"
    # os.system(command1)
    # os.system(command2)
    
    # GET RID OF NON CODE-LABEL INFO FROM TXT FILE
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
                                                    x.lstrip())))))) for x in\
                            re.sub('With cash rent: ', '', line).split(":")[1].split("to") if '0' in x or '9' in x] #AND DROP NON-NUMERIC


            if len(list_of_nums) > 0: #DROP 'TOTAL' COLUMN
                midpoint = round(np.mean([int(x) for x in list_of_nums]))
                col_label_dict[code] = str(midpoint)
            else:
                col_label_dict[code] = re.sub('With cash rent: ', '', line).split(":")[1].split("to")[0][:-1].lstrip()

    def relabel(code):
        if code in col_label_dict.keys():
            label = col_label_dict[code]
            return label
        else:
            return code

    # RENAME
    df = df.rename(mapper = relabel, axis = 1)
    df = df.drop(columns = ['Total', 'No cash rent'])
    df.rename(columns={'With cash rent':'Total'}, inplace=True)
    # FOR MULTI-YEAR JUST PULL LAST YEAR
    df['YEAR'] = df['YEAR'].apply(lambda x: x[-4:] if '-' in x else x)
    
    
    
    # NEW COL FOR RENT VAL
    df['average_rent'] = None

    for i in range(len(df)):
        for col in df.columns:
            if re.search(r'[0-9]', col): #ONLY LOOK AT VALUE COLUMNS
                amt = int(col)

                # AVERAGE REN IS SUM OF HOUSEHOLD COUNT * VALUE/TOTAL; 
                # CAN DIVIDE BY TOTAL HERE AND GET SAME NUMBER
                df.loc[i, col] = (df.loc[i, col] * amt)/df.loc[i, 'Total']

        # AND NOW SUM IT
        average_price = sum([x for x in df.loc[i].values.tolist() if type(x) == np.float64][1:])
        df.loc[i, 'average_rent'] = round(average_price, 2) * 12 #AND STORE IT/ANNUALIZE


    # HAVE SUMMARY METRIC WE NEED, SO DROP COLS USED TO DEFINE
    df = df.drop(columns = [x for x in df.columns if re.search(r'[0-9]', x) or x == 'Total'])

    # AND NAME THEM FOR EASE-OF-USE
    df.columns = ['year', 'state', 'county', 'average_annual_rent']

    # COMBINE STATE AND COUNTY FOR 'PLACE' KEY
    df['place'] = df['county'] + ' - ' + df['state']
    df = df.drop(columns = ['county'])
    
    return df
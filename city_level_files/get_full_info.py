# IMPORT UPSTREAM PACKAGES
import get_rental_income
import get_home_val
import get_total_pop
import get_income
import get_race
import get_sex_age
import get_vacancy

# PULL EACH INDIVIDUAL DF FROM UPSTREAM PACKAGE
df_rent = get_rental_income.df_rent
df_home_val = get_home_val.df_home_val
df_pop = get_total_pop.df_pop
df_inc = get_income.df_inc
df_race = get_race.df_race
df_sex_age = get_sex_age.df_sex_age
df_vac = get_vacancy.df_vac

# MERGE TOGETHER FOR FULL DATAFRAME
df = df_rent.merge(right = df_home_val, on = ['year', 'place', 'state'], how = 'inner')
df = df.merge(right = df_pop, on = ['year', 'place', 'state'], how = 'inner')
df = df.merge(right = df_inc, on = ['year', 'place', 'state'], how = 'inner')
df = df.merge(right = df_race, on = ['year', 'place', 'state'], how = 'inner')
df = df.merge(right = df_sex_age, on = ['year', 'place', 'state'], how = 'inner')
df = df.merge(right = df_vac, on = ['year', 'place', 'state'], how = 'inner')

# SPLIT OUT YEARS TOO RECENT TO HAVE 3 YEARS LATER DATA (THIS IS TIMEFRAME FOR ROI PREDS LATER)
df_realtime = df[df['year'] > 2019]

df = df.dropna() #NOTE THAT THIS WILL DROP ANYTHING FROM DF_REALTIME

# DEFINE ROI AS (MONEY MADE ON RENT + HOME VALUE APPRECIATION)/(ORIGINAL HOME VALUE)
# RENT AND APPRECIATION IN THREE ARE DEFINED UPSTREAM
df['money_made'] = df['three_year_growth'] + df['rent_in_three']
df['roi'] = df['money_made'] / df['average_home_value']
df = df.drop(columns = ['money_made', 'rent_in_three', 'three_year_growth'])

df['roi'] = df['roi'].apply((lambda x: round(x, 4)))
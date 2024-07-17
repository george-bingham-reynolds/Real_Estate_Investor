# Real_Estate_Investor

This project contains a virtual Real Estate Investor as the end product, with a queryable API containing predictions for return on investment for real estate purchases. The general flow of the repo is laid out below from upstream work to downstream. Natural sections for consideration are titled. Please note that I am not an investment advisor, and no purchases should be made based on predictions.


## Data
All data is originally from Census Publice Use Microsample (PUMS) data, pulled from here: https://data2.nhgis.org/. I have pulled data grouped on two different geographic levels - Census Counties and Census Place. Counties are fairly self-explanatory, and place is a level below. This includes things like cities or municipalities. Moving forward I reference this as city-level. 

For county-level data I use 5-year data for 2009, 2010 and 2020. Otherwise I use 1-year data. 1-year data is not feasible for city-level analysis, as the Census redacts some information on this level out of privacy concerns for individuals (there are few enough observations on this level to risk identification), so on this front all data is 5-year PUMS. 

I pull data for total population, population sizes by race, population sizes by age and sex, rental costs, vacancy, home values and household income. While far from exhaustive, this set of information seems sufficient for a first pass at modeling out housing markets.

All data is pulled for years 2009-2022.

## Data Preprocessing
Data preprocessing varies by dataset but generally follows the same basic process, described below. 

The first stage of preprocessing comes with the set of python files with the prefix preprocessing_. The suffix (e.g. income) describes the dataset to which it applies. I describe their function here.

PUMS CSVs have accompanying txt codebooks, in which they give the code pattern used for population information. For example, city-level household income used the pattern "AFJ8" in 2016. In addition, they supply a list of which iteration of the code pattern belongs to which bucket of people. For example, in the same dataset, AFJ8E009 applies to households making $40,000 to $44,999. The CSV then gives population sizes for each bucket for a given area, with the buckets labeled with the code pattern iteration. In the set of python files with the prefix preprocessing_, I pull these values from each year's respective codebook and create a dictionary with keys equal to code pattern iterations. Values are equal to formatted versions of the accompanying group. In the case of categorical variables (e.g. age by sex) it remains a plain string; in the event of continuous variable bucketing (e.g. income) I convert the string to the two numbers and take the midpoint. Categoricals are converted to percentages by dividing the number of people in the group by the total population. For numerical buckets I get average outcome for the area by multiplying the bucket midpoint by the number of people in the bucket and dividing the total sum of these values by population. For example, if 100 households make betwen $40,000 and $44,999 and another 100 make between $45,000 and $49,999 (and these represent all households), I define the average income for that area as ((100 * (40,000 + 44,999)/2) + (100 * (45000 + 49999)/2))/200 = 44,999.5.

The output of these files flows into their corresponding (as noted by suffix) get_ file. The first part of this file pulls in all dataframes for individual years and concatenates them into a single dataframe. For continuous variable datasets (e.g. income, rental costs), there is additional code to define growth over the last 1, 2 and 3 years. Imputation methodology is described within the file comments.

Home value and rental costs warrant additional consideration. Home value has, in addition to the growth rates defined, a future-looking 3-year growth rate defined. In addition, the rent dataframe has a variable for total rent paid over the next three years.

Finally, get_full_info.py pulls all information together. First, it merges all dataframes into one, resulting in a dataframe with full information across datasets tied to a place-year combination. This is then split into two dataframes - one for which three-year return on investment can be defined, and ones too recent for this (e.g. the year 2020 cannot be in the former, as 2023 data was not available). Lastly, ROI is defined for the former dataframe. This is set equal to (rent paid over the three year period + home value growth over the next three years)/(average home value). The idea is that this will capture average home value appreciation, add it to average rent paid (equivalent to average rent received by an owner renting out) and divided by average cost of the initial purchase.

## Predictive Modeling
There are two notebooks for each set of predictions - Hyperperameter_Tuning and Model_Dev. The former uses time series splits for cross-validated hyperparamter tuning for Random Forest, Adaboost and XGBoost regressors. Each is tested both with and without Kernel Principal Component Analysis due to the fairly high dimensionality of the data, with the more performant of the two sets of parameters being stored and passed on to Model_Dev. Note that while the county-level dataframe used is small enough for simple git uploads, the city-level one is not. As such, the former simply uses the csv, but the latter generates the csv from scratch. This is a lengthy process, so expect a long runtime.

Within Model_Dev some basic EDAV is performed and model performances compared. Ultimately, the most performant model on validation data is used to make predictions on 2022 data and saved in a CSV format to be used in the API section of code.

## API
The API itself is built primarily using Flask, Marshmallow and SQLAlchemy. Key files are those within the Resources and Models folders, as well as app.py, db.py, requirements.txt and and schemas.py. Please note that while the Dockerfile was included for potential future iterations of the project it is not used in the current version. 

Next, simply open the Start_API notebook and run the first cell in order to start up the app. 

Lastly, City_API_Walkthrough and County_API_Walkthrough are essentially the same but set up for the separate geographic levels for predictions. Each posts its corresponding dataframe to the API, has a few cells to read in info on any city/county of the users choice, and then cells to delete all records after using it.

## Potential Next Steps
While the project is finished for its current iteration, there are several potential areas of future improvement. The first is updating the data being used, as there are many potential sources of signal not being used currently. Next would be greater model developement (e.g. there currently are issues of overfitting present), and lastly further development of the API to rely on Docker and to be deployed rather than needing to be started up would be the top priorities. In the meantime, the repo contains a workable end-to-end virtual real estate investor.

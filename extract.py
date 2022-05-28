 
# THIS PROGRAM WILL EXTRACT SOME WORLD BANK PROJECT DATA SETS,  TRANSFORM AND MERGE 
       # AND THEN LOAD THESE MERGED DATA INTO A TARGET DATABASE. 


import pandas as pd

# CONNECT to target Postgres database through SQLAlchamey
import pandas as pd
from allconfigs.configs import psql_config   #foldername.filemane import function_name
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

engine_target=create_engine(
    str(
        URL.create(
            drivername=psql_config['postgres']['drivername'],
            host=psql_config['postgres']['host'],
            port=psql_config['postgres']['port'],
            database=psql_config['postgres']['database'],
            username=psql_config['postgres']['user'],
            password=psql_config['postgres']['password']
        )
  )
)
connection = engine_target.connect()

# TEST_ connection1
query= "SELECT DISTINCT tablename FROM pg_catalog.pg_tables WHERE pg_tables.schemaname='public';"  # BE CAREFUL CASE-SENSITIVE!!!
df=pd.read_sql(sql=query,con=engine_target)
table_names=list(df.tablename)
table_names


            
#CONVERT CSV FILES into Dataframe format.  
#during convertions, some problems occured, adding encoding and skiprows 
# of parameters have solved it.

pd.set_option("display.max_rows", 250)
df_bankProjects=pd.read_csv('World_Bank_Projects.csv',encoding='ISO-8859-1',skiprows=2)
df_bankProjects.shape


#CLEAN DATAFRAMES
# NaN rows are removed under 'countryname' column
# Remove duplicate rows  under 'countryname' column with df.dropna 

pd.set_option('max_columns', None)
df_worldPopulation=pd.read_csv('World_population.csv',skiprows=3)
df_worldPopulation.dropna(subset = ['Country Name'])
df_worldPopulation.drop_duplicates( subset= 'Country Name') 

df_GDP=pd.read_csv('GDP.csv')
df_GDP.drop_duplicates( subset= 'Country Name') 
df_GDP.dropna(subset = ['Country Name'])

# MERGE TWO  'World Bank Data Set' based on 'Country Name' column  with pd.merge() function
# pd.merge(frame_1, frame_2, left_on='county_ID', right_on='countyid') if column names are not the same
df_populationGDP = pd.merge(df_worldPopulation, df_GDP, how='inner', on='Country Name')

#GET RID OF unnecessary columns
df_populationGDP.drop(['2021', 'Unnamed: 66'], axis=1)


# bring all transformed dataframes here.
df_bankProjects=pd.read_csv('World_Bank_Projects.csv',encoding='ISO-8859-1',skiprows=2)

df_worldPopulation=pd.read_csv('World_population.csv',skiprows=3)
df_worldPopulation.dropna(subset = ['Country Name'])
df_worldPopulation.drop_duplicates( subset= 'Country Name') 

df_GDP=pd.read_csv('GDP.csv')
df_GDP.drop_duplicates( subset= 'Country Name') 
df_GDP.dropna(subset = ['Country Name'])

df_populationGDP = pd.merge(df_worldPopulation, df_GDP, how='inner', on='Country Name')

df_populationGDP.drop(['2021', 'Unnamed: 66'], axis=1)



#SAVE the MERGED DF AS CSV file under the project
df_populationGDP.to_csv('populationGDP_merged.csv')



# LOAD THE DATAFRAMES/MERGED DATAFRAMES TO TARGET DB.
df_bankProjects.to_sql('world_bank_projects', con=engine_target,if_exists='replace')
df_populationGDP.to_sql('population_GDP', con=engine_target,if_exists='replace')


#test_connection2
query= "SELECT DISTINCT tablename FROM pg_catalog.pg_tables WHERE pg_tables.schemaname='public';"  # BE CAREFUL CASE-SENSITIVE!!!
df=pd.read_sql(sql=query,con=engine_target)
table_names=list(df.tablename)
table_names





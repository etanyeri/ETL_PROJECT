#%%

import pandas as pd
import matplotlib 
from matplotlib import pyplot as plt


# GET ALL DATAFRAMES READY.
df_bankProjects=pd.read_csv('World_Bank_Projects.csv',encoding='ISO-8859-1',skiprows=2)

df_worldPopulation=pd.read_csv('World_population.csv',skiprows=3)
df_worldPopulation.dropna(subset = ['Country Name'])
df_worldPopulation.drop_duplicates( subset= 'Country Name') 

df_GDP=pd.read_csv('GDP.csv')
df_GDP.drop_duplicates( subset= 'Country Name') 
df_GDP.dropna(subset = ['Country Name'])

df_populationGDP = pd.merge(df_worldPopulation, df_GDP, how='inner', on='Country Name')


#  DECIDE WHICH TWO COLUMNS WILL BE COMPARED
plt.title('country pop')
plt.plot(df_populationGDP['Country Name'], df_populationGDP['1961'])
plt.show()




# %%

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 15:37:25 2021

@author: Lutz
"""

import pandas as pd

base_path='C:/Users/Lutz/Desktop/Data Science/Politics/cleaned_polls/'
file_ending='.csv'

list_of_csv_files=['allensbach', 'dimap', 'emnid', 'forsa', 'gms', 'insa', 'politbarometer', 'yougov']


list_of_dfs=[]

for i in list_of_csv_files:
    df=pd.read_csv(base_path+i+file_ending)
    list_of_dfs.append(df)
    
    
df_combined=pd.concat(list_of_dfs)

df_combined=df_combined.sort_values(by = 'DATUM')
df_combined.reset_index(inplace=True, drop= True)

df_combined.loc[(df_combined['BUNDESTAGSWAHL']== True), 'INSTITUT']='BUNDESTAGSWAHL'

df_combined.loc[(df_combined['DATUM']== '1998-09-27'), 'SONSTIGE']=5.9
df_combined.loc[(df_combined['DATUM']== '2009-09-27'), 'SONSTIGE']=6.0
df_combined.loc[(df_combined['DATUM']== '2013-09-22'), 'SONSTIGE']=6.2
df_combined.loc[(df_combined['DATUM']== '2017-09-24'), 'SONSTIGE']=5.0

df_combined.drop('NICHTWÄHLER/UNENTSCHL.', axis=1, inplace=True)


df_combined.drop_duplicates(keep='first',inplace=True)

df_combined.drop([127], axis=0, inplace=True)

df_combined.reset_index(inplace=True, drop= True)
df_combined.drop(list(range(4541,4566)), axis=0, inplace=True)
df_combined.reset_index(inplace=True, drop= True)




df_combined.to_csv('C:/Users/Lutz/Desktop/Data Science/Politics/cleaned_polls/combined_historical_poll_data.csv', index=False)
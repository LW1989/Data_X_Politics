# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 15:51:22 2021

@author: Lutz
"""

import pandas as pd 
from datetime import date


old_file_path='C:/Users/Lutz/Desktop/Data Science/Politics/cleaned_polls/combined_historical_poll_data'
historical_data=pd.read_csv(old_file_path + '.csv')

historical_data['DATUM']=pd.to_datetime(historical_data['DATUM'], errors='coerce', format='%Y-%m-%d')


base_url_allensbach='https://www.wahlrecht.de/umfragen/index.htm'
        

new_data=pd.read_html('https://www.wahlrecht.de/umfragen/index.htm')
new_data=new_data[1]
new_data_transposed=new_data.T

new_data_transposed.drop(['Unnamed: 1','Unnamed: 10'], axis=0, inplace=True)

institute_list=list(new_data_transposed.index)[1:9]


new_data_transposed.columns=list(new_data_transposed.iloc[0,:])
new_data_transposed.drop(['Institut', 'Bundes-tagswahl'], axis=0, inplace=True)
new_data_transposed['Institut']=institute_list
institut_dict={'Forsch’gr.Wahlen':'POLITBAROMETER','Allensbach':'ALLENSBACH','Forsa':'FORSA','Kantar(Emnid)':'EMNID', \
               'Infratestdimap':'DIMAP', 'yougov':'YOUGOV'}
    
new_data_transposed.replace(institut_dict, inplace=True)

new_data_transposed.rename(columns={'Veröffentl.':'Datum', 'DIE LINKE':'LINKE', 'Erhebung':'Befragte'}, inplace=True)
new_data_transposed.columns=new_data_transposed.columns.str.upper()

new_data_transposed['BEFRAGTE']=new_data_transposed['BEFRAGTE'].str.replace(r'[TOMF]* • ', '', regex=True)

for i in new_data_transposed.loc[:,'CDU/CSU':'SONSTIGE']:
    new_data_transposed[i]=new_data_transposed[i].str.replace(',', '.').str.replace('%','').astype('float')
    

new_data_transposed['DATUM']=pd.to_datetime(new_data_transposed['DATUM'], errors='coerce', format='%d.%m.%Y')
    
new_data_transposed['BEFRAGTE']=new_data_transposed['BEFRAGTE'].str.replace(r'[0-9]{2}\.[0-9]{2}\.\–[0-9]{2}\.[0-9]{2}\.', '', regex=True)
new_data_transposed['BEFRAGTE']=new_data_transposed['BEFRAGTE'].str.replace(r'.', '', regex=True).astype('float')
new_data_transposed.sort_values(by = 'DATUM', inplace=True)
new_data_transposed.reset_index(inplace=True, drop= True)
new_data_transposed['BUNDESTAGSWAHL']=False


new_data_append=new_data_transposed.copy()

for it_count,i in enumerate(new_data_transposed['DATUM']):
    if i in historical_data['DATUM'].unique():
        new_data_append.drop([it_count], axis=0, inplace=True)
        
        
new_data_append_end=pd.concat([historical_data, new_data_append], ignore_index=True)
new_data_append_end.sort_values(by = 'DATUM', inplace=True)
new_data_append_end.reset_index(inplace=True, drop= True)



today = date.today()

date_str = '_' + (today.strftime("%d_%m_%Y")) 
new_data_append_end.to_csv(old_file_path + date_str + '.csv', index=False)
    







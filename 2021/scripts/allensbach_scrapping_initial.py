# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 15:46:10 2021

@author: Lutz
"""

import pandas as pd
import numpy as np

base_url_allensbach='https://www.wahlrecht.de/umfragen/allensbach'
sub_url_years=['/2002', '/2005', '/2009','/2013', '']

list_of_df=[]

for i in sub_url_years:
    url=base_url_allensbach + i + '.htm' 
    dfs = pd.read_html(url)
    for ii in dfs:
        if hasattr(ii, 'columns'):
            if 'SPD' in ii.columns:
                list_of_df.append(ii)
        

for x in list_of_df:
    x.dropna(thresh=20, axis=1, inplace=True)
    x.rename(columns={'Unnamed: 0':'Datum', 'PDS':'LINKE', 'Linke.PDS':'LINKE', 'Zeitraum':'Bundestagswahl'}, inplace=True)
    
    
allensbach_concat=pd.concat(list_of_df, ignore_index=True)
allensbach_concat.columns=allensbach_concat.columns.str.upper()
allensbach_concat.drop(['REP','PIRATEN'],axis=1, inplace=True)
allensbach_concat.drop([65,108, 109, 163, 164, 218, 219, 314, 315, 316],axis=0, inplace=True)


allensbach_concat['BUNDESTAGSWAHL']=allensbach_concat['BUNDESTAGSWAHL']=='Bundestagswahl' 

allensbach_concat['DATUM']=pd.to_datetime(allensbach_concat['DATUM'], errors='coerce', format='%d.%m.%Y')

removal_list=['-','–','?','Bundestagswahl','']

for i in removal_list:
    allensbach_concat.replace(i, np.nan, inplace=True)
    

# allensbach_concat.replace('-', np.nan, inplace=True)
# allensbach_concat.replace('–', np.nan, inplace=True)
# allensbach_concat.replace('?', np.nan, inplace=True)
# allensbach_concat.replace('Bundestagswahl', np.nan, inplace=True)
# allensbach_concat.replace('', np.nan, inplace=True)
    
parties=['CDU/CSU', 'SPD', 'GRÜNE', 'FDP', 'LINKE', 'AFD', 'SONSTIGE'] 

for i in parties:
    allensbach_concat[i]=allensbach_concat[i].str.replace(',','.').str.replace('%','').str.replace('PIR 2.2 Sonst. 4.0','6.2').astype('float')
    
allensbach_concat['BEFRAGTE']=allensbach_concat['BEFRAGTE'].str.replace('>', '').str.replace('≈','').str.replace('.','')
    
allensbach_concat['BEFRAGTE'] = allensbach_concat['BEFRAGTE'].str.replace('?','')
allensbach_concat.replace('', np.nan, inplace=True)
allensbach_concat['BEFRAGTE'] = allensbach_concat['BEFRAGTE'].astype('float')
allensbach_concat['BEFRAGTE'][allensbach_concat['BEFRAGTE']<500]= np.nan

allensbach_concat['INSTITUT']='ALLENSBACH'

allensbach_concat=allensbach_concat.sort_values(by = 'DATUM')
allensbach_concat.reset_index(inplace=True, drop= True)
allensbach_concat.drop([63,106,159,213],axis=0, inplace=True)
allensbach_concat.reset_index(inplace=True, drop= True)


allensbach_concat.to_csv('C:/Users/Lutz/Desktop/Data Science/Politics/cleaned_polls/allensbach.csv', index=False)
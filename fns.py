# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 18:28:03 2017

@author: dcockbur
"""

#%%
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dictionaries import replacedic, replacereaddic, nonprodlist
import fns 

#%%


def folderdata(folder):
    def make_file_list(path):
        newlist = []
        nonelist = [f for f in os.listdir(path) if f.endswith('.csv')]
        for item in nonelist:
            newlist.append(item)
        return newlist
    
    filelist = make_file_list(folder)
    
    list_=[]
    
    for file_ in filelist:
        df = pd.read_csv(folder+'\\'+file_, dtype='object')
        list_.append(df)
    frame = pd.concat(list_)
    return frame

#%%
def adjustframe1(frame):
    
    frame.replace('-', np.nan, inplace=True) # Replace - with nans
    frame['Age'] = pd.to_numeric(frame['Age']) # Make age column numeric
    frame  = frame[frame['Age'] > 9] # Remove anyone below 10 for illeteracy and of course kids alive

    frame.replace({'Religion':replacedic}, inplace = True)
    religions = frame['Religion'].value_counts()[0:11].index.values
    #print(religions)
    frame = frame[frame['Religion'].isin(religions)]
    frame['Religion'].value_counts()[0:24]
    return frame

#%%
def adjustframelit(frame):
    # Create list of most repeating literacy values
    lala = frame['Literacy'].value_counts() 
    staylist = [lala.index.values[i] for i in range(len(frame['Literacy'].value_counts())) if lala.iloc[i] > 500]
    
    framelit = frame[frame['Literacy'].isin(staylist)]
    framelit.replace({'Literacy':replacereaddic}, inplace = True)
   
    framelit = framelit[framelit['Literacy'] != '-'] #remove the non values for lit      
#    frame['Literacy'].value_counts()[0:24]
    framelit = framelit.groupby(['Religion', 'Literacy']).Street.count() #keeping different religions, frame 2 for later graphs
    
    rellist = list(framelit.index.get_level_values(0).unique())
    prodlist = list([x for x in rellist if x not in nonprodlist])
    prodlistdic = dict(zip(prodlist[::1],['Protestant']*len(prodlist)))
    
    framelit = framelit.reset_index()
    framelit.replace({'Religion': prodlistdic}, inplace=True)
    framelit = framelit.groupby(['Religion', 'Literacy']).Street.sum()
    framelit = framelit.rename('Count').to_frame().unstack(level=0).transpose()
    framelit.index = framelit.index.droplevel(level=0)
    framelit = framelit.transpose().iloc[::-1]
    try:
        del framelit['Jewish']
    except:
        pass
    return framelit


#%%
    
def adjustframekid(frame):
    frame = frame[frame['Children Born'].notnull()]
    frame['Children Living'].fillna(0, inplace=True)
    frame = frame.groupby(['Religion', 'Children Born', 'Children Living']).Street.count()
    
    rellist = list(frame.index.get_level_values(0).unique())
    prodlist = list([x for x in rellist if x not in nonprodlist])
    prodlistdic = dict(zip(prodlist[::1],['Protestant']*len(prodlist)))
    
    frame = frame.reset_index()
    frame.replace({'Religion': prodlistdic}, inplace=True)
    frame['Children Living'] = pd.to_numeric(frame['Children Living'])
    frame['Children Born'] = pd.to_numeric(frame['Children Born'])  

    frame.rename(columns={'Street': 'Count'}, inplace = True)
    #Test veracity of the %, not sure if I believe it or doing something wrong...
    
    frame['perclivingx'] = frame['Children Living']*frame['Count'] / frame['Children Born']
    count = frame.groupby('Religion').Count.sum()
    percliving = frame.groupby('Religion').perclivingx.sum()
    jaysus = percliving / count
    #percliving.head(10)
    jaysus = jaysus.rename('Percentage Living').to_frame()
    jaysus['Percentage Dead'] = 1 - jaysus['Percentage Living']
    jaysus = jaysus.transpose()
    try:
        del jaysus['Jewish']
    except:
        pass
    return jaysus

#%%
    
def makepie(data, county):
    pie = plt.figure()
    #.plot(kind='pie', subplots=True, figsize=(12,6), layout =(1,2))
    pie.suptitle(county, fontsize = 20, color = 'darkred')
    #plt.tight_layout()
    pie.subplots_adjust(bottom = 0.05) #Move plots and their titles lower
    for i in range(len(data.columns)):
        ax = plt.subplot(1,2,i+1)
        title = str(data.columns.values[i])
        labels = list(data.index.values)
        ax.pie(data[title], startangle = 90, shadow=True)
        ax.axis('equal')
        ax.set_title(title)
        ax.legend(labels,loc='lower center')
        ttl = ax.title
        ttl.set_position([0.5, 0.82]) #Set titles to centre and down a bit (default is 1?)
    return pie

    

#%%
    

#%%
    

#%%










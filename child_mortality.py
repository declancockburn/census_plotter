# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 16:08:11 2017

@author: dcockbur
"""
"""
Python Data analysis project
Religion in Wicklow?


"""

"""
Research Question: 

For Wicklow vs. Antrim i 1911

Total mumber of Children for Catholics
Children living %
Literacy rate of catholics > 10

Total number of Children for Protestants
Children living %
Literacy rate of Children > 10

Hypothesis:
In 1911, Leinster Protestants in (Wicklow as a sample) were significantly 
more socio-economically advantaged than Catholics in the same area),
    
AND Ulster protestants (Antrim as a sample) were far socio-economically equivalent 
to their Catholic neighbours.

Metric:
    Total children, % of children living, and literacy will be used.
    
Null hypthosis 1: No difference between Catholics and protestants
Null hypthosis 2: Difference between catholics and protestants but not between leinster and Ulster
 
4.2 update:
Make it so that it works on folders in python anywhere, and names graphs after folder.
Tidy up functions.

"""

#%%

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from dictionaries import replacedic, replacereaddic, nonprodlist
import fns 
import re


#%%
# Make a list of only directories
onlydirs = [x for x in os.listdir() if not os.path.isfile(x)]
regex = re.compile('^[a-zA-Z0-9]')

onlydirs = [x for x in onlydirs if regex.search(x)]
litlist = []
kidlist = []



#%%
for i in range(0,len(onlydirs)):
    county = onlydirs[i]
    litname = str(county) + '_literacy.png'
    kidname = str(county) + '_childmort.png'
    # Function to import all data from a folder into a dataframe
    frame = fns.folderdata(county)
    # Adjust the frame, removes age below 10, cleans up religions
    frame = fns.adjustframe1(frame)
    #Adjust the frame: reduce incidences of literacy to only the most common stated, remove unstated values i.e. '-', 
    # and groupby only Religion and Literacy.
    # Then Make a list of the non catholic religions, and a dictionary to rename them protestant.
    # Get list of just Catholics and Prods lit and illit
    framelit = fns.adjustframelit(frame)
    #Strip it down to just catholics and protestants, average ratio of kids living to dead per adult w/ kids.
    jaysus = fns.adjustframekid(frame)
    #Make lists of frames
    litlist.append(framelit)
    kidlist.append(jaysus)
    
#    #Plot pie-chart
#    pie = fns.makepie(framelit, county)
#    pie.savefig(litname)
#    #and plot kids living to dead
#    pie2 = fns.makepie(jaysus, county)
#    pie2.savefig(kidname)
    
litframe = pd.concat(litlist, keys = onlydirs[0:len(litlist)])
kidframe = pd.concat(kidlist, keys = onlydirs[0:len(kidlist)])

#litframe.index.replace(['County3' if x=='County1' else x for x in litframe.index.get_level_values(0)])
#litframe

#%%

counties = onlydirs#list(litframe.index.get_level_values(0).unique())

print(counties)
print(list(litframe.index.get_level_values(0).unique()))
litframe = litframe.transpose()
for val in counties:
    litframe[val, 'percil'] = litframe[val, 'Illiterate']*100 / (litframe[val, 'Illiterate'] + litframe[val, 'Literate'])

litframe = litframe.sort_index(axis=1) 
litframe = litframe.transpose()
litframeperc = litframe.loc[(slice(None), 'percil'),:]

#%%
kidframedead =  kidframe.loc[(slice(None),'Percentage Dead'),:]*100




#%%
#fig, ax = plt.subplots()
counties = ['County3' if x=='County1' else x for x in counties]
plt.figure(1)
plt.style.use('seaborn')
ax=plt.gca()
colors = ['green','darkorange']
kidframedead.plot(kind='bar', ax=ax, color=colors)
ax.set_xticklabels(kidframedead.index.get_level_values(0), rotation=30, ha='right')
#ax.set_xticklabels(counties, rotation=30, ha='right')
ax.set_ylabel('Child Mortality Rate\n (avg % per parent)', fontsize=15)
ax.set_xlabel('County', fontsize=15)
ax.legend(loc='best', frameon=True, framealpha=0.85, fancybox=True, shadow=True, facecolor=(1,1,1,1))
ax.set_title('Child Mortality Rates in Ireland in 1911\n', fontsize=18)
plt.tight_layout()
plt.savefig('Child_Mortality.png')

#plt.xticks(index + bar_width / 2, ('A', 'B', 'C', 'D', 'E'))


#%%

plt.figure(2, figsize=(10,7.5))
plt.style.use('seaborn')
ax=plt.gca()
colors = ['green','darkorange']
litframeperc.plot(kind='bar', ax=ax, color=colors)
#kidframedead.plot(kind='bar', ax=ax)
ax.set_xticklabels(litframeperc.index.get_level_values(0), rotation=30, ha='right')
ax.set_ylabel('Percentage Illiterate adults \n (adults = 10 or older)', fontsize=15)
ax.set_xlabel('County', fontsize=15)
ax.legend(loc='best', frameon=True, framealpha=0.85, fancybox=True, shadow=True, facecolor=(1,1,1,1))
ax.set_title('Illiteracy in Ireland in 1911\n', fontsize=18)
plt.tight_layout()
plt.savefig('Illiteracy.png')




#%%

#print(plt.style.available)


#%%
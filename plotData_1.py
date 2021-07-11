# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 14:39:34 2020

@author: Azadeh Haji
"""
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from os import path as osp
#import seaborn as sns
#sns.set(style="whitegrid")

study='FoodReg3'
# plot taste and health weights on choice=
choiceBetas = pd.read_csv('RegBetas_Choice.csv')
#get rid of the Unnamed column
choiceBetas = choiceBetas.drop(choiceBetas.columns[0],axis=1)
#get rid of - in column labels to be possible to call
cols = list(choiceBetas.columns)
for c in range(len(cols)):
    cols[c] = cols[c].replace('-','')
choiceBetas.columns = cols

#[cols[c] = cols[c].replace('-','') for c in range(len(cols))]
condsOld = ['Nat','Hlt','Dsr']
condsNew = ['NATURAL','HEALTH','DISTANCE']
attsOld  = ['Taste','Health']
attsNew  = ['Tastiness','Healthiness']
colors   = ['royalblue','salmon','gold']
fig, ax = plt.subplots()
width = .4
x = np.asarray([0,2])
dist = [-1,0,1]
for c in range(len(condsNew)):
    y = list()
    ysd = list()
    [y.append(np.mean(choiceBetas[condsOld[c]+attsOld[a]])) for a in range(len(attsOld))]
    [ysd.append(np.std(choiceBetas[condsOld[c]+attsOld[a]])/np.sqrt(choiceBetas.shape[0])) for a in range(len(attsOld))]
    att = ax.bar(x+np.asarray(dist[c])*width,y,width,label =condsNew[c],color=colors[c])
    att = ax.errorbar(x+np.asarray(dist[c])*width,y,yerr=ysd,ecolor='k',fmt='none')

ax.set_ylabel('choice betas',fontdict={'fontsize':16,'fontweight': 'bold'})
ax.set_title(study+ ', N='+str(choiceBetas.shape[0]),fontdict={'fontsize':20,'fontweight': 'bold'})
ax.set_xticks(x)
ax.set_xticklabels(attsNew,fontdict={'fontsize':14,'fontweight': 'bold'})
#remove top frame border
ax.spines['top'].set_visible(False)
#remove right frame border
ax.spines['right'].set_visible(False)
plt.legend(fontsize = 12, prop = {'weight':'bold'},frameon=False)
# ax.grid(b=None)
plt.show()

savefile = osp.join('Figures','choiceBetas.png')
fig.savefig(savefile)

#ax.set_yticklabels(ax.get_yticklabels,fontdict={'fontsize':12,'fontweight': 'bold'})
                   

# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:54:53 2019
Finds the regression betas for tastiness and healthiness on choice
@author: hajih
"""
import pandas as pd
import numpy as np
import os
import sys

from sklearn.linear_model import LinearRegression

def calcRegression(path2csv,RegBetascsv,xcludeFile,inst,DV):
    
    dirList = os.listdir(path2csv)
    
    xclude =pd.read_csv(xcludeFile)
    xclude = xclude.to_dict()
    
    if ' ' in inst[0]:
        shortInst = ['Nat','Hlt','Dsr']
    else:
        shortInst = inst
    if DV == 'Choice':    
        RegBetas ={'Subject':[],shortInst[0]+'-Taste':[],shortInst[0]+'-Health':[],\
                 shortInst[1]+'-Taste':[],shortInst[1]+'-Health':[],\
                 shortInst[2]+'-Taste':[],shortInst[2]+'-Health':[]}
    elif DV == 'Liking':
        RegBetas ={'Subject':[],shortInst[0]+'-Taste-pre':[],shortInst[0]+'-Health-pre':[],\
                 shortInst[1]+'-Taste-pre':[],shortInst[1]+'-Health-pre':[],\
                 shortInst[2]+'-Taste-pre':[],shortInst[2]+'-Health-pre':[],\
                 shortInst[0]+'-Taste-post':[],shortInst[0]+'-Health-post':[],\
                 shortInst[1]+'-Taste-post':[],shortInst[1]+'-Health-post':[],\
                 shortInst[2]+'-Taste-post':[],shortInst[2]+'-Health-post':[]}
    elif DV == 'RT' :
        RegBetas ={'Subject':[],shortInst[0]+'-Taste':[],shortInst[0]+'-Health':[],\
                 shortInst[1]+'-Taste':[],shortInst[1]+'-Health':[],\
                 shortInst[2]+'-Taste':[],shortInst[2]+'-Health':[]}

    else:
        sys.exit("DV not recognized. Must be 'Choice','Liking' or 'RT'") 
    
    for s in range(len(dirList)):
        if xclude['ByChoice'][s] == 1 and xclude['ByRating'][s] == 1: # check that they aren't excluded
            print (dirList[s])
            data = pd.read_csv(path2csv+dirList[s])
            RegBetas['Subject'].append(int(dirList[s][:len(dirList[s])-4]))

            for ins in shortInst:
                X       = np.zeros((len(data.Trial[data.Instruction == inst[shortInst.index(ins)]]),2))
                X[:,0]  = data.Taste[data.Instruction == inst[shortInst.index(ins)]]
                X[:,1]  = data.Health[data.Instruction == inst[shortInst.index(ins)]]
 
                if DV == 'Choice':
                    Y       = data.Choice[data.Instruction == inst[shortInst.index(ins)]]
                    whichTr = [list(~np.isnan(X[:,0]))[t]  and list(~np.isnan(X[:,1]))[t] and\
                    list(~np.isnan(Y))[t] for t in range(len(Y))]
                    
                    if any(whichTr):
                        Y = Y[whichTr]
                        X = X[whichTr,:]
                
                        reg      = LinearRegression().fit(X,Y)
                        RegBetas[ins+'-Taste'].append(reg.coef_[0])
                        RegBetas[ins+'-Health'].append(reg.coef_[1])
                elif DV == 'Liking':
                    Y1       = data.preLiking[data.Instruction == inst[shortInst.index(ins)]]
                    whichTr = [list(~np.isnan(X[:,0]))[t]  and list(~np.isnan(X[:,1]))[t] and\
                    list(~np.isnan(Y1))[t] for t in range(len(Y1))]
                    
                    if any(whichTr):
                        Y1 = Y1[whichTr]
                        X1  = X[whichTr,:]
                        reg      = LinearRegression().fit(X1,Y1)
                        RegBetas[ins+'-Taste-pre'].append(reg.coef_[0])
                        RegBetas[ins+'-Health-pre'].append(reg.coef_[1])
                
                    Y2       = data.Liking[data.Instruction == inst[shortInst.index(ins)]]
                    whichTr = [list(~np.isnan(X[:,0]))[t]  and list(~np.isnan(X[:,1]))[t] and\
                    list(~np.isnan(Y2))[t] for t in range(len(Y2))]
                    
                    if any(whichTr):
                        Y2 = Y2[whichTr]
                        X2  = X[whichTr,:]
                        reg      = LinearRegression().fit(X2,Y2)
                        RegBetas[ins+'-Taste-post'].append(reg.coef_[0])
                        RegBetas[ins+'-Health-post'].append(reg.coef_[1])
                        
                elif DV == 'RT':
                    Y       = data.RT[data.Instruction == inst[shortInst.index(ins)]]
                    whichTr = [list(~np.isnan(X[:,0]))[t]  and list(~np.isnan(X[:,1]))[t] and\
                    list(~np.isnan(Y))[t] for t in range(len(Y))]
                    
                    if any(whichTr):
                        Y = Y[whichTr]
                        X = X[whichTr,:]
                    
                        reg      = LinearRegression().fit(X,Y)
                        RegBetas[ins+'-Taste'].append(reg.coef_[0])
                        RegBetas[ins+'-Health'].append(reg.coef_[1])

#        if len(RegBetas['Subject']) != len(RegBetas['Nat-Taste']):
#           print('PROBLEM')
#           break

    temp = pd.DataFrame.from_dict(RegBetas)
    temp.to_csv(RegBetascsv)

    return RegBetas

def findRegressionByStudy(study,DV):
    
    crnpath = os.getcwd()
    
    if study in ['FoodReg3','FoodRegEEG1']:
        #path2csv    = 'CSVFiles\\'
        #xcludeFile  = crnpath+'\\XCludes.csv'
        #RegBetascsv = path2csv[:path2csv.find('CSVFiles')]+'RegBetas_'+DV+'.csv'

        path2csv    = crnpath[:crnpath.find('Experiments')]+'Experiments\\'+\
        study+'\\CSVFiles\\'
        xcludeFile  = path2csv[:path2csv.find('CSVFiles')]+'XCludes.csv'
        RegBetascsv = path2csv[:path2csv.find('CSVFiles')]+'Analysis\\Python\\RegBetas_'+DV+'.csv'

        inst        = ['Respond Naturally','Focus on Healthiness','Decrease Desire']

#    elif study == 'FoodRegEEG1':
#        path2csv    = crnpath[:crnpath.find('Experiments')]+'Experiments\\'+\
#        study+'\\CSVFiles\\'
#        xcludeFile  = path2csv[:path2csv.find('CSVFiles')]+'XCludes.csv'
#        RegBetascsv = path2csv[:path2csv.find('CSVFiles')]+'Analysis\\Python\\RegBetas_'+DV+'.csv'

        inst        = ['Respond Naturally','Focus on Healthiness','Decrease Desire']
    
    elif study in ['Learning','Learning2']:
        path2csv    = crnpath[:crnpath.find('Experiments')]+'Experiments\\'+\
        study+'\\CSVFiles\\'
        xcludeFile  = path2csv[:path2csv.find('CSVFiles')]+'XCludes.csv'
        RegBetascsv = path2csv[:path2csv.find('CSVFiles')]+'Analysis\\Python\\RegBetas_'+DV+'.csv'

        inst        = ['NRL1','RL','NRL2']

    RegBetas    = calcRegression(path2csv,RegBetascsv,xcludeFile,inst,DV)
    return RegBetas

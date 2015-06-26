# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
load_=[]
# spring:
#load_spr=[]
OSI_FACTOR=12
def loadGene(list):
    for day in range(61):
        load_spr_day=[1.1,1.1,1.1,1.1,1.1,1.2,1.6,2.2,1.6,1.2,1.2,2.2,1.2,1.2,1.2,1.5,2.4,1.5,1.2,1.2,1.1,1.1,1.1,1.1]
        for hour in range(24):
            load_spr_day[hour]+=np.random.randn()/OSI_FACTOR
            list.append(load_spr_day[hour])
    for day in range(30):
        load_spr_day=[1.0,1.0,1.0,1.0,1.0,1.2,1.3,1.8,1.2,1.0,1.2,2.0,1.0,1.0,1.2,1.5,2.2,1.3,1.0,1.0,1.0,1.0,1.0,1.0]
        print 
        for hour in range(24):
            load_spr_day[hour]+=np.random.randn()/OSI_FACTOR
            list.append(load_spr_day[hour])
            
loadGene(load_)

#data_spr=pd.Series(wind_spr).plot()
#summer:
#load_sum=[]
def loadGene(list):
    for day in range(31):
        load_sum_day=[0.9,0.9,0.9,0.9,0.9,1.2,1.4,1.5,1.2,1.0,1.5,1.8,1.1,1.1,1.1,1.2,1.5,2.0,1.2,1.0,0.9,0.9,0.9,0.9]
        for hour in range(24):
            load_sum_day[hour]+=np.random.randn()/OSI_FACTOR
            list.append(load_sum_day[hour])
    for day in range(61):
        load_sum_day=[1.1,1.1,1.1,1.1,1.1,1.2,1.5,2.2,1.6,1.3,1.8,2.5,1.5,1.3,1.3,2.0,2.7,2.0,1.5,1.3,1.1,1.1,1.1,1.1]
        for hour in range(24):
            load_sum_day[hour]+=np.random.randn()/OSI_FACTOR
            list.append(load_sum_day[hour])
loadGene(load_)
#data_spr=pd.Series(wind_sum).plot()
#autumn:
#solar_aut=[]
def loadGene(list):
    for day in range(31):
        load_aut_day=[1.0,1.0,1.0,1.0,1.0,1.2,1.5,2.0,1.6,1.2,1.2,2.1,1.2,1.2,1.2,1.5,2.2,1.5,1.2,1.2,1.0,1.0,1.0,1.0]
        for hour in range(24):
            load_aut_day[hour]+=np.random.randn()/OSI_FACTOR
            list.append(load_aut_day[hour])
    for day in range(61):
        load_aut_day=[0.9,0.9,0.9,0.9,0.9,1.0,1.3,1.6,1.0,1.0,1.0,1.8,1.2,1.0,1.2,1.5,2.0,1.3,1.0,1.0,1.0,1.0,0.9,0.9]
        for hour in range(24):
            load_aut_day[hour]+=np.random.randn()/OSI_FACTOR
            list.append(load_aut_day[hour])
loadGene(load_)
#data_spr=pd.Series(wind_aut).plot()
#windter:
# spring:
#wind_win=[]
def loadGene(list):
    for day in range(31):
        load_win_day=[1.0,1.0,1.0,1.0,1.0,1.2,1.5,2.0,1.6,1.2,1.2,2.1,1.2,1.2,1.2,1.5,2.2,1.5,1.2,1.2,1.0,1.0,1.0,1.0]
        for hour in range(24):
            load_win_day[hour]+=np.random.randn()/OSI_FACTOR
            list.append(load_win_day[hour])
    for day in range(60):
        load_win_day=[1.2,1.2,1.2,1.2,1.2,1.4,1.8,2.2,1.6,1.2,1.2,2.5,1.2,1.2,1.2,1.5,2.7,1.8,1.2,1.2,1.0,1.0,1.0,1.0]
        for hour in range(24):
            load_win_day[hour]+=np.random.randn()/OSI_FACTOR
            list.append(load_win_day[hour])
loadGene(load_)
#data_spr=pd.Series(load_).plot()

if __name__!='__main__':
    print 'import load'
else:
    data_spr=pd.Series(load_).plot()    
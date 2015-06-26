# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

temp_=[]
# spring:
solor_spr=[]
def solorGene(list):
    for day in range(61):
        solor_spr_day=[2,2,3,4,5,6,7,8,9,10,10,10,11,15,14,12,11,10,9,8,7,6,5,4]
        for hour in range(24):
            solor_spr_day[hour]+=np.random.randn()
            list.append(solor_spr_day[hour])
    for day in range(30):
        solor_spr_day=[5,6,6,7,8,9,10,11,12,14,16,17,19,20,19,17,15,13,10,9,8,7,6,5]
        for hour in range(24):
            solor_spr_day[hour]+=np.random.randn()
            list.append(solor_spr_day[hour])
solorGene(temp_)
#data_spr=pd.Series(wind_spr).plot()
#summer:
wind_sum=[]
def solorGene(list):
    for day in range(31):
        solor_sum_day=[10,11,12,13,14,15,16,17,18,20,21,22,23,25,24,22,20,18,17,16,15,14,12,10]
        for hour in range(24):
            solor_sum_day[hour]+=np.random.randn()
            list.append(solor_sum_day[hour])
    for day in range(60):
        solor_sum_day=[20,20,21,22,23,23,24,25,26,27,29,30,31,33,32,30,28,25,25,24,23,22,21,20]
        for hour in range(24):
            solor_sum_day[hour]+=np.random.randn()
            list.append(solor_sum_day[hour])
solorGene(temp_)
#data_spr=pd.Series(wind_sum).plot()
#autumn:
solar_aut=[]
def solorGene(list):
    for day in range(31):
        solor_aut_day=[20,20,21,22,23,23,24,25,26,27,28,29,30,31,28,25,24,23,22,22,22,21,21,20]
        for hour in range(24):
            solor_aut_day[hour]+=np.random.randn()
            list.append(solor_aut_day[hour])
    for day in range(61):
        solor_aut_day=[10,11,12,13,14,15,16,17,18,20,21,22,23,25,24,22,20,18,17,16,15,14,12,10]
        for hour in range(24):
            solor_aut_day[hour]+=np.random.randn()
            list.append(solor_aut_day[hour])
solorGene(temp_)
#data_spr=pd.Series(wind_aut).plot()
#windter:
# spring:
wind_win=[]
def solorGene(list):
    for day in range(91):
        solor_win_day=[2,2,3,4,5,6,7,8,9,10,10,10,11,15,14,12,11,10,9,8,7,6,5,4]
        for hour in range(24):
            solor_win_day[hour]+=np.random.randn()
            list.append(solor_win_day[hour])
solorGene(temp_)
data_spr=pd.Series(temp_).plot()
if __name__!='__main__':
    print 'import tmp'
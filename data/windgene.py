# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import integrate 
import math
wind_=[]
power_=[]
wind_out=[]
# DEFINE :
RATED_WIND_POWER=3.0  #KW
HIGH_WIND=10.0
IN_WIND_SPEED=5.0  #3 rate
RATED_WIND_SPEED=12.0 # 6 rate
OUT_WIND_SPEED=20.0 # 8 rate
COUNTS=1
#gamma func()
def gamma(num):
    return math.gamma(num)
#wind speed gene
def speedGene(speed,high):
    return speed*((high/9.0)**0.143)
# wind speed : probability density function
def proDenFunc(speed):
    return (k/c)*(speed/c)**(k-1)*np.exp(-(speed/c)**k)
#power out & speed 
def powerOut(speed):
    if IN_WIND_SPEED<=speed and speed<RATED_WIND_SPEED:
        return RATED_WIND_POWER*((speed**k-IN_WIND_SPEED**k)/(RATED_WIND_SPEED**k-IN_WIND_SPEED**k)) * (k/c)*(speed/c)**(k-1)*np.exp(-(speed/c)**k)  
    elif RATED_WIND_SPEED<=speed and speed<=OUT_WIND_SPEED:
        return RATED_WIND_POWER * (k/c)*(speed/c)**(k-1)*np.exp(-(speed/c)**k)
    else :
        return 0.0
# power real out
def windPowerOUT(speed_min,speed_max):
   return integrate.quad(powerOut,speed_min,speed_max)
# runtime power curve:
def windPowerRt(speed):
    if IN_WIND_SPEED<=speed and speed<RATED_WIND_SPEED:
         return RATED_WIND_POWER*((speed**k-IN_WIND_SPEED**k)/(RATED_WIND_SPEED**k-IN_WIND_SPEED**k)) 
    elif RATED_WIND_SPEED<=speed and speed<=OUT_WIND_SPEED:
        return RATED_WIND_POWER
    else :
        return 0.0

def windPowerGene(plist,vlist,quarter):
    for day in range(91):
        for hour in range(24):
            plist.append(windPowerOUT(0,vlist[(quarter-1)*91*24+day*24+hour])[0])

# spring:by speed exchange
#wind_spr=[]
def windGene(vlist):
    for day in range(91): 
        wind_spr_day= [6,7,8,9,10,11,12,10,9,8,7,7,6,7,9,10,12,13,10,9,8,7,7,6]
        for hour in range(24):
            wind_spr_day[hour]+=np.random.randn()
            vlist.append(speedGene(wind_spr_day[hour],HIGH_WIND))

# to create results:          
windGene(wind_)
k=((np.std(wind_)/np.mean(wind_))**-1.086)
c=np.mean(wind_)/gamma(1.0/k+1)
windPowerGene(wind_out,wind_,1)
print 'spr     wind gene: %f'%sum(wind_out[:91*24])
#print windPowerOUT(1,np.min(wind_),np.max(wind_))
#data_spr=pd.Series(wind_spr).plot()
#summer:
#wind_sum=[]
def windGene(list):
    for day in range(61):
        wind_sum_day=[5,6,7,8,9,12,14,16,14,12,10,8,7,9,10,12,15,16,14,13,10,9,8,7,6,5]
        for hour in range(24):
            wind_sum_day[hour]+=np.random.randn()
            list.append(wind_sum_day[hour])
    for day in range(30):
        wind_sum_day=[6,7,8,9,10,11,12,10,9,8,7,7,6,7,9,10,11,12,10,9,8,7,7,6]
        for hour in range(24):
            wind_sum_day[hour]+=np.random.randn()
            list.append(wind_sum_day[hour])
            
       
windGene(wind_)
k=((np.std(wind_[91*24-1:91*24*2])/np.mean(wind_[91*24-1:91*24*2]))**-1.086)
c=np.mean(wind_[91*24-1:91*24*2])/gamma(1.0/k+1)
windPowerGene(wind_out,wind_,2)
print 'summer  wind gene: %f'%sum(wind_out[91*24:91*24*2])
#print windPowerOUT(1,np.min(wind_),np.max(wind_))
#data_spr=pd.Series(wind_sum).plot()
#autumn:
#wind_aut=[]
def windGene(list):
    for day in range(61):
        wind_aut_day=[6,7,8,9,10,11,12,10,9,8,7,7,6,7,9,10,12,13,10,9,8,7,7,6]
        for hour in range(24):
            wind_aut_day[hour]+=np.random.randn()
            list.append(wind_aut_day[hour])
    for day in range(31):
        wind_aut_day=[5.5,6,7,7,8,8,10,8,7,7,6,5,6,7,7,8,9,11,9,8,8,6,7,5]
        for hour in range(24):
            wind_aut_day[hour]+=np.random.randn()
            list.append(wind_aut_day[hour])
            
         
windGene(wind_)
k=((np.std(wind_[91*24*2-1:91*24*3+24])/np.mean(wind_[91*24*2-1:91*24*3+24]))**-1.086)
c=np.mean(wind_[91*24*2-1:91*24*3+24])/gamma(1.0/k+1)
windPowerGene(wind_out,wind_,3)
print 'automn  wind gene: %f'%sum(wind_out[2*91*24:3*91*24])
#data_spr=pd.Series(wind_aut).plot()
#windter:
# spring:
#wind_win=[]
def windGene(list):
    for day in range(61):
        wind_win_day=[6,7,8,9,10,11,12,10,9,8,7,7,6,7,9,10,12,13,10,9,8,7,7,6]
        for hour in range(24):
            wind_win_day[hour]+=np.random.randn()
            list.append(wind_win_day[hour])
    for day in range(30):
        wind_win_day=[5,6,7,8,9,12,14,16,14,12,10,8,7,9,10,12,15,16,14,13,10,9,8,7,6,5]
        for hour in range(24):
            wind_win_day[hour]+=np.random.randn()
            list.append(wind_win_day[hour])
windGene(wind_)
k=((np.std(wind_[91*24*3+24-1:91*24*4+24])/np.mean(wind_[91*24*3+24-1:91*24*4+24]))**-1.086)
c=np.mean(wind_[91*24*2-1:91*24*3+24])/gamma(1.0/k+1)
windPowerGene(wind_out,wind_,4)
print 'winter  wind gene: %f'%sum(wind_out[91*24*3:91*24*4])

#data_spr=pd.Series(wind_).plot()
if __name__!='__main__':
    print 'import winds'
else:
    data_spr=pd.Series(wind_).plot()

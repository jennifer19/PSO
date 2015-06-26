# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from scipy import integrate
from scipy import stats
solor_=[]
power_rt=[]

pv_out=[]
STC_G=1000.0 #W/M**2
STC_T=25 # DU
STC_P=0.1  #KW
TMP_POWER_K=-0.004
PV_COUNTS=1 #2kw
NOCT_T=45
T_ENV=25

R_dust=0.9 # dust efficient
R_loss=0.8 #dc-ac
R_mppt=0.8 #mppt 

def gamma(num):
    return math.gamma(num)
def proDenfunc(light_rat):
    return gamma(alpha+beta)/(gamma(alpha)*gamma(beta)) * (light_rat)**(alpha-1) * (1-light_rat)**(beta-1)

def powerOut(G):
    T=T_ENV+(G/800.0)*(NOCT_T-20)
    return (1.0/G_max)* STC_P*(G/STC_G)*(1+TMP_POWER_K*(T-STC_T)) * gamma(alpha+beta)/(gamma(alpha)*gamma(beta)) * (G/G_max)**(alpha-1) * (1-(G/G_max))**(beta-1)
def solorPowOut(low_G,high_G):
    return integrate.quad(powerOut,low_G,high_G)
def solorPowRT(G):
    T=T_ENV+(G/800.0)*(NOCT_T-20)
    return STC_P*(G/STC_G)*(1+TMP_POWER_K*(T-STC_T))
def solorPowerRT(plist,vlist):
    for day in range(91):
        for hour in range(24):
            plist.append(solorPowRT(vlist[day*24+hour]))
def solorPowerGene(plist,vlist,quarter):
    for day in range(91):
        for hour in range(24):
            plist.append(solorPowOut(0,abs(vlist[(quarter-1)*91*24+day*24+hour]))[0]*PV_COUNTS)
# spring:
#solor_spr=[]
def solorGene(list):
    for day in range(61):
        solor_spr_day=[50,50,50,50,100,300,500,600,600,700,700,750,750,800,700,600,500,400,300,100,100,100,50,50]
        for hour in range(24):
            solor_spr_day[hour]+=(np.random.randn()*30)
            list.append(solor_spr_day[hour])
    for day in range(30):
        solor_spr_day=[50,50,50,50,200,300,500,600,600,700,700,750,900,1000,900,700,600,400,300,100,100,100,50,50]
        for hour in range(24):
            solor_spr_day[hour]+=(np.random.randn()*30)
            list.append(solor_spr_day[hour])      
solorGene(solor_)
solorPowerRT(power_rt,solor_)

u=np.mean(solor_/np.max(solor_))
var=np.var(solor_/np.max(solor_))
alpha=u*((u*(1.0-u)/var)-1.0)
beta=(1-u)*(u*(1.0-u)/var-1.0)
G_max=np.max(solor_)
BetaDen=stats.beta(alpha,beta)
solorPowerGene(pv_out,solor_,1)
print 'spr    pv gene: %f'%sum(pv_out[:91*24])

#data_spr=pd.Series(wind_spr).plot()
#summer:
#wind_sum=[]
def solorGene(list):
    for day in range(30):
        solor_sum_day=[50,50,50,50,300,400,500,600,600,700,700,800,1000,1050,1000,800,700,600,400,200,100,100,50,50]
        for hour in range(24):
            solor_sum_day[hour]+=(np.random.randn()*30)
            list.append(solor_sum_day[hour])
    for day in range(61):
        solor_sum_day=[50,50,50,50,300,400,500,600,600,700,900,1000,1100,1150,1100,1000,700,600,400,200,100,100,50,50,50]
        for hour in range(24):
            solor_sum_day[hour]+=(np.random.randn()*30)
            list.append(solor_sum_day[hour])
solorGene(solor_)
solorPowerRT(power_rt,solor_)


u=np.mean(solor_[91*24-1:91*24*2]/np.max(solor_[91*24-1:91*24*2]))
var=np.var(solor_[91*24-1:91*24*2]/np.max(solor_[91*24-1:91*24*2]))
alpha=u*((u*(1.0-u)/var)-1.0)
beta=(1-u)*(u*(1.0-u)/var-1.0)
G_max=np.max(solor_)
BetaDen=stats.beta(alpha,beta)
solorPowerGene(pv_out,solor_,2)
print 'summer pv gene :%f'%sum(pv_out[91*24:91*24*2])
#data_spr=pd.Series(wind_sum).plot()
#autumn:
#solar_aut=[]
def solorGene(list):
    for day in range(31):
        solor_aut_day=[50,50,50,50,300,400,500,600,600,700,700,800,1000,1050,1000,800,700,600,400,200,100,100,50,50]
        for hour in range(24):
            solor_aut_day[hour]+=(np.random.randn()*30)
            list.append(solor_aut_day[hour])
    for day in range(61):
        solor_aut_day=[50,50,50,50,100,200,400,600,600,700,700,750,800,950,800,700,600,400,300,100,100,100,50,50]
        for hour in range(24):
            solor_aut_day[hour]+=(np.random.randn()*30)
            list.append(solor_aut_day[hour])
solorGene(solor_)
solorPowerRT(power_rt,solor_)


u=np.mean(solor_[91*24*2-1:91*24*3+24]/np.max(solor_[91*24*2-1:91*24*3+24]))
var=np.var(solor_[91*24*2-1:91*24*3+24]/np.max(solor_[91*24*2-1:91*24*3+24]))
alpha=u*((u*(1.0-u)/var)-1.0)
beta=(1-u)*(u*(1.0-u)/var-1.0)
G_max=np.max(solor_)
BetaDen=stats.beta(alpha,beta)
solorPowerGene(pv_out,solor_,3)
print 'automn pv gene :%f'%sum(pv_out[91*24*2:91*24*3])
#data_spr=pd.Series(wind_aut).plot()
#windter:
# spring:
#wind_win=[]
def solorGene(list):
    for day in range(91):
        solor_win_day=[50,50,50,50,50,100,400,400,500,500,600,600,650,650,700,600,500,400,300,100,100,100,50,50]
        for hour in range(24):
            solor_win_day[hour]+=(np.random.randn()*30)
            list.append(solor_win_day[hour])
solorGene(solor_)
solorPowerRT(power_rt,solor_)


u=np.mean(solor_[91*24*3+24-1:91*24*4+24]/np.max(solor_[91*24*3+24-1:91*24*4+24]))
var=np.var(solor_[91*24*3+24-1:91*24*4+24]/np.max(solor_[91*24*3+24-1:91*24*4+24]))
alpha=u*((u*(1.0-u)/var)-1.0)
beta=(1-u)*(u*(1.0-u)/var-1.0)
G_max=np.max(solor_)
BetaDen=stats.beta(alpha,beta)
solorPowerGene(pv_out,solor_,4)
print 'winter pv gene :%f'%sum(pv_out[91*24*3:91*24*4])
#data_spr=pd.Series(solor_).plot()

if __name__!='__main__':
    print 'import solor'

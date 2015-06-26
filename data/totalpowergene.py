# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math
import loadgene
import windgene
import solargene
import recyclemodule
import copy
from scipy import stats

#pos :wind pv bat ele-tank-fc :
WINDS_COUNTS=3
PV_COUNTS=40
BAT_COUNTS=0
ELE_COUNTS=0
TANK_COUNTS=0
FC_COUNTS=0


# price all kinds of dvice
WINDS_PRICE_DEVICE=9702 #3KW
WINDS_PRICE_MAINT=40
WINDS_PV_CONTROLLER=2500  #CHANGE 
WINDS_LIFESPAN=10
PV_PRICE_BAT1=450 #100W
PV_PRICE_BAT2=1280 #250W
PV_PRICE_MAINT=20
PV_LIFESPAN=20
BAT_PRICE_DEVICE=1050 #200AH 
BAT_PRICE_RESET=850
BAT_PRICE_MAINT=24
BAT_LIFESPAN=8
BAT_CHDH_COUNTS=500 
DA_PRICE_DEVICE=2500  #2KW
DA_PRICE_MAINT=25
DA_LIFESPAN=20
ELE_PRICE_DEVICE=12760 #1KW
ELE_PRICE_MAINT=160  #1KW
ELE_LIFSPAN=20
TANK_PRICE_DEVICE=1800
TANK_PRICE_MAINT=10
TANK_LIFESPAN=20
FC_PRICE_DEVICE=19140 #1KW
FC_PRICE_MAINT=1110
FC_PRICE_RESET=15900
FC_LIFESPAN=5

#para :
BAT_POWER=2.4 #kw
RATIO_RISK=200000
RATIO_OUTAGE=1000


#total power
pv_out=[]
wind_out=[]
load=[]
power_net=[]
power_ren=[]
energy_net=[]
pv_out=solargene.pv_out
wind_out=windgene.wind_out
load=loadgene.load_

def powerRenGene(p_ren,pos_):
    del p_ren[:]
    for day in range(364):
        for hour in range(24):
            p_ren.append(windgene.wind_out[day*24+hour]*pos_[0]+solargene.pv_out[day*24+hour]*pos_[1])

def powerNetGene(p_net,pos_):
    del p_net[:]
    for day in range(364):
        for hour in range(24):
            p_net.append(windgene.wind_out[day*24+hour]*pos_[0]+solargene.pv_out[day*24+hour]*pos_[1]-load[day*24+hour]) 


def energyNetGene(egy_net,p_net):
    del egy_net[:]
    for day in range(364):
        for hour in range(24):
            if day==0 and hour==0:
                 egy_net.append(p_net[day*24+hour]*1)
            else:
                 egy_net.append(egy_net[day*24+hour-1]+p_net[day*24+hour]*1)



#GOAL FUNC:  
max_tank_Volumn=[]
cycle_counts=[] #0123:ele  fc tank |bat
ren=[3,70]  #01 wind pv
#goal=config cost + reset cost + maintain cost + outage cost +risk cost
def cost_config(pos_,Qnet,Pnet,counts):
    p_wind=pos_[0]*WINDS_PRICE_DEVICE
    p_pv=pos_[1]*PV_PRICE_BAT1
    counts.append(int(max(Pnet)))
    counts.append(abs(int(min(Pnet))))
    Qmin=min(Qnet)
    print 'Qmin:%f   '%Qmin
    Qmax=max(max(Qnet),abs(min(Qnet)))
    Pmax=max(max(Pnet),abs(min(Pnet)))
    maxVol=recyclemodule.tank_svgas(recyclemodule.ele_mkgas(Qmax))
    max_tank_Volumn.append(abs(maxVol)) 
    print 'maxVol :%f'%maxVol
    counts.append(abs(maxVol/100.0))
    q=(Qmax/BAT_POWER)*BAT_PRICE_DEVICE
    if abs(q)>ELE_PRICE_DEVICE+TANK_PRICE_DEVICE+FC_PRICE_DEVICE:
        p_cycle=ELE_PRICE_DEVICE*counts[0]+TANK_PRICE_DEVICE*counts[2]+FC_PRICE_DEVICE*counts[1]
        counts.append(round(Pmax))            
        p_bat=(Pmax)/BAT_POWER*BAT_PRICE_DEVICE
        #print 'cycle price :%f'%p_cycle
        #print 'bat   price :%f'%p_bat
           
    else:
        counts.append(0.0)
        p_bat=q
        p_cycle=0
        #print 'cycle not use'
        #print q

    print 'ele: %d fc : %d tank : %d bat : %d'%(counts[0],counts[1],counts[2],counts[3])       
    return p_wind+p_pv+p_bat+p_cycle
    
def cost_maintain(pos_,counts):
    return pos_[0]*WINDS_PRICE_MAINT+pos_[1]*PV_PRICE_MAINT+counts[0]*ELE_PRICE_MAINT+counts[1]*FC_PRICE_MAINT+counts[2]*TANK_PRICE_MAINT
def cost_reset(pos_,counts):
    return counts[2]*FC_PRICE_RESET/FC_LIFESPAN+counts[3]*BAT_PRICE_RESET/BAT_LIFESPAN
def cost_risk(Qnet):
    count=0
    for item in range(364*24):
        if Qnet[item]+10<0:
            count+=1         
    return count*RATIO_RISK
def cost_outage(Pnet):
    sum_=0
    for item in range(364*24):
        if Pnet[item]>abs(min(Pnet)):
            sum_+=1
    return sum_*RATIO_OUTAGE

def goaltotal(pos_,counts,Qnet,Pnet):
    mcounts=[]
    install=cost_config(pos_,Qnet,Pnet,mcounts)
    return install+cost_maintain(pos_,mcounts)+cost_reset(pos_,mcounts)+cost_risk(Qnet)+cost_outage(Pnet)

powerNetGene(power_net,ren)
powerRenGene(power_ren,ren)
energyNetGene(energy_net,power_net)  
#print 'payment install : %f'%cost_config(ren,energy_net,power_net,cycle_counts)
#print 'tank max volumn : %f'%max_tank_Volumn[0]
#print 'payment maintain: %f'%cost_maintain(ren,cycle_counts)
#print 'payment reset   : %f'%cost_reset(ren,cycle_counts)
#print 'payment risk    : %f'%cost_risk(energy_net)
#print 'payment outage  : %f'%cost_outage(power_net)
#print '!!payment total goal: %f'%goaltotal(ren,cycle_counts,energy_net,power_net)


#my QPSO  Algorithn
xPOS=[]  
xPOS_local_best=[]  
xPOS_global_best=[]
w=0.8  
r1=0.4
results=[]
def inti_population(pos_,size_,local_,global_,goalfunc_,results,Qnet,Pnet,Rnet):
    del local_[:]
    del global_[:]
    del results[:]
    for i in range(size_):
        pos_.append([])
        local_.append([])
    for i in range(size_):
        pos_[i].append(np.random.randint(0,300))
        pos_[i].append(np.random.randint(0,300))
    for i in range(size_):
        powerNetGene(Pnet,pos_[i])
        powerRenGene(Rnet,pos_[i])
        energyNetGene(Qnet,Pnet)
        results.append(goalfunc_(pos_[i],cycle_counts,Qnet,Pnet))   
        temp=pos_[i][0]
        local_[i].append(temp)
        temp=pos_[i][1]
        local_[i].append(temp)
    index=results.index(min(results))
    print 'init min value index: %d'%index
    temp=pos_[index][0]
    global_.append(temp)
    temp=pos_[index][1]
    global_.append(temp)

    
def get_potential_center(local_,global_,r):
    Pd=[]
    Pd.append(local_[0]*r+global_[0]*(1-r))
    Pd.append(local_[1]*r+global_[1]*(1-r))
    return Pd
    
def get_particle_best_ave(local_):
    mbest=[]
    x1=0
    x2=0
    for item in range(len(local_)):
        x1+=local_[item][0]
        x2+=local_[item][1]
    mbest.append(x1/len(local_))
    mbest.append(x2/len(local_))
    print 'best ave:[%f,%f]'%(mbest[0],mbest[1])
    return mbest
    
def get_beta_particle(itera_count):
    return 0.5
    
def updata_population(pos_,local_,global_,goalfunc_): 
    L=[]
    result=[]
    u=stats.norm
    Pi=get_particle_best_ave(local_)
    print 'Pi: (%f,%f)'%(Pi[0],Pi[1])
    # use pd pi to change particle pos
    for item in range(len(pos_)): 
        del L[:]
        print 'origin pos:[%f,%f]'%(pos_[item][0],pos_[item][1])
        print 'origin loc:[%f,%f]'%(local_[item][0],local_[item][1])
        Pd=get_potential_center(local_[item],global_,0.4)
  
        beta=get_beta_particle(1)
        L.append(2*beta*abs(Pi[0]-pos_[item][0]))
        L.append(2*beta*abs(Pi[1]-pos_[item][1]))
        
        pos_[item][0]=Pd[0]+0.5*L[0]*math.log(abs(1/u.rvs(size=1)),math.e)
        pos_[item][1]=Pd[1]+0.5*L[1]*math.log(abs(1/u.rvs(size=1)),math.e)
        print 'dealed pos:[%f,%f]'%(pos_[item][0],pos_[item][1])
        print 'origin loc:[%f,%f]'%(local_[item][0],local_[item][1])
    for item in range(len(pos_)):
        result.append(goalfunc_(pos_[item],cycle_counts,energy_net,power_net))
    index=result.index(min(result))
    print 'min value index: %d'%index
    temp=pos_[index][0]
    global_.append(temp)
    temp=pos_[index][1]
    global_.append(temp)    
   
   #for item in range(pos_.size()):
        

inti_population(xPOS,10,xPOS_local_best,xPOS_global_best,goaltotal,results,energy_net,power_net,power_ren)

updata_population(xPOS,xPOS_local_best,xPOS_global_best,goaltotal)
print '----'
print xPOS_local_best












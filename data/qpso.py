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
RATIO_OUTAGE=10000


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
ren=[3,70]  #01 wind pv
#goal=config cost + reset cost + maintain cost + outage cost +risk cost
def cost_config(pos_,Qnet,Pnet,cycleCounts_):
    p_wind=pos_[0]*WINDS_PRICE_DEVICE
    p_pv=pos_[1]*PV_PRICE_BAT1
    cycleCounts_.append(abs(int(max(Pnet))))
    cycleCounts_.append(abs(int(min(Pnet))))
    Qmin=min(Qnet)
    #print 'Qmin:%f   '%Qmin
    Qmax=max(abs(max(Qnet)),abs(min(Qnet)))
    Pmax=max(abs(max(Pnet)),abs(min(Pnet)))
    maxVol=recyclemodule.tank_svgas(recyclemodule.ele_mkgas(Qmax))
    max_tank_Volumn.append(abs(maxVol)) 
    #print 'maxVol :%f'%maxVol
    cycleCounts_.append(abs(maxVol/100.0))
    q=(Qmax/BAT_POWER)*BAT_PRICE_DEVICE
    if abs(q)>ELE_PRICE_DEVICE+TANK_PRICE_DEVICE+FC_PRICE_DEVICE:
        p_cycle=ELE_PRICE_DEVICE*cycleCounts_[0]+TANK_PRICE_DEVICE*cycleCounts_[2]+FC_PRICE_DEVICE*cycleCounts_[1]
        cycleCounts_.append(round(Pmax))            
        p_bat=(Pmax)/BAT_POWER*BAT_PRICE_DEVICE
        #print 'cycle price :%f'%p_cycle
        #print 'bat   price :%f'%p_bat
    else:
        cycleCounts_.append(0.0)
        p_bat=q
        p_cycle=0
        #print 'cycle not use'
        #print q
    #print 'ele: %d fc : %d tank : %d bat : %d'%(cycleCounts_[0],cycleCounts_[1],cycleCounts_[2],cycleCounts_[3])       
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

def goaltotal(pos_,cycleCounts_,Qnet,Pnet):
    install=cost_config(pos_,Qnet,Pnet,cycleCounts_)
    return install+cost_maintain(pos_,cycleCounts_)+cost_reset(pos_,cycleCounts_)+cost_risk(Qnet)+cost_outage(Pnet)

#powerNetGene(power_net,ren)
#powerRenGene(power_ren,ren)
#energyNetGene(energy_net,power_net)  
#print 'payment install : %f'%cost_config(ren,energy_net,power_net,cycle_counts)
#print 'tank max volumn : %f'%max_tank_Volumn[0]
#print 'payment maintain: %f'%cost_maintain(ren,cycle_counts)
#print 'payment reset   : %f'%cost_reset(ren,cycle_counts)
#print 'payment risk    : %f'%cost_risk(energy_net)
#print 'payment outage  : %f'%cost_outage(power_net)
#print '!!payment total goal: %f'%goaltotal(ren,cycle_counts,energy_net,power_net)


#my QPSO  Algorithn
cycle_counts=[] # [T][N][4]0123:ele  fc tank |bat=[] #0123:ele  fc tank |bat
xPOS=[]  #[T]generate [N]particle size :tn--id[2]dimenssion
xPOS_local_best=[]  #[N]particle size [2]dimenssion
xPOS_global_best=[] #[T][2] dimenssion
results=[] # goalfunc(pos) to get result:[T][N][1]
def inti_population(pos_,cycleCount_,gen_,size_,local_,global_,goalfunc_,res_,Qnet,Pnet,Rnet):
    rlist=[]
    for igen in range(gen_):
        pos_.append([])
        cycleCount_.append([])
        res_.append([])
        global_.append([])
        for isize in range(size_): 
            pos_[igen].append([])
            cycleCount_[igen].append([])
            res_[igen].append([])
    for item in range(size_):
        local_.append([])
        pos_[0][item].append(np.random.randint(1,100))
        pos_[0][item].append(np.random.randint(1,300))
    for item in range(size_):
        powerNetGene(Pnet,pos_[0][item])
        powerRenGene(Rnet,pos_[0][item])
        energyNetGene(Qnet,Pnet)
        rlist.append(goalfunc_(pos_[0][item],cycleCount_[0][item],Qnet,Pnet))   
        temp=pos_[0][item][0]
        local_[item].append(temp)
        temp=pos_[0][item][1]
        local_[item].append(temp)
    #print rlist
    index=rlist.index(min(rlist))
    for item in range(size_):
        res_[0][item].append(rlist[item])
    #print res_
    print 'init min value index: %d'%index
    temp=pos_[0][index][0]
    global_[0].append(temp)
    temp=pos_[0][index][1]
    global_[0].append(temp)

    
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
    #print 'best ave:[%f,%f]'%(mbest[0],mbest[1])
    return mbest
    
def get_beta_particle(itera_count):
    # x-1 nonlinear reduce  0.5--->0.1
    if itera_count%10==0:
        return 0.5
    else:
        return 0.5
        #return 1.0/(itera_count%10+1)
    
xPOS=[]  #[T]generate [N]particle size :tn--id[2]dimenssion
xPOS_local_best=[]  #[N]particle size [2]dimenssion
xPOS_global_best=[] #[2] dimenssion
results=[] # goalfunc(pos) to get result:[T][N][1]  
temp_counts=[]
temp_values=[]  
def update_population(pos_,cycleCounts_,curgen_,local_,global_,goalfunc_,res_,Qnet,Pnet,Rnet): 
    del temp_values[:]   
    del temp_counts[:]
    L=[]
    rlist=[]
    u=stats.norm
    chaos_factor=5
    print '----------------'
    print 'gen is %d'%curgen_
    print '----------------'
    Pi=get_particle_best_ave(local_)
    #print 'Pi: (%f,%f)'%(Pi[0],Pi[1])
    # use pd pi to change particle pos
    beta=get_beta_particle(curgen_)
    muniform=stats.uniform().rvs(size=1)
    Pd_r=muniform[0]**(1+curgen_/GEN_MAX)
    print '----Pd_r:%f-------'%Pd_r
    for item in range(len(local_)):
        
        del L[:]
        # !!!!'print' to check the dif  between pos_ and local_ 
        #print 'origin pos:[%f,%f]'%(pos_[curgen_-1][item][0],pos_[curgen_-1][item][1])
        #print 'origin loc:[%f,%f]'%(local_[item][0],local_[item][1])

        # muniform changing parameter :Pd_r for local from 0.5-->0.33 
        #                              1-Pd_r for global the Pd going to global best

        Pd=get_potential_center(local_[item],global_[curgen_-1],0.4)
  
        L.append(2*beta*abs(Pi[0]-pos_[curgen_-1][item][0]))
        L.append(2*beta*abs(Pi[1]-pos_[curgen_-1][item][1]))
        # to comfirm pos  >0
        # pos_[x1,x2]  x1,x2 can not below 1
        temp=Pd[0]+0.5*L[0]*math.log(abs(1/u.rvs(size=1)),math.e)
        if temp>0.98:
            pos_[curgen_][item].append(temp)
        else:
            pos_[curgen_][item].append(pos_[curgen_-1][item][0])
            
        temp=Pd[1]+0.5*L[1]*math.log(abs(1/u.rvs(size=1)),math.e)
        if temp>1.0:
            pos_[curgen_][item].append(temp)
        else:
            pos_[curgen_][item].append(pos_[curgen_-1][item][1])       
        #print 'dealed pos:[%f,%f]'%(pos_[curgen_][item][0],pos_[curgen_][item][1])
        #print 'origin loc:[%f,%f]'%(local_[item][0],local_[item][1])  
    # use new pos to update cycle_counts  and  new results throught goalfunc() 
    for item in range(len(pos_[curgen_])):
        powerNetGene(Pnet,pos_[curgen_][item])
        energyNetGene(Qnet,Pnet)
        rlist.append(goalfunc_(pos_[curgen_][item],cycleCounts_[curgen_][item],Qnet,Pnet))
    index=rlist.index(min(rlist))
    #record the fitness value of new pos  
    for item in range(len(pos_[curgen_])):
        res_[curgen_][item].append(rlist[item])
    print 'min value index: %d'%index
    
   
          #chaos the racer
    z1=[]
    z2=[]
    z1_temp=0
    len_temp=0
    lenlist=[]
    for item in range(len(local_)):
        len_temp=((local_[item][0]-global_[curgen_-1][0])**2+(local_[item][1]-global_[curgen_-1][1])**2)
        lenlist.append(len_temp)
    #print lenlist
    print '------------------------------------------'
    if curgen_%chaos_factor==0:
        print '---------------------------------------'
        print 'chao start'
        print '---------------------------------------'
        print global_[curgen_-1]
        for i in range(len(local_)):
            #when pos start gathering z1  close to 0.99 z2 to 0.01 
            z1_temp=(lenlist[i])/max(lenlist)
            z1.append(1-z1_temp)
            z2.append(z1_temp)
            local_[i][0]=local_[i][0]*z1[i]+local_[i][1]*z2[i]
            local_[i][1]=local_[i][0]*z2[i]+local_[i][1]*z1[i]
        print global_[curgen_-1]
    print z1
    #calculate local fitness: whatever  chaos to update global or not chaos to update new local
    for item in range(len(pos_[curgen_])):
        powerNetGene(Pnet,local_[item])
        energyNetGene(Qnet,Pnet)
        temp_values.append(goalfunc_(local_[item],temp_counts,Qnet,Pnet))
    #update particle pos , rlist is current result ,temp_value is local best result 
    
    if curgen_%chaos_factor!=0:
        for item in range(len(pos_[curgen_])):
                if temp_values[item]>rlist[item]:
                    print 'the %d had changed'%item
                    print 'local best: %f'%temp_values[item]
                    print 'curent    : %f'%rlist[item]
                    print 'has change local from [%f,%f] to [%f,%f]'%(local_[item][0],local_[item][1],pos_[curgen_][item][0],pos_[curgen_][item][1])
                    local_[item]=copy.deepcopy(pos_[curgen_][item])
                else:
                    print 'local best: %f'%temp_values[item]
                    print 'curent    : %f'%rlist[item]
                    
    #update global best ,it is the best in local and histoty:
      #update global pos

    gb_index=temp_values.index(min(temp_values))
    temp=copy.deepcopy(min(temp_values))
    powerNetGene(Pnet,global_[curgen_-1])
    energyNetGene(Qnet,Pnet)
    if temp<goalfunc_(global_[curgen_-1],temp_counts,Qnet,Pnet):
        global_[curgen_]=copy.deepcopy(local_[gb_index])
    else:
        global_[curgen_]=copy.deepcopy(global_[curgen_-1])


global_best_record=[0,0]
GEN_MAX=100
inti_population(xPOS,cycle_counts,GEN_MAX,100,xPOS_local_best,xPOS_global_best,goaltotal,results,energy_net,power_net,power_ren)
while True:    
    for genitem in range(1,GEN_MAX+1):
        update_population(xPOS,cycle_counts,genitem,xPOS_local_best,xPOS_global_best,goaltotal,results,energy_net,power_net,power_ren)
        global_best_record[0]=xPOS_global_best[genitem]















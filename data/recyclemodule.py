# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp
#!!bat::
SOC_=[]
SOC_MAX=0.8
SOC_MIN=0.2

BAT_COUNTS=4
BAT_C=200 #a.h
E_bat=12
E_maxloss=10.5
I_DH_MAX=40#A
I_CH_MAX=40#A
R_dh=0.003
R_ch=0.1
RATIO_LOSS=0.004

#!ele:  RECYCLE::
I_CH_ELE=600 #A
I_DH_ELE=20 #A
NA=6.02*10**23
C_cap_e=6.25*10**18
VM_std=22.4 #l/mol
VM_nol=24.5 #l/mol

RATIO_ele2tank=0.75
RATIO_STORE=0.95
RATIO_fc=0.5
e_tank=[]
p_ele=[]
p_tank2fc=[] #from p_fc 
RATED_P_ELE=1.5
RATED_GAS_ELE=200 #L.H 
RATED_Vout_ELE=1.6 #v
RATED_P_FC=2
E_TANK_N=30.0
E_TANK_MAX=E_TANK_N
E_TANK_MIN=0.2*E_TANK_N

def SOC_Gene(P_bat,V_bat,SOC):
    if P_bat>0:
        i=P_bat*1000/(BAT_COUNTS*V_bat)
        n=0.75
        return SOC*(1-RATIO_LOSS)+i*1*n/BAT_C
    else:
        i=P_bat*1000/(BAT_COUNTS*V_bat)
        n=1
        print i
        return SOC*(1-RATIO_LOSS)+i*1*n/BAT_C
        
def ch_IGene(P_bat):
    return P_bat*1000/(E_bat*BAT_COUNTS*0.95)
def dh_IGene(P_load):
    return P_load*1000/(E_maxloss*BAT_COUNTS*0.95)
# SOC :   0.2< SOC <0.8
def BAT_Pch_max(SOC):
    return np.max((0,np.min(((SOC_MAX-SOC)*BAT_C,I_CH_MAX))*E_bat))/1000
def BAT_Pdh_max(SOC):
    return np.max((0,np.min(((SOC-SOC_MIN)*BAT_C,I_DH_MAX))*E_bat))/1000
        
#print BAT_Pdh_max(0.4)  
#print BAT_Pch_max(0.2)    
#-----------------------i am cut-off line！--------------

def power_Ele2Tank(p_ele):
    return p_ele*RATIO_ele2tank
def power_Tank2Fc(p_tank):
    return p_tank*RATIO_fc
def E_tank(tank,Pele,Ptank):
    return tank+Pele*1-Ptank*1*RATIO_STORE
def Ele_powerOut_max(tank):
    return np.min((RATED_P_ELE,(E_TANK_MAX-tank)/(1*RATIO_ele2tank)))
def FC_powerOut_max(tank):
    return np.min((RATED_P_ELE,(tank-E_TANK_MIN)/(1*RATIO_fc)))

#function func:
def ratio_gas2power():
    return (RATED_GAS_ELE/VM_nol*2*NA)/((C_cap_e)*3600)*RATED_Vout_ELE/1000.0
def ele_mkgas(p):
    return p*RATIO_ele2tank*RATED_GAS_ELE/RATIO_POWER2GAS
def tank_svgas(v):
    return v*RATIO_STORE/E_TANK_N   #30
def fc_getpower(v):
    return (v*E_TANK_N/RATIO_STORE)/(RATED_GAS_ELE)*RATIO_POWER2GAS  * RATIO_fc
RATIO_POWER2GAS=ratio_gas2power()
ele_power_in=2  #kw
print 'power to gas ratio  : %f'%RATIO_POWER2GAS
print '%f power produce gas: %f L'%(ele_power_in,ele_mkgas(ele_power_in))
print '%f raw gas save tank: %f L'%(ele_mkgas(ele_power_in),tank_svgas(ele_mkgas(ele_power_in)))
print '%f tank-gas fc get p: %f kw'%(tank_svgas(ele_mkgas(ele_power_in)),fc_getpower(tank_svgas(ele_mkgas(ele_power_in))))
if __name__!='__main__':
    print 'import recycle'

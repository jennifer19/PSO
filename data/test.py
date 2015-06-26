# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import math
from scipy import stats


#my QPSO  Algorithn
pos=[]   
pos_local_best=[]  
pos_global_best=[]  
for i in range(10):
    pos.append(i)
pos_local_best.append(pos[0])
pos[0]=100000
print pos
print pos_local_best


print '----------------'
l=range(10)
ll=l[:]

l[0]=100000
print ll
print l
from __future__ import division,print_function
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import os, sys
import gridtools as gt
import datatools as dt
import plottools as pt
import misctools as mt
import interptools as ipt
np.set_printoptions(precision=16,suppress=True,threshold=sys.maxsize)
import pandas as pd
from collections import OrderedDict
import copy



def residual_stats(mod, obs):
    
    modm=np.mean(mod)
    obsm=np.mean(obs)
    
    out=OrderedDict()
    
    out['meansl']=modm-obsm
    out['stdsl']=np.std(mod-obs)
    out['rmsesl']=np.sqrt(((mod - obs)**2).mean())
    out['relaverr']=100*np.sum((mod-obs)**2)/np.sum(np.fabs(mod-obsm)**2+np.fabs(obs-obsm)**2)
    out['corsl']=np.sum((mod-modm)*(obs-obsm))/(np.sqrt(np.sum((mod-modm)**2))*np.sqrt(np.sum((obs-obsm)**2)))
    #out['skewsl']=sp.stats.skew(mod-obsm)
    #out['skewsl']=sp.stats.skew(obs)-sp.stats.skew(mod)
    if sp.stats.skew(obs)==0:
        out['skewsl']=0
    else:
        out['skewsl']=1-((sp.stats.skew(obs-mod))/sp.stats.skew(obs))

    out['skill']=1-(np.sum(np.fabs(mod-obs)**2)/(np.sum((np.fabs(mod-modm)+np.fabs(obs-obsm))**2)))
    
    return out
    

def remove_common_nan(in1, in2):
    bidx=np.isnan(in1)+np.isnan(in2)
    
    return in1[~bidx], in2[~bidx]
    
    
    
def interp_clean_common(time1,data1,time2,data2,filter_max=1000.0,filter_min=-1000.0):
    
    
    #copy and filter dataset 1
    data11=copy.copy(data1)
    data11[data1>=filter_max]=np.nan
    data11[data1<=filter_min]=np.nan

    #copy and filter dataset 2
    data22=copy.copy(data2)   
    data22[data2>=filter_max]=np.nan
    data22[data2<=filter_min]=np.nan

    # interp filtered data2 to dataset1 times
    #print(time2.shape,data22.shape,time1.shape)
    data21=ipt.interp1d(time2,data22,time1)    

    #idx to remove all nans from either dataset
    bidx=np.isnan(data11)+np.isnan(data21)
    
    #return time and data
    return time1[~bidx],data11[~bidx],data21[~bidx]
   
    
def interp_common(time1,data1,time2,data2,dt=60):
    
    # tmin is the biggest small number
    # tmax is the smallest big number
    tmin=np.max([time1[0],time2[0]])
    tmax=np.min([time1[-1],time2[-1]])
    
    time=np.arange(tmin,tmax+dt/(24*60*60.0),dt/(24*60*60.0))
   
    data1n=ipt.interp1d(time1,data1,time)
    data2n=ipt.interp1d(time2,data2,time)    
    
    #return time and data
    return time,data1n,data2n

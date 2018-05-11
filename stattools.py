from __future__ import division,print_function
import numpy as np
import matplotlib as mpl
import scipy as sp
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import gridtools as gt
import datatools as dt
import plottools as pt
import misctools as mt
np.set_printoptions(precision=16,suppress=True,threshold=np.nan)
import pandas as pd
from collections import OrderedDict




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
    out['skewsl']=1-((sp.stats.skew(obs-mod))/sp.stats.skew(obs))

    out['skill']=1-(np.sum(np.fabs(mod-obs)**2)/(np.sum((np.fabs(mod-modm)+np.fabs(obs-obsm))**2)))
    
    return out
    

def remove_common_nan(in1, in2):
    bidx=np.isnan(in1)+np.isnan(in2)
    
    return in1[~bidx], in2[~bidx]
    
    
    
    
    
    
    

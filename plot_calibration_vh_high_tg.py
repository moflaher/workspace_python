#!/usr/bin/python2.7
# encoding: utf-8

from __future__ import division
from pyseidon import *
from pyseidon.utilities.pyseidon_error import PyseidonError
import os
import glob
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import collections


folder2results=['2012-02-01_2012-03-01_0.01_0.001','2012-02-01_2012-03-01_0.03_0.01']
path2results = 'figures/png/vh_high_2d/calibration_tg/'

savepath=path2results+'stat_plots/'
if not os.path.exists(savepath): os.makedirs(savepath)

fdict=collections.OrderedDict()

# runs
for case in folder2results:
    filename=glob.glob(path2results+case+'/*.csv')
    if len(filename)>1:
        print('There was more then one csv file in ' + case)
    df = pd.read_csv(filename[0])
    
    dfdict={}
    for mtype in df.Type.unique():
            dfdict[mtype]=df.loc[df.Type==mtype]
            
    fdict[case]=dfdict


def calibration_plot(fdict,varname,stat):
    
    f=plt.figure()
    ax=f.add_axes([.125,.2,.775,.7])
    
    ymax=-100000000000000
    ymin=100000000000000
    casenum=[]
    casename=[]
    for i,case in enumerate(fdict):
        ymax=np.max(np.hstack([np.array(fdict[case][varname][stat]),ymax]))
        ymin=np.min(np.hstack([np.array(fdict[case][varname][stat]),ymin]))
        ax.plot(np.zeros((len(fdict[case][varname][stat]),))+i+1,fdict[case][varname][stat],'*b')
        casenum+=[i+1]
        casename+=[case[22:]]
    
          
    
    ax.set_xlim([0,i+2])
    ax.set_ylim([ymin-(ymax-ymin)*.33,ymax+(ymax-ymin)*.33])
    ax.set_xlabel('Case')
    ax.set_ylabel(stat)    
    f.suptitle(varname.title())
    
    casenum=np.array(casenum)    
    ticks=ax.get_xticks()
    ticksstr=[str(val) for val in ticks]
    for i,tick in enumerate(ticks):
        if tick not in casenum:
            ticksstr[i]=''
        else:
            idx=np.argwhere(casenum==tick)
            ticksstr[i]=casename[idx]
    ax.set_xticklabels(ticksstr,rotation=70)  
    
    
    f.savefig(savepath+varname+'_'+stat+'.png',dpi=150)
    plt.close(f)
    
types=['speed', 'dir', 'u', 'v', 'vel', 'cubic_speed']    
stats=['pbias','r2', 'RMSE', 'NOF', 'CF', 'SI', 'bias', 'NRMSE', 'corr', 'POF', 'NSE', 'skill','MDNO', 'SD']    

types=['elev']
stats=['r2', 'RMSE','bias', 'NRMSE', 'corr'] 
for varname in types:
    for stat in stats:
        calibration_plot(fdict,varname,stat)

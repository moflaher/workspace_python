from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from folderpath import *
from fvcomtools import *
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import collections
import pandas as pd




name='template'
grid='sjh_lr_v2_double'



dry=True

if dry:
    data=load_nei2fvcom('/home/suh001/scratch/{}/runs/{}/input/{}.nei'.format(grid,name,grid))
else:
    data=loadnc('/home/suh001/scratch/{}/runs/{}/output/'.format(grid,name),'{}_0001.nc'.format(grid))
    st=0
    et=-1

data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
#data['xc']=data['x'][data['nv']].mean(axis=1)
#data['yc']=data['y'][data['nv']].mean(axis=1)
#data['lonc']=data['lon'][data['nv']].mean(axis=1)
#data['latc']=data['lat'][data['nv']].mean(axis=1)

station=collections.OrderedDict()
obsloc=pd.read_csv('data/NEMO-FVCOM_SaintJohn_BOF_Observations_oct2017_phase1.csv',delimiter=',')

for i,iid in enumerate(obsloc.Num):
    name=iid
    station[str(name)]=[obsloc.Lon[i],obsloc.Lat[i]]
    

station2=collections.OrderedDict() 
 
for key in station:
    print(key)
    xloc,yloc = data['proj'](station[key][0],station[key][1])
    tidx=np.argmin((data['x']-xloc)**2+(data['y']-yloc)**2)
    station2[key]=station[key]+[(tidx+1),data['h'][tidx]]

    if not dry:
        dist=np.sqrt((data['x']-xloc)**2+(data['y']-yloc)**2)
        asort=np.argsort(dist)
        close=0
        while np.sum(data['wet_nodes'][st:et,asort[close]])<len(data['time'][st:et]):
            close+=1 
        node=asort[close]
        if node!=tidx:
            station2[key+'W']=station[key]+[(cell+1),data['h'][node]]
    
if dry:
    drystr='without_wet'
else:
    drystr='with_wet'
    
save_stationfile(station2,'{}_sjh_obs_{}_{}.dat'.format(grid,drystr,time.strftime('%y%m%d')))
 






















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



#data=load_nei2fvcom('/media/moflaher/data/grids/stj_harbour/add_dn/9_makerun_fixcoastline/sjh_hr_v3_fixcoastdepth_dclean_2.nei')
data=loadnc('/home/mif001/scratch/sjh_lr_v1_sub/old/sjh_lr_v1_sub_baroclinic_2/output/','sjh_lr_v1_sub_0001.nc')
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
data['xc']=data['x'][data['nv']].mean(axis=1)
data['yc']=data['y'][data['nv']].mean(axis=1)
et=-1


station=collections.OrderedDict()


obsloc=pd.read_csv('data/NEMO-FVCOM_SaintJohn_BOF_Observations_oct2017_phase1.csv',delimiter=',')

for i,iid in enumerate(obsloc.Num):
    name=iid
    #if 'Tide Gauge' in obsloc.Cat[i]:
        #name='TG_{}'.format(iid)
    #if 'ADCP' in obsloc.Cat[i]:
        #name='ADCP_{}'.format(iid)
    #if 'River' in obsloc.Cat[i]:
        #name='RG_{}'.format(iid) 
    
    #name=name.replace(' ','_').replace('(','').replace(')','')
    
    station[str(name)]=[obsloc.Lon[i],obsloc.Lat[i]]
    
        
print('after')    



station2=collections.OrderedDict() 
 
for key in station:
    print(key)
    xloc,yloc = data['proj'](station[key][0],station[key][1])
    dist=np.sqrt((data['x']-xloc)**2+(data['y']-yloc)**2)
    asort=np.argsort(dist)
    close=0
    while np.sum(data['wet_nodes'][:et,asort[close]])<len(data['time'][:et]):
        close+=1 
    cell=asort[close]

    tidx=np.argmin((data['lon']-station[key][0])**2+(data['lat']-station[key][1])**2)
    if cell!=tidx:
        station2[key+'W']=station[key]+[(cell+1),data['h'][cell]]
    station2[key]=station[key]+[(tidx+1),data['h'][tidx]]
    
    
save_stationfile(station2,'sjh_lr_v1_sub_feb19_wet_nodupe.dat')
 

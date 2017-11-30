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



data=load_nei2fvcom('/media/moflaher/data/grids/stj_harbour/add_dn/9_makerun_fixcoastline/sjh_hr_v3_fixcoastdepth_dclean_2.nei')
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])

station=collections.OrderedDict()


obsloc=pd.read_csv('/mnt/drive_0/misc/NEMO-FVCOM_SaintJohn_BOF_Observations_timeseries.txt',delimiter=' ')
obsloc2=pd.read_csv('/mnt/drive_0/misc/NEMO-FVCOM_SaintJohn_BOF_Observations_ctd.txt',delimiter=' ')


for i,iid in enumerate(obsloc.deploy):
    name=iid
    #if 'Tide Gauge' in obsloc.Cat[i]:
        #name='TG_{}'.format(iid)
    #if 'ADCP' in obsloc.Cat[i]:
        #name='ADCP_{}'.format(iid)
    #if 'River' in obsloc.Cat[i]:
        #name='RG_{}'.format(iid) 
    
    name=name.replace(' ','_').replace('(','').replace(')','')
    
    station[name]=[obsloc.lon[i],obsloc.lat[i]]
    
    
for i,iid in enumerate(obsloc2.deploy):
    name=iid
    #if 'Tide Gauge' in obsloc.Cat[i]:
        #name='TG_{}'.format(iid)
    #if 'ADCP' in obsloc.Cat[i]:
        #name='ADCP_{}'.format(iid)
    #if 'River' in obsloc.Cat[i]:
        #name='RG_{}'.format(iid) 
    
    name=name.replace(' ','_').replace('(','').replace(')','')
    
    station[name]=[obsloc2.lon[i],obsloc2.lat[i]]
        
    

  
for key in station:
    if 'TC' in key:
        xloc,yloc = data['proj'](station[key][0]station[key][1])
        dist=np.sqrt((data['xc']-xloc)**2+(data['yc']-yloc)**2)
        asort=np.argsort(dist)
        close=0
        while np.sum(data['wet_cells'][:,asort[close]])<len(data['time']):
            close+=1 
        node=asort[close]
    
    tidx=np.argmin((data['lonc']-station[key][0])**2+(data['latc']-station[key][1])**2)
    station[key]+=[tidx,data['uvh'][tidx]]
    
    
save_stationfile(station,'/media/moflaher/data/grids/stj_harbour/add_dn/9_makerun_fixcoastline/sjh_hr_v3_stationfile.dat')
    
    
    
    
    
    
    
    

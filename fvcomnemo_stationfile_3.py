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



data=load_nei2fvcom('/media/moflaher/data/grids/stj_harbour/sjh_lr_v1_subdomain/makerun/sjh_lr_v1_sub_r.nei')
#data=load_nei2fvcom('/media/moflaher/data/grids/stj_harbour/add_dn/10_wet/new_wet_hr.nei')
#data=loadnc('/home/suh001/scratch/sjh_lr_v1/runs/sjh_lr_v1_jul2015_nest_noriverspg/output/','sjh_lr_v1_0001.nc')
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
data['xc']=data['x'][data['nv']].mean(axis=1)
data['yc']=data['y'][data['nv']].mean(axis=1)


station=collections.OrderedDict()


obsloc=pd.read_csv('/mnt/drive_1/obs_data/NEMO-FVCOM_SaintJohn_BOF_Observations_oct2017_phase1.csv',delimiter=',')

for i,iid in enumerate(obsloc.Num):
    name=iid
    #if 'Tide Gauge' in obsloc.Cat[i]:
        #name='TG_{}'.format(iid)
    #if 'ADCP' in obsloc.Cat[i]:
        #name='ADCP_{}'.format(iid)
    #if 'River' in obsloc.Cat[i]:
        #name='RG_{}'.format(iid) 
    
    #name=name.replace(' ','_').replace('(','').replace(')','')
    
    station[name]=[obsloc.Lon[i],obsloc.Lat[i]]
    
        
print('after')    

station2={} 
 
for key in station:
    print(key)

    tidx=np.argmin((data['lon']-station[key][0])**2+(data['lat']-station[key][1])**2)
    station2[key]=station[key]+[tidx+1,data['h'][tidx]]
    
    
save_stationfile(station2,'sjh_lr_v1_sub_stationfile_feb15.dat')
 

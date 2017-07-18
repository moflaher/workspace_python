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



data=loadnc('/media/moflaher/runs/sjh_hr_v2/sjh_hr_v2_2_0.5/output','sjh_hr_v2_0001.nc')


station=collections.OrderedDict()


obsloc=pd.read_csv('/mnt/drive_1/obs_data/NEMO-FVCOM_SaintJohn_BOF_Observations_clean.csv')

for i,iid in enumerate(obsloc.InstrumentID):
    name=iid
    if 'Tide Gauge' in obsloc.Cat[i]:
        name='TG_{}'.format(iid)
    if 'ADCP' in obsloc.Cat[i]:
        name='ADCP_{}'.format(iid)
    if 'River' in obsloc.Cat[i]:
        name='RG_{}'.format(iid) 
    
    name=name.replace(' ','_').replace('(','').replace(')','')
    
    station[name]=[obsloc.Lon[i],obsloc.Lat[i]]
    
    
    
    

  
for key in station:
    tidx=np.argmin((data['lonc']-station[key][0])**2+(data['latc']-station[key][1])**2)
    station[key]+=[tidx,data['uvh'][tidx]]
    
    
save_stationfile(station,'sjh_hr_v2_stationfile.dat')
    
    
    
    
    
    
    
    

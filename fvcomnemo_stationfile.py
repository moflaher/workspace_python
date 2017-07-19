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



data=load_nei2fvcom('../dfo/grids/stj_harbour/add_dn/6_makerun/sjh_hr_v3_clean/input/sjh_hr_v3.nei')


station=collections.OrderedDict()


obsloc=pd.read_csv('data/misc/NEMO-FVCOM_SaintJohn_BOF_Observations_clean.csv')

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
    
    
save_stationfile(station,'../dfo/grids/stj_harbour/add_dn/6_makerun/sjh_hr_v3_clean/input/sjh_hr_v3_stationfile.dat')
    
    
    
    
    
    
    
    

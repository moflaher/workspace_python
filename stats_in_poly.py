from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from folderpath import *
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
from stattools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pandas as pd
import netCDF4 as n4
import copy
import matplotlib.dates as dates
import argparse
import matplotlib.path as path


data=loadnc('/home/suh001/scratch/passbay_v4/runs/passbay_v4_sjr_flow_limiter_test.2/output','passbay_v4_0001.nc')


farmslat=np.array([[44,39,27.69],
                   [44,39,28.17],
                   [44,39,22.82],
                   [44,38,59.59],
                   [44,38,58.53],
                   [44,39,18.77]])
farmslon=np.array([[65,45,24.29],
                   [65,45,15.70],
                   [65,45,12.46],
                   [65,45,09.59],
                   [65,45,26.32],
                   [65,45,27.03]])



lat=farmslat[:,0]+farmslat[:,1]/60.0+farmslat[:,2]/3600.0
lon=farmslon[:,0]+farmslon[:,1]/60.0+farmslon[:,2]/3600.0
lon=-1*lon


#ft=data['trigrid'].get_trifinder()
#host=ft(data['lonc'],data['latc'])


p=path.Path(np.vstack([lon,lat]).T)
    
    
#find points in path and remove and return as array
idx=p.contains_points(np.array([data['lonc'],data['latc']]).T)    
idxa=p.contains_points(np.array([data['lon'],data['lat']]).T)

ua=data['ua'][:,idx]
#print('ua')
#print(ua.min(),ua.max(),ua.mean(),np.percentile(ua,[10,90]))
va=data['va'][:,idx]
#print('va')
#print(va.min(),va.max(),va.mean(),np.percentile(va,[10,90]))
kill
#zeta=data['zeta'][:,idxa]
#print('zeta')
#print(zeta.min(),zeta.max(),zeta.mean(),np.percentile(zeta,[10,90]))

#speed=np.sqrt(ua**2+va**2)
#print('speed')
#print(speed.min(),speed.max(),speed.mean(),np.percentile(speed,[10,90]))

ua=data['u'][:,-1,idx]
print('u')
print(ua.min(),ua.max(),ua.mean(),np.percentile(ua,[10,90]))
va=data['v'][:,-1,idx]
print('v')
print(va.min(),va.max(),va.mean(),np.percentile(va,[10,90]))

speed=np.sqrt(ua**2+va**2)
print('speed noda')
print(speed.min(),speed.max(),speed.mean(),np.percentile(speed,[10,90]))

farmsoldlat=np.array([[44,39,20.34],
		   [44,39,20.40],
		   [44,39,08.76],
           [44,39,05.52],
           [44,39,05.40]])
farmsoldlon=np.array([[65,45,27.36],
		   [65,45,20.10],
		   [65,45,17.64],
           [65,45,17.58],
           [65,45,27.06]])

latold=farmsoldlat[:,0]+farmsoldlat[:,1]/60.0+farmsoldlat[:,2]/3600.0
lonold=farmsoldlon[:,0]+farmsoldlon[:,1]/60.0+farmsoldlon[:,2]/3600.0

lonold=-1*lonold


p=path.Path(np.vstack([lonold,latold]).T)
    
    
#find points in path and remove and return as array
idx=p.contains_points(np.array([data['lonc'],data['latc']]).T)    
idxa=p.contains_points(np.array([data['lon'],data['lat']]).T)

#ua=data['ua'][:,idx]
#print('ua')
#print(ua.min(),ua.max(),ua.mean(),np.percentile(ua,[10,90]))
#va=data['va'][:,idx]
#print('va')
#print(va.min(),va.max(),va.mean(),np.percentile(va,[10,90]))

#zeta=data['zeta'][:,idxa]
#print('zeta')
#print(zeta.min(),zeta.max(),zeta.mean(),np.percentile(zeta,[10,90]))


#speed=np.sqrt(ua**2+va**2)
#print('speed')
#print(speed.min(),speed.max(),speed.mean(),np.percentile(speed,[10,90]))

ua=data['u'][:,-1,idx]
print('u')
print(ua.min(),ua.max(),ua.mean(),np.percentile(ua,[10,90]))
va=data['v'][:,-1,idx]
print('v')
print(va.min(),va.max(),va.mean(),np.percentile(va,[10,90]))

speed=np.sqrt(ua**2+va**2)
print('speed noda')
print(speed.min(),speed.max(),speed.mean(),np.percentile(speed,[10,90]))











# u=data['u'][:,:,idx]
# print('u')
# print(u.min(axis=0),u.max(axis=0),u.mean(axis=0),np.percentile(u,[10,90]))
# v=data['v'][:,:,idx]
# print('v')
# print(v.min(axis=0),v.max(axis=0),v.mean(axis=0),np.percentile(v,[10,90]))

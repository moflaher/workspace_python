from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from folderpath import *
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
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


# Define names and types of data
name='sjh_lr_v1_jul2015_nogotm_jcool1'
grid='sjh_lr_v1'
datatype='2d'


### load the .nc file #####
#data = loadnc(runpath+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data = loadnc('/fs/vnas_Hdfo/odis/mif001/scratch/sjh_lr_v1/{}/output/'.format(name),singlename=grid + '_0001.nc')
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
print('done load')

ctd=pd.read_csv('~/R_scripts/ctd.txt')


deploy=ctd.deploy.astype(int)
lon=ctd.lon.astype(float)
lat=ctd.lat.astype(float)
locations=np.vstack([lon,lat]).T
time=np.empty((len(ctd.date),),dtype='S26')
for i,d in enumerate(ctd.date):
    time[i]='{} {}'.format(d,ctd.time[i])





savepath='{}/{}_{}/ctd/{}/'.format(datapath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)


for i,loc in enumerate(locations):
    print('='*80)
    print(i)
    xloc,yloc = data['proj'](loc[0],loc[1])

    dist=np.sqrt((data['x']-xloc)**2+(data['y']-yloc)**2)
    asort=np.argsort(dist)
    node=asort[0]

    print(dist[node])
    timenum=dates.datestr2num(time[i])

    t=np.argmin(np.fabs(data['time']-timenum))


    temp=data['temp'][t,:,node]
    sal=data['salinity'][t,:,node]
    d=(data['zeta'][t,node]+data['h'][node])*data['siglay'][:,0]

    fp=open('{}ctd_{}.txt'.format(savepath,deploy[i]),'w')
    fp.write('node latitude longitue date time depth temperature salinity\n')
    for j,tem in enumerate(temp):
        fp.write('{} {} {} {} {} {} {} {}\n'.format(node+1,lat[i],lon[i],data['Time'][t][:10],data['Time'][t][11:19],d[j],temp[j],sal[j]))

    fp.close()


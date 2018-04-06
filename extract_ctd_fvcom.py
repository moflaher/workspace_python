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
name='test01'
grid='sjh_lr_v1'
datatype='2d'


### load the .nc file #####
#data = loadnc(runpath+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
#data = loadnc('/fs/vnas_Hdfo/odis/mif001/scratch/sjh_lr_v1/testing/{}/output/'.format(name),singlename=grid + '_0001.nc')
data = loadnc('/gpfs/fs1/dfo/dfo_odis/yow001/BoF/{}/output/'.format(name),grid + '_0001_SST.nc')
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
print('done load')


ctdbio=pd.read_csv('/home/suh001/data/NEMO-FVCOM_SaintJohn_BOF_Observations_ctd_BIO.txt',delimiter=' ')
ctdsabs=pd.read_csv('/home/suh001/data/NEMO-FVCOM_SaintJohn_BOF_Observations_ctd_SABS.txt',delimiter=' ')
 
lon=np.append(ctdbio['lon'],ctdsabs['lon'])
lat=np.append(ctdbio['lat'],ctdsabs['lat'])
locations=np.vstack([lon,lat]).T
deploy=np.append(ctdbio['deploy'],ctdsabs['deploy'])
Time=np.append(['{} {}'.format(ctdbio['date'][i],ctdbio['time'][i]) for i in range(len(ctdbio['lon']))],
               ['{} {}'.format(ctdsabs['date'][i],ctdsabs['time'][i]) for i in range(len(ctdsabs['lon']))])
time=dates.datestr2num(Time)


savepath='{}/{}_{}/ctd/{}/'.format(datapath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)


for i,dep in enumerate(deploy):
    print('='*80)
    print(i)
    print(dep)
    xloc,yloc = data['proj'](lon[i],lat[i])

    dist=np.sqrt((data['x']-xloc)**2+(data['y']-yloc)**2)
    asort=np.argsort(dist)
    node=asort[0]

    print(node)
    print(dist[node])

    tidx=np.argwhere((data['time']>=time[i]-3/24.0) &(data['time']<=time[i]+3/24.0) )
    temp=data['temp'][tidx,:,node]
    sal=data['salinity'][tidx,:,node]
    d=(data['zeta'][tidx,node]+data['h'][node])*data['siglay'][:,0]
    
    fp=open('{}ctd_timeseries_{}.txt'.format(savepath,deploy[i]),'w')
    fp.write('node it latitude longitue date time depth temperature salinity\n')
    for k,t in enumerate(tidx):
        for j,tem in enumerate(temp[k,0,]):
            fp.write('{} {} {} {} {} {} {} {} {}\n'.format(node+1,t[0],data['lat'][node],data['lon'][node],data['Time'][t[0]][:10],data['Time'][t[0]][11:19],d[k,j],temp[k,0,j],sal[k,0,j]))
    fp.close()



    tidx=np.argmin(np.fabs(data['time']-time[i]))
    temp=data['temp'][tidx,:,node]
    sal=data['salinity'][tidx,:,node]
    d=(data['zeta'][tidx,node]+data['h'][node])*data['siglay'][:,0]
    
    fp=open('{}ctd_{}.txt'.format(savepath,deploy[i]),'w')
    fp.write('node latitude longitue date time depth temperature salinity\n')
    for j,tem in enumerate(temp):
        fp.write('{} {} {} {} {} {} {} {}\n'.format(node+1,data['lat'][node],data['lon'][node],data['Time'][tidx][:10],data['Time'][tidx][11:19],d[j],temp[j],sal[j]))
    fp.close()



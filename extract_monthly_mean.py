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
name='sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1_jcool0'
grid='sjh_lr_v1'
datatype='2d'


### load the .nc file #####
data = loadnc('/fs/vnas_Hdfo/odis/suh001/scratch/sjh_lr_v1/runs/{}/output/'.format(name),singlename=grid + '_0001.nc')
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
print('done load')




#times=np.array(['2015-02-01T12:00:00','2015-03-01T00:00:00','2015-04-01T00:00:00','2015-05-01T00:00:00','2015-03-01T00:00:00','2015-03-01T00:00:00','2015-03-01T00:00:00'])
times=['2015-02-01T12:00:00']
for i in range(3,13):
    times+=['2015-{:02d}-01T00:00:00'.format(i)]
for i in range(1,6):
    times+=['2016-{:02d}-01T00:00:00'.format(i)]

time=dates.datestr2num(times)


savepath='{}/{}_{}/monthly_mean_surface/{}/'.format(datapath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)


for i in range(len(time)):
    print('='*80)
    print('{} to {}'.format(times[i],times[i+1]))

    t=np.argwhere((data['time']>=time[i])&(data['time']<time[i+1]))

    temp=np.ravel(data['temp'][t,0,:].mean(axis=0))
    sal=np.ravel(data['salinity'][t,0,:].mean(axis=0))
    zeta=np.ravel(data['zeta'][t,:].mean(axis=0))
    u=data['u'][t,0,:]
    v=data['v'][t,0,:]
    surf_speed=np.ravel(np.sqrt(u**2+v**2).mean(axis=0))
    da_speed=np.ravel(np.sqrt(data['ua'][t,:]**2+data['va'][t,:]**2).mean(axis=0))


    fp=open('{}node_fields_{}_to_{}.dat'.format(savepath,times[i],times[i+1]),'w')
    fp.write('node lon lat zeta temp sal\n')
    for j,tem in enumerate(temp):
        fp.write('{} {} {} {} {} {}\n'.format(j+1,data['lon'][j],data['lat'][j],zeta[j],temp[j],sal[j]))
    fp.close()

    fp=open('{}cell_fields_{}_to_{}.dat'.format(savepath,times[i],times[i+1]),'w')
    fp.write('cell lon lat surf_speed da_speed\n')
    for j,tem in enumerate(surf_speed):
        fp.write('{} {} {} {} {}\n'.format(j+1,data['uvnodell'][j,0],data['uvnodell'][j,1],surf_speed[j],da_speed[j]))
    fp.close()

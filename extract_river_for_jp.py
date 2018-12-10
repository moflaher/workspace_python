from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
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
import ttide


# Define names and types of data
name='sjh_lr_v1_year_origbc_wet_hfx100'
grid='sjh_lr_v1'

starttime=0
endtime=25


### load the .nc file #####
data = loadnc('/fs/vnas_Hdfo/odis/suh001/scratch/sjh_lr_v1/runs/{}/output/'.format(name),singlename=grid + '_0001.nc')
print('done load')

elobc=loadnc('/fs/vnas_Hdfo/odis/suh001/scratch/sjh_lr_v1/runs/{}/input/el_obc_all/'.format(name),'sjh_lr_v1_el_obc_webtide_riops_hourly_detide_oak_point_1feb2015-1jun2016.nc',False)




obc=elobc['obc_nodes'][-4:]-1


x=data['x'][obc]
y=data['y'][obc]


h=data['h'][obc]
d=np.sqrt(np.diff(x)**2+np.diff(y)**2)

area=np.zeros((3,))

for i in range(3):
    hmin=np.min([h[i],h[i+1]])
    htri=np.fabs(h[i]-h[i+1])
    area[i]=hmin*d[i]		
    area[i]+=htri*d[i]*.5



print(area)
print(np.sum(area))


time=elobc['Itime']+elobc['Itime2']/(24*60*60*1000.0)
el=elobc['elevation'][:,-1]

arr=np.vstack([time,el]).T
save_array(arr,'jp_river_timeseries.dat')















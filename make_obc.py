from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import netCDF4 as n4
import scipy.interpolate as interp
from gridtools import _load_nc
import copy



# Define names and types of data
name='kit4_kelp_20m_0.018'
grid='kit4'


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')
indata=load_fvcom_files('runs/'+grid+'/'+name+'/input','kit4','kit4_non_julian_obc.nc')
elobc_old=_load_nc('runs/'+grid+'/'+name+'/input/kit4_non_julian_obc.nc')

# Define names and types of data
filename='kit4_wave_nnh.nei'


neifile=loadnei('data/grid_stuff/'+filename)
neifile=get_nv(neifile)
nn=sort_boundary(neifile)




startidx=np.argwhere(nn==30659)
obc=nn[startidx:(startidx+48)]
startidx=np.argwhere(nn==13218)
obc=np.append(obc,nn[startidx:(startidx+81)])


#plot to check obc nodes
#f=plt.figure()
#ax=f.add_axes([.125,.1,.775,.8])
#ax.triplot(neifile['trigrid'],lw=.15,color='b')
#plotcoast(ax,filename='world_GSHHS_f_L1.nc',color='k',fill=True)
#ax.scatter(neifile['lon'][obc-1],neifile['lat'][obc-1],s=20,edgecolor='None',c='r')
#ax.axis([-132.5,-127,50.5,56])
#f.show()

dataout={}
dataout['spgf_num']=len(obc)
dataout['spgf_nodes']=(obc).astype(int)
dataout['spgf_distance']=np.zeros((len(obc),))+15000
dataout['spgf_value']=np.zeros((len(obc),))+0.000100

dataout['obcf_num']=len(obc)
dataout['obcf_numbers']=(np.arange(len(obc))+1).astype(int)
dataout['obcf_nodes']=(obc).astype(int)
dataout['obcf_value']=(np.zeros((len(obc),))+1).astype(int)

save_obcfile(dataout,'data/grid_stuff/','kit4_wave')
save_spgfile(dataout,'data/grid_stuff/','kit4_wave')

obcold=elobc_old['obc_nodes']-1
elobc=copy.deepcopy(elobc_old)

elobc['obc_nodes']=obc



var='tide_Ephase'
tmp=np.empty((len(elobc[var]),len(obc)))
for level in range(len(elobc_old[var])):
    nn_tmp=interp.NearestNDInterpolator((data['nodell'][obcold,0],data['nodell'][obcold,1]), elobc_old[var][level,:])
    tmp[level,:]=nn_tmp.__call__(neifile['nodell'][obc-1,0],neifile['nodell'][obc-1,1])
elobc[var]=tmp

var='tide_Eamp'
tmp=np.empty((len(elobc[var]),len(obc)))
for level in range(len(elobc_old[var])):
    nn_tmp=interp.NearestNDInterpolator((data['nodell'][obcold,0],data['nodell'][obcold,1]), elobc_old[var][level,:])
    tmp[level,:]=nn_tmp.__call__(neifile['nodell'][obc-1,0],neifile['nodell'][obc-1,1])
elobc[var]=tmp

var='tide_Eref'
tmp=np.empty((len(obc),))
nn_tmp=interp.NearestNDInterpolator((data['nodell'][obcold,0],data['nodell'][obcold,1]), elobc_old[var])
tmp=nn_tmp.__call__(neifile['nodell'][obc-1,0],neifile['nodell'][obc-1,1])
elobc[var]=tmp

save_elobc(elobc,'data/grid_stuff/kit4_wave_el_obc.nc')


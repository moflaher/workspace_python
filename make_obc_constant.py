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
casename='kelpchannel'
filename='kelpchannel.nei'
filepath='data/kelp_ideal/xy_5/makerun/input/'

neifile=loadnei(filepath+filename)
neifile=get_nv(neifile)
nn=sort_boundary(neifile)


nnloop=np.append(nn,nn)

startidx=np.argwhere(nn==100755) #99541
obc1=nnloop[startidx:(startidx+21)]
startidx=np.argwhere(nn==99621)#100835
obc2=nnloop[startidx:(startidx+21)]

obc=np.append(obc1,obc2)

#plot to check obc nodes
f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.triplot(neifile['trigrid'],lw=.15,color='b')
#plotcoast(ax,filename='world_GSHHS_f_L1.nc',color='k',fill=True)
ax.scatter(neifile['lon'][obc1-1],neifile['lat'][obc1-1],s=20,edgecolor='None',c='r')
ax.scatter(neifile['lon'][obc2-1],neifile['lat'][obc2-1],s=20,edgecolor='None',c='g')
f.show()

dataout={}
dataout['spgf_num']=0
dataout['spgf_nodes']=(obc).astype(int)
dataout['spgf_distance']=np.zeros((len(obc),))+0
dataout['spgf_value']=np.zeros((len(obc),))+0.0000

dataout['obcf_num']=len(obc)
dataout['obcf_numbers']=(np.arange(len(obc))+1).astype(int)
dataout['obcf_nodes']=(obc).astype(int)
dataout['obcf_value']=(np.zeros((len(obc),))+1).astype(int)

save_obcfile(dataout,filepath,casename)
save_spgfile(dataout,filepath,casename)

elobc={}
elobc['obc_nodes']=obc
elobc['tide_period']=np.array([44712])
elobc['tide_Eref']=np.append( np.zeros((len(obc1),))+.05, np.zeros((len(obc2),)))
elobc['tide_Ephase']=elobc['tide_Eref']*0
elobc['tide_Eamp']=elobc['tide_Eref']*0
elobc['equilibrium_tide_Eamp']=np.array([0])
elobc['equilibrium_beta_love']=np.array([0])
elobc['equilibrium_tide_type']=np.atleast_2d(np.array([x for x in "SEMIDIURNAL               "]))
elobc['time_origin']="0.0"


save_elobc(elobc,filepath+casename+'_el_obc.nc')


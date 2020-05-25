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
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)




data=loadnc('/fs/hnas1-evs1/Ddfo/dfo_odis/suh001/sjh_lr_v1/runs/sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1/output/','sjh_lr_v1_0001.nc')
data=ncdatasort(data,trifinder=True)
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])


nemo=loadnc('/space/hall0/sitestore/dfo/odis/jpp001/FOR_SUSAN/','Bathymetry_SJAP100_NEW_range_0.5_7m_smooth_BDYN_notip_deep.nc',False)

nemo['x'],nemo['y']=data['proj'](np.ravel(nemo['nav_lon']),np.ravel(nemo['nav_lat']))

xx=np.arange(nemo['x'].min(),nemo['x'].max(),50)
yy=np.arange(nemo['y'].min(),nemo['y'].max(),50)
XX,YY=np.meshgrid(xx,yy)

print(np.ravel(XX).shape)

lon,lat=data['proj'](np.ravel(XX),np.ravel(YY),inverse=True)

host=data['trigrid_finder'](lon,lat)

a=host!=-1
idx=np.argwhere(host!=-1)
print(a.sum())

f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.scatter(lon[idx],lat[idx],c='r')
#f.show()
	
np.savetxt('data/nemofvcom_100m_grid_particles_50m.dat',np.vstack([lon,lat]).T,fmt='%.12f')
np.savetxt('data/nemofvcom_100m_grid_particles_50m_fvcom.dat',np.hstack([lon[idx],lat[idx]]),fmt='%.12f')

boxll=regions('stjohn_harbour')['region']
boxll[0]=-66.125
boxll[1]=-65.96
boxll[2]=45.16
boxx,boxy=data['proj'](boxll[:2],boxll[2:])
xx=np.arange(boxx.min(),boxx.max(),10)
yy=np.arange(boxy.min(),boxy.max(),10)
XX,YY=np.meshgrid(xx,yy)

print(np.ravel(XX).shape)

lon,lat=data['proj'](np.ravel(XX),np.ravel(YY),inverse=True)

host=data['trigrid_finder'](lon,lat)

a=host!=-1
idx=np.argwhere(host!=-1)
print(a.sum())

#f=plt.figure()
#ax=f.add_axes([.125,.1,.775,.8])
ax.scatter(lon[idx],lat[idx],c='b')
f.show()


np.savetxt('data/nemofvcom_stjohn_particles_10m.dat',np.vstack([lon,lat]).T,fmt='%.12f')
np.savetxt('data/nemofvcom_stjohn_particles_10m_fvcom.dat',np.hstack([lon[idx],lat[idx]]),fmt='%.12f')

 

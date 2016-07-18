from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
from misctools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import time
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import matplotlib.path as path
import netCDF4 as n4

# Define names and types of data
name='2012-02-01_2012-03-01_0.01_0.001'
grid='vh_high'
datatype='2d'
region={}
#vh_high
#region['region']=np.array([-123.17,-122.96,49.26,49.33])
#stjohn
region['region']=np.array([-66.17,-65.96,45.18,45.29])
starttime=0
endtime=23
stride=1
outputpath='data/enav/stjohn_24hourby1hour_spacing_0.00025.nc'



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
#data = loadnc('data/enav/',singlename='sfm5m_sjr_ua_va_15feb2003.nc')
print('done load')
data = ncdatasort(data,trifinder=True)
print('done sort')

lona=np.arange(region['region'][0],region['region'][1],.00025)
lata=np.arange(region['region'][2],region['region'][3],.00025)

lon,lat=np.meshgrid(lona,lata)

LON=lon.flatten()
LAT=lat.flatten()

print(LON.shape)

#proj=gridproj(grid)
_,_,proj = lcc(data['lon'],data['lat'])
x,y = proj(LON,LAT)




length=len(range(starttime,endtime,stride))

ua=np.empty((length,len(x)))
va=np.empty((length,len(x)))

for i,timein in enumerate(range(starttime,endtime,stride)):
    print(i)
    print(timein)
    ua[i,:]=ipt.interpEfield_locs(data,'ua',np.array([x, y]).T,timein)
    va[i,:]=ipt.interpEfield_locs(data,'va',np.array([x, y]).T,timein)


hosts=data['trigrid_finder'].__call__(LON,LAT)
host=hosts==-1
host=host.astype(bool)

i=0
u=np.ma.masked_array(ua[i,:],host)
v=np.ma.masked_array(va[i,:],host)

f=plt.figure()
ax=plt.subplot(111)
ax.pcolormesh(lon,lat,speeder(u,v).reshape(lon.shape))
f.show()

#tt=1000
##tt +=4
#f2=plt.figure()
#ax2=plt.subplot(111)
#ax2.tripcolor(data['trigrid'],speeder(data['ua'][tt,:],data['va'][tt,:]))
#f2.show()

ncid=n4.Dataset(outputpath,'w',format='NETCDF3_64BIT')
ncid.createDimension('time',length)        
ncid.createDimension('lon_dim',lon.shape[1])
ncid.createDimension('lat_dim',lon.shape[0])

ncid.createVariable('lon','d',('lat_dim','lon_dim'))
ncid.createVariable('lat','d',('lat_dim','lon_dim'))
ncid.createVariable('landmask','b',('lat_dim','lon_dim'))
ncid.createVariable('ua','d',('time','lat_dim','lon_dim'))
ncid.createVariable('va','d',('time','lat_dim','lon_dim'))
ncid.createVariable('time','d',('time'))
ncid.__setattr__('history','Created on ' +time.ctime(time.time()) + '.' )

#save grid and velocities

ncid.variables['lon'][:]=lon
ncid.variables['lat'][:]=lat
ncid.variables['landmask'][:]=host.reshape(lon.shape)
for i,timein in enumerate(range(starttime,endtime,stride)):
    ncid.variables['ua'][i,:]=ua[i,:].reshape(lon.shape)
    ncid.variables['va'][i,:]=va[i,:].reshape(lon.shape)
    ncid.variables['time'][i]=data['time'][timein]
    
ncid.close()



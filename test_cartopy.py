from __future__ import division
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeat


# Define names and types of data
name='kit4_45days_3'
grid='kit4'
regionname='kit4'
datatype='2d'



### load the .nc file #####
data = loadnc('/media/moflaher/My Book/kit4_runs/' + name + '/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'


region=regions(regionname)





plt.close()

# Plot mesh
ax=plt.axes(projection=ccrs.GOOGLE_MERCATOR())
ax.coastlines(resolution='10m')
ax.gridlines(draw_labels=True)
ax.set_extent(region['region'])
#plt.axis(region['region'],)
ax.plot(data['nodell'][:,0],data['nodell'][:,1],'.',transform=ccrs.Geodetic())

plt.show()



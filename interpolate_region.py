from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
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
import time
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import matplotlib.path as path

# Define names and types of data
name='2012-02-01_2012-03-01_0.01_0.001'
grid='vh_high'
datatype='2d'
region={}
region['region']=np.array([-123.17,-122.96,49.26,49.33])
starttime=1000
endtime=1095
stride=4
forward=False



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

x=np.arange(region['region'][0],region['region'][1],.0001)
y=np.arange(region['region'][2],region['region'][3],.0001)

xx,yy=np.meshgrid(x,y)

XX=xx.flatten()
YY=yy.flatten()

print(XX.shape)

length=len(range(starttime,endtime,stride))

ua=np.empty((length,len(XX)))
va=np.empty((length,len(XX)))

for i,time in enumerate(range(starttime,endtime,stride)):
    print(i)
    print(time)
    ua[i,:]=ipt.interpEfield_locs(data,'ua',np.array([XX, YY]).T,time,ll=True)
    va[i,:]=ipt.interpEfield_locs(data,'va',np.array([XX, YY]).T,time,ll=True)


hosts=data['trigrid_finder'].__call__(XX,YY)
host=hosts==-1
host=host.astype(bool)

i=2
u=np.ma.masked_array(ua[i,:],host)
v=np.ma.masked_array(va[i,:],host)

f=plt.figure()
ax=plt.subplot(111)
ax.pcolormesh(xx,yy,speeder(u,v).reshape(xx.shape))
f.show()

tt=1000
#tt +=4
f2=plt.figure()
ax2=plt.subplot(111)
ax2.tripcolor(data['trigrid'],speeder(data['ua'][tt,:],data['va'][tt,:]))
f2.show()




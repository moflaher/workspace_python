from __future__ import division
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


# Define names and types of data
name1='kit4_45days_3'
name2='kit4_kelp_0.1'
grid='kit4'
regionname='gilisland'
datatype='2d'
starttime=384
cmin=0
cmax=5


### load the .nc file #####
data1 = loadnc('/media/moflaher/My Book/kit4_runs/' + name1 +'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('/media/moflaher/My Book/kit4_runs/' + name2 +'/output/',singlename=grid + '_0001.nc')
print 'done load'
data1 = ncdatasort(data1)
data2 = ncdatasort(data2)
print 'done sort'


cages=np.genfromtxt('/media/moflaher/My Book/kit4_runs/' +name2+ '/input/kit4_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)


region=regions(regionname)
nidx=get_nodes(data1,region)

savepath='figures/timeseries/' + grid + '_' + datatype + '/speed_difference_relative/' + name1 + '_' +name2 + '_' + regionname + '_' +("%d" %cmin) + '_' + ("%d" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)




plt.close()
# Plot mesh
plt.tripcolor(data1['trigrid'],data1['h'],vmin=data1['h'][nidx].min(),vmax=data1['h'][nidx].max())
plt.plot(data1['uvnodell'][cages,0],data1['uvnodell'][cages,1],'k.',markersize=2)
plt=prettyplot_ll(plt,setregion=region,grid=True)
plt.colorbar()
plt.savefig(savepath + grid + '_' + regionname +'_cage_locations.png',dpi=1200)


plt.close()
# Plot mesh
for i in range(starttime,len(data1['time'])):
    print i
    plt.tripcolor(data1['trigrid'],100*np.fabs(np.sqrt(data1['ua'][i,:]**2+data1['va'][i,:]**2)-np.sqrt(data2['ua'][i,:]**2+data2['va'][i,:]**2))/np.sqrt(data1['ua'][i,:]**2+data1['va'][i,:]**2),vmin=cmin,vmax=cmax)
    #plt.plot(data1['uvnodell'][cages,0],data1['uvnodell'][cages,1],'k.',markersize=.5)
    plt=prettyplot_ll(plt,setregion=region,grid=True)
    plt.colorbar()
    plt.savefig(savepath + grid + '_' + regionname +'_speeddiff_' + ("%04d" %(i)) + '.png',dpi=300)
    plt.close()
































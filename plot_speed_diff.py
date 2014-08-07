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


# Define names and types of data
name1='kit4_45days_3'
name2='kit4_kelp_0.001'
grid='kit4'
regionname='fasttip'
datatype='2d'
starttime=384
cmin=-0.001
cmax=0.001


### load the .nc file #####
data1 = loadnc('/media/moflaher/My Book/kit4_runs/' + name1 +'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('/media/moflaher/My Book/kit4_runs/' + name2 +'/output/',singlename=grid + '_0001.nc')
print 'done load'
data1 = ncdatasort(data1)
data2 = ncdatasort(data2)
print 'done sort'


cages=np.genfromtxt('/media/moflaher/My Book/kit4_runs/kit4_kelp_0.001/input/kit4_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)


region=regions(regionname)

savepath='figures/timeseries/' + grid + '_' + datatype + '/speed_diff/' + name1 + '_' +name2 + '_' + regionname + '_' +("%d" %cmin) + '_' + ("%d" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)


plt.close()
# Plot mesh
for i in range(starttime,len(data1['time'])):
    print i
    plt.tripcolor(data1['trigrid'],np.sqrt(data1['ua'][i,:]**2+data1['va'][i,:]**2)-np.sqrt(data2['ua'][i,:]**2+data2['va'][i,:]**2),vmin=cmin,vmax=cmax)
    plt.plot(data1['uvnodell'][cages,0],data1['uvnodell'][cages,1],'k.',markersize=2)
    plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
    plt.grid()
    plt.colorbar()
    plt.axis(region['region'])
    plt.savefig(savepath + grid + '_' + regionname +'_speeddiff_' + ("%04d" %(i)) + '.png',dpi=300)
    plt.close()
































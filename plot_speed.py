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
name='kit4_kelp_0.1'
grid='kit4'
regionname='fasttip_back'
datatype='2d'
starttime=300
endtime=384
cmin=0
cmax=1


### load the .nc file #####
data = loadnc('/media/moflaher/My Book/kit4_runs/' + name + '/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'


region=regions(regionname)

savepath='figures/timeseries/' + grid + '_' + datatype + '/speed/' + name + '_' + regionname + '_' +("%d" %cmin) + '_' + ("%d" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)
plt.close()

# Plot mesh
for i in range(starttime,len(data['time'])):
    print i
    plt.tripcolor(data['trigrid'],np.sqrt(data['ua'][i,:]**2+data['va'][i,:]**2),vmin=cmin,vmax=cmax)
    plt=prettyplot_ll(plt,setregion=region,grid=True)
    plt.colorbar()
    plt.savefig(savepath + grid + '_' + regionname +'_speed_' + ("%04d" %(i)) + '.png',dpi=300)
    plt.close()
































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
name='sfm6_musq2_all_cages'
grid='sfm6_musq2'
regionname='musq_cage'
datatype='2d'
starttime=1009-1008
endtime=1049-1008
cmin=-.01
cmax=0


### load the .nc file #####
data = loadnc('/media/moflaher/My Book/cages/' + name + '/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'


region=regions(regionname)

savepath='figures/timeseries/' + grid + '_' + datatype + '/vertical_speed/' + name + '_' + regionname + '_' +("%f" %cmin) + '_' + ("%f" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)
plt.close()

# Plot mesh
for i in range(starttime,endtime):
    print i
    plt.tripcolor(data['trigrid'],np.max(data['ww'][i,:,:],axis=0),vmin=cmin,vmax=cmax)
    prettyplot_ll(plt.gca(),setregion=region,grid=True,cblabel=r'ww (ms$^{=1}$)')
    plt.savefig(savepath + grid + '_' + regionname +'_vertical_speed_' + ("%04d" %(i)) + '.png',dpi=300)
    plt.close()
































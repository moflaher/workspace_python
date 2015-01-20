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
name='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'
regionname='kit4_kelp_tight2_small'
datatype='2d'
starttime=100
endtime=133
cmin=0
cmax=1


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

region=regions(regionname)

savepath='figures/timeseries/' + grid + '_' + datatype + '/speed/' + name + '_' + regionname + '_' +("%f" %cmin) + '_' + ("%f" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)
plt.close()

# Plot mesh
for i in range(starttime,endtime):
    print i
    f=plt.figure()
    ax=plt.axes([.1,.1,.7,.85])
    triax=ax.tripcolor(data['trigrid'],np.sqrt(data['ua'][i,:]**2+data['va'][i,:]**2),vmin=cmin,vmax=cmax)
    prettyplot_ll(ax,setregion=region,cblabel=r'Speed (ms$^{-1}$)',cb=triax,grid=True)
    f.savefig(savepath + grid + '_' + regionname +'_speed_' + ("%04d" %(i)) + '.png',dpi=300)
    plt.close(f)































from __future__ import division
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import scipy.io as sio
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
from StringIO import StringIO
from gridtools import *
from datatools import *
from misctools import *
from plottools import *
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name='kit4_45days_3'
grid='kit4'
regionname='kit4_area3'
datatype='2d'
starttime=384



### load the .nc file #####
data = loadnc('/media/moflaher/My Book/kit4_runs/' + name + '/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

starttime=0
region=regions(regionname)
nodes=get_nodes(data,region)
elements=get_elements(data,region)



savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)
plt.close()

# Plot mesh
plt.triplot(data['trigrid'],lw=.1)
plt.grid()
plt.axis(region['region'])
plt.title(grid + ' Grid')
plt.savefig(savepath + grid + '_' + regionname +'_grid.png',dpi=1200)
plt.close()

# Plot depth
plt.tripcolor(data['trigrid'],data['h'],vmin=data['h'][nodes].min(),vmax=data['h'][nodes].max())
plt.grid()
plt.axis(region['region'])
plt.title('Depth (m)')
plt.colorbar()
plt.savefig(savepath + grid + '_' + regionname +'_depth.png',dpi=600)
plt.close()


# Plot depth percentile
clims=np.percentile(data['h'][nodes],[1,99])
plt.tripcolor(data['trigrid'],data['h'],vmin=clims[0],vmax=clims[1])
plt.grid()
plt.axis(region['region'])
plt.title('Depth (m)')
plt.colorbar()
plt.savefig(savepath + grid + '_' + regionname +'_depth_percentile.png',dpi=600)
plt.close()


# Plot dh/h
dh=np.zeros([len(data['nv']),])
for i in range(0,len(data['nv'])):
    one=data['h'][data['nv'][i,0]]
    two=data['h'][data['nv'][i,1]]
    three=data['h'][data['nv'][i,2]]
    hmin=np.min([one,two,three])
    first=np.absolute(one-two)/hmin
    second=np.absolute(two-three)/hmin
    thrid=np.absolute(three-one)/hmin
	
    if ( (first > 0) or (second >0) or (thrid> 0) ):
        dh[i]=np.max([first,second,thrid]);
clims=np.percentile(dh[nodes],[1,99])
plt.tripcolor(data['trigrid'],dh,vmin=clims[0],vmax=clims[1])
plt.grid()
plt.axis(region['region'])
plt.title(r'$\frac{\delta H}{H}$')
plt.colorbar()
plt.savefig(savepath + grid + '_' + regionname +'_dhh.png',dpi=600)
plt.close()


# Plot mean speed
meanspeed=(np.sqrt(data['ua'][starttime:,]**2 +data['va'][starttime:,]**2)).mean(axis=0)
plt.tripcolor(data['trigrid'],meanspeed,vmin=meanspeed[elements].min(),vmax=meanspeed[elements].max())
plt.grid()
plt.axis(region['region'])
plt.title(r'Mean Speed $(ms^{-1})$')
plt.colorbar()
plt.savefig(savepath + grid + '_' + regionname +'_DA_meanspeed.png',dpi=600)
plt.close()



# Plot mean speed percentile
clims=np.percentile(meanspeed[elements],[1,99])
plt.tripcolor(data['trigrid'],meanspeed,vmin=clims[0],vmax=clims[1])
plt.grid()
plt.axis(region['region'])
plt.title(r'Mean Speed $(ms^{-1})$')
plt.colorbar()
plt.savefig(savepath + grid + '_' + regionname +'_DA_meanspeed_percentile.png',dpi=600)
plt.close()



# Plot max speed
maxspeed=(np.sqrt(data['ua'][starttime:,]**2 +data['va'][starttime:,]**2)).max(axis=0)
plt.tripcolor(data['trigrid'],maxspeed,vmin=maxspeed[elements].min(),vmax=maxspeed[elements].max())
plt.grid()
plt.axis(region['region'])
plt.title(r'Max Speed $(ms^{-1})$')
plt.colorbar()
plt.savefig(savepath + grid + '_' + regionname +'_DA_maxspeed.png',dpi=600)
plt.close()



# Plot max speed percentile
clims=np.percentile(maxspeed[elements],[1,99])
plt.tripcolor(data['trigrid'],maxspeed,vmin=clims[0],vmax=clims[1])
plt.grid()
plt.axis(region['region'])
plt.title(r'Max Speed $(ms^{-1})$')
plt.colorbar()
plt.savefig(savepath + grid + '_' + regionname +'_DA_maxspeed_percentile.png',dpi=600)
plt.close()































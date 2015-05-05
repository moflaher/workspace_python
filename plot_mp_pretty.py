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
from projtools import *
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name='test_interp_bathymetry'
grid='smallcape_force'
regionname='blackrock_fld'
datatype='2d'

starttime=429
starttime=405


### load the .nc file #####
data = loadnc('runs/' +grid+'/' + name + '/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'


region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)
vidx=equal_vectors(data,region,100)
scale1=1500

savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)



speed=speeder(data['ua'][starttime,:],data['va'][starttime,:])

# Plot depth
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigrid'],speed,vmin=0,vmax=3)
Q1=ax.quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],data['ua'][starttime,vidx],data['va'][starttime,vidx],angles='xy',scale_units='xy',scale=scale1,zorder=10)
prettyplot_ll(ax,setregion=region,cblabel=r'Speed ($\frac{m}{s}$)',cb=triax)
scalebar(ax,region,200,color='w',loc=2)
plotcoast(ax,filename='mid_nwatl6b.nc',fill=True,fcolor='darkgreen')
f.savefig(savepath + grid + '_'+name+'_' + regionname +'_speed_pretty.png',dpi=600)
plt.close(f)





























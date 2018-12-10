from __future__ import division,print_function
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
name='kit4_45days_3'
grid='kit4'

starttime=96
interpheight=2
regionname='douglaslarge'



### load the .nc file #####
data = loadnc('runs/' +grid+'/' + name + '/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')






savepath='figures/png/' + grid + '_'  + '/interp_max/'
if not os.path.exists(savepath): os.makedirs(savepath)




region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)

uava=np.load('data/interp_currents/'+grid+'_'+name+'_2m.npy')
uava=uava[()]


print('plotting region: ' +regionname)



# Plot max speed
maxspeed=(np.sqrt(uava['u'][starttime:,]**2 +uava['u'][starttime:,]**2)).max(axis=0)
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigrid'],maxspeed,vmin=maxspeed[eidx].min(),vmax=maxspeed[eidx].max())
prettyplot_ll(ax,setregion=region,cblabel=r'Max Speed (ms$^{-1}$)',cb=triax)
f.savefig(savepath + grid + '_' + name+'_'+ regionname +'_2m_maxspeed.png',dpi=600)
plt.close(f)

# Plot max speed percentile
clims=np.percentile(maxspeed[eidx],[5,95])
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigrid'],maxspeed,vmin=clims[0],vmax=clims[1])
prettyplot_ll(ax,setregion=region,cblabel=r'Max Speed (ms$^{-1}$)',cb=triax)
f.savefig(savepath + grid + '_'  + name+'_'+ regionname +'_2m_maxspeed_percentile.png',dpi=600)
plt.close(f)





























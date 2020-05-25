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
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)


# Define names and types of data
name='sfm6_musq2_no_cages'
grid='sfm6_musq2'
regionname='musq_cage'

offset=0
starttime=1008
endtime=1080
spacing=150
scaleset=75
#remember 0 is surface and 19/9 is bottom
level=0

### load the .nc file #####
data = loadnc('/media/moflaher/My Book/cages/' + name + '/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')


region=regions(regionname)
sidx=equal_vectors(data,region,spacing)
nidx=get_nodes(data,region)

if datatype=='2d':
    savepath='figures/timeseries/' + grid + '_'  + '/currents_at_level/' + name + '_' + regionname + '/DA/'
    newu=data['ua'][starttime:,:]
    newv=data['va'][starttime:,:]
else:
    savepath='figures/timeseries/' + grid + '_'  + '/currents_at_level/' + name + '_' + regionname + '/'+("%d",level)+'/'
    newu=data['u'][starttime:,level,:]
    newv=data['v'][starttime:,level,:]
if not os.path.exists(savepath): os.makedirs(savepath)



plt.close('all')
for i in range(0,endtime):
    print i
    uplot=newu[i,sidx].copy()
    vplot=newv[i,sidx].copy()
    tspeed=np.sqrt(uplot**2+vplot**2)
    uplot[tspeed<=.01]=np.nan
    vplot[tspeed<=.01]=np.nan
    ax=plt.tripcolor(data['trigrid'],data['h'],vmin=data['h'][nidx].min(),vmax=data['h'][nidx].max())
    prettyplot_ll(ax.get_axes(),setregion=region,grid=True,cblabel=r'Depth (m)')
    Q=ax.get_axes().quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],uplot,vplot,angles='xy',scale_units='xy',scale=scaleset)
    qk = ax.get_axes().quiverkey(Q,  .35,.9,1.0, r'1.0 ms$^{-1}$', labelpos='W')
    if datatype=='2d':
        plt.savefig(savepath + name + '_' + regionname +'_vector_levelDA_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(i+starttime+offset)) + '_with_bathy.png',dpi=1200)
    else:
        plt.savefig(savepath + name + '_' + regionname +'_vector_level' +("%d" %level)+ '_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(i+starttime+offset)) + '_with_bathy.png',dpi=1200)
    plt.close('all')



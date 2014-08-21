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

### load the .nc file #####
data = loadnc('/media/moflaher/My Book/cages/' + name + '/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'


region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)


savepathe='figures/png/' + grid + '_' + datatype + '/ttide/' + name + '_' + regionname + '/el/'
savepathc='figures/png/' + grid + '_' + datatype + '/ttide/' + name + '_' + regionname + '/currents/'
if not os.path.exists(savepathe): os.makedirs(savepathe)
if not os.path.exists(savepathc): os.makedirs(savepathc)
plt.close()


el=np.load('/home/moflaher/Desktop/workspace_python/data/ttide/'+grid+'_'+name+'_'+datatype+'_el.npy')
el=el[()]
uv=np.load('/home/moflaher/Desktop/workspace_python/data/ttide/'+grid+'_'+name+'_'+datatype+'_uv.npy')
uv=uv[()]

# Plot ttide amp and phase
plt.tripcolor(data['trigrid'],el['tidecon'][:,3,0],vmin=el['tidecon'][nidx,3,0].min(),vmax=el['tidecon'][nidx,3,0].max())
prettyplot_ll(plt.gca(),setregion=region,grid=True,cblabel=r'M2 Elevation Amplitude (m)')
plt.savefig(savepathe + grid + '_' + regionname +'_el_m2_amp',dpi=600)
plt.close()

plt.tripcolor(data['trigrid'],el['tidecon'][:,3,2],vmin=el['tidecon'][nidx,3,2].min(),vmax=el['tidecon'][nidx,3,2].max())
prettyplot_ll(plt.gca(),setregion=region,grid=True,cblabel=r'M2 Elevation Phase ($^{\deg}$)')
plt.savefig(savepathe + grid + '_' + regionname +'_el_m2_phase',dpi=600)
plt.close()



plt.tripcolor(data['trigrid'],uv['tidecon'][:,3,0],vmin=uv['tidecon'][nidx,3,0].min(),vmax=uv['tidecon'][nidx,3,0].max())
prettyplot_ll(plt.gca(),setregion=region,grid=True,cblabel=r'M2 Current Amplitude Major (m)')
plt.savefig(savepathc + grid + '_' + regionname +'_uv_m2_major_amp',dpi=600)
plt.close()

plt.tripcolor(data['trigrid'],uv['tidecon'][:,3,2],vmin=uv['tidecon'][nidx,3,2].min(),vmax=uv['tidecon'][nidx,3,2].max())
prettyplot_ll(plt.gca(),setregion=region,grid=True,cblabel=r'M2 Current Amplitude Minor (m)')
plt.savefig(savepathc + grid + '_' + regionname +'_uv_m2_minor_phase',dpi=600)
plt.close()

plt.tripcolor(data['trigrid'],uv['tidecon'][:,3,4],vmin=0,vmax=360)
prettyplot_ll(plt.gca(),setregion=region,grid=True,cblabel=r'M2 Current Direction ($^{\deg}$)')
plt.savefig(savepathc + grid + '_' + regionname +'_uv_m2_inc',dpi=600)
plt.close()

plt.tripcolor(data['trigrid'],uv['tidecon'][:,3,6],vmin=0,vmax=360)
prettyplot_ll(plt.gca(),setregion=region,grid=True,cblabel=r'M2 Current Phase ($^{\deg}$)')
plt.savefig(savepathc + grid + '_' + regionname +'_uv_m2_phase',dpi=600)
plt.close()





















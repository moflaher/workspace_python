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
name_orig='kit4_45days_3'
name_change='kit4_kelp_20m_0.018'
grid='kit4'
datatype='2d'
regionname='kit4_kelp_tight2'


### load the .nc file #####
data = loadnc('/media/moflaher/My Book/'+grid+'/'+name_orig+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'






region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)


savepath='figures/png/' + grid + '_' + datatype + '/ttide_diff/' + name_orig + '_' + name_change + '/'
if not os.path.exists(savepath): os.makedirs(savepath)



base_dir = os.path.dirname(__file__)

uv_orig=np.load(base_dir +'/data/ttide/'+grid+'_'+name_orig+'_'+datatype+'_uv.npy')
uv_orig=uv_orig[()]

uv_change=np.load(base_dir +'/data/ttide/'+grid+'_'+name_change+'_'+datatype+'_uv.npy')
uv_change=uv_change[()]



f=plt.figure()
ax=f.add_axes([.125,.1,.8,.8])
uvdiff=uv_orig['tidecon'][:,3,0]-uv_change['tidecon'][:,3,0]
#axtri=ax.tripcolor(data['trigrid'],uvdiff,vmin=uvdiff[eidx].min(),vmax=uvdiff[eidx].max())
axtri=ax.tripcolor(data['trigrid'],uvdiff,vmin=-.1,vmax=.6)
prettyplot_ll(ax,setregion=region,cb=axtri,cblabel=r'M2 Major Axis (m s$^{-1}$) ')
f.savefig(savepath + grid + '_' + regionname +'_uv_m2_amp_major_difference.png',dpi=600)
plt.close(f)



f=plt.figure()
ax=f.add_axes([.125,.1,.8,.8])
uvdiff=uv_orig['tidecon'][:,3,2]-uv_change['tidecon'][:,3,2]
axtri=ax.tripcolor(data['trigrid'],uvdiff,vmin=uvdiff[eidx].min(),vmax=uvdiff[eidx].max())
prettyplot_ll(ax,setregion=region,cb=axtri,cblabel=r'M2 Minor Axis (m s$^{-1}$) ')
f.savefig(savepath + grid + '_' + regionname +'_uv_m2_amp_minor_difference.png',dpi=600)
plt.close(f)













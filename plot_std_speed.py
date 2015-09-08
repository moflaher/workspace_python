from __future__ import division,print_function
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
regionname='kelparea2'
starttime=384


### load the .nc file #####
data = loadnc('/media/moflaher/My Book/'+grid+'/'+name_orig+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('/media/moflaher/MB_3TB/'+grid+'/'+name_change+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')






region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)


savepath='figures/png/' + grid + '_' + datatype + '/std_speed_diff/' + name_orig + '_' + name_change + '/'
if not os.path.exists(savepath): os.makedirs(savepath)



sorig=np.sqrt(data['ua'][starttime:,:]**2+data['va'][starttime:,:]**2)
schange=np.sqrt(data2['ua'][starttime:,:]**2+data2['va'][starttime:,:]**2)


sorig_std=sorig.std(axis=0)
schange_std=schange.std(axis=0)
sdiff_std=schange_std-sorig_std
sdiff_std_rel=np.divide(sdiff_std,sorig_std)*100

#plot sorig std
f=plt.figure()
ax=f.add_axes([.125,.1,.8,.8])
axtri=ax.tripcolor(data['trigrid'],sorig_std,vmin=sorig_std[eidx].min(),vmax=sorig_std[eidx].max())
prettyplot_ll(ax,setregion=region,cb=axtri,cblabel=r'Speed STD (m s$^{-1}$) ')
f.savefig(savepath + grid + '_' + regionname +'_speed_orig_std.png',dpi=600)
plt.close(f)

#plot schange std
f=plt.figure()
ax=f.add_axes([.125,.1,.8,.8])
axtri=ax.tripcolor(data['trigrid'],schange_std,vmin=schange_std[eidx].min(),vmax=schange_std[eidx].max())
prettyplot_ll(ax,setregion=region,cb=axtri,cblabel=r'Speed STD (m s$^{-1}$) ')
f.savefig(savepath + grid + '_' + regionname +'_speed_change_std.png',dpi=600)
plt.close(f)

#plot sdiff_std 
f=plt.figure()
ax=f.add_axes([.125,.1,.8,.8])
axtri=ax.tripcolor(data['trigrid'],sdiff_std,vmin=sdiff_std[eidx].min(),vmax=sdiff_std[eidx].max())
prettyplot_ll(ax,setregion=region,cb=axtri,cblabel=r'Speed STD difference absolute (m s$^{-1}$) ')
f.savefig(savepath + grid + '_' + regionname +'_speed_std_diff_absolute.png',dpi=600)
plt.close(f)

#plot sdiff_std 
f=plt.figure()
ax=f.add_axes([.125,.1,.8,.8])
#axtri=ax.tripcolor(data['trigrid'],sdiff_std_rel,vmin=sdiff_std_rel[eidx].min(),vmax=sdiff_std_rel[eidx].max())
axtri=ax.tripcolor(data['trigrid'],sdiff_std_rel,vmin=-80,vmax=40)
prettyplot_ll(ax,setregion=region,cb=axtri,cblabel=r'Speed STD difference relative (%) ')
f.savefig(savepath + grid + '_' + regionname +'_speed_std_diff_relative.png',dpi=600)
plt.close(f)







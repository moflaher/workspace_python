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

regionname='kit4_crossdouble'
starttime=384

cbfix=True


### load the .nc file #####
data = loadnc('/media/moflaher/My Book/'+grid+'/'+name_orig+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('/media/moflaher/MB_3TB/'+grid+'/'+name_change+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')






region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)


savepath='figures/png/' + grid + '_'  + '/current_var_mag_diff/' + name_orig + '_' + name_change + '/'
if not os.path.exists(savepath): os.makedirs(savepath)

uvar_o=data['ua'][starttime:,:].var(axis=0)
vvar_o=data['va'][starttime:,:].var(axis=0)
uvar_c=data2['ua'][starttime:,:].var(axis=0)
vvar_c=data2['va'][starttime:,:].var(axis=0)

cvarm_o=np.sqrt(uvar_o+vvar_o)
cvarm_c=np.sqrt(uvar_c+vvar_c)

cvarm_diff=cvarm_c-cvarm_o
cvarm_diff_rel=np.divide(cvarm_diff,cvarm_o)*100


#plot sdiff_std 
f=plt.figure()
ax=f.add_axes([.125,.1,.8,.8])
if cbfix==True:
    axtri=ax.tripcolor(data['trigrid'],cvarm_diff_rel,vmin=-80,vmax=40)
else:
    axtri=ax.tripcolor(data['trigrid'],cvarm_diff_rel,vmin=cvarm_diff_rel[eidx].min(),vmax=cvarm_diff_rel[eidx].max())
prettyplot_ll(ax,setregion=region,cb=axtri,cblabel=r'Relative difference current variance magnitude (%) ')
f.savefig(savepath + grid + '_' + regionname +'_current_variance_magnitude_diff_relative.png',dpi=600)
plt.close(f)

#plot sdiff_std 
f=plt.figure()
ax=f.add_axes([.125,.1,.8,.8])
if cbfix==True:
    axtri=ax.tripcolor(data['trigrid'],cvarm_diff,vmin=-.25,vmax=0.1)
else:
    axtri=ax.tripcolor(data['trigrid'],cvarm_diff,vmin=cvarm_diff[eidx].min(),vmax=cvarm_diff[eidx].max())
prettyplot_ll(ax,setregion=region,cb=axtri,cblabel=r'Absolute difference current variance magnitude (m s$^{-1}$) ')
f.savefig(savepath + grid + '_' + regionname +'_current_variance_magnitude_diff_absolute.png',dpi=600)
plt.close(f)

#plot schange std
f=plt.figure()
ax=f.add_axes([.125,.1,.8,.8])
if cbfix==True:
    axtri=ax.tripcolor(data['trigrid'],cvarm_c,vmin=0,vmax=0.8)
else:
    axtri=ax.tripcolor(data['trigrid'],cvarm_c,vmin=cvarm_c[eidx].min(),vmax=cvarm_c[eidx].max())
prettyplot_ll(ax,setregion=region,cb=axtri,cblabel=r'Current variance magnitude (m s$^{-1}$)')
f.savefig(savepath + grid + '_' + regionname +'_current_variance_magnitude_change.png',dpi=600)
plt.close(f)

#plot sorig std
f=plt.figure()
ax=f.add_axes([.125,.1,.8,.8])
if cbfix==True:
    axtri=ax.tripcolor(data['trigrid'],cvarm_o,vmin=0,vmax=.8)
else:
    axtri=ax.tripcolor(data['trigrid'],cvarm_o,vmin=cvarm_o[eidx].min(),vmax=cvarm_o[eidx].max())

prettyplot_ll(ax,setregion=region,cb=axtri,cblabel=r'Current variance magnitude (m s$^{-1}$)')
f.savefig(savepath + grid + '_' + regionname +'_current_variance_magnitude_orig.png',dpi=600)
plt.close(f)












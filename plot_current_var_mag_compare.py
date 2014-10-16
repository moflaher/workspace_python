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
regionname='kelparea2'
starttime=384

cbfix=True


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name_orig+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name_change+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'






region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)


savepath='figures/png/' + grid + '_' + datatype + '/current_var_mag_diff/' + name_orig + '_' + name_change + '/'
if not os.path.exists(savepath): os.makedirs(savepath)

uvar_o=data['ua'][starttime:,:].var(axis=0)
vvar_o=data['va'][starttime:,:].var(axis=0)
uvar_c=data2['ua'][starttime:,:].var(axis=0)
vvar_c=data2['va'][starttime:,:].var(axis=0)

cvarm_o=np.sqrt(uvar_o+vvar_o)
cvarm_c=np.sqrt(uvar_c+vvar_c)

cvarm_diff=cvarm_c-cvarm_o
cvarm_diff_rel=np.divide(cvarm_diff,cvarm_o)*100


f=plt.figure()
ax0=f.add_axes([-.05,.25,.8,.675])
ax1=f.add_axes([.3,.25,.8,.675])



if cbfix==True:
    axtri1=ax0.tripcolor(data['trigrid'],cvarm_o,vmin=.1,vmax=.5)
else:
    axtri1=ax0.tripcolor(data['trigrid'],cvarm_o,vmin=cvarm_o[eidx].min(),vmax=cvarm_o[eidx].max())
prettyplot_ll(ax0,setregion=region)






if cbfix==True:
    axtri2=ax1.tripcolor(data['trigrid'],cvarm_diff_rel,vmin=-80,vmax=20)
else:
    axtri2=ax1.tripcolor(data['trigrid'],cvarm_diff_rel,vmin=cvarm_diff_rel[eidx].min(),vmax=cvarm_diff_rel[eidx].max())
prettyplot_ll(ax1,setregion=region)
ax1.yaxis.set_tick_params(labelleft='off')


plt.draw()
ax0bb=ax0.get_axes().get_position().bounds
ax1bb=ax1.get_axes().get_position().bounds

ax0ca=f.add_axes([ax0bb[0],ax0bb[1]-.125,ax0bb[2],0.025])
ax1ca=f.add_axes([ax1bb[0],ax1bb[1]-.125,ax1bb[2],0.025])

cb=plt.colorbar(axtri1,cax=ax0ca,orientation='horizontal')
cb.set_label(r'Current variance magnitude (m s$^{-1}$)',fontsize=8)
for label in cb.ax.get_xticklabels():
    label.set_rotation(90)

cb2=plt.colorbar(axtri2,cax=ax1ca,orientation='horizontal')
cb2.set_label(r'Relative difference of current variance magnitude (%)',fontsize=8)
ax1.set_ylabel('')
for label in cb2.ax.get_xticklabels():
    label.set_rotation(90)


ax0.annotate("A",xy=(.025,.95),xycoords='axes fraction')
ax1.annotate("B",xy=(.025,.95),xycoords='axes fraction')

#plotcoast(ax0,filename='pacific.nc',color='k')
#plotcoast(ax1,filename='pacific.nc',color='k')

f.savefig(savepath + grid + '_' + regionname+'_current_variance_magnitude_diff_relative_subplot.png',dpi=600)
plt.close(f)












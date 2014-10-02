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
regionname1='kelpchain'
regionname2='doubleisland'
starttime=384


### load the .nc file #####
data = loadnc('/media/moflaher/My Book/'+grid+'/'+name_orig+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('/media/moflaher/MB_3TB/'+grid+'/'+name_change+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'






region1=regions(regionname1)
region2=regions(regionname2)
eidx1=get_elements(data,region1)
eidx2=get_elements(data,region2)

savepath='figures/png/' + grid + '_' + datatype + '/std_speed_diff/' + name_orig + '_' + name_change + '/'
if not os.path.exists(savepath): os.makedirs(savepath)



sorig=np.sqrt(data['ua'][starttime:,:]**2+data['va'][starttime:,:]**2)
schange=np.sqrt(data2['ua'][starttime:,:]**2+data2['va'][starttime:,:]**2)


sorig_std=sorig.std(axis=0)
schange_std=schange.std(axis=0)
sdiff_std=schange_std-sorig_std
sdiff_std_rel=np.divide(sdiff_std,sorig_std)*100


f,ax=plt.subplots(nrows=2,ncols=2)


axtri=ax[0,0].tripcolor(data['trigrid'],sorig_std,vmin=sorig_std[eidx1].min(),vmax=sorig_std[eidx1].max())
ax[0,0].axis(region1['region'])
fix_osw(ax[0,0])#,setregion=region1,cb=axtri,cblabel=r'Speed STD (m s$^{-1}$)')
cb=plt.colorbar(axtri,ax=ax[0,0])
cb.set_label(r'Speed STD (m s$^{-1}$)')


axtri=ax[1,0].tripcolor(data['trigrid'],sdiff_std_rel,vmin=sdiff_std_rel[eidx1].min(),vmax=sdiff_std_rel[eidx1].max())
ax[1,0].axis(region1['region'])
fix_osw(ax[1,0])#,setregion=region1,cb=axtri,cblabel=r'Speed STD difference relative (%)')
cb=plt.colorbar(axtri,ax=ax[1,0])
cb.set_label(r'Speed STD difference relative (%)')



axtri=ax[0,1].tripcolor(data['trigrid'],sorig_std,vmin=sorig_std[eidx2].min(),vmax=sorig_std[eidx2].max())
ax[0,1].axis(region2['region'])
fix_osw(ax[0,1])#,setregion=region2,cb=axtri,cblabel=r'Speed STD (m s$^{-1}$)')
cb=plt.colorbar(axtri,ax=ax[0,1])
cb.set_label(r'Speed STD (m s$^{-1}$)')


axtri=ax[1,1].tripcolor(data['trigrid'],sdiff_std_rel,vmin=sdiff_std_rel[eidx2].min(),vmax=sdiff_std_rel[eidx2].max())
ax[1,1].axis(region2['region'])
fix_osw(ax[1,1])#,setregion=region2,cb=axtri,cblabel=r'Speed STD difference relative (%)')
cb=plt.colorbar(axtri,ax=ax[1,1])
cb.set_label(r'Speed STD difference relative (%)')

f.tight_layout(pad=0.6)
f.savefig(savepath + grid + '_' + regionname1+ '_' + regionname2 +'_speed_std_diff_relative.png',dpi=600)
plt.close(f)







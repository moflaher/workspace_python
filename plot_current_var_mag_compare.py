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
regionname='kit4_kelp_tight4'
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




savepath='figures/png/' + grid + '_' + datatype + '/current_var_mag_subplot/' + name_orig + '_' + name_change + '/'
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

xtarget=.4
ytarget=.675

aspect=get_aspectratio(region)
dr=get_data_ratio(region)
figW, figH = f.get_size_inches()
fa = figH / figW

if aspect>=1.1:    
    finalspace=((ytarget*fa)/aspect/dr)
    if finalspace>.4:
        finalspace[0]=.4
        ax0f=[.125,.275,finalspace[0],ytarget]
        ax1f=[ax0f[0]+finalspace[0]+.025,.275,finalspace[0],ytarget]
    else:
        ax0f=[.125,.275,1,ytarget]
        ax1f=[ax0f[0]+finalspace[0]+.025,.275,1,ytarget]
else:    
    finalspace=((((xtarget*fa)/aspect/dr)*aspect*dr)/fa)
    #ax1f=[.125,.1,.75,xtarget]
    #ax0f=[.125,ax1f[1]+finalspace[0]+.05,.75,xtarget]
    #finalspace=((ytarget*fa)/aspect/dr)
    ax1f=[.125,.1,1,xtarget]
    ax0f=[.125,ax1f[1]+finalspace[0]+.025,1,xtarget]




ax0=f.add_axes(ax0f)
ax1=f.add_axes(ax1f)



if cbfix==True:
    axtri1=ax0.tripcolor(data['trigrid'],cvarm_o,vmin=0,vmax=.1)
    axtri2=ax1.tripcolor(data['trigrid'],cvarm_diff_rel,vmin=-50,vmax=50)
else:
    axtri1=ax0.tripcolor(data['trigrid'],cvarm_o,vmin=cvarm_o[eidx].min(),vmax=cvarm_o[eidx].max())
    axtri2=ax1.tripcolor(data['trigrid'],cvarm_diff_rel,vmin=cvarm_diff_rel[eidx].min(),vmax=cvarm_diff_rel[eidx].max())


prettyplot_ll(ax0,setregion=region)
prettyplot_ll(ax1,setregion=region)
ax_label_spacer(ax0)
ax_label_spacer(ax1)


if aspect>=1.1:
    ax1.yaxis.set_tick_params(labelleft='off')
else:
    ax0.xaxis.set_tick_params(labelleft='off')
    ax0.set_xlabel('')

plt.draw()
ax0bb=ax0.get_axes().get_position().bounds
ax1bb=ax1.get_axes().get_position().bounds

if aspect>=1.1:
    ax0ca=f.add_axes([ax0bb[0],ax0bb[1]-.125,ax0bb[2],0.025])
    ax1ca=f.add_axes([ax1bb[0],ax1bb[1]-.125,ax1bb[2],0.025])
    cb=plt.colorbar(axtri1,cax=ax0ca,orientation='horizontal')
    cb.set_label(r'Current variance magnitude (m s$^{-1}$)',fontsize=6)
    for label in cb.ax.get_xticklabels():
        label.set_rotation(90)

    cb2=plt.colorbar(axtri2,cax=ax1ca,orientation='horizontal')
    cb2.set_label(r'Relative difference (%)',fontsize=6)
    ax1.set_ylabel('')
    for label in cb2.ax.get_xticklabels():
        label.set_rotation(90)

else:
    ax0ca=f.add_axes([ax0bb[0]+ax0bb[2]+.025,ax0bb[1],.025,ax0bb[3]])
    ax1ca=f.add_axes([ax1bb[0]+ax1bb[2]+.025,ax1bb[1],.025,ax1bb[3]])
    cb=plt.colorbar(axtri1,cax=ax0ca)
    cb.set_label(r'Current variance magnitude (m s$^{-1}$)',fontsize=8)
    cb2=plt.colorbar(axtri2,cax=ax1ca)
    cb2.set_label(r'Relative difference (%)',fontsize=8)




ax0.annotate("A",xy=(.025,1-(.05/dr)),xycoords='axes fraction')
ax1.annotate("B",xy=(.025,1-(.05/dr)),xycoords='axes fraction')

#plotcoast(ax0,filename='pacific.nc',color='k')
#plotcoast(ax1,filename='pacific.nc',color='k')

f.savefig(savepath + grid + '_' + regionname+'_current_variance_magnitude_diff_relative_subplot.png',dpi=600)
#plt.close(f)












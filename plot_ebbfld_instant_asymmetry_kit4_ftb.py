from __future__ import division
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from misctools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from matplotlib.collections import LineCollection as LC


# Define names and types of data
name='kit4_45days_3'
name2='kit4_kelp_20m_0.018'
grid='kit4'
regionname='kit4_ftb'
datatype='2d'
starttime=384
cmin=-0.8
cmax=0.8


data_f=[.125,.515,.825,.425]
data2_f=[.125,.075,.825,.425]
ABC=[.025,.9]


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'


cages=np.genfromtxt('runs/'+grid+'/' +name2+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)

region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)

tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
color='g'
lw=.5
ls='solid'






savepath='figures/png/' + grid + '_' + datatype + '/ebbfld_instant_asymmetry_subplots/'+name+'_'+name2+'/'
if not os.path.exists(savepath): os.makedirs(savepath)
plt.close()




zeta_grad=np.gradient(data['zeta'][starttime:,nidx])[0]
fld=np.argmax(np.sum(zeta_grad,axis=1))
ebb=np.argmin(np.sum(zeta_grad,axis=1))


    
f=plt.figure()


uf=data['ua'][starttime+fld,:]
ue=data['ua'][starttime+ebb,:]
vf=data['va'][starttime+fld,:]
ve=data['va'][starttime+ebb,:]
efs=np.divide(np.sqrt(uf**2+vf**2)-np.sqrt(ue**2+ve**2),np.sqrt(uf**2+vf**2)+np.sqrt(ue**2+ve**2))
print runstats(efs[eidx])
ax1=f.add_axes(data_f)  
ax1.tripcolor(data['trigrid'],efs,vmin=cmin,vmax=cmax)
ax1.axis(region['region'])
fix_osw(ax1)
ax1.set_aspect(get_aspectratio(region))
ax1.xaxis.set_tick_params(labelbottom='off')
plotcoast(ax1,filename='pacific.nc',color='k')
lseg1=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
ax1.add_collection(lseg1)


uf=data2['ua'][starttime+fld,:]
ue=data2['ua'][starttime+ebb,:]
vf=data2['va'][starttime+fld,:]
ve=data2['va'][starttime+ebb,:]
efs=np.divide(np.sqrt(uf**2+vf**2)-np.sqrt(ue**2+ve**2),np.sqrt(uf**2+vf**2)+np.sqrt(ue**2+ve**2))
print runstats(efs[eidx])
ax2=f.add_axes(data2_f)  
triax=ax2.tripcolor(data['trigrid'],efs,vmin=cmin,vmax=cmax)
ax2.axis(region['region'])
fix_osw(ax2)
ax2.set_aspect(get_aspectratio(region))
plotcoast(ax2,filename='pacific.nc',color='k')
lseg2=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
ax2.add_collection(lseg2)

plt.draw()

ax1bb=ax1.get_axes().get_position().bounds
ax2bb=ax2.get_axes().get_position().bounds
axcb=f.add_axes([ax2bb[0]+.015+ax2bb[2],ax2bb[1],.025,ax1bb[1]+ax1bb[3]-ax2bb[1]])

cb=plt.colorbar(triax,cax=axcb)
cb.set_label('Asymmetry')

for label in ax1.get_yticklabels():
    label.set_fontsize(8)
for label in ax1.get_xticklabels():
    label.set_fontsize(8)
for label in ax2.get_yticklabels():
    label.set_fontsize(8)
for label in ax2.get_xticklabels():
    label.set_fontsize(8)


for label in ax2.get_xticklabels()[::2]:
    label.set_visible(False)
for label in ax1.get_yticklabels()[1::2]:
    label.set_visible(False)
for label in ax2.get_yticklabels()[1::2]:
    label.set_visible(False)


ax1.text(ABC[0],ABC[1],"A",transform=ax1.transAxes)#,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3},zorder=31)
ax2.text(ABC[0],ABC[1],"B",transform=ax2.transAxes)#,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3},zorder=31)

ax1.set_ylabel(r'Latitude ($^{\circ}$N)',fontsize=8)
ax2.set_ylabel(r'Latitude ($^{\circ}$N)',fontsize=8)
ax2.set_xlabel(r'Longitude ($^{\circ}$W)',fontsize=8)


f.savefig(savepath + grid + '_'+name+'_'+name2+'_' + regionname +'_ebbfld_asymmetry.png',dpi=600)
plt.close(f)































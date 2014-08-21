from __future__ import division
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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name='sfm6_musq2_all_cages'
grid='sfm6_musq2'
regionname='musq_cage'
datatype='2d'
starttime=0
spacing=150
scaleset=75
#remember 0 is surface and 19/9 is bottom
level=0

### load the .nc file #####
data = loadnc('/media/moflaher/My Book/cages/' + name + '/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'


region=regions(regionname)
sidx=equal_vectors(data,region,spacing)
nidx=get_nodes(data,region)

if datatype=='2d':
    savepath='figures/png/' + grid + '_' + datatype + '/currents_at_level/DA/'
    newu=data['ua']
    newv=data['va']
else:
    savepath='figures/png/' + grid + '_' + datatype + '/currents_at_level/'+("%d",level)+'/'
    newu=data['u'][starttime:,level,:]
    newv=data['v'][starttime:,level,:]
if not os.path.exists(savepath): os.makedirs(savepath)







zeta_grad=np.gradient(data['zeta'][starttime:,:])[0]


#find biggest ebb and fld
fld=np.argmax(np.sum(zeta_grad>0,axis=1))
ebb=np.argmax(np.sum(zeta_grad<0,axis=1))


#plot ebb vectors
plt.close()
uplot=newu[ebb,sidx].copy()
vplot=newv[ebb,sidx].copy()
tspeed=np.sqrt(uplot**2+vplot**2)
uplot[tspeed<=.01]=np.nan
vplot[tspeed<=.01]=np.nan
Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],uplot,vplot,angles='xy',scale_units='xy',scale=scaleset)
qk = plt.quiverkey(Q,  .2,1.05,1.0, r'1.0 ms$^{-1}$', labelpos='W')
prettyplot_ll(plt.gca(),setregion=region,grid=True)
if datatype=='2d':
    plt.savefig(savepath + name + '_' + regionname +'_vector_ebb_levelDA_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(ebb+starttime)) + '.png',dpi=1200)
else:
    plt.savefig(savepath + name + '_' + regionname +'_vector_ebb_level' +("%d" %level)+ '_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(ebb+starttime)) + '.png',dpi=1200)

plt.close()
uplot=newu[ebb,sidx].copy()
vplot=newv[ebb,sidx].copy()
tspeed=np.sqrt(uplot**2+vplot**2)
uplot[tspeed<=.01]=np.nan
vplot[tspeed<=.01]=np.nan
plt.tripcolor(data['trigrid'],data['h'],vmin=data['h'][nidx].min(),vmax=data['h'][nidx].max())
cb=plt.colorbar()
cb.set_label('(meter)')
Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],uplot,vplot,angles='xy',scale_units='xy',scale=scaleset)
qk = plt.quiverkey(Q,  .2,1.05,1.0, r'1.0 ms$^{-1}$', labelpos='W')
prettyplot_ll(plt.gca(),setregion=region,grid=True)
if datatype=='2d':
    plt.savefig(savepath + name + '_' + regionname +'_vector_ebb_levelDA_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(ebb+starttime)) + '_with_bathy.png',dpi=1200)
else:
    plt.savefig(savepath + name + '_' + regionname +'_vector_ebb_level' +("%d" %level)+ '_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(ebb+starttime)) + '_with_bathy.png',dpi=1200)



#plot fld vectors
plt.close()
uplot=newu[fld,sidx].copy()
vplot=newv[fld,sidx].copy()
tspeed=np.sqrt(uplot**2+vplot**2)
uplot[tspeed<=.01]=np.nan
vplot[tspeed<=.01]=np.nan
Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],uplot,vplot,angles='xy',scale_units='xy',scale=scaleset)
qk = plt.quiverkey(Q,  .2,1.05,1.0, r'1.0 ms$^{-1}$', labelpos='W')
prettyplot_ll(plt.gca(),setregion=region,grid=True)
if datatype=='2d':
    plt.savefig(savepath + name + '_' + regionname +'_vector_fld_levelDA_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(fld+starttime)) + '.png',dpi=1200)
else:
    plt.savefig(savepath + name + '_' + regionname +'_vector_fld_level' +("%d" %level)+ '_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(fld+starttime)) + '.png',dpi=1200)

plt.close()
uplot=newu[fld,sidx].copy()
vplot=newv[fld,sidx].copy()
tspeed=np.sqrt(uplot**2+vplot**2)
uplot[tspeed<=.01]=np.nan
vplot[tspeed<=.01]=np.nan
plt.tripcolor(data['trigrid'],data['h'],vmin=data['h'][nidx].min(),vmax=data['h'][nidx].max())
cb=plt.colorbar()
cb.set_label('(meter)')
Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],uplot,vplot,angles='xy',scale_units='xy',scale=scaleset)
qk = plt.quiverkey(Q,  .2,1.05,1.0, r'1.0 ms$^{-1}$', labelpos='W')
prettyplot_ll(plt.gca(),setregion=region,grid=True)
if datatype=='2d':
    plt.savefig(savepath + name + '_' + regionname +'_vector_fld_levelDA_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(fld+starttime)) + '_with_bathy.png',dpi=1200)
else:
    plt.savefig(savepath + name + '_' + regionname +'_vector_fld_level' +("%d" %level)+ '_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(fld+starttime)) + '_with_bathy.png',dpi=1200)

#plot max speed
plt.close()
plt.tripcolor(data['trigrid'],np.max(np.sqrt(newu**2+newv**2),axis=0),vmin=1.15*np.min(np.max(np.sqrt(newu[:,sidx]**2+newv[:,sidx]**2),axis=0)),vmax=.85*np.max(np.max(np.sqrt(newu[:,sidx]**2+newv[:,sidx]**2),axis=0)))
cb=plt.colorbar()
cb.set_label(r'$(ms^{-1})$')
prettyplot_ll(plt.gca(),setregion=region,grid=True)
plt.savefig(savepath + name + '_' + regionname +'_maxspeed_at_' + ("%d" %level)+ 'm.png',dpi=1200)



from __future__ import division
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
from numba import jit
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name='kit4_45days_3'
grid='kit4'
regionname='kit4_area2'
datatype='2d'
starttime=384
spacing=500
interpheight=1

### load the .nc file #####
data = loadnc('/media/moflaher/My Book/kit4_runs/' + name + '/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'


region=regions(regionname)
sidx=equal_vectors(data,region,spacing)

savepath='figures/png/' + grid + '_' + datatype + '/currents_' + ("%d" %interpheight)+ 'm/'
if not os.path.exists(savepath): os.makedirs(savepath)

base_dir = os.path.dirname(__file__)
filename='_' + grid + '_' +name+ '_' + ("%d" %interpheight) + 'm.npy'
if (os.path.exists(os.path.join(base_dir,'data', 'u' + filename)) & os.path.exists(os.path.join(base_dir,'data', 'v' + filename))):
    print 'Loading old interpolated currents'
    newu=np.load(os.path.join(base_dir,'data', 'u' + filename))
    newv=np.load(os.path.join(base_dir,'data', 'v' + filename))
    print 'Loaded old interpolated currents'
else:
    print 'Interpolate currents first'
    sys.exit(0)






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
Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],uplot,vplot,angles='xy',scale_units='xy',scale=10)
qk = plt.quiverkey(Q,  .2,1.05,0.25, r'$0.25\ ms^{-1}$', labelpos='W')
plt.grid()
plt.axis(region['region'])
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
plt.gca().set_xticklabels(-1*(plt.gca().get_xticks()))
plt.gca().set_xlabel(r'Longitude $(W^{\circ})$')
plt.gca().set_ylabel(r'Latitude $(N^{\circ})$')
plt.savefig(savepath + name + '_' + regionname +'_vector_ebb_' +("%d" %interpheight)+ 'm_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(ebb+starttime)) + '.png',dpi=1200)

plt.close()
uplot=newu[ebb,sidx].copy()
vplot=newv[ebb,sidx].copy()
tspeed=np.sqrt(uplot**2+vplot**2)
uplot[tspeed<=.01]=np.nan
vplot[tspeed<=.01]=np.nan
plt.tripcolor(data['trigrid'],data['h'])
cb=plt.colorbar()
cb.set_label('(meter)')
Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],uplot,vplot,angles='xy',scale_units='xy',scale=10)
qk = plt.quiverkey(Q,  .2,1.05,0.25, r'$0.25\ ms^{-1}$', labelpos='W')
plt.grid()
plt.axis(region['region'])
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
plt.gca().set_xticklabels(-1*(plt.gca().get_xticks()))
plt.gca().set_xlabel(r'Longitude $(W^{\circ})$')
plt.gca().set_ylabel(r'Latitude $(N^{\circ})$')
plt.savefig(savepath + name + '_' + regionname +'_vector_ebb_' +("%d" %interpheight)+ 'm_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(ebb+starttime)) + '_with_bathy.png',dpi=1200)



#plot fld vectors
plt.close()
uplot=newu[fld,sidx].copy()
vplot=newv[fld,sidx].copy()
tspeed=np.sqrt(uplot**2+vplot**2)
uplot[tspeed<=.01]=np.nan
vplot[tspeed<=.01]=np.nan
Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],uplot,vplot,angles='xy',scale_units='xy',scale=10)
qk = plt.quiverkey(Q,  .2,1.05,0.25, r'$0.25\ ms^{-1}$', labelpos='W')
plt.grid()
plt.axis(region['region'])
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
plt.gca().set_xticklabels(-1*(plt.gca().get_xticks()))
plt.gca().set_xlabel(r'Longitude $(W^{\circ})$')
plt.gca().set_ylabel(r'Latitude $(N^{\circ})$')
plt.savefig(savepath + name + '_' + regionname +'_vector_fld_' +("%d" %interpheight)+ 'm_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(fld+starttime)) + '.png',dpi=1200)

plt.close()
uplot=newu[fld,sidx].copy()
vplot=newv[fld,sidx].copy()
tspeed=np.sqrt(uplot**2+vplot**2)
uplot[tspeed<=.01]=np.nan
vplot[tspeed<=.01]=np.nan
plt.tripcolor(data['trigrid'],data['h'])
cb=plt.colorbar()
cb.set_label('(meter)')
Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],uplot,vplot,angles='xy',scale_units='xy',scale=10)
qk = plt.quiverkey(Q,  .2,1.05,0.25, r'$0.25\ ms^{-1}$', labelpos='W')
plt.grid()
plt.axis(region['region'])
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
plt.gca().set_xticklabels(-1*(plt.gca().get_xticks()))
plt.gca().set_xlabel(r'Longitude $(W^{\circ})$')
plt.gca().set_ylabel(r'Latitude $(N^{\circ})$')
plt.savefig(savepath + name + '_' + regionname +'_vector_fld_' +("%d" %interpheight)+ 'm_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(fld+starttime)) + '_with_bathy.png',dpi=1200)

#plot max speed
plt.close()
plt.tripcolor(data['trigrid'],np.max(np.sqrt(newu**2+newv**2),axis=0),vmin=1.15*np.min(np.max(np.sqrt(newu[:,sidx]**2+newv[:,sidx]**2),axis=0)),vmax=.85*np.max(np.max(np.sqrt(newu[:,sidx]**2+newv[:,sidx]**2),axis=0)))
cb=plt.colorbar()
cb.set_label(r'$(ms^{-1})$')
plt.grid()
plt.axis(region['region'])
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
plt.gca().set_xticklabels(-1*(plt.gca().get_xticks()))
plt.gca().set_xlabel(r'Longitude $(W^{\circ})$')
plt.gca().set_ylabel(r'Latitude $(N^{\circ})$')
plt.savefig(savepath + name + '_' + regionname +'_maxspeed_at_' + ("%d" %interpheight)+ 'm.png',dpi=1200)



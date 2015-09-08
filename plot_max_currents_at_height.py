from __future__ import division,print_function
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
regionname='kit4_area3'
datatype='2d'
starttime=384
spacing=500
interpheight=1

### load the .nc file #####
data = loadnc('/media/moflaher/My Book/kit4_runs/' + name + '/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')


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
else:
    print 'Interpolate currents first'
    sys.exit(0)






zeta_grad=np.gradient(data['zeta'][starttime:,:])[0]


ebbu=newu.copy()
ebbv=newv.copy()
ebbu[zeta_grad>0]=np.nan
ebbv[zeta_grad>0]=np.nan
ebbspeed=np.nanargmax(np.sqrt(ebbu**2+ebbv**2),axis=0)
del ebbu
del ebbv

fldu=newu.copy()
fldv=newv.copy()
fldu[zeta_grad<0]=np.nan
fldv[zeta_grad<0]=np.nan
fldspeed=np.nanargmax(np.sqrt(fldu**2+fldv**2),axis=0)
del fldu
del fldv

#plot max ebb vectors
plt.close()
ebbuplot=newu[ebbspeed,range(0,data['nele'])].copy()
ebbvplot=newv[ebbspeed,range(0,data['nele'])].copy()
ebbspeedplot=np.sqrt(ebbuplot**2+ebbvplot**2)
ebbuplot[ebbspeedplot<=.01]=np.nan
ebbvplot[ebbspeedplot<=.01]=np.nan
Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],ebbuplot[sidx],ebbvplot[sidx],angles='xy',scale_units='xy',scale=10)
qk = plt.quiverkey(Q,  .2,1.05,0.25, '0.25 ms^-1', labelpos='W')
plt.grid()
plt.axis(region['region'])
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
plt.savefig(savepath + name + '_' + regionname +'_vector_maxebb_s_' + ("%d" %spacing) + '.png',dpi=1200)


#plot max fld vectors
plt.close()
flduplot=newu[fldspeed,range(0,data['nele'])].copy()
fldvplot=newv[fldspeed,range(0,data['nele'])].copy()
fldspeedplot=np.sqrt(flduplot**2+fldvplot**2)
flduplot[fldspeedplot<=.01]=np.nan
fldvplot[fldspeedplot<=.01]=np.nan
Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],flduplot[sidx],fldvplot[sidx],angles='xy',scale_units='xy',scale=10)
qk = plt.quiverkey(Q, .2,1.05,0.25, '0.25 ms^-1', labelpos='W')
plt.grid()
plt.axis(region['region'])
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
plt.savefig(savepath + name + '_' + regionname +'_vector_maxfld_s_' + ("%d" %spacing) + '.png',dpi=1200)


#plot max speed
plt.close()
plt.tripcolor(data['trigrid'],np.max(np.sqrt(newu**2+newv**2),axis=0),vmin=1.15*np.min(np.max(np.sqrt(newu[:,sidx]**2+newv[:,sidx]**2),axis=0)),vmax=.85*np.max(np.max(np.sqrt(newu[:,sidx]**2+newv[:,sidx]**2),axis=0)))
plt.colorbar()
plt.grid()
plt.axis(region['region'])
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
plt.savefig(savepath + name + '_' + regionname +'_maxspeed.png',dpi=1200)

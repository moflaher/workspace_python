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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name='kit4_45days_3'
grid='kit4'
regionname='mostchannels'
datatype='2d'
starttime=384
spacing=500


### load the .nc file #####
data = loadnc('/media/moflaher/My Book/kit4_runs/' + name + '/output/',singlename=grid + '_0001.nc')

print 'done load'
data = ncdatasort(data)
print 'done sort'


region=regions(regionname)


sidx=equal_vectors(data,region,spacing)


savepath='figures/png/' + grid + '_' + datatype + '/maxs_1m/'
if not os.path.exists(savepath): os.makedirs(savepath)



zeta_grad=np.gradient(data['zeta'][starttime:,:])[0]



ebbu=data['u'][starttime:,19,:].copy()
ebbv=data['v'][starttime:,19,:].copy()
fldu=ebbu.copy()
fldv=ebbv.copy()
ebbu[zeta_grad>0]=np.nan
ebbv[zeta_grad>0]=np.nan
fldu[zeta_grad<0]=np.nan
fldv[zeta_grad<0]=np.nan

ebbspeed=np.nanargmax(np.sqrt(ebbu**2+ebbv**2),axis=0)
fldspeed=np.nanargmax(np.sqrt(fldu**2+fldv**2),axis=0)

u=data['u'][starttime:,19,:]
v=data['v'][starttime:,19,:]


plt.close()

ebbuplot=u[ebbspeed,range(0,data['nele'])].copy()
ebbvplot=v[ebbspeed,range(0,data['nele'])].copy()
ebbspeedplot=np.sqrt(ebbuplot**2+ebbvplot**2)
ebbuplot[ebbspeedplot<=.01]=np.nan
ebbvplot[ebbspeedplot<=.01]=np.nan
#Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],ebbuplot[sidx],ebbvplot[sidx],width=.002,pivot='tail',headwidth=3.,headlength=4)
Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],ebbuplot[sidx],ebbvplot[sidx],angles='xy',scale_units='xy',scale=10)
qk = plt.quiverkey(Q, .1,.9,0.5, '0.5 ms^-1', labelpos='W')
plt.grid()
plt.axis(region['region'])
#plt.show()
plt.savefig(savepath + name + '_' + regionname +'_vector_maxebb_s_' + ("%d" %spacing) + '.png',dpi=1200)


plt.close()
flduplot=u[fldspeed,range(0,data['nele'])].copy()
fldvplot=v[fldspeed,range(0,data['nele'])].copy()
fldspeedplot=np.sqrt(flduplot**2+fldvplot**2)
flduplot[fldspeedplot<=.01]=np.nan
fldvplot[fldspeedplot<=.01]=np.nan
#Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],flduplot[sidx],fldvplot[sidx],width=.002,pivot='tail',headwidth=3.,headlength=4)
Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],flduplot[sidx],fldvplot[sidx],angles='xy',scale_units='xy',scale=10)
qk = plt.quiverkey(Q, .1,.9,0.5, '0.5 ms^-1', labelpos='W')
plt.grid()
plt.axis(region['region'])
#plt.show()
plt.savefig(savepath + name + '_' + regionname +'_vector_maxfld_s_' + ("%d" %spacing) + '.png',dpi=1200)

plt.close()
plt.tripcolor(data['trigrid'],np.max(np.sqrt(u**2+v**2),axis=0),vmin=0,vmax=1)
plt.colorbar()
plt.grid()
plt.axis(region['region'])
#plt.show()
plt.savefig(savepath + name + '_' + regionname +'_maxspeed.png',dpi=1200)


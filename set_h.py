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
import netCDF4 as n4
import scipy.interpolate as interp



# Define names and types of data
name='kit4_kelp_20m_0.018'
grid='kit4'
datatype='2d'

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'
indata=load_fvcom_files('runs/'+grid+'/'+name+'/input','kit4','kit4_non_julian_obc.nc')



# Define names and types of data
name2='kit4_kelp_clean'
grid2='kit4_kelp'
datatype='2d'


indata2=load_fvcom_files('runs/'+grid2+'/'+name2+'/input','kit4_kelp')
neifile=loadnei('runs/'+grid2+'/'+name2+'/input/kit4_kelp.nei')
indata2.update(neifile)

interp_h=mpl.tri.LinearTriInterpolator(data['trigrid'], data['h'])
new_h=interp_h(indata2['nodell'][:,0],indata2['nodell'][:,1])


nn_h=interp.NearestNDInterpolator((data['nodell'][:,0],data['nodell'][:,1]), data['h'])
new_h2=nn_h.__call__(indata2['nodell'][:,0],indata2['nodell'][:,1])



f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
triax=ax.tripcolor(indata2['trigridxy'],new_h-new_h2,vmin=-100,vmax=100)
plt.colorbar(triax,ax=ax)
f.show()

f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
triax=ax.tripcolor(indata2['trigridxy'],new_h2,vmin=0,vmax=650)
plt.colorbar(triax,ax=ax)
f.show()

f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigridxy'],data['h'],vmin=0,vmax=650)
plt.colorbar(triax,ax=ax)
f.show()





indata2['h']=new_h2

savenei('data/grid_stuff/kit4_kelp_nnh.nei',indata2)






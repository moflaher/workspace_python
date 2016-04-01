from __future__ import division,print_function
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
from projtools import *
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name='kelpchannel_drag_0.018_500x100'
grid='kelpchannel'
datatype='2d'

### load the .nc file #####
data = loadnc('runs/' +grid+'/' + name + '/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')

savepath='figures/png/' + grid + '_' + datatype + '/kelpideal/'
if not os.path.exists(savepath): os.makedirs(savepath)



# Plot speed
f=plt.figure(figsize=(4,2))
ax=f.add_axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigridxy'],speeder(data['ua'][-1,:],data['va'][-1,:]))
cb=plt.colorbar(triax)
cb.set_label(r'Speed (m/s)')
ax.axis([1000,5000,-1000,1000])
if np.shape(cages)!=():
    cagebox={}
    cagebox['region']=np.array([data['xc'][cages].min(),data['xc'][cages].max(),data['yc'][cages].min(),data['yc'][cages].max()])
    plot_box(ax,cagebox,color='w',lw=.5)
f.savefig(savepath + grid + '_' + name +'_speed.png',dpi=1200)
plt.close(f)

# Plot zeta
f=plt.figure(figsize=(4,2))
ax=f.add_axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigridxy'],data['zeta'][-1,:])
cb=plt.colorbar(triax)
cb.set_label(r'Elevation (m)')
ax.axis([1000,5000,-1000,1000])
if np.shape(cages)!=():
    cagebox={}
    cagebox['region']=np.array([data['xc'][cages].min(),data['xc'][cages].max(),data['yc'][cages].min(),data['yc'][cages].max()])
    plot_box(ax,cagebox,color='w',lw=.5)
f.savefig(savepath + grid + '_' + name +'_zeta.png',dpi=1200)
plt.close(f)




























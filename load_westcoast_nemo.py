from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
from misctools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import time
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import matplotlib.path as path
import netCDF4 as n4
import xarray as xr


# Define names and types of data
name='2012-02-01_2012-03-01_0.01_0.001'
grid='vh_high'
datatype='2d'

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')


grid = xr.open_dataset('https://salishsea.eos.ubc.ca/erddap/griddap/ubcSSnBathymetry2V1')



#old plots for wrong thing.
#f=plt.figure()
#ax=f.add_axes([.125,.1,.775,.8])
#triax=ax.tripcolor(data['trigrid'],data['h'],vmin=-10,vmax=30)
#cb=plt.colorbar(triax)
#cb.set_label('h (m)')
#f.show()

#f=plt.figure()
#ax=f.add_axes([.125,.1,.775,.8])
#triax=ax.tripcolor(data['trigrid'],meanel)
#cb=plt.colorbar(triax)
#cb.set_label('meanel (m)')
#f.show()

#f=plt.figure()
#ax=f.add_axes([.125,.1,.775,.8])
#triax=ax.tripcolor(data['trigrid'],cdnomask)
#cb=plt.colorbar(triax)
#cb.set_label('cdnomask (m)')
#f.show()

#f=plt.figure()
#ax=f.add_axes([.125,.1,.775,.8])
#triax=ax.tripcolor(data['trigrid'],data['h']-meanel-cdnomask,vmin=-10,vmax=30)
#cb=plt.colorbar(triax)
#cb.set_label('all (m)')
#f.show()





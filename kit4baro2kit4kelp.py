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
name_old='kit4_kelp_20m_0.018'
grid_old='kit4'
datatype='2d'
### load the .nc file #####
data_old = loadnc('runs/'+grid_old+'/'+name_old+'/output/',singlename=grid_old + '_0001.nc')
print 'done load'
data_old = ncdatasort(data_old)
print 'done sort'


# Define names and types of data
name_new='kit4_kelp_20m_drag_0.018'
grid_new='kit4_kelp'
datatype='2d'
### load the .nc file #####
data_new = loadnc('runs/'+grid_new+'/'+name_new+'/output/',singlename=grid_new + '_0001.nc')
print 'done load'
data_new = ncdatasort(data_new)
print 'done sort'


indata2=load_fvcom_files('runs/'+grid_new+'/'+name_new+'/input','kit4_kelp')


filepath='data/misc/baroclinic/kit4-spring/'

kill
nn_h=interp.NearestNDInterpolator((data['nodell'][:,0],data['nodell'][:,1]), data['h'])
new_h2=nn_h.__call__(indata2['nodell'][:,0],indata2['nodell'][:,1])















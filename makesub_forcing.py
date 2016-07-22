from __future__ import division,print_function
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
import netCDF4 as n4
import scipy.interpolate as interp
import shutil

cons=['M2','K1']
place=[0,4]

#cons=['M2']
#place=[0]

#cons=['K1']
#place=[4]


filepath='data/grid_stuff/'

#new ncfile name
ncid = n4.Dataset(filepath+'vhhigh_v3_spectide.nc', 'r',format='NETCDF3_CLASSIC')
g = n4.Dataset(filepath+'vhhigh_v3_spectide_m2k1.nc', 'w',format='NETCDF3_CLASSIC')



#Create new its.nc file
# To copy the global attributes of the netCDF file  
for attname in ncid.ncattrs():
    setattr(g,attname,getattr(ncid,attname))

# To copy the dimension of the netCDF file
for dimname,dim in ncid.dimensions.iteritems():
       # if you want to make changes in the dimensions of the new file
       # you should add your own conditions here before the creation of the dimension.
        if dimname=='tidal_components':
            g.createDimension(dimname,len(cons))
        else:
            g.createDimension(dimname,len(dim))

# To copy the variables of the netCDF file
for varname,ncvar in ncid.variables.iteritems():
        #if you want to make changes in the variables of the new file
        # you should add your own conditions here before the creation of the variable.

        var = g.createVariable(varname,ncvar.dtype,ncvar.dimensions)
        #Proceed to copy the variable attributes
        for attname in ncvar.ncattrs():  
           setattr(var,attname,getattr(ncvar,attname))
        #Finally copy the variable data to the new created variable
        if varname=='tide_period':
            g.variables['tide_period'][:]=ncid.variables['tide_period'][place]
        elif varname=='tide_Ephase':
            g.variables['tide_Ephase'][:]=ncid.variables['tide_Ephase'][place,:]
        elif varname=='tide_Eamp':
            g.variables['tide_Eamp'][:]=ncid.variables['tide_Eamp'][place,:]
        elif varname=='equilibrium_tide_Eamp':
            g.variables['equilibrium_tide_Eamp'][:]=ncid.variables['equilibrium_tide_Eamp'][place]
        elif varname=='equilibrium_beta_love':
            g.variables['equilibrium_beta_love'][:]=ncid.variables['equilibrium_beta_love'][place]
        elif varname=='equilibrium_tide_type':
            g.variables['equilibrium_tide_type'][:]=ncid.variables['equilibrium_tide_type'][place,:]
        else:
            var[:] = ncvar[:]


ncid.close()
g.close()




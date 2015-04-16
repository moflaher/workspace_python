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
import netCDF4 as n4
import scipy.interpolate as interp
import shutil



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


indata_new=load_fvcom_files('runs/'+grid_new+'/'+name_new+'/input','kit4_kelp')


filepath='data/misc/baroclinic/kit4-spring-convert/'
indata_old=load_fvcom_files(filepath,'kit4')



#new ncfile name
ncid = n4.Dataset(filepath+'kit4-spring-its.nc', 'r',format='NETCDF3_CLASSIC')
g = n4.Dataset(filepath+'kit4_kelp-spring-its.nc', 'w',format='NETCDF3_CLASSIC')

newtsl=np.empty((1,ncid.variables['tsl'].shape[1],len(data_new['nodell'][:,0])))
for level in range(ncid.variables['tsl'].shape[1]):
    nn_tsl=interp.NearestNDInterpolator((data_old['nodell'][:,0],data_old['nodell'][:,1]), np.squeeze(ncid.variables['tsl'][0,level,:]))
    newtsl[0,level,:]=nn_tsl.__call__(indata_new['nodell'][:,0],indata_new['nodell'][:,1])

newssl=np.empty((1,ncid.variables['ssl'].shape[1],len(data_new['nodell'][:,0])))
for level in range(ncid.variables['ssl'].shape[1]):
    nn_ssl=interp.NearestNDInterpolator((data_old['nodell'][:,0],data_old['nodell'][:,1]), np.squeeze(ncid.variables['ssl'][0,level,:]))
    newssl[0,level,:]=nn_ssl.__call__(indata_new['nodell'][:,0],indata_new['nodell'][:,1])



#Create new its.nc file
# To copy the global attributes of the netCDF file  
for attname in ncid.ncattrs():
    setattr(g,attname,getattr(ncid,attname))

# To copy the dimension of the netCDF file
for dimname,dim in ncid.dimensions.iteritems():
       # if you want to make changes in the dimensions of the new file
       # you should add your own conditions here before the creation of the dimension.
        if dimname=='node':
            g.createDimension(dimname,len(data_new['nodell'][:,0]))
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
        if varname=='tsl':
            g.variables['tsl'][:]=newtsl
        elif varname=='ssl':
            g.variables['ssl'][:]=newssl
        else:
            var[:] = ncvar[:]


ncid.close()
g.close()


#new ncfile name
os.system('cp '+ filepath+'kit4-spring-tsobc.nc '+filepath+'kit4_kelp-spring-tsobc.nc')
ncid = n4.Dataset(filepath+'kit4_kelp-spring-tsobc.nc', 'r+',format='NETCDF3_CLASSIC')
ncid.variables['obc_nodes'][:]=indata_new['obcf_nodes'].astype(int)
ncid.variables['obc_h'][:]=data_new['h'][indata_new['obcf_nodes'].astype(int)-1]
ncid.close()


os.system('cp '+ filepath+'kit4-20140401-el_obc.nc '+filepath+'kit4_kelp-20140401-el_obc.nc')
ncid = n4.Dataset(filepath+'kit4_kelp-20140401-el_obc.nc', 'r+',format='NETCDF3_CLASSIC')
ncid.variables['obc_nodes'][:]=indata_new['obcf_nodes'].astype(int)
ncid.close()






















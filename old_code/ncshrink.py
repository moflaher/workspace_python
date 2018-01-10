from __future__ import division
import numpy as np
import sys
import netCDF4 as n4
import time



zlib = True
least_significant_digit = 3
cl= 9
shuf=True


start = time.clock()

ncid = n4.Dataset('vh_high_0001.nc', 'r',format='NETCDF3_CLASSIC')
g = n4.Dataset('vh_high_0001_small_4c_z{}_cl{}_lsd{}_shuf{}.nc'.format(zlib,cl,least_significant_digit,shuf), 'w',format='NETCDF4_CLASSIC')

for attname in ncid.ncattrs():
    setattr(g,attname,getattr(ncid,attname))

# To copy the dimension of the netCDF file
for dimname,dim in ncid.dimensions.iteritems():
       # if you want to make changes in the dimensions of the new file
       # you should add your own conditions here before the creation of the dimension.
        g.createDimension(dimname,len(dim))

# To copy the variables of the netCDF file
for varname,ncvar in ncid.variables.iteritems():
        #if you want to make changes in the variables of the new file
        # you should add your own conditions here before the creation of the variable.
        if 'float' in ncvar.dtype.name:
            var = g.createVariable(varname,ncvar.dtype,ncvar.dimensions, zlib=zlib, least_significant_digit=least_significant_digit, complevel=cl, shuffle=shuf)
        else:
            var = g.createVariable(varname,ncvar.dtype,ncvar.dimensions)
        #Proceed to copy the variable attributes
        for attname in ncvar.ncattrs():  
           setattr(var,attname,getattr(ncvar,attname))
        #Finally copy the variable data to the new created variable
        var[:] = ncvar[:]


ncid.close()
g.close()

print ('savefile: %f' % (time.clock() - start))

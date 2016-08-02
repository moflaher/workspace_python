from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import netCDF4 as n4


fileone='ncfilewith_latlon'
filetwo='ncfilewith_xy'

fileout='newncfile_withboth'


#have to remove file first or errors...
os.system('rm '+fileout)
os.system('cp '+fileone+' '+fileout)
#new ncfile name
ncid = n4.Dataset(filetwo, 'r',format='NETCDF3_CLASSIC')
g = n4.Dataset(fileout, 'r+',format='NETCDF3_CLASSIC')



##Create new its.nc file
## To copy the global attributes of the netCDF file  
#for attname in ncid.ncattrs():
    #setattr(g,attname,getattr(ncid,attname))

## To copy the dimension of the netCDF file
#for dimname,dim in ncid.dimensions.iteritems():
       ## if you want to make changes in the dimensions of the new file
       ## you should add your own conditions here before the creation of the dimension.
        #if dimname=='node':
            #g.createDimension(dimname,len(data_new['nodell'][:,0]))
        #elif dimname=='time':
            #g.createDimension(dimname,None)
        #else:
            #g.createDimension(dimname,len(dim))

# To copy the variables of the netCDF file
for varname,ncvar in ncid.variables.iteritems():
        #if you want to make changes in the variables of the new file
        # you should add your own conditions here before the creation of the variable.
        if varname in ['x', 'y']:
            var = g.createVariable(varname,ncvar.dtype,ncvar.dimensions)
            #Proceed to copy the variable attributes
            for attname in ncvar.ncattrs():  
               setattr(var,attname,getattr(ncvar,attname))
            #Finally copy the variable data to the new created variable
            var[:] = ncvar[:]


ncid.close()
g.close()









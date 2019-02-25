from __future__ import division,print_function
import numpy as np
import scipy as sp
from mytools import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import os, sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pandas as pd
import matplotlib.dates as dates
import argparse
from collections import OrderedDict


parser = argparse.ArgumentParser()
parser.add_argument("oldfile", help="name of the file to convert", type=str)
parser.add_argument("oldpath", help="where is the file to convert", type=str)
parser.add_argument("newpath", help="where to put the new file", type=str)
args = parser.parse_args()

print("The current commandline arguments being used are")
print(args)


# data=loadnc('','Creg12-CMC-ANAL_1d_grid_T_20151028-20151028.nc',False)

# r=np.array([-71.6,-57.5,37.25,46.5])
# b={}
# b['region']=np.array([-71.6,-57.5,37.25,46.5])

# idx=np.argwhere((data['nav_lon']>=r[0]) & (data['nav_lon']<=r[1]) & (data['nav_lat']>=r[2]) & (data['nav_lat']<=r[3]))



# lonmin=idx[:,0].min()-1
# lonmax=idx[:,0].max()+2
# latmin=idx[:,1].min()-1
# latmax=idx[:,1].max()+2
ll=np.array([166, 334, 265, 442])



# f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8]);

# #ax.plot(data['nav_lon'][:],data['nav_lat'][:],'.')
# cax=ax.pcolormesh(data['nav_lon'][lonmin:lonmax,latmin:latmax],data['nav_lat'][lonmin:lonmax,latmin:latmax],data['so'][0,0,lonmin:lonmax,latmin:latmax],vmin=20,vmax=35)
# plt.colorbar(cax)
# plot_box(ax,b)
# f.show()
# #plt.close(f)


oldpath=args.oldpath
oldfile=args.oldfile
newpath=args.newpath
newfile=args.oldfile.replace(args.oldfile[-12:-3],'')


#oldfile='Creg12-CMC-ANAL_1h_grid_T_2D_20151028-20151028.nc'
#newfile='test/Creg12-CMC-ANAL_1h_grid_T_2D_20151028_test.nc'


#oldfile='Creg12-CMC-ANAL_1d_grid_T_20151028-20151028.nc'
#newfile='test/Creg12-CMC-ANAL_1d_grid_T_20151028_test.nc'


ncid = n4.Dataset(oldfile, 'r',format='NETCDF4')
g = n4.Dataset(newfile, 'w',format='NETCDF4')


for attname in ncid.ncattrs():
    setattr(g,attname,getattr(ncid,attname))

for dimname,dim in ncid.dimensions.iteritems():
    if dimname=='y':
        g.createDimension(dimname,ll[1]-ll[0])
    elif dimname=='x':
        g.createDimension(dimname,ll[3]-ll[2])
    elif dimname=='time_counter':
        g.createDimension('time',len(dim))
        print(len(dim))
    elif dimname=='deptht':
        g.createDimension('depth',75)
    elif dimname=='axis_nbounds':
        g.createDimension(dimname,len(dim))
    else:
        print('Derp bad dim: {}'.format(dimname))


for varname,ncvar in ncid.variables.iteritems():
    print('='*80)
    print(varname)
    if varname=='tdhm' or varname=='ssh_ib':
        continue
    dims=tuple([t.replace('deptht','depth').replace('time_counter','time') for t in ncvar.dimensions])
    varname=varname.replace('deptht','depth').replace('time_counter','time').replace('thetao','votemper').replace('so','vosaline').replace('zos','sossheig')
    print(dims,varname)
    if varname=='votemper':
        var = g.createVariable(varname,ncvar.dtype,dims,fill_value=ncid.variables['thetao']._FillValue)
    elif varname=='vosaline':
        var = g.createVariable(varname,ncvar.dtype,dims,fill_value=ncid.variables['so']._FillValue)
    elif varname=='sossheig':
        var = g.createVariable(varname,ncvar.dtype,dims,fill_value=ncid.variables['zos']._FillValue)
    else:
        var = g.createVariable(varname,ncvar.dtype,dims)
    
    #Proceed to copy the variable attributes
    for attname in ncvar.ncattrs():  
        if attname=='_FillValue':
            continue
        else:
            if attname=='name':
                attname='standard_name'
                setattr(var,attname,getattr(ncvar,'name'))
            else:
                setattr(var,attname,getattr(ncvar,attname))
    
    if varname=='nav_lon' or varname=='nav_lat':
        g.variables[varname][:]=ncid.variables[varname][ll[0]:ll[1],ll[2]:ll[3]]
    elif varname=='depth':
        g.variables['depth'][:]=ncid.variables['deptht'][:]
    elif varname=='depth_bounds':
        g.variables['depth_bounds'][:]=ncid.variables['deptht_bounds'][:]
    elif varname=='time_bounds':
        g.variables['time_bounds'][:]=ncid.variables['time_counter_bounds'][:]
    elif varname=='time':
        g.variables['time'][:]=ncid.variables['time_counter'][:]
    elif varname=='votemper':
        g.variables[varname][:]=ncid.variables['thetao'][:,:,ll[0]:ll[1],ll[2]:ll[3]]
    elif varname=='vosaline':
        g.variables[varname][:]=ncid.variables['so'][:,:,ll[0]:ll[1],ll[2]:ll[3]]
    elif varname=='sossheig':
        g.variables[varname][:]=ncid.variables['zos'][:,ll[0]:ll[1],ll[2]:ll[3]]-ncid.variables['tdhm'][:,ll[0]:ll[1],ll[2]:ll[3]]-ncid.variables['ssh_ib'][:,ll[0]:ll[1],ll[2]:ll[3]]
    else:
        var[:] = ncid.variables[varname][:]

ncid.close()
g.close()


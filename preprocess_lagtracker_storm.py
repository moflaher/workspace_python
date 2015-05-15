from __future__ import division
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
import scipy.io as sio
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import netCDF4 as n4
import pyproj
import time 

filepath='data/misc/lagtracker_storm/'

for num in range(6):
    filename='Storm' + ("%02d"%(num+1)) + '.mat'
    print filename

    storm=sio.loadmat(filepath+filename)

    projstr='lcc +lon_0=-129.4954 +lat_0=53.55285 +lat_1=52.36906 +lat_2=54.73664'
    p=pyproj.Proj(proj=projstr)

    LON,LAT=np.meshgrid(storm['lon'],storm['lat'])

    X, Y = p(LON,LAT)

    os.system('rm '+filepath+filename[:-3]+'nc')
    ncid = n4.Dataset(filepath+filename[:-3]+'nc', 'w',format='NETCDF3_CLASSIC')

    #create dimensions
    ncid.createDimension('npts',Y.size)
    ncid.createDimension('time',None) 

    #define variables
    lat = ncid.createVariable('lat','d',('npts',))
    lon = ncid.createVariable('lon','d',('npts',))
    x = ncid.createVariable('x','d',('npts',))
    y = ncid.createVariable('y','d',('npts',))
    uwnd = ncid.createVariable('uwnd','d',('time','npts'))
    vwnd = ncid.createVariable('vwnd','d',('time','npts'))
    uuss = ncid.createVariable('uuss','d',('time','npts'))
    uvss = ncid.createVariable('vuss','d',('time','npts'))
    times = ncid.createVariable('time','d',('time',))

    lon[:] = LON
    lat[:] = LAT
    x[:]=X
    y[:]=Y
    tl=len(storm['time'])

    #linear interpcode to hourly data to match nc file. code assumes 3hour input data
    newtime=np.linspace(storm['time'][0],storm['time'][-1],3*(tl-1)+1)

    def lininterp(varin):
        tl=varin.shape[2]
        vartmp=varin.transpose(1,0,2).reshape(-1,tl).T
        varout=np.empty((3*(tl-1)+1,vartmp.shape[1]))
        for i in range(tl):
            if i==tl-1:
                varout[3*(i),:]=vartmp[i,:]
            else:
                varout[3*(i),:]=vartmp[i,:]
                varout[3*(i)+1,:]=(vartmp[i,:]*2/3)+(vartmp[i+1,:]*1/3)
                varout[3*(i)+2,:]=(vartmp[i,:]*1/3)+(vartmp[i+1,:]*2/3)

        return varout
        

    uwnd[:]=lininterp(storm['uwnd'])
    vwnd[:]=lininterp(storm['vwnd'])
    uuss[:]=lininterp(storm['uuss'])
    uvss[:]=lininterp(storm['vuss'])
    times[:]=newtime


    ncid.__setattr__('description','Reprocessed from ' +filename)
    ncid.__setattr__('history','Created ' +time.ctime(time.time()) )
    ncid.__setattr__('warning','Data was projected using LCC for the kit4_kelp grid.')
    ncid.__setattr__('coordinateprojection',projstr)

    ncid.close()




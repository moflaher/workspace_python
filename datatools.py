# -*- coding: utf-8 -*-
"""
Front Matter
=============

Created on Fri Jun 21 12:42:46 2013

Author: Robie Hennigar

A compilation of functions that are used for analysing the data
contained in .nc files.

Requirements
===================================
Absolutely Necessary:

* Numpy
* SciPy
* Matplotlib
* Numexpr

Optional, but recommended:

* Numba

Functions
=========
"""
#load modules
from __future__ import division,print_function,print_function
import collections
import matplotlib.dates as dates

#Numerical modules
import numpy as np
import matplotlib.tri as mplt
import bisect
import numexpr as ne
import h5py
import scipy.stats as stats

#I/O modules
import glob
from scipy.io import netcdf
import scipy.io as sio
import mmap
import os
from osgeo import ogr
from osgeo import osr





def loadnc(datadir, singlename=None):
    """
    Loads a .nc  data file

    :Parameters:
        **datadir** -- The path to the directory where the data is stored.

        **singlename (optional)** -- the name of the .nc file of interest,
            not needed if there is only one .nc file in datadir       
    """
    #identify the file to load
    if singlename == None:
        files = glob.glob(datadir + "*.nc")
        filepath = files[0]
        #print filepath
    else:
        filepath = datadir + singlename

    #initialize a dictionary for the data.
    data = {}
    #store the filepath in case it is needed in the future
    data['filepath'] = filepath

    #load data
    ncid = netcdf.netcdf_file(filepath, 'r',mmap=True)

    for i in ncid.variables.keys():
        data[i]=ncid.variables[i].data

   
    #data['nv'] = np.transpose(ncid.variables['nv'].data.astype(int))-[1] #python index
    #data['nbe'] = np.transpose(ncid.variables['nbe'].data.astype(int))-[1] #python index
    if ('nv' in data):
        data['nv']=data['nv'].astype(int).T-1
    if ('nbe' in data):
        data['nbe']=data['nbe'].astype(int).T-1
    if ('nele' in ncid.dimensions):    
        data['nele'] = ncid.dimensions['nele']
    if ('node' in ncid.dimensions):
        data['node'] = ncid.dimensions['node']

   
    #ncid.close()
    #Now we get the long/lat data.  Note that this method will search
    #for long/lat files in the datadir and up to two levels above
    #the datadir.
    if (('lon' in data) and ('x' in data)):
        if ((data['lon'].sum()==0).all() or (data['x']==data['lon']).all()):
            long_matches = []
            lat_matches = []

            if glob.glob(datadir + "*_long.dat"):
                long_matches.append(glob.glob(datadir + "*_long.dat")[0])
            if glob.glob(datadir + "*_lat.dat"):
                lat_matches.append(glob.glob(datadir + "*_lat.dat")[0])
            if glob.glob(datadir + "../*_long.dat"):
                long_matches.append(glob.glob(datadir + "../*_long.dat")[0])
            if glob.glob(datadir + "../*_lat.dat"):
                lat_matches.append(glob.glob(datadir + "../*_lat.dat")[0])
            if glob.glob(datadir + "../../*_long.dat"):
                long_matches.append(glob.glob(datadir + "../../*_long.dat")[0])
            if glob.glob(datadir + "../../*_lat.dat"):
                lat_matches.append(glob.glob(datadir + "../../*_lat.dat")[0])
            if glob.glob(datadir + "../input/*_long.dat"):
                long_matches.append(glob.glob(datadir + "../input/*_long.dat")[0])
            if glob.glob(datadir + "../input/*_lat.dat"):
                lat_matches.append(glob.glob(datadir + "../input/*_lat.dat")[0])

                #let's make sure that long/lat files were found.
            if (len(long_matches) > 0 and len(lat_matches) > 0):
                data['lon'] = np.loadtxt(long_matches[0])
                data['lat'] = np.loadtxt(lat_matches[0])        
            else:        
                print("No long/lat files found. Long/lat set to x/y")
                data['lon'] = data['x']
                data['lat'] = data['y']

            
    if ('nv' in data):
        data['trigrid'] = mplt.Triangulation(data['lon'], data['lat'],data['nv'])   
        data['trigridxy'] = mplt.Triangulation(data['x'], data['y'],data['nv'])
  
        
    return data


def ncdatasort(data,trifinder=False,uvhset=True):
    """
    From the nc data provided, common variables are produced.

    :Parameters: **data** -- a data dictionary of data from a .nc file

    :Returns: **data** -- Python data dictionary updated to include uvnode and uvnodell
    """

    nodexy = np.zeros((len(data['x']),2))
    nodexy[:,0]

    x = data['x']
    y = data['y']
    nv = data['nv']
    lon = data['lon']
    lat = data['lat']

    #make uvnodes by averaging the values of ua/va over the nodes of
    #an element
    nodexy = np.empty((len(lon),2))
    nodexy[:,0] = x
    nodexy[:,1] = y
    uvnode = np.empty((len(nv[:,0]),2))
    uvnode[:,0] = (x[nv[:,0]] + x[nv[:,1]] + x[nv[:,2]]) / 3.0
    uvnode[:,1] = (y[nv[:,0]] + y[nv[:,1]] + y[nv[:,2]]) / 3.0

    nodell = np.empty((len(lon),2))
    nodell[:,0] = lon
    nodell[:,1] = lat
    uvnodell = np.empty((len(nv[:,0]),2))
    uvnodell[:,0] = (lon[nv[:,0]] + lon[nv[:,1]] + lon[nv[:,2]]) / 3.0
    uvnodell[:,1] = (lat[nv[:,0]] + lat[nv[:,1]] + lat[nv[:,2]]) / 3.0
   
    if (uvhset==True):
        uvh= np.empty((len(nv[:,0]),1))   
        uvh[:,0] = (data['h'][nv[:,0]] + data['h'][nv[:,1]] + data['h'][nv[:,2]]) / 3.0
        data['uvh']=uvh

    data['uvnode'] = uvnode
    data['uvnodell'] = uvnodell
    data['nodell'] = nodell
    data['nodexy'] = nodexy

    if ('time' in data):
        data['time']=data['time']+678576

    if ('trigrid' in data)==False:
        if (('nv' in data) and('lon' in data) and ('lat' in data)):
            data['trigrid'] = mplt.Triangulation(data['lon'], data['lat'],data['nv'])  
    
    if ('trigridxy' in data)==False:
        if (('nv' in data) and('x' in data) and ('y' in data)):
            data['trigridxy'] = mplt.Triangulation(data['x'], data['y'],data['nv'])  

    if trifinder==True:
        data['trigrid_finder']=data['trigrid'].get_trifinder()
        data['trigridxy_finder']=data['trigridxy'].get_trifinder()

    return data


def closest_node(data, locations):
    """
    Given long\lat points, find the nearest nodes, and return the node indexs.  
    """

    #make the locations at least 2d so that the code works for a single location
    locations=np.atleast_2d(locations)


    #this is just a list comprehension of 
    #idx=np.argmin((data['nodell'][:,0]-location[0])**2+(data['nodell'][:,1]-location[1])**2)
    idx=np.array([np.argmin((data['nodell'][:,0]-locations[i,0])**2+(data['nodell'][:,1]-locations[i,1])**2) for i in range(len(locations))])

    #if locations only had one point return the value instead of array of the value.
    #this is so that the multipoint function acts like the only one when given a single point
    if idx.size==1:
        idx=idx[0]
    
    return idx


def closest_element(data, locations):
    """
    Given long\lat points, find the nearest elements, and return the element indexs.  
    """

    #make the locations at least 2d so that the code works for a single location
    locations=np.atleast_2d(locations)


    #this is just a list comprehension of 
    #idx=np.argmin((data['uvnodell'][:,0]-location[0])**2+(data['uvnodell'][:,1]-location[1])**2)
    idx=np.array([np.argmin((data['uvnodell'][:,0]-locations[i,0])**2+(data['uvnodell'][:,1]-locations[i,1])**2) for i in range(len(locations))])

    #if locations only had one point return the value instead of array of the value.
    #this is so that the multipoint function acts like the only one when given a single point
    if idx.size==1:
        idx=idx[0]
    
    return idx


def get_elements(data, region):
    """
    Takes uvnodes and a  region (specified by the corners of a
    rectangle) and determines the elements of uvnode that lie within the
    region
    """
    elements = np.where((data['uvnodell'][:,0] >= region['region'][0]) & (data['uvnodell'][:,0] <= region['region'][1]) & (data['uvnodell'][:,1] >= region['region'][2]) & (data['uvnodell'][:,1] <= region['region'][3]))[0]

    return elements


def get_elements_xy(data, region):
    """
    Takes uvnodes and a  region (specified by the corners of a
    rectangle) and determines the elements of uvnode that lie within the
    region
    """
    elements = np.where((data['uvnode'][:,0] >= region['region'][0]) & (data['uvnode'][:,0] <= region['region'][1]) & (data['uvnode'][:,1] >= region['region'][2]) & (data['uvnode'][:,1] <= region['region'][3]))[0]

    return elements


def get_nodes(data, region):
    """
    Takes nodexy and a region (specified by the corners of a rectangle)
    and determines the nodes that lie in the region
    """
   
    nodes = np.where((data['nodell'][:,0] >= region['region'][0]) & (data['nodell'][:,0] <= region['region'][1]) & (data['nodell'][:,1] >= region['region'][2]) & (data['nodell'][:,1] <= region['region'][3]))[0]
    return nodes


def get_nodes_xy(data, region):
    """
    Takes nodexy and a region (specified by the corners of a rectangle)
    and determines the nodes that lie in the region
    """
   
    nodes = np.where((data['nodexy'][:,0] >= region['region'][0]) & (data['nodexy'][:,0] <= region['region'][1]) & (data['nodexy'][:,1] >= region['region'][2]) & (data['nodexy'][:,1] <= region['region'][3]))[0]
    return nodes


def calc_speed(data):
    """
    Calculates the speed from ua and va

    :Parameters:
        **data** -- the standard python data dictionary

    .. note:: We use numexpr here because, with multiple threads, it is\
    about 30 times faster than direct calculation.
    """
    #name required variables
    ua = data['ua']
    va = data['va']

    #we can take advantage of multiple cores to do this calculation
    ne.set_num_threads(ne.detect_number_of_cores())
    #calculate the speed at each point.
    data['speed'] = ne.evaluate("sqrt(ua*ua + va*va)")
    return data


def calc_energy(data):
    """Calculate the energy of the entire system.

    :Parameters: **data** -- the standard python data dictionary
    """
    #name relevant variables
    x = data['x']
    y = data['y']
    nv = data['nv']
    rho = 1000 #density of water
    #initialize EK to zero
    l = nv.shape[0]
    area = np.zeros(l)
    for i in xrange(l):
        #first, calculate the area of the triangle
        xCoords = x[nv[i,:]]
        yCoords = y[nv[i,:]]
        #Compute two vectors for the area calculation.
        v1x = xCoords[1] - xCoords[0]
        v2x = xCoords[2] - xCoords[0]
        v1y = yCoords[1] - yCoords[0]
        v2y = yCoords[2] - yCoords[0]
        #calculate the area as the determinant
        area[i] = abs(v1x*v2y - v2x*v1y)
    #get a vector of speeds.
    sdata = calc_speed(data)
    speed = sdata['speed']

    #calculate EK, use numexpr for speed (saves ~15 seconds)
    ne.set_num_threads(ne.detect_number_of_cores())
    ek = ne.evaluate("sum(rho * area * speed * speed, 1)")
    ek = ek / 4
    data['ek'] = ek
    return data


def size_check(datadir):
    """Used in ncMerger.  Determines the total number of time series for a
    number of .nc files in a directory

    :Parameters:
        **datadir** -- The directory where the .nc files are contained.
    """
    files = glob.glob(datadir + '*.nc')
    numFiles = len(files)
    ncid = netcdf.netcdf_file(files[0])
    nele = ncid.dimensions['nele']
    node = ncid.dimensions['node']
    ncid.close()
    timeDim = 0
    for i in xrange(numFiles):
        ncid = netcdf.netcdf_file(files[i])
        timeDim += len(ncid.variables['time'].data)
        ncid.close()
    return nele, node, timeDim


def time_sorter(datadir):
    """Used in ncMerger.  Sorts the output of glob (which has no inherent
    order) so that the files can be loaded chronologically.

    :Parameters:
        **datadir** -- The directory where the .nc files are contained.

    :Returns:
        **ordered_time** -- A list of indices that sort the output of glob.
    """
    files = glob.glob(datadir + "*.nc")
    first_time = np.zeros(len(files))
    for i in xrange(len(files)):
        ncid = netcdf.netcdf_file(files[i])
        first_time[i] = ncid.variables['time'][0]
        ncid.close()
    ordered_time = first_time.argsort()
    return ordered_time


def nan_index(data, dim='2D'):
    """Used in ncMerger. Determines, for a given data set, what time series
    contain nans.  Also calculates the fraction of
    a data set that is nans (a measure of the 'goodness' of
    the data set).

    :Parameters:
        **data** -- The typical python data dictionary, containing
        merged data.

        **dim = {'2D', '3D'}** -- The dimension of the data.

    :Returns:
        **nanInd** -- A list containing the time series that contain nans

        **nanFrac** -- The fraction of nans in a given time series.
    """
    #name necessary variables
    #initialize list of nan-containing time series
    nanInd = []
    key = ['ua', 'va']
    if dim == '3D':
        three_d =['u', 'v', 'ww']
        key.append(i for i in three_d)

    for i in xrange(data['time'].shape[0]):
        checkArray = []
        for j in key:
            checkArray.append(np.isnan(np.sum(data[j][i,:])))
        if dim == '3D':
            for p in key:
                checkArray.append(np.isnan(np.sum(data[p][i,:,:])))
        if True in checkArray:
            nanInd.append(i)
    #calculate percentage of nans
    nanFrac = len(nanInd)/data['time'].shape[0]
    return nanInd, nanFrac


def merge_nc(datadir, savedir, clean_nans = False, intelligent=False,dim='2D'):
    """Merge data for all .nc files in a particular directory.  Assumes
    that all the data has the same nele, node (i.e. is for the same grid)

    :Parameters:
        **datadir** -- The directory where the .nc files are contained.

        **savedir** -- The directory where the output should be saved.

        **clean_nans = {True, False}** -- Optional. If set to True,
            any time series that contain nans in the data series will be
            stripped.  Will result in slightly slower code.

        **intelligent = {True, False}** -- Optional.  This is only useful
            for  data files that have overlap.  If set to True, and two
            time series overlap, the code will select the time series
            with the smallest nanFrac.  This will result in a noticable
            slowdown.  Sets clean_nans to True.

        **dim ={'2D', '3D'} ** -- Optional.  The dimension of the datafile,
            assumed to be 2D unless otherwise specified.

    """
    #generate a list of all files in the directory
    files = glob.glob(datadir + '*.nc')
    numFiles = len(files)
    #get the proper indices to load the files.
    ordered_time = time_sorter(datadir)
    #load the first file
    singlename = os.path.basename(files[ordered_time[0]])
    data = loadnc(datadir, singlename=singlename, dim=dim)
    #name the variables that will be used, according to dimension
    if dim == '2D':
        key = ['time', 'ua', 'va', 'zeta']
    elif dim == '3D':
        key = ['time', 'ua', 'va', 'zeta', 'u', 'v', 'ww']
    else:
        raise Exception('Dim must be 2D or 3D.  Correct this in your \
            call to nc_merge.')
    #get the dimensions we will need.
    nele, node, timeDim = size_check(datadir)

    #pre-allocate arrays that we will dump the data in, for speed.
    Time = np.zeros(timeDim)
    UA = np.zeros((timeDim, nele))
    VA = np.zeros((timeDim, nele))
    ZETA = np.zeros((timeDim, node))
    if dim == '3D':
        a = data['u'].shape[1]
        U = np.zeros((timeDim, a, nele))
        V = np.zeros((timeDim, a, nele))
        WW = np.zeros((timeDim, a, nele))
    #The code will now differ depending on whether intelligent was set to
    #True or not.
    if not intelligent:
        #start filling the matrices
        l = len(data['time'])
        Time[0:l] = data['time']
        UA[0:l,:] = data['ua']
        VA[0:l,:] = data['va']
        ZETA[0:l,:] = data['zeta']
        if dim == '3D':
            U[0:l,...] = data['u']
            V[0:l,...] = data['v']
        #placeholder for the last time series
        nt = l - 1
        #loop through all files in the directory, remember the first has
        #already been loaded.

        #first, for a 2D file
        if dim == '2D':
            for i in xrange(1, numFiles):
                #load a file
                ncid = netcdf.netcdf_file(files[ordered_time[i]],'r')
                ua_temp = ncid.variables['ua'].data
                va_temp = ncid.variables['va'].data
                zeta_temp = ncid.variables['zeta'].data
                time_temp = ncid.variables['time'].data
                ncid.close()

                #how many time series could be added, at most
                ltt = len(time_temp)

                #discover if there is any overlap in time series
                start = bisect.bisect_left(Time, time_temp[0])
                start_ind = start
                #determine if there was a match.  Note that if there was
                #no match, bisect returns the last index.

                if start != timeDim:
                    #there is a matching index, i.e. the data overlaps
                    NT = ltt + start
                    Time[start_ind:NT] = time_temp
                    UA[start_ind:NT,:] = ua_temp
                    VA[start_ind:NT,:] = va_temp
                    ZETA[start_ind:NT,:] = zeta_temp
                    nt = NT
                else:
                    #there was no matching index, i.e. the data does not                         overlap
                    numT = ltt + nt
                    Time[nt:numT] = time_temp
                    UA[nt:numT,:] = ua_temp
                    VA[nt:numT,:] = va_temp
                    ZETA[nt:numT,:] = zeta_temp
                    nt += ltt
                print("Loaded file " + str(i+1) + " of " + str(numFiles) + ".")
        else:
            for i in xrange(1, numFiles):
                #load a file
                ncid = netcdf.netcdf_file(files[ordered_time[i]],'r')
                ua_temp = ncid.variables['ua'].data
                va_temp = ncid.variables['va'].data
                zeta_temp = ncid.variables['zeta'].data
                time_temp = ncid.variables['time'].data
                u_temp = ncid.variables['u'].data
                v_temp = ncid.variables['v'].data
                ww_temp = ncid.variables['ww'].data
                ncid.close()

                #how many time series could be added, at most
                ltt = len(time_temp)

                #discover if there is any overlap in time series
                start = bisect.bisect_left(Time, time_temp[0])

                #determine if there was a match.  Note that if there was
                #no match, bisect returns the last index.

                if start != timeDim:
                    #there is a matching index, i.e. the data overlaps
                    NT = ltt + start
                    Time[start_ind:NT] = time_temp
                    UA[start_ind:NT,:] = ua_temp
                    VA[start_ind:NT,:] = va_temp
                    ZETA[start_ind:NT,:] = zeta_temp
                    U[start_ind:NT,...] = u_temp
                    V[start_ind:NT,...] = v_temp
                    WW[start_ind:NT,...] = ww_temp
                    nt = NT
                else:
                    #there was no matching index, i.e. the data does not                         overlap
                    numT = ltt + nt
                    Time[nt:numT] = time_temp
                    UA[nt:numT,:] = ua_temp
                    VA[nt:numT,:] = va_temp
                    ZETA[nt:numT,:] = zeta_temp
                    U[nt:numT,...] = u_temp
                    V[nt:numT,...] = v_temp
                    WW[nt:numT,...] = ww_temp
                    nt += ltt
            print("Loaded file " + str(i+1) + " of " + str(numFiles) + ".")
        #now for the intelligent part
    else:
        l = len(data['time'])
        Time[0:l] = data['time']
        UA[0:l,:] = data['ua']
        VA[0:l,:] = data['va']
        ZETA[0:l,:] = data['zeta']
        if dim == '3D':
            U[0:l,...] = data['u']
            V[0:l,...] = data['v']
            WW[0:l,...] = data['ww']

        for i in xrange(1,numFiles):
            #load the current file
            ncid = netcdf.netcdf_file(files[ordered_time[i]],'r')
            time_temp = ncid.variables['time'].data
            ua_temp = ncid.variables['ua'].data
            va_temp = ncid.variables['va'].data
            zeta_temp = ncid.variables['zeta'].data
            time_temp = ncid.variables['time'].data
            ncid.close()
            singlename = os.path.basename(files[ordered_time[i]])
            data = loadnc(datadir, singlename=singlename, dim=dim)
            #how many time series could be added, at most
            ltt = len(time_temp)

            #see if there is any overlap between the two files
            start = bisect.bisect_left(Time, time_temp[0])
            #if there is overlap, then for the overlapping region, we
            #will want to choose the time series with the smallest nanFrac
            if start != timeDim:
                #we have a match, lets check for nans
                data1 = {}
                data1['ua'] = UA[start:,...]
                data1['va'] = VA[start:,...]
                if dim  == '3D':
                    data1['u'] = U[start:,...]
                    data1['v'] = V[start:,...]
                    data1['ww'] = WW[start:,...]
                #get the nan fracs
                nanind, nanFrac = nan_index(data,dim=dim)
                nanind, nanFrac1 = nan_index(data1, dim=dim)
                if nanFrac < nanFrac1:
                    #the data already in the arrays has the lower nanfrac
                    diff = nt - start
                    numT = nt + ltt - diff
                    UA[nt:numT,...] = ua_temp[diff:,...]
                    VA[nt:numT,...] = va_temp[diff:,...]
                    ZETA[nt:numT,...] = zeta_temp[diff:,...]
                    if dim == '3D':
                        U[nt:numT,...] = u_temp[diff:,...]
                        V[nt:numT,...] = v_temp[diff:,...]
                        WW[nt:numT,...] = ww_temp[diff:,...]
                    nt = numT
                else:
                    #the overlapping data has fewer nans
                    nt = start
                    numT = start + ltt
                    UA[nt:numT,...] = ua_temp
                    VA[nt:numT,...] = va_temp
                    ZETA[nt:numT,...] = zeta_temp
                    if dim == '3D':
                        U[nt:numT,...] = u_temp
                        V[nt:numT,...] = v_temp
                        WW[nt:numT,...] = ww_temp
                    nt = numT
            else:
                numT = ltt + nt
                Time[nt:numT] = time_temp
                UA[nt:numT,:] = ua_temp
                VA[nt:numT,:] = va_temp
                ZETA[nt:numT,:] = zeta_temp
                if dim == '3D':
                    U[nt:numT,...] = u_temp
                    V[nt:numT,...] = v_temp
                    WW[nt:numT,...] = ww_temp
                nt += ltt
        print("Loaded file " + str(i+1) + " of " + str(numFiles) + ".")
    #delete  any extra space at the end of the arrays.
    try:
        toDelete =tuple(np.arange(nt, len(Time)))
        Time = np.delete(Time, toDelete)
        UA = np.delete(UA,  toDelete, 0)
        VA = np.delete(VA, toDelete, 0)
        ZETA = np.delete(ZETA, toDelete, 0)
        if  dim == '3D':
            U = np.delete(U, toDelete, 0)
            V = np.delete(V, toDelete, 0)
            WW = np.delete(WW, toDelete, 0)
    except:
        pass
    data['time'] = Time
    data['ua'] = UA
    data['va'] = VA
    data['zeta'] = ZETA
    if dim == '3D':
        data['u'] = U
        data['v'] = V
        data['ww'] = WW
    if clean_nans:
        nanInd,  nanFrac = nan_index(data, dim=dim)
        nan_ind = tuple(nanInd)
        UA = np.delete(UA, nan_ind, 0)
        VA = np.delete(VA, nan_ind, 0)
        Time = np.delete(Time, nan_ind)
        if dim == '3D':
            U = np.delete(U, nan_ind, 0)
            V = np.delete(V, nan_ind, 0)
            WW = np.delete(WW, nan_ind, 0)
        data['time'] = Time
        data['ua'] = UA
        data['va'] = VA
        data['zeta'] = ZETA
        if dim == '3D':
            data['u'] = U
            data['v'] = V
            data['ww'] = WW
    return data


def npydic2mat(path, filename):
    """
    Takes an npy file that holds a dictionary and saves it as a mat file in the same location.
    """
    
    print('Loading npy file')
    indata=np.load(path+filename)
    indata=indata[()]    
    print('Saving Mat-File')
    sio.savemat(path+filename[:-3]+'mat',mdict=indata)
    print('Mat-File saved')


def loadCUR(filename):
    """
    Loads an IOS CUR file. (Different from a cur file).
    """
    
    with open(filename) as fp:
        FILEHEADER={}
        CUR={}
        dataheader=r''
        first=True
        num=0
        for line in fp:
            if (line[0]=='*') :
                if first:
                    first=False
                    tdict=collections.OrderedDict()
                else:
                    FILEHEADER[heading]=tdict   
                    tdict=collections.OrderedDict()
              
                
                if ('END OF HEADER' in line[1:]): 
                    FILEHEADER[heading]=tdict   
                    heading='data'  
                    tdict=collections.OrderedDict()     
                    #print line        
                    break              
                
                heading=line[1:].strip()
                tdict['title']=line[1:].strip()

                    
                
            if ( (line[0:4]=='    ') and (line[4]!='$') ):
                sidx=line.find(':')
                tname=line[4:sidx].strip()
                
                eidx=line.find('!')
                tdata=line[(sidx+1):eidx].strip()

                tdict[tname]=tdata
                    
            if ( (line[0:4]=='    ') and (line[4]=='$') ):
                tname=line[5:].strip()
                table=r''
                
                line=fp.next() 
                num+=1
                while line[4:8] != '$END':                    
                    table+=line
                    line=fp.next()  
                    num+=1               
                
                tdict[tname]=table
                
            if line[0]=='!':
                dataheader+=line
                
            num+=1
                
     
                
        CUR['dataheader']=dataheader        
        data=np.genfromtxt(filename,skip_header=num+1)
        CUR['FILEHEADER']=FILEHEADER
        
        #data is all loaded other then comments.....
        #can add that later if needed
        
        #process data so its usable
        stimestr=FILEHEADER['FILE']['START TIME'][4:]+' '+FILEHEADER['FILE']['START TIME'][:4] 
        etimestr=FILEHEADER['FILE']['END TIME'][4:]+' '+FILEHEADER['FILE']['END TIME'][:4]         
        tspace=np.array([float(x) for x in FILEHEADER['FILE']['TIME INCREMENT'].split()])*np.array([1,1/24,1/(24*60),1/(24*60*60),1/(24*60*60*1000)])
        stime=dates.datestr2num(stimestr)
        etime=dates.datestr2num(etimestr)

        CUR['time']=np.arange(stime,etime+tspace.sum(),tspace.sum())
        
        lonstr=FILEHEADER['LOCATION']['LONGITUDE']
        if ('W' in lonstr):
            lonstr=lonstr.replace('W','')
            CUR['lon']=np.sum(np.array([float(x) for x in lonstr.split()])*np.array([-1,-1/60]))            
        latstr=FILEHEADER['LOCATION']['LATITUDE']
        if ('N' in latstr):
            latstr=latstr.replace('N','')
            CUR['lat']=np.sum(np.array([float(x) for x in latstr.split()])*np.array([1,1/60]))
            
        CUR['h']=float(FILEHEADER['INSTRUMENT']['DEPTH'])

        a=np.array([ x for x in FILEHEADER['FILE']['TABLE: CHANNELS'].split('\r\n')])        
        tstr=a[0].replace('!','').split()
        nameidx=tstr.index('Name')        
        names=np.array([])
        for row in a[2:]:
            if row!='':
                names=np.append(names,row.split()[nameidx])
        for i,name in enumerate(names):
            CUR[name]=data[:,i]
        
                
    return CUR
                
        
def loadkml(filename):
    """
    Loads a kml file.
    """

    try:
        import fastkml
    except ImportError:
        print('Install fastkml.')
        return
        
    doc=file(filename).read()
    k=fastkml.kml.KML()
    k.from_string(doc)
    f1=[f.features() for f in k.features()]
    pm=list(f1[0])
    
    return np.array(pm[0].geometry.coords)
    

def loadcur(filename,exact=False):
        
    files=glob.glob(filename)
    files.sort()

    returndic={} 

    for j,fname in enumerate(files):

        fp=open(fname,'r')

        numlines = len(fp.readlines())
        fp.seek(0)
        headerdone=False

        indata={}

        for i,line in enumerate(fp.readlines()):
            if '||' in line:
                if '!Observed' in line:
                    sline=line.split()            
                    indata['lon']=-1*(float(sline[3])+float(sline[4][:-1])/60)
                    indata['lat']=1*(float(sline[1])+float(sline[2][:-1])/60)
                elif 'Computed from spatial average bin' in line:
                    sline=line.split()  
                    indata['bin']=int(sline[5][:-1])
                    indata['range']=np.array([int(val) for val in sline[6][:-1].split('-')])
            else:
                if headerdone==False:
                    headerdone=True
                    arrstart=i
                    indata['time']=np.empty((numlines-i,))
                    indata['timestr']=np.empty((numlines-i,),dtype='S16')
                    indata['u']=np.empty((numlines-i,))
                    indata['v']=np.empty((numlines-i,))
                sline=line.split()
                if len(sline)==2:
                    indata['timestr'][i-arrstart]=sline[0]+' '+sline[1][:5]
                    indata['u'][i-arrstart]=np.nan
                    indata['v'][i-arrstart]=np.nan
                elif len(sline)==4:
                    indata['timestr'][i-arrstart]=sline[0]+' '+sline[1]
                    indata['u'][i-arrstart]=float(sline[2])
                    indata['v'][i-arrstart]=float(sline[3])
                else:
                    print('Unhandled Case')
        fp.close()        
        
        returndic[j+1]=indata
        returndic[j+1]['time']=dates.datestr2num(returndic[j+1]['timestr'])
        returndic[j+1]['filename']=fname
        
    return returndic


def loadslev(filename):
    
    with open(filename) as fp:
        numlines = len(fp.readlines())
        fp.seek(0)
        cnt=0
        
        rd={}
        rd['timestr']=np.empty((numlines-8,),dtype='S16')
        rd['zeta']=np.zeros((numlines-8,))              
        
        for i,line in enumerate(fp.readlines()):
            line=line.replace('\r','').replace('\n','') 
            if '' == line:
                continue
            if i<8:                               
                if 'Station_Name' in line:
                    rd['Station_Name']=line[13:]
                if 'Station_Number' in line:
                    rd['Station_Number']=line[15:]
                if 'Latitude_Decimal_Degrees' in line:
                    rd['lat']=float(line[25:])           
                if 'Longitude_Decimal_Degrees' in line:
                    rd['lon']=-1*float(line[26:])    
                if 'Datum' in line:
                    rd['datum']=line[6:]
                if 'Time_zone' in line:
                    rd['tz']=line[10:]
            else:
                lsplit=line.split(',')
                rd['timestr'][cnt]=lsplit[0]
                rd['zeta'][cnt]=lsplit[1]
                cnt+=1
          
        #remove empty values due to extra spaces in file  
        idx=np.argwhere(rd['timestr']=='')
        rd['timestr']=np.delete(rd['timestr'],idx)
        rd['zeta']=np.delete(rd['zeta'],idx)
        
        rd['time']=dates.datestr2num(rd['timestr'])
        
    return rd

def linReg(mod,obs, alpha=0.05):
        '''
        Does linear regression on the model data vs. recorded data.

        Gives a 100(1-alpha)% confidence interval for the slope
        '''

        obs_mean = np.mean(obs)
        mod_mean = np.mean(mod)
        n = mod.size
        df = n - 2

        # calculate square sums
        SSxx = np.sum(mod**2) - np.sum(mod)**2 / n
        SSyy = np.sum(obs**2) - np.sum(obs)**2 / n
        SSxy = np.sum(mod * obs) - np.sum(mod) * np.sum(obs) / n
        SSE = SSyy - SSxy**2 / SSxx
        MSE = SSE / df

        # estimate parameters
        slope = SSxy / SSxx
        intercept = obs_mean - slope * mod_mean
        sd_slope = np.sqrt(MSE / SSxx)
        r_squared = 1 - SSE / SSyy

        # calculate 100(1 - alpha)% CI for slope
        width = stats.t.isf(0.5 * alpha, df) * sd_slope
        lower_bound = slope - width
        upper_bound = slope + width
        slope_CI = (lower_bound, upper_bound)

        # calculate 100(1 - alpha)% CI for intercept
        lower_intercept = obs_mean - lower_bound * mod_mean
        upper_intercept = obs_mean - upper_bound * mod_mean
        intercept_CI = (lower_intercept, upper_intercept)

        # estimate 100(1 - alpha)% CI for predictands
        predictands = slope * mod + intercept
        sd_resid = np.std(obs - predictands)
        y_CI_width = stats.t.isf(0.5 * alpha, df) * sd_resid * \
            np.sqrt(1 - 1 / n)

        # return data in a dictionary
        data = {}
        data['slope'] = slope
        data['intercept'] = intercept
        data['r_2'] = r_squared
        data['slope_CI'] = slope_CI
        data['intercept_CI'] = intercept_CI
        data['pred_CI_width'] = y_CI_width
        data['conf_level'] = 100 * (1 - alpha)
        
        return data     
        
        
def save_poly_shp(data,varLabel,filename):
    epsg_in=4326
    
    lon = data['lon']
    lat = data['lat']
    trinodes = data['nv']
    var=data[varLabel]



    driver = ogr.GetDriverByName('ESRI Shapefile')
    shapeData = driver.CreateDataSource(filename)

    spatialRefi = osr.SpatialReference()
    spatialRefi.ImportFromEPSG(epsg_in)
    lyr = shapeData.CreateLayer("poly_layer", spatialRefi, ogr.wkbPolygon )

    #var is just a rdm string?
    lyr.CreateField(ogr.FieldDefn(varLabel, ogr.OFTReal))

    cnt = 0
    for row in trinodes:
        val1 = -999
        ring = ogr.Geometry(ogr.wkbLinearRing)
        for val in row:
            if val1 == -999:
                val1 = val
            ring.AddPoint(lon[val], lat[val])
        #Add 1st point to close ring
        ring.AddPoint(lon[val1], lat[val1])

        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)

        #Now add field values from array
        feat = ogr.Feature(lyr.GetLayerDefn())
        feat.SetGeometry(poly)
        feat.SetField(varLabel, float(var[cnt]))

        lyr.CreateFeature(feat)
        feat.Destroy()
        poly.Destroy()

        val1 = -999
        cnt += 1
        
    shapeData.Destroy()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

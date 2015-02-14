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
* Matplotlib version 1.3.0
* Numexpr

Optional, but recommended:

* Numba

.. Note:: A convenient package that is both easy to install and contains nearly all the required packages for the python code herein is Anaconda (available here http://www.continuum.io/downloads).  Note that if you choose to use  Anaconda, it is necessary to install matplotlib v1.3.0  manually, as Anaconda comes with an older version.


Functions
=========
"""
#load modules
#Numerical modules
import numpy as np
import matplotlib.tri as mplt
import bisect
import numexpr as ne
import h5py

#I/O modules
import glob
from scipy.io import netcdf
import scipy.io as sio
import mmap
import os



def loadnc(datadir, singlename=None):
    """Loads a .nc  data file

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
    if data.has_key('nv'):
        data['nv']=data['nv'].astype(int).T-1
    if data.has_key('nbe'):
        data['nbe']=data['nbe'].astype(int).T-1
    if ncid.dimensions.has_key('nele'):    
        data['nele'] = ncid.dimensions['nele']
    if ncid.dimensions.has_key('node'):
        data['node'] = ncid.dimensions['node']

   
    ncid.close()
    #Now we get the long/lat data.  Note that this method will search
    #for long/lat files in the datadir and up to two levels above
    #the datadir.
    if (data.has_key('lon') and data.has_key('x')):
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
                print "No long/lat files found. Long/lat set to x/y"
                data['lon'] = data['x']
                data['lat'] = data['y']
    else: 
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
            if (data.has_key('x') and data.has_key('y')):
                print "No long/lat files found. Long/lat set to x/y"
                data['lon'] = data['x']
                data['lat'] = data['y']
            
    if data.has_key('nv'):
        data['trigrid'] = mplt.Triangulation(data['lon'], data['lat'],data['nv'])   
        data['trigridxy'] = mplt.Triangulation(data['x'], data['y'],data['nv'])
  
        
    return data


def load_timeslice(datadir, start, end, singlename=None,  dim = '2D'):
    """Loads a timeslice of data from a .nc file for the time series between start
    and end, which are provided as indices.

    :Parameters:
        **datadir** -- the directory where the .nc file is located.  Be sure to
            end with a '/'.
        **start/end** -- the start and end index for time series to be loaded.
            Remember, python indexing starts at 0, not 1.
        **singlename** -- Optional.  Specify the name of the file to be loaded.
        **dim** -- Optional.  Either '2D' or '3D', the dimension of the data file.

    """

    if singlename == None:
        files = glob.glob(datadir + "*.nc")
        filepath = files[0]
    else:
        filepath = datadir + singlename

    #initalize data dictionary
    data = {}
    #store the filepath, in case it is needed in the future
    data['filepath'] = filepath
    #make it known the data was loaded using timeslice
    data['timeslice'] = True
    #list of things to be loaded
    toLoad = ['x', 'y', 'nv', 'nbe', 'h', 'a1u', 'a2u', 'siglev', 'siglay', 'time']
    dims = ['nele', 'node']
    asInt = ['nv', 'nbe']
    toTranspose = ['nv', 'nbe', 'a1u', 'a2u']

    toTimeCut = ['time', 'ua', 'va', 'zeta']

    if dim == '3D':
        three_d = ['aw0', 'awx', 'awy']
        for i in three_d:
            toLoad.append(i)
        three_trans = ['aw0', 'awx', 'awy']
        for i in three_trans:
            toTranspose.append(i)
        three_timecut = ['u', 'v', 'ww']
        for i in three_timecut:
            toTimeCut.append(i)

    #load data
    ncid = netcdf.netcdf_file(filepath, 'r')
    #load the general data that requires no time cuts
    for i in toLoad:
        try:
            if i in asInt:
                data[i] = np.transpose(ncid.variables[i].data.astype(int) - [1])
            elif i in toTranspose:
                data[i] = np.transpose(ncid.variables[i].data)
            else:
                data[i] = ncid.variables[i].data
        except:
            print i + ' is not an entry in the nc file'
    #load and timecut the data
    for i in toTimeCut:
        try:
            data[i] = ncid.variables[i].data[start:end,...]
        except:
            print 'there was an issue slicing ' + i
    #load the dimensions
    for i in dims:
        data[i] = ncid.dimensions[i]
    ncid.close()

    #Now we get the long/lat data.  Note that this method will search
    #for long/lat files in the datadir and up to two levels above
    #the datadir.

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
        print "No long/lat files found. Long/lat set to x/y"
        data['lon'] = data['x']
        data['lat'] = data['y']

    data['trigrid'] = mplt.Triangulation(data['lon'], data['lat'], \
        data['nv'])
    return data


def ncdatasort(data,trifinder=False):
    """From the nc data provided, common variables are produced.

    :Parameters: **data** -- a data dictionary of data from a .nc file

	|

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
    
    uvh= np.empty((len(nv[:,0]),1))   
    uvh[:,0] = (data['h'][nv[:,0]] + data['h'][nv[:,1]] + data['h'][nv[:,2]]) / 3.0

    data['uvh']=uvh
    data['uvnode'] = uvnode
    data['uvnodell'] = uvnodell
    data['nodell'] = nodell
    data['nodexy'] = nodexy

    if data.has_key('time'):
        data['time']=data['time']+678576

    if ~data.has_key('trigrid'):
        if (data.has_key('nv') and data.has_key('lat') and data.has_key('lon')):
            data['trigrid'] = mplt.Triangulation(data['lon'], data['lat'],data['nv'])  
    
    if ~data.has_key('trigridxy'):
        if (data.has_key('nv') and data.has_key('x') and data.has_key('y')):
            data['trigridxy'] = mplt.Triangulation(data['x'], data['y'],data['nv'])  

    if trifinder==True:
        data['trigrid_finder']=data['trigrid'].get_trifinder()
        data['trigridxy_finder']=data['trigridxy'].get_trifinder()

    return data

def node_finder(XY, neiDir, grdDir):
    """Given an array of long\lat points, find the nearest node
    to each, and return that node's index.  Reads long/lat from
    a .nei file
    """
    #read long/lat info from .nei file
    grid_info = np.genfromtxt(neiDir, skip_header=3)
    #read element data from grd.dat file
    lon_lat = grid_info[:,1:3]

    with open(grdDir) as f:
        m = mmap.mmap(f.fileno(),0,prot=mmap.PROT_READ)

    done = False
    while not done:
        line = m.readline()
        if "Cell" in line:
            numEle = int(line.split()[-1])
            done = True

    nv_tmp = np.empty((numEle, 5))
    for i in xrange(numEle):
        nv_tmp[i,:] = m.readline().split()

    nv = nv_tmp[:,1:4].astype(int)
    trigrid = mplt.Triangulation(lon_lat[:,0], lon_lat[:,1], nv - 1)
    trifinder = mplt.TrapezoidMapTriFinder(trigrid)

    elements = []
    for i in xrange(XY.shape[0]):
        elements.append(trifinder.__call__(XY[i,0], XY[i,1]).item())

    #find the indices that surround each element
    index = []
    for i in elements:
        index.append(list(nv[i,:]))

    #create the difference array, for each XY
    return elements, index


def tri_finder(XY, data, nodes=False):
    """Determines which element a given X, Y value is in.

    :Parameters: **XY** -- an N x 2 dimensional array of points to locate in triangles. The first column consists of the x coordinate (long), while the second column consists of the y coordinate (lat).

	**data** -- dictionary containing all the data from the .nc file.

    :Returns: **indicies** -- a list of indices, in order, giving the 			triangle that each x,y pair of XY belongs to.

    .. Note:: if indices contains -1, this means that the cooresponding XY
        value did not belong to any of the elements.
    """

    #get the relevant variables
    trigrid = data['trigrid']
    trifinder = mplt.TrapezoidMapTriFinder(trigrid)
    indices = [] #indices of the triangle where the points are found.
    #find the polygon that X, Y is in.

    l = len(XY[:,0])

    for i in xrange(l):
        element = trifinder.__call__(XY[i,0],XY[i,1])
        indices.append(element.item())

    #test for correctness
    badInds = np.where(indices == -1)[0]
    if len(badInds) > 0:
        print "No triangle found for some of the points given.  Please \
            ensure that the following entries in XY are correct: "
        print badInds

    if nodes:
        #find the nodes that surround an element
        nodes = []
        for i in indices:
            nodes.append(list(data['nv'][i,:]))
        return indices, nodes
    return indices

def closest_node(data, location):
    """Given a long\lat point, find the nearest node
    to each, and return that node's index.  
    """

	#argsort array to return index that would sort locations
    idx=np.argsort((data['nodell'][:,0]-location[0])**2+(data['nodell'][:,1]-location[1])**2)
    
    return idx[0]


def closest_element(data, location):
    """Given a long\lat point, find the nearest element
    to each, and return that elements's index.  
    """

	#argsort array to return index that would sort locations
    idx=np.argsort((data['uvnodell'][:,0]-location[0])**2+(data['uvnodell'][:,1]-location[1])**2)
    
    return idx[0]

def interp_vel_old(XY, triInds, data, numjit=False):
    """Interpolates velocity data from the known locations to the xa, y
    coordinates given in the array XY.

    :Parameters:
        **XY** -- Nx2 array of x, y values (in long/lat) where the velocity should be interpolated to.

        **TriInds** -- indices of the triangles that each XY point belongs to.  This is returned by tri_finder.

        **data** -- Typical data dictionary returned by loadnc or ncdatasort.

        **jit = {True, False} (optional)** -- Optional just in time compilation of code.  This is very worthwhile for larger datasets as the compiled code runs much faster.  Requires Numba.

    .. Note:: Since this contains a (potentially large) for loop, the first
        call of the code will be slow.  For faster interpolation
        (10-100 times faster) install Numba and make use of the jit (just in
        time) compilation feature.
    """
    if numjit:
        #this assumes numba is installed on the users computer.
        #we must first cast the data in float form to ensure it will work.
        #This method is incredibly fast compared to the numba-free method,
        #so it is highly recommended for interpolating large numbers of points.
        from numba import autojit
        u = np.transpose(data['ua']).astype(float)
        v = np.transpose(data['va']).astype(float)
        uvnodell = data['uvnodell']
        a1u = data['a1u'].astype(float)
        a2u = data['a2u'].astype(float)
        nbe = data['nbe']
        nv = data['nv']

        inds = np.array(triInds)
        numba_interp = autojit()(jit_interp_vel)
        UI, VI = numba_interp(XY, inds, u, v, uvnodell, a1u, a2u, nbe, nv)
    else:
        #name the required data pieces
        u = np.transpose(data['ua'])
        v = np.transpose(data['va'])
        uvnodell = data['uvnodell']
        a1u = data['a1u']
        a2u = data['a2u']
        nbe = data['nbe']
        nv = data['nv']

        i = 0
        lnv = len(nv[:,0])
        UI = np.empty((len(XY[:,0]), len(u[0,:])))
        VI = np.empty(UI.shape)
        for j in triInds:
            if j != 0 and j != -1:
                e = nbe[j,:]
                e[e == 0] = lnv - 1
                xy0c = XY[i,:] - uvnodell[j,:]

                #Now we calculate derivatives.  Note that we attempt to do this
                #in a vectorized fashion, as much as possible, while
                #avoiding the large matrix products that occur in
                #totally vectorized code
                u_tmp = np.vstack((u[j,:], u[e,:]))
                v_tmp = np.vstack((v[j,:], v[e,:]))

                a1 = a1u[j,:]
                a2 = a2u[j,:]

                dudx = np.dot(a1, u_tmp)
                dudy = np.dot(a2, u_tmp)

                dvdx = np.dot(a1, v_tmp)
                dvdy = np.dot(a1, v_tmp)

                UI[i,:] = u[j,:] + xy0c[0] * dudx + xy0c[1] * dudy
                VI[i,:] = v[j,:] + xy0c[1] * dvdx + xy0c[1] * dvdy


            else:
                UI[i,:] = np.nan
                VI[i,:] = np.nan
            i += 1
    return UI, VI

def jit_interp_vel(XY, triInds, u, v, uvnodell, a1u, a2u, nbe, nv):
    """
    .. warning:: This function is not meant to be called by the user. Use "interp_vel".
    """
    i = 0
    lnv = len(nv[:,0])
    UI = np.empty((len(XY[:,0]), len(u[0,:])))
    VI = np.empty(UI.shape)
    for j in triInds:
        if j != 0 and j != -1:
            e = nbe[j,:]
            e[e == 0] = lnv - 1
            xy0c = XY[i,:] - uvnodell[j,:]

            #Now we calculate derivatives.  Note that we attempt to do this
            #in a vectorized fashion, as much as possible, while
            #avoiding the large matrix products that occur in
            #totally vectorized code
            u_tmp = np.vstack((u[j,:], u[e,:]))
            v_tmp = np.vstack((v[j,:], v[e,:]))

            a1 = a1u[j,:]
            a2 = a2u[j,:]

            dudx = np.array([np.dot(a1, u_tmp)])
            dudy = np.array([np.dot(a2, u_tmp)])

            dvdx = np.array([np.dot(a1, v_tmp)])
            dvdy = np.array([np.dot(a1, v_tmp)])

            UI[i,:] = u[j,:] + xy0c[0] * dudx + xy0c[1] * dudy
            VI[i,:] = v[j,:] + xy0c[1] * dvdx + xy0c[1] * dvdy


        else:
            UI[i,:] = np.nan
            VI[i,:] = np.nan
            i += 1
    return UI, VI


def get_elements(data, region):
    """Takes uvnodes and a  region (specified by the corners of a
    rectangle) and determines the elements of uvnode that lie within the
    region
    """
    elements = np.where((data['uvnodell'][:,0] >= region['region'][0]) & (data['uvnodell'][:,0] <= region['region'][1]) & (data['uvnodell'][:,1] >= region['region'][2]) & (data['uvnodell'][:,1] <= region['region'][3]))[0]

    return elements

def get_elements_xy(data, region):
    """Takes uvnodes and a  region (specified by the corners of a
    rectangle) and determines the elements of uvnode that lie within the
    region
    """
    elements = np.where((data['uvnode'][:,0] >= region['region'][0]) & (data['uvnode'][:,0] <= region['region'][1]) & (data['uvnode'][:,1] >= region['region'][2]) & (data['uvnode'][:,1] <= region['region'][3]))[0]

    return elements

def get_nodes(data, region):
    """Takes nodexy and a region (specified by the corners of a rectangle)
    and determines the nodes that lie in the region
    """
   
    nodes = np.where((data['nodell'][:,0] >= region['region'][0]) & (data['nodell'][:,0] <= region['region'][1]) & (data['nodell'][:,1] >= region['region'][2]) & (data['nodell'][:,1] <= region['region'][3]))[0]
    return nodes

def get_nodes_xy(data, region):
    """Takes nodexy and a region (specified by the corners of a rectangle)
    and determines the nodes that lie in the region
    """
   
    nodes = np.where((data['nodexy'][:,0] >= region['region'][0]) & (data['nodexy'][:,0] <= region['region'][1]) & (data['nodexy'][:,1] >= region['region'][2]) & (data['nodexy'][:,1] <= region['region'][3]))[0]
    return nodes

def regioner_old(region, data, name=None, savedir=None, dim='2D'):
    """
    Takes as input a region (given by a four elemenTakes as input a region
    (given by a four element NumPy array),
    and some standard data output by ncdatasort and loadnc2d_python
    and returns only the data that lies within the region specified
    in the region arrayt NumPy array),
    and some standard data output by ncdatasort and loadnc2d_python
    and returns only the data that lies within the region specified
    in the region array

    :Parameters:
        **region** -- four element array containing the four corners of the
            region box.  Entires should be in the following form:
            [long1, long2, lat1, lat2] with the following property:
            abs(long1) < abs(long2), etc.

        **data** -- standard python data dictionary for these files

        **name** -- what should  the region be called in the output file?

        **savedir** -- where should the resultant data be saved? Default is 			none, i.e. the data will not be saved, only returned.

        **dim = {'2D', '3D'}** the dimension of the data to use regioner 				on.  Default is 2D.
    """
    #short name for relevant variables

    nv = data['nv']
    nbe = data['nbe']
    a1u = data['a1u']
    a2u = data['a2u']


    l = nv.shape[0]
    if savedir == None:
        regionData = "/not/a/real/path"
    else:
        regionData = savedir + name + "_region_" + str(region[0]) \
    		+ "_" + str(region[1]) + "_" + str(region[2]) + "_" + str(region[3]) + ".mat"
    files = glob.glob(regionData)

    #find the nodes that lie in the region
    idx = get_nodes(data, region)
    if len(files)==0:
        #There is currently no file with this particular region data
        #build a new data set for this region

        #first, reindex elements in the region
        element_index_tmp = np.zeros(l, int)
        nv_rs = nv.reshape(l*3, order='F')
        #find indices that sort nv_rs
        nv_sortedind = nv_rs.argsort()
        #sort the array
        nv_sortd = nv_rs[nv_sortedind]
        #pick out the values in the region
        for i in xrange(len(idx)):
            i1 = bisect.bisect_left(nv_sortd, idx[i])
            i2 = bisect.bisect_right(nv_sortd, idx[i])
            inds = nv_sortedind[i1:i2]
            element_index_tmp[inds % l] = 1
        element_index = np.where(element_index_tmp == 1)[0]
        node_index = np.unique(nv[element_index,:])
        #create new linkage arrays
        nv_tmp = nv[element_index,:]
        L = len(nv_tmp[:,0])
        nv_tmp2 = np.empty((1, L*3.0))

        #make a new array of the node labellings for the tri's in the region

        nv2 = nv_tmp.reshape(L * 3, order='F')
        nv2_sortedind = nv2.argsort()
        nv2_sortd = nv2[nv2_sortedind]

        for i in xrange(len(node_index)):
            i1 = bisect.bisect_left(nv2_sortd, node_index[i])
            i2 = bisect.bisect_right(nv2_sortd, node_index[i])
            inds = nv2_sortedind[i1:i2]
            nv_tmp2[0, inds] = i

        nv_new = np.reshape(nv_tmp2, (L, 3), 'F')
        #now do the same for nbe
        nbe_index = np.unique(nbe[element_index, :])
        nbe_tmp = nbe[element_index,:]
        lnbe = len(nbe_tmp[:,0])
        nbe_tmp2 = np.empty((1, lnbe*3))

        nbe2 = nbe_tmp.reshape(lnbe*3, order='F')
        nbe_sortedind = nbe2.argsort()
        nbe_sortd = nbe2[nbe_sortedind]

        for i in xrange(len(nbe_index)):
            i1 = bisect.bisect_left(nbe_sortd, nbe_index[i])
            i2 = bisect.bisect_right(nbe_sortd, nbe_index[i])
            inds = nbe_sortedind[i1:i2]
            nbe_tmp2[0, inds] = i

        nbe_new = np.reshape(nbe_tmp2, (lnbe,3), 'F')
        nbe_new[nbe_new > len(nv_new[:,0]), :] = 0

        #create new variables for the region
        data['node_index'] = node_index
        data['element_index'] = element_index
        data['nbe'] = nbe_new
        data['nv'] = nv_new
        try:
            #if the data was loaded using load_timeslice,
            #we do not wish to alter it.
            data['timeslice']

            data['a1u'] = a1u[element_index, :]
            print 'a1u'
            data['a2u'] = a2u[element_index, :]
            print 'a2u'
            data['h'] = data['h'][node_index]
            print 'h'
            data['uvnodell'] = data['uvnodell'][element_index,:]
            data['x'] = data['x'][node_index]
            print 'x'
            data['y'] = data['y'][node_index]
            print 'y'
            data['zeta'] = data['zeta'][:,node_index]
            print 'zeta'
            data['ua'] = data['ua'][:,element_index]
            print 'ua'
            data['va'] = data['va'][:,element_index]
            print 'va'
            data['lon'] = data['lon'][node_index]
            print 'lon'
            data['lat'] = data['lat'][node_index]
            print 'lat'
            if dim=='3D':
                data['u'] = data['u'][:,:,element_index]
                print 'u'
                data['v'] = data['v'][:,:,element_index]
                print 'v'
                data['ww'] = data['ww'][:,:,element_index]
                print 'ww'
        except:
            data = _cut_data(data, node_index, element_index, dim)
        data['trigrid'] = mplt.Triangulation(data['lon'], data['lat'], \
            data['nv'])

        #save the data if that was requested.
        if savedir != None and name != None:
            mat_save(data, regionData)
    return data
def _cut_data(data, node_index, element_index, dim):
    """Routine used by regioner.  Cuts the data for the elements specified by
    node_index and element_index."""

    filepath = data['filepath']
    #things cut at elements with the first index
    eleCutForward = ['a1u', 'a2u']
    #things cut at elements with the last index
    eleCutBack = ['ua', 'va']
    if dim == '3D':
        alsoCutB = ['u', 'v', 'ww']
        alsoCutF = ['aw0', 'awx', 'awy']
        for i in alsoCutB:
            eleCutBack.append(i)
        for i in alsoCutF:
            eleCutForward.append(i)

    nodeCut = ['zeta', 'lon', 'lat', 'h', 'x', 'y']
    #load nc file
    ncid = netcdf.netcdf_file(filepath, 'r')
    #cut element-based data
    print 'cuting element data, forward'
    for i in eleCutForward:
       data[i] = np.transpose(ncid.variables[i].data)[element_index,...]
       print i
    print 'cutting element data, back'
    for i in eleCutBack:
        data[i] = ncid.variables[i].data[...,element_index]
        print i
    #cut node-based data
    print 'cutting node data'
    for i in nodeCut:
        data[i] = ncid.variables[i].data[..., node_index]
        print i

    return data
def mat_save(data, saveDirName, dim='2D'):
    """
    Save .nc data to a mat file.

    :Parameters:
        **data** -- the standard data dictionary

        **saveDirName** -- the path to where the data should be saved,
        along with the name. Ex: "/home/user/Desktop/data.mat"

        **dim ={'2D', '3D'} (optional)** -- the dimension of the data file.

    """
    dtype = float
    rdata={}
    if dim=='3D':
        rdata['a1u'] = data['a1u'].astype(dtype)
        rdata['a2u'] = data['a2u'].astype(dtype)
        rdata['h'] = data['h'].astype(dtype)
        rdata['uvnodell'] = data['uvnodell']
        rdata['x'] = data['x'].astype(dtype)
        rdata['y'] = data['y'].astype(dtype)
        rdata['u'] = data['u'].astype(dtype)
        rdata['v'] = data['v'].astype(dtype)
        rdata['ww'] = data['ww'].astype(dtype)
        rdata['zeta'] = data['zeta'].astype(dtype)
        rdata['h'] = data['h'].astype(dtype)
        rdata['ua'] = data['ua'].astype(dtype)
        rdata['va'] = data['va'].astype(dtype)

    elif dim=='2D':
        rdata['a1u'] = data['a1u'].astype(dtype)
        rdata['a2u'] = data['a2u'].astype(dtype)
        rdata['h'] = data['h'].astype(dtype)
        rdata['uvnodell'] = data['uvnodell']
        rdata['x'] = data['x'].astype(dtype)
        rdata['y'] = data['y'].astype(dtype)
        rdata['zeta'] = data['zeta'].astype(dtype)
        rdata['ua'] = data['ua'].astype(dtype)
        rdata['va'] = data['va'].astype(dtype)
    else:
        raise Exception("Dim must be '2D', '3D', or absent.")
    sio.savemat(saveDirName, rdata, oned_as='column')

def h5_save(data, savedir, filename, cast=False):
	"""Save data into an htf5 format.  This is faster than saving to
	.mat files.  Note this this code assumes that the data is already cast,
	unless it explicitly told to cast  the data by setting cast=True.

	:Parameters:
		**data** -- Standard python data dictionary with data to be saved.

		**savedir** -- The directory where the resultant hft5 file should be 				saved.  Include a '/' at the end, like this: /path/to/save/

		**filename** -- The name for the file.

		**cast = {True, False}** -- Optional. If True the data will be cast 		to float form before saving.  This is necessary if the data has not 		yet been cast.
	"""
	#a list of data entries that will need to be casted.
	toCast = ['x', 'y', 'lon', 'lat', 'h', 'a1u', 'a2u']
	#a list of data entries that would not need to be cast to floats
	noCast = ['nv', 'nbe']
	#make sure there are not any 'unsavable' structures in the dictionary
	key = data.keys()
	#initialize list of items not to be saved.
	noWrite = []
	for i in key:
		try:
			data[i].shape
		except:
			noWrite.append(i)
	#cast the data to float form.
	if cast:
		for i in toCast:
			data[i] = data[i].astype('float32')
	#get the dictionary that will be saved ready.
	sdict = {i:data[i] for i in key if i not in noWrite}
	#initalize a dictionary of random variables.  This serves
	#only to make it possible to do the following in a condensed form
	rdata = {}
	for i in sdict.keys():
		rdata[i] = 4

	#save to h5 file.
	f = h5py.File(savedir + filename + '.h5py', 'w')
	for i in sdict.keys():
		if i not in noCast:
			rdata[i] = f.create_dataset(i, sdict[i].shape, 'f')
			rdata[i][...] = sdict[i]
		else:
			rdata[i] = f.create_dataset(i, sdict[i].shape, 'i')
			rdata[i][...] = sdict[i]
	f.close()
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


def merge_nc(datadir, savedir, clean_nans = False, intelligent=False, \
dim='2D'):
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
                    #there was no matching index, i.e. the data does not 						overlap
                    numT = ltt + nt
                    Time[nt:numT] = time_temp
                    UA[nt:numT,:] = ua_temp
                    VA[nt:numT,:] = va_temp
                    ZETA[nt:numT,:] = zeta_temp
                    nt += ltt
                print "Loaded file " + str(i+1) + " of " + str(numFiles) + "."
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
                    #there was no matching index, i.e. the data does not 						overlap
                    numT = ltt + nt
                    Time[nt:numT] = time_temp
                    UA[nt:numT,:] = ua_temp
                    VA[nt:numT,:] = va_temp
                    ZETA[nt:numT,:] = zeta_temp
                    U[nt:numT,...] = u_temp
                    V[nt:numT,...] = v_temp
                    WW[nt:numT,...] = ww_temp
                    nt += ltt
            print "Loaded file " + str(i+1) + " of " + str(numFiles) + "."
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
        print "Loaded file " + str(i+1) + " of " + str(numFiles) + "."
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





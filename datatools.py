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
from __future__ import division,print_function
import collections
import matplotlib.dates as dates

#Numerical modules
import numpy as np
import matplotlib.tri as mplt
import bisect
import numexpr as ne
import scipy.stats as stats

#I/O modules
import glob
from scipy.io import netcdf
import scipy.io as sio
import mmap
import os
#from osgeo import ogr
#from osgeo import osr
import netCDF4 as n4

from projtools import lcc


def loadnc(datadir, singlename=[], fvcom=True, suppress=False):
    """
    Loads a .nc  data file

    :Parameters:
        **datadir** -- The path to the ncfile.
        **filename** -- The nc filename.
        
        **fvcom** -- True/False - is the ncfile an fvcom file. 
    """
    if singlename==[]:
        singlename = glob.glob('*.nc')[0]

    # Initialize a dictionary for the data.
    data = {}
    #does the datadir end in / if not append it
    if (len(datadir)>0) and (not datadir.endswith('/')):
        datadir = datadir + '/'
    # Store the filepath and data dir in case it is needed in the future
    data['datadir'] = datadir
    data['filepath'] = datadir + singlename
    
    try:
        # Load data with scipy netcdf
        ncid = netcdf.netcdf_file(data['filepath'], 'r', mmap=True)

        for key in ncid.variables.keys():
            data[key] = ncid.variables[key].data   
        
        data['dims'] = {}
        for key in ncid.dimensions.keys():
            data['dims'][key] = ncid.dimensions[key]
            
        if hasattr(ncid,'CoordinateProjection'):
            data['projstr']=ncid.CoordinateProjection.decode()
    except TypeError:
        if not suppress:
            print('File is netcdf4 type')
        ncid = n4.Dataset(data['filepath'])
        data = ncid.variables      
            

    if fvcom:
        if 'nv' in data:
            data['nv'] = data['nv'].astype(int).T-1
        if 'nbe' in data:
            data['nbe'] = data['nbe'].astype(int).T-1
        data = ncdatasort(data)  
        
    return data


def ncdatasort(data,trifinder=False,uvhset=True):
    """
    From the nc data provided, common variables are produced.

    :Parameters: **data** -- a data dictionary of data from a .nc file

    :Returns: **data** -- Python data dictionary updated to include uvnode and uvnodell
    """
    lond=False
    latd=False
    try:
        #load lon/lat from files and use it
        if glob.glob(data['datadir'] + "../input/*_lon.dat"):        
            data['lon'] = np.loadtxt(glob.glob(data['datadir'] + "../input/*_lon.dat")[0])
            lond=True
        if glob.glob(data['datadir'] + "../input/*_long.dat"):        
            data['lon'] = np.loadtxt(glob.glob(data['datadir'] + "../input/*_long.dat")[0])
            lond=True
        if glob.glob(data['datadir'] + "../input/*_lat.dat"):
            data['lat'] = np.loadtxt(glob.glob(data['datadir'] + "../input/*_lat.dat")[0])
            latd=True
    except:
        pass

    lonx=False
    if 'lon' not in data:
        print("No lon found. Lon set to x")
        data['lon'] = data['x']
        lonx=True
    latx=False
    if 'lat' not in data:
        print("No lat found. Lat set to y")
        data['lat'] = data['y']
        latx=True

    
    if ('lonc' not in data) or lond or lonx:    
        data['lonc'] = data['lon'][data['nv']].mean(axis=1)
    if ('latc' not in data) or latd or latx:   
        data['latc'] = data['lat'][data['nv']].mean(axis=1)

    data['nodell'] = np.vstack([data['lon'],data['lat']]).T
    data['uvnodell'] = np.vstack([data['lonc'],data['latc']]).T


    data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
        
    data['nodexy'] = np.vstack([data['x'],data['y']]).T
    data['uvnodexy'] = data['nodexy'][data['nv'],:].mean(axis=1)
    data['xc'] = data['uvnodexy'][:,0]
    data['yc'] = data['uvnodexy'][:,1]
    
    try:
        if 'nele' in data['dims']:    
            data['nele'] = data['dims']['nele']
        if 'node' in data['dims']:
            data['node'] = data['dims']['node']
    except KeyError:
        pass

    if 'Times' in data:
        data['Time']=np.empty((len(data['Times']),),dtype='|S26')
        for i in range(len(data['Times'])):
                data['Time'][i]=''.join(data['Times'][i,].astype(str))
        data['time']=dates.datestr2num(data['Time'])    
        
    if 'trigrid' not in data:
        if (('nv' in data) and('lon' in data) and ('lat' in data)):
            data['trigrid'] = mplt.Triangulation(data['lon'], data['lat'],data['nv'])      
    if 'trigridxy' not in data:
        if (('nv' in data) and('x' in data) and ('y' in data)):
            data['trigridxy'] = mplt.Triangulation(data['x'], data['y'],data['nv'])  

    if uvhset:
        data['uvh']=data['h'][data['nv']].mean(axis=1)

    if trifinder:
        data['trigrid_finder'] = data['trigrid'].get_trifinder()
        data['trigridxy_finder'] = data['trigridxy'].get_trifinder()

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
    
    
def load_wlev(filename):
    
    with open(filename) as fp:
        wlev={}
        wlev['tidecon']=np.empty((0,3))
        wlev['name']=np.array([])        

        days=False     
    
        for i,line in enumerate(fp.readlines()):
            line=line.replace('\r','').replace('\n','')#.replace('\t',' ')
            sline = line.split()

            if '||' not in line:
                wlev['name']=np.append(wlev['name'],sline[0])
                wlev['tidecon']=np.vstack([wlev['tidecon'],np.hstack([float(sline[1]),float(sline[2]),float(sline[3])])])
            if days:
                wlev['days']=int(sline[1][:-4])
                days=False
            if 'Computed' in line:
                s=0
                if 'N' in sline[2] or 'n' in sline[2]:
                    s=-1
                wlev['lat']=float(sline[1])+float(sline[2].replace('N','').replace('n',''))/60.0
                wlev['lon']=-1*(float(sline[4+s])+float(sline[5+s].replace('W','').replace('w',''))/60.0)
                wlev['offset']=float(sline[7+2*s])
                days=True
            if 'WaterLevConstit' in line:
                a=1
                if '00000m' in line:
                    a=0
                wlev['snum']=sline[1]
                wlev['sname']='_'.join(sline[2:(-2+a)])
                wlev['date']=sline[-1][:-2]
            if 'Reference' in line:
                wlev['ref']=sline[1]
            
    fp.close()
    
    return wlev
    
def mdate2pydate(date):
    return date-366.0
    
def pydate2mdate(date):
    return date+366.0
    

def load_ctd_obs(filename):
    tmp=np.genfromtxt(filename,dtype=str)
    
    if np.atleast_2d(tmp).shape[0]>1:
    
        out={}
        out[tmp[0,0]]=tmp[1,0].astype(int)
        out[tmp[0,1]]=tmp[1,1]
        out['time']=dates.datestr2num(tmp[1,1])
        out[tmp[0,2]]=tmp[1,2].astype(float)
        out[tmp[0,3]]=tmp[1,3].astype(float)
        out[tmp[0,4]]=tmp[1:,4].astype(float)
        out[tmp[0,5]]=tmp[1:,5].astype(float)
        out[tmp[0,6]]=tmp[1:,6].astype(float)
        out[tmp[0,7]]=tmp[1:,7].astype(float)
    
        return out
    else:
        out=True
        print('No data in {}'.format(filename))
        return out
    
    
def load_ctd_mod(filename):
    tmp=np.genfromtxt(filename,dtype=str)
    
    out={}
    out[tmp[0,0]]=tmp[1,0].astype(int)
    out[tmp[0,1]]=tmp[1:,1].astype(int)    
    out[tmp[0,2]]=tmp[1,2].astype(float)
    out[tmp[0,3]]=tmp[1,3].astype(float)    
    out["{}{}".format(tmp[0,4],tmp[0,5])]=np.array(["{} {}".format(d,t) for d,t in zip(tmp[1:,4],tmp[1:,5])])
    out['time']=dates.datestr2num(out["{}{}".format(tmp[0,4],tmp[0,5])])
    out[tmp[0,6]]=tmp[1:,6].astype(float)
    out[tmp[0,7]]=tmp[1:,7].astype(float)
    out[tmp[0,8]]=tmp[1:,8].astype(float)
    
    uit=np.unique(out['it'])
    
    for i,it in enumerate(uit):
        if i==0:
            idx=np.argwhere(out['it']==it)
        else:
            idx=np.hstack([idx,np.argwhere(out['it']==it)])
    aout={}
    for key in out:
        if idx.shape[0]*idx.shape[1] == np.atleast_2d(out[key]).shape[0]*np.atleast_2d(out[key]).shape[1]:
            aout[key]=out[key][idx]
            
    out['arrays']=aout
    
    return out
    
    
def load_ctd_zeta_mod(filename):
    tmp=np.genfromtxt(filename,dtype=str)
    
    out={}
    out[tmp[0,0]]=tmp[1,0].astype(int)
    out[tmp[0,1]]=tmp[1:,1].astype(int)    
    out[tmp[0,2]]=tmp[1,2].astype(float)
    out[tmp[0,3]]=tmp[1,3].astype(float)    
    out["{}{}".format(tmp[0,4],tmp[0,5])]=np.array(["{} {}".format(d,t) for d,t in zip(tmp[1:,4],tmp[1:,5])])
    out['time']=dates.datestr2num(out["{}{}".format(tmp[0,4],tmp[0,5])])
    out[tmp[0,6]]=tmp[1:,6].astype(float)
    
    return out
    
    
    
def ncfile_clone_regioner(data,oldfile,newfile):
    
    
    
    
    ncid = n4.Dataset(oldfile, 'r',format='NETCDF3_CLASSIC')
    g = n4.Dataset(newfile, 'w',format='NETCDF3_CLASSIC')
    
    
    for attname in ncid.ncattrs():
        setattr(g,attname,getattr(ncid,attname))
    
    for dimname,dim in ncid.dimensions.iteritems():
        if dimname=='node':
            g.createDimension(dimname,len(data['nidx_sub']))
        elif dimname=='nele':
            g.createDimension(dimname,len(data['eidx_sub']))
        elif dimname=='time':
            g.createDimension(dimname,None)
        else:
            g.createDimension(dimname,len(dim))
    
    
    for varname,ncvar in ncid.variables.iteritems():
        var = g.createVariable(varname,ncvar.dtype,ncvar.dimensions)
        #Proceed to copy the variable attributes
        for attname in ncvar.ncattrs():  
           setattr(var,attname,getattr(ncvar,attname))
           
        #Finally copy the variable data to the new created variable
        for varname in data:
            s=np.array(np.shape(data[varname]))
            nele=False
            node=False
            if data['nele'] in s:
                idx=np.argwhere(s==data['nele'])
                nele=True
                sub=data['eidx_sub']
            if data['node'] in s:
                idx=np.argwhere(s==data['node'])
                node=True
                sub=data['nidx_sub']
            print(varname,s,idx[0][0])
            
        if s==0 and (nele or node):
            g.variables[varname][:]=data[varname][sub,] 
        elif s==1 and (nele or node):
            g.variables[varname][:]=data[varname][:,sub]
        elif s==2 and (nele or node):
            g.variables[varname][:]=data[varname][:,:,sub] 
        else:
            var[:] = data['varname'][:]
    
    ncid.close()
    g.close()
    
        
        
    
    
    
    
    
    
    

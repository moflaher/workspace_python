from __future__ import division,print_function
import numpy as np
import matplotlib as mpl
import scipy as sp
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import time
from scipy.io import netcdf

import datatools as dt
import misctools as mt
import plottools as pt
import interptools as ipt
import projtools as pjt

np.set_printoptions(precision=16,suppress=True,threshold=np.nan)
import bisect
import collections
import copy

import pyproj as pyp
#from osgeo import ogr


"""
Front Matter
=============

Created in 2014

Author: Mitchell O'Flaherty-Sproul

A bunch of functions dealing with finite element grids.

           
"""

def load_neifile(neifilename=None):
    """
    Loads a .nei file and returns the data as a dictionary. 
    """
    
    if neifilename==None:
        print('loadnei requires a filename to load.')
        return
    try:
        fp=open(neifilename,'r')
    except IOError:
        print('Can not find ' + neifilename)
        return

    nnodes=int(fp.readline())
    maxnei=int(fp.readline())
    llminmax=np.array([float(x) for x in fp.readline().split()])
    t_data=np.loadtxt(neifilename,skiprows=3,dtype='float64')
    fp.close()

    neifile={}

    neifile['nnodes']=nnodes
    neifile['maxnei']=maxnei
    neifile['llminmax']=llminmax

    neifile['nodenumber']=t_data[:,0].astype(int)
    neifile['nodell']=t_data[:,1:3]
    neifile['bcode']=t_data[:,3].astype(int)
    neifile['h']=t_data[:,4]
    neifile['neighbours']=t_data[:,5:].astype(int)
    neifile['lon']=t_data[:,1]
    neifile['lat']=t_data[:,2]
    
    return neifile


def find_land_nodes(neifile=None):
    """
    Given an neifile dictionary from loadnei. 
    This fuction returns a list of nodes which are constructed from only boundary nodes. 
    """

    if neifile==None:
        print('find_land_nodes requires a neifile dictionary.')
        return
    #the numbers of the boundary nodes
    nn=neifile['nodenumber'][neifile['bcode']!=0]
    #take the neighbour list for the boundary nodes
    #for each node count the number of non-zero neighbours
    #where there are only two neighbours give the idx
    #and convert that to the true nodenumber
    nodes=nn[np.where(np.sum(neifile['neighbours'][neifile['bcode']!=0,:]!=0,axis=1)==2)[0]]  

    return nodes


def save_neifile(neifilename=None,neifile=None):
    """
    Loads a .nei file and returns the data as a dictionary.

 
    """
    
    if neifilename==None:
        print('savenei requires a filename to save.')
        return
    try:
        fp=open(neifilename,'w')
    except IOError:
        print('Can''t make ' + neifilename)
        return

    if neifile==None:
        print('No neifile dict given.')
        return



    fp.write('%d\n' % neifile['nnodes'])
    fp.write('%d\n' % neifile['maxnei'])
    fp.write('%f %f %f %f\n' % (neifile['llminmax'][0],neifile['llminmax'][1],neifile['llminmax'][2],neifile['llminmax'][3]))   
   

    for i in range(0,neifile['nnodes']):
        fp.write('%d %f %f %d %f %s\n' % (neifile['nodenumber'][i], neifile['nodell'][i,0], neifile['nodell'][i,1], neifile['bcode'][i] ,neifile['h'][i],np.array_str(neifile['neighbours'][i,].astype(int))[1:-1] ) )

    
    fp.close()


def max_element_side_ll(data=None,elenum=None):
    """
    Given data and an element number returns the length of the longest side in ll. 
    """
    if data==None:
        print('Need proper data structure')
        return
    if elenum==None:
        print('Need to specify an element')
        return
    
    a=data['nodell'][data['nv'][elenum,0],]
    b=data['nodell'][data['nv'][elenum,1],]
    c=data['nodell'][data['nv'][elenum,2],]

    return np.max(sp.spatial.distance.pdist(np.array([a,b,c])))


def save_cagefile(filename=None,nodes=None,drag=None,depth=None):
    """
    Saves a fvcom cage file. 
    """
    #Check for filename and open, catch expection if it can't create file.
    if filename==None:
        print('fvcom_savecage requires a filename to save.')
        return
    try:
        fp=open(filename,'w')
    except IOError:
        print('Can''t make ' + filename)
        return

    #Make sure all arrays were given
    if ((nodes==None) or (drag==None) or (depth==None)):
        print('Need to gives arrays of nodes,drag, and depth.')
        fp.close()
        return
    #Make sure they are all the same size
    if ((nodes.size!=drag.size) or (nodes.size!=depth.size)):
        print('Arrays are not the same size.')
        fp.close()
        return 
    #Make sure that the arrays are single columns or rank 1. If not then transpose them.
    #Check if the transposed arrays are the same as size, if not then they have more then one column/row so exit
    if (nodes.shape[0]<nodes.size):
        nodes=nodes.T
        drag=drag.T
        depth=depth.T
        if (nodes.shape[0]<nodes.size):  
            fp.close()
            return
     
  
    fp.write('%s %d\n' % ('CAGE Node Number = ',np.max(nodes.shape) ) )

    for i in range(0,len(nodes)):
        fp.write('%d %f %f\n' % (nodes[i],drag[i],depth[i]) )

    
    fp.close()


def equal_vectors(data,region,spacing):
    """
    Take an FVCOM data dictionary, a region dictionary and a spacing in meters.
    Returns: The element idx that best approximates the given spacing in the region. 
    """

    ll=np.array([region['region'][0],region['region'][2]])
    ur=np.array([region['region'][1],region['region'][3]])
    
    x,y,proj=pjt.lcc(data['lon'],data['lat'])
    
    llxy=ll
    urxy=ur
    
    llxy[0],llxy[1]=proj(ll[0],ll[1])
    urxy[0],urxy[1]=proj(ur[0],ur[1])
    
    spacing=np.atleast_1d(np.array(spacing))
    xspacing=spacing[0]
    yspacing=spacing[0]
    if len(spacing)==2:
        yspacing=spacing[1]  

    rangex=np.arange(llxy[0],urxy[0]+xspacing,xspacing)
    rangey=np.arange(llxy[1],urxy[1]+yspacing,yspacing)
    xv,yv=np.meshgrid(rangex,rangey)
    
    lon,lat = proj(xv.flatten(),yv.flatten(),inverse=True)
    host=data['trigrid'].get_trifinder().__call__(lon,lat)

    idx=dt.get_elements(data,region)
    common=np.in1d(host,idx)

    return np.unique(host[common].flatten())


def regioner(data,region,subset=False):    
    nidx=dt.get_nodes(data,region)

    idx0=np.in1d(data['nv'][:,0],nidx)
    idx1=np.in1d(data['nv'][:,1],nidx)
    idx2=np.in1d(data['nv'][:,2],nidx)
    eidx=idx0+idx1+idx2

    nv2 = data['nv'][eidx].flatten(order='F')
    nidx_uni=np.unique(nv2)
    nv_tmp2=np.empty(shape=nv2.shape)
    nv2_sortedind = nv2.argsort()
    nv2_sortd = nv2[nv2_sortedind]
         
    for i in xrange(len(nidx_uni)):
        i1 = bisect.bisect_left(nv2_sortd, nidx_uni[i])
        i2 = bisect.bisect_right(nv2_sortd,nidx_uni[i])
        inds = nv2_sortedind[i1:i2]
        nv_tmp2[inds] = i

    nv_new = np.reshape(nv_tmp2, (-1, 3), 'F')
    
    data['trigrid_sub'] = mplt.Triangulation(data['lon'][nidx_uni], data['lat'][nidx_uni],nv_new)
    data['nidx_sub']=nidx_uni
    data['eidx_sub']=eidx
    data['nv_sub']=nv_new

    if subset==True:  
        data['zeta']=data['zeta'][:,nidx_uni]
        data['ua']=data['ua'][:,eidx]
        data['va']=data['va'][:,eidx]
        data['u']=data['u'][:,:,eidx]
        data['v']=data['v'][:,:,eidx]
        data['ww']=data['ww'][:,:,eidx]
        
    return data


def interp_vel(data,loc,layer=None,ll=True):
    #This function is deprecated in favor of ipt.interpE_at_loc.
    #It has been modified to call ipt.interpE_at_loc, should return identical results.
    print("This function is deprecated in favor of ipt.interpE_at_loc, please switch.")

    if (layer==None and loc.size==2):
        ua=ipt.interpE_at_loc(data,'ua',loc,layer=layer,ll=ll)
        va=ipt.interpE_at_loc(data,'va',loc,layer=layer,ll=ll)

        return ua,va

    if (layer!=None and loc.size==2):           
        u=ipt.interpE_at_loc(data,'u',loc,layer=layer,ll=ll)
        v=ipt.interpE_at_loc(data,'v',loc,layer=layer,ll=ll)
        w=ipt.interpE_at_loc(data,'ww',loc,layer=layer,ll=ll)
        
        return u,v,w

    
def _load_grdfile(casename=None):
    """
    Loads an FVCOM grd input file and returns the data as a dictionary. 
    """
    
    data={}    

    if casename==None:
        print('_load_grdfile requires a filename to load.')
        return
    try:
        fp=open(casename+'_grd.dat','r')
    except IOError:
        print('_load_grdfiles: invalid case name.')
        return data

    nodes_str=fp.readline().split('=')
    elements_str=fp.readline().split('=')
    nnodes=int(nodes_str[1])
    nele=int(elements_str[1])
    t_data1=np.genfromtxt(casename+'_grd.dat',skip_header=2, skip_footer=nnodes,dtype='int64')
    t_data2=np.genfromtxt(casename+'_grd.dat',skip_header=2+nele,dtype='float64')
    fp.close()

    data['nnodes']=nnodes
    data['nele']=nele
    data['nodexy']=t_data2[:,1:3]
    data['x']=t_data2[:,1]
    data['y']=t_data2[:,2]
    data['nv']=t_data1[:,1:4].astype(int)-1
    data['trigridxy'] = mplt.Triangulation(data['x'], data['y'],data['nv'])
    
    return data


def _load_depfile(casename=None):
    """
    Loads an FVCOM dep input file and returns the data as a dictionary. 
    """

    data={}
    
    if casename==None:
        print('_load_depfile requires a filename to load.')
        return
    try:
        fp=open(casename+'_dep.dat','r')
    except IOError:
        print('_load_depfile: invalid case name.')
        return data

    dep_str=fp.readline().split('=')
    dep_num=int(dep_str[1])
    t_data1=np.genfromtxt(casename+'_dep.dat',skip_header=1)
    fp.close()

    data['dep_num']=dep_num
    data['x']=t_data1[:,0]
    data['y']=t_data1[:,1]
    data['h']=t_data1[:,2]
    data['nodexy']=t_data1[:,0:2]
    
    return data


def _load_spgfile(casename=None):
    """
    Loads an FVCOM spg input file and returns the data as a dictionary. 
    """

    data={}
    
    if casename==None:
        print('_load_spgfile requires a filename to load.')
        return
    try:
        fp=open(casename+'_spg.dat','r')
    except IOError:
        print('_load_spgfile: invalid case name.')
        return data

    spg_str=fp.readline().split('=')
    spg_num=int(spg_str[1])
    t_data1=np.genfromtxt(casename+'_spg.dat',skip_header=1)
    fp.close()

    data['spgf_num']=spg_num
    data['spgf_nodes']=t_data1[:,0]
    data['spgf_distance']=t_data1[:,1]
    data['spgf_value']=t_data1[:,2]

    
    return data


def _load_obcfile(casename=None):
    """
    Loads an FVCOM obc input file and returns the data as a dictionary. 
    """    

    data={}

    if casename==None:
        print('_load_obcfile requires a filename to load.')
        return
    try:
        fp=open(casename+'_obc.dat','r')
    except IOError:
        print('_load_obcfile: invalid case name.')
        return data

    obc_str=fp.readline().split('=')
    obc_num=int(obc_str[1])
    t_data1=np.genfromtxt(casename+'_obc.dat',skip_header=1)
    fp.close()

    data['obcf_num']=obc_num
    data['obcf_numbers']=t_data1[:,0]
    data['obcf_nodes']=t_data1[:,1]
    data['obcf_value']=t_data1[:,2]

    
    return data


def _load_llfiles(casename=None):
    """
    Loads an long/lat files and returns the data as a dictionary. 
    """

    data={}
    
    if casename==None:
        print('_load_llfiles requires a filename to load.')
        return
    try:
        fp=open(casename+'_long.dat','r')
    except IOError:
        print('_load_llfiles: long file is invalid.')
        return data

    lon=np.genfromtxt(casename+'_long.dat')
    fp.close()

    try:
        fp=open(casename+'_lat.dat','r')
    except IOError:
        print('_load_llfiles: lat file is invalid.')
        return data

    lat=np.genfromtxt(casename+'_lat.dat')
    fp.close()

    data['nodell']=np.vstack([lon,lat]).T
    data['lat']=lat
    data['lon']=lon
    
    return data


def _load_nc(filename=None):
    """
    Loads an .nc  data file      
    """

    ncid = netcdf.netcdf_file(filename, 'r',mmap=True)
    
    data={}

    for i in ncid.variables.keys():
        data[i]=ncid.variables[i].data

    return data


def load_fvcom_files(filepath=None,casename=None,ncname=None,neifile=None):
    """
    Loads FVCOM input files and returns the data as a dictionary. 
    """

    currdir=os.getcwd()
    os.chdir(filepath)

    data=_load_grdfile(casename)

    data.update(_load_depfile(casename))
    
    data.update(_load_spgfile(casename))

    data.update(_load_obcfile(casename))

    data.update(_load_llfiles(casename))

    if ncname!=None:
        data.update(_load_nc(ncname))

    if neifile!=None:
        data.update(loadnei(neifile))

    os.chdir(currdir)

    return data


def save_spgfile(datain,filepath,casename=None):
    """
    Save an FVCOM spg input file. 
    """

    data={}
    
    if casename==None:
        print('save_spgfile requires a filename to save.')
        return
    try:
        fp=open(filepath + casename+'_spg.dat','w')
    except IOError:
        print('save_spgfile: invalid case name.')
        return data

    fp.write('Sponge Node Number = %d\n' % datain['spgf_num'] )
    for i in range(0,datain['spgf_num']):
        fp.write('%d %f %f\n'% (datain['spgf_nodes'][i],datain['spgf_distance'][i],datain['spgf_value'][i]))
    fp.close()


def save_obcfile(datain,filepath,casename=None):
    """
    Save an FVCOM obc input file. 
    """

    data={}
    
    if casename==None:
        print('save_obcfile requires a filename to save.')
        return
    try:
        fp=open(filepath + casename+'_obc.dat','w')
    except IOError:
        print('save_obcfile: invalid case name.')
        return data

    fp.write('OBC Node Number = %d\n' % datain['obcf_num'] )
    for i in range(0,datain['obcf_num']):
        fp.write('%d %d %d\n'% (datain['obcf_numbers'][i],datain['obcf_nodes'][i],datain['obcf_value'][i]))
    fp.close()


def loadcage(filepath):
    cages=None
    try:
        with open(filepath) as f_in:
            cages=np.genfromtxt(f_in,skip_header=1)
            if len(cages)>0:
                cages=(cages[:,0]-1).astype(int)
            else:
                cages=None
    except:
        cages=None

    return cages


def load_nodfile(filename=None,h=False):
    """
    Loads an nod file the data as a dictionary. 
    """

    data={}
    
    if filename==None:
        print('load_nodfile requires a filename to load.')
        return
    try:
        fp=open(filename,'r')
    except IOError:
        print('load_nodfile: invalid filename.')
        return data

    t_data1=np.genfromtxt(filename)
    fp.close()

    data['node_num']=t_data1[:,0]
    data['x']=t_data1[:,1]
    data['y']=t_data1[:,2]
    if h==True:
        data['h']=t_data1[:,3]
    else:
        data['h']=np.zeros((len(data['x']),))
    
    return data


def load_elefile(filename=None):
    """
    Loads an ele file the data as a dictionary. 
    """

    data={}
    
    if filename==None:
        print('load_elefile requires a filename to load.')
        return
    try:
        fp=open(filename,'r')
    except IOError:
        print('load_elefile: invalid filename.')
        return data

    t_data1=np.genfromtxt(filename)
    fp.close()

    data['ele_num']=t_data1[:,0]
    data['nv']=t_data1[:,1:4]
    
    return data


def save_grdfile(grddata,depdata,outname,is31=True):
    """
    Save an FVCOM grd input file. 
    """
    
    if outname==None:
        print('save_grdfile requires a filename to save.')
        return
    try:
        fp=open(outname,'w')
    except IOError:
        print('save_grdfile: invalid filename.')
        return data
    if is31:
        fp.write('Node Number = %d\n' % len(depdata['node_num']) )
        fp.write('Cell Number = %d\n' % len(grddata['nv']) )
    for i in range(0,len(grddata['nv'])):
        fp.write('%d %d %d %d %d\n'% (grddata['ele_num'][i],grddata['nv'][i,0],grddata['nv'][i,1],grddata['nv'][i,2],0))

    for i in range(0,len(depdata['node_num'])):
        fp.write('%d %f %f %f\n'% (depdata['node_num'][i],depdata['x'][i],depdata['y'][i],depdata['h'][i]))
    fp.close()

   
    return 


def save_depfile(depdata,outname,is31=True):
    """
    Save an FVCOM dep input file. 
    """
  

    if outname==None:
        print('save_depfile requires a filename to save.')
        return
    try:
        fp=open(outname,'w')
    except IOError:
        print('save_depfile: invalid filename.')
        return data
    if is31:
        fp.write('Node Number = %d\n' % len(depdata['node_num']) )
    for i in range(0,len(depdata['node_num'])):
        fp.write('%f %f %f\n'% (depdata['x'][i],depdata['y'][i],depdata['h'][i]))
    fp.close()

   
    return 


def load_rivfile(filename=None):
    """
    Loads an FVCOM riv input file and returns the data as a dictionary. 
    """    

    data={}

    if filename==None:
        print('load_rivfile requires a filename to load.')
        return
    try:
        fp=open(filename,'r')
    except IOError:
        print('load_rivfile: invalid filename.')
        return data
    
    data['RIVER_NAME']=''
    data['RIVER_GRID_LOCATION']=0
    data['RIVER_VERTICAL_DISTRIBUTION']=''


    for line in fp:
        if line.strip().startswith('RIVER_NAME'):
            data['RIVER_NAME']=np.append(data['RIVER_NAME'],line[line.find('"')+1:line.rfind('"')])
        if line.strip().startswith('RIVER_GRID_LOCATION'):
            data['RIVER_GRID_LOCATION']=np.append(data['RIVER_GRID_LOCATION'],int(line[line.find('=')+1:line.rfind(',')]))
        if line.strip().startswith('RIVER_VERTICAL_DISTRIBUTION'):
            data['RIVER_VERTICAL_DISTRIBUTION']=np.append(data['RIVER_VERTICAL_DISTRIBUTION'],line[line.find('"')+1:line.rfind('"')])

    data['RIVER_NAME']=np.delete(data['RIVER_NAME'],0)
    data['RIVER_GRID_LOCATION']=np.delete(data['RIVER_GRID_LOCATION'],0)
    data['RIVER_VERTICAL_DISTRIBUTION']=np.delete(data['RIVER_VERTICAL_DISTRIBUTION'],0)

    
    return data


def save_rivfile(rivdata,filename=None):
    """
    Saves an FVCOM riv input file. 
    """    

    data={}

    if filename==None:
        print('save_rivfile requires a filename to save.')
        return
    try:
        fp=open(filename,'w')
    except IOError:
        print('save_rivfile: invalid filename.')
        return data
    
    for i in range(len(rivdata['RIVER_NAME'])):
        block='''&NML_RIVER
        RIVER_NAME          = "{0}",
        RIVER_GRID_LOCATION = {1},
        RIVER_VERTICAL_DISTRIBUTION = "{2}" / '''.format(rivdata['RIVER_NAME'][i],rivdata['RIVER_GRID_LOCATION'][i],rivdata['RIVER_VERTICAL_DISTRIBUTION'][i])    

        print >> fp, block


def load_segfile(filename=None):
    """
    Loads an seg file the data as a dictionary. 
    """

    data={}
    
    if filename==None:
        print('load_segfile requires a filename to load.')
        return
    try:
        fp=open(filename,'r')
    except IOError:
        print('load_segfile: invalid filename.')
        return data

    data=collections.OrderedDict()

    for line in fp:
        llist=line.split()
        if len(llist)==2:
            cnt=0
            currentseg=llist[0]
            data[currentseg]=np.empty((int(llist[1]),2))
        else:
            data[currentseg][cnt,:]=llist[1:3]
            cnt+=1

    fp.close()

    return data
    
    
def load_nodefile(filename=None):
    """
    Loads an nod file into a dictionary. 
    """

    data={}
    
    if filename==None:
        print('load_nodefile requires a filename to load.')
        return
    try:
        fp=open(filename,'r')
    except IOError:
        print('load_nodefile: invalid filename.')
        return data

    data=collections.OrderedDict()

    tp = fp.readline()
    nbnd = int(fp.readline())

    for cnt in range(nbnd):
        cnt=str(cnt)
        llist=fp.readline().split()        
        data[cnt]=np.empty((int(llist[0]),2))
        for i in range(int(llist[0])):
            llist=fp.readline().split() 
            data[cnt][i,0] = float(llist[0])
            data[cnt][i,1] = float(llist[1])
            
    fp.close()

    return data


def find_outside_seg(segfile=None,swap=True):
    """
    Takes a segfile dict and finds which segment is the outside.
    
    swap - swaps the outside segment with the first segment (default=True)
    """


    
    if segfile==None:
        print('find_outside_seg needs a segfile dict')
        return

    lonmin=10000000
    lonmax=-10000000
    latmin=10000000
    latmax=-10000000
    first=100000000
    for key in segfile.keys():
        first=np.min([first,int(key)])
        if lonmax<np.max(segfile[key][:,0]):
            lonmax=np.max(segfile[key][:,0])
            lonmaxkey=key
        if lonmin>np.min(segfile[key][:,0]):
            lonmin=np.min(segfile[key][:,0])
            lonminkey=key
        if latmax<np.max(segfile[key][:,1]):
            latmax=np.max(segfile[key][:,1])
            latmaxkey=key
        if latmin>np.min(segfile[key][:,1]):
            latmin=np.min(segfile[key][:,1])
            latminkey=key

    if swap==True:
        if (lonmaxkey==lonminkey==latmaxkey==latminkey):
            print('Swapping ' +lonmaxkey+ ' and first segment')
            segfile[first.astype(str)],segfile[lonmaxkey]=segfile[lonmaxkey],segfile[first.astype(str)]
        else:
            print('Could not find single outside segment')            

        return segfile
    else:
        if lonmaxkey==lonminkey==latmaxkey==latminkey:
            print(lonmaxkey+ ' is the outside segment')
        else:
            print('Could not find single outside segment')
        return  


def save_nodfile(segfile,filename=None,bnum=[]):
    """
    Save a nod file from a seg dict. 
    """
    
    if filename==None:
        print('save_nodfile requires a filename to save.')
        return
    try:
        fp=open(filename,'w')
    except IOError:
        print('save_nodfile: invalid filename.')
        return data

    dictlen=0
    for key in segfile.keys():
        dictlen+=len(segfile[key])


    fp.write('%d\n' % dictlen )
    if bnum==[]:
        fp.write('%d\n' % len(segfile.keys()) )
    else:
        fp.write('%d\n' % bnum )

    for key in segfile.keys():
        fp.write('%d\n'% len(segfile[key]))
        for i in range(len(segfile[key])):
            fp.write('%f %f %f\n'% (segfile[key][i,0],segfile[key][i,1],0.0))

    fp.close()

   
    return 


def save_llz(data,filename=None):
    """
    Saves a llz array as a file. Takes an Nx3 array 
    """
    
    if filename==None:
        print('save_llz requires a filename to save.')
        return
    try:
        fp=open(filename,'w')
    except IOError:
        print('Can''t make ' + filename)
        return

    for i in range(len(data)):
        fp.write('%f %f %f\n' % (data[i,0],data[i,1],data[i,2] ) )

    fp.close()


def save_nv(data,filename=None):
    """
    Saves a nv array as a file.

 
    """
    
    if filename==None:
        print('save_nv requires a filename to save.')
        return
    try:
        fp=open(filename,'w')
    except IOError:
        print('Can''t make ' + filename)
        return

    for i in range(len(data)):
        fp.write('%d %d %d\n' % (data[i,0],data[i,1],data[i,2] ) )

    fp.close()

def doubleres_nei(neifile):    
   
    #newneifile
    nnf=copy.deepcopy(neifile)
    #newnodenumber
    nnn=neifile['nnodes']
    
    for node in range(neifile['nnodes']):
        neighbours=(neifile['neighbours'][node,(neifile['neighbours'][node,:]>0) & (neifile['neighbours'][node,:]>(node+1))])-1
        for i,neighbour in enumerate(neighbours):
            nnn+=1
            nnf['nodell']=np.vstack([nnf['nodell'],(neifile['nodell'][node,:]+neifile['nodell'][neighbour,:])/2])
            nnf['h']=np.append(nnf['h'],(neifile['h'][node]+neifile['h'][neighbour])/2)
            if neifile['bcode'][node]==neifile['bcode'][neighbour]:
                nnf['bcode']=np.append(nnf['bcode'],neifile['bcode'][node])
            else:
                nnf['bcode']=np.append(nnf['bcode'],0)
            nnf['neighbours'][node,neifile['neighbours'][node,:]==(neighbour+1)]=nnn
            nnf['neighbours'][neighbour,neifile['neighbours'][neighbour,:]==(node+1)]=nnn
            nnf['neighbours']=np.vstack([nnf['neighbours'],np.zeros((1,neifile['maxnei']))])
            nnf['neighbours'][nnn-1,0]=node+1
            nnf['neighbours'][nnn-1,1]=neighbour+1
            nnf['nodenumber']=np.append(nnf['nodenumber'],nnn)
              
    nnf['nnodes']=len(nnf['nodenumber'])
    nnf['lon']=nnf['nodell'][:,0]
    nnf['lat']=nnf['nodell'][:,1]
    
    parents=copy.deepcopy(nnf['neighbours'][neifile['nnodes']:,:])
    for node in range(neifile['nnodes'],nnf['nnodes']):
        p0=nnf['neighbours'][node,0]
        p1=nnf['neighbours'][node,1]
        n0=neifile['neighbours'][p0-1,np.nonzero(neifile['neighbours'][p0-1,:])][0]
        n1=neifile['neighbours'][p1-1,np.nonzero(neifile['neighbours'][p1-1,:])][0]
        common=n0[np.in1d(n0,n1)]
        #for i,p in enumerate(common):
            #nnf['neighbours'][node,(2*i)+2]=np.argwhere(((parents==p).sum(axis=1)+(parents==p0).sum(axis=1))==2)+1
            #nnf['neighbours'][node,(2*i)+3]=np.argwhere(((parents==p).sum(axis=1)+(parents==p1).sum(axis=1))==2)+1
        for i,p in enumerate(common):
            pb=parents==p
            pb0=parents==p0
            pb1=parents==p1            
            nnf['neighbours'][node,(2*i)+2]=np.argwhere((pb+pb0).sum(axis=1)==2)+1+neifile['nnodes']
            nnf['neighbours'][node,(2*i)+3]=np.argwhere((pb+pb1).sum(axis=1)==2)+1+neifile['nnodes']
    
    return nnf


def load_stationfile(filename=None):
    """
    Loads an FVCOM station input file and returns the data as a dictionary. 
    """
    
    data={}    

    if filename==None:
        print('load_stationfile requires a filename to load.')
        return
    try:
        fp=open(filename,'r')
    except IOError:
        print('load_stationfile: invalid filename.')
        return data

    headerstr=fp.readline()
    data_str=np.genfromtxt(filename,skip_header=1,dtype=str)
    fp.close()

    data['header']=headerstr
    data['station_num']=data_str[:,0].astype(np.int32)
    data['cell']=data_str[:,3].astype(np.int32)
    data['x']=data_str[:,1].astype(np.float64)
    data['y']=data_str[:,2].astype(np.float64)
    data['h']=data_str[:,4].astype(np.float64)
    data['station_name'] = data_str[:,5]
    
    return data


def save_stationfile(sdata,outname):
    """
    Save an FVCOM station input file. 
    """
    
    if outname==None:
        print('save_stationfile requires a filename to save.')
        return
    try:
        fp=open(outname,'w')
    except IOError:
        print('save_stationfile: invalid filename.')
        return data
        

    fp.write('%s' % sdata['header'] )        
    for i in range(0,len(sdata['x'])):
        fp.write('%d %f %f %d %f %s\n'% (sdata['station_num'][i],sdata['x'][i],sdata['y'][i],sdata['cell'][i],sdata['h'][i],sdata['station_name'][i] )   )

    fp.close()

   
    return 


def get_nv(neifile):

    try:
        import pyximport; pyximport.install()
        import get_nv as gnv
        
        neifile['nv']=gnv.get_nvc(neifile['neighbours'],neifile['nnodes'],neifile['maxnei'])
        neifile['trigrid'] = mplt.Triangulation(neifile['lon'], neifile['lat'],neifile['nv'])  
    except:
        print('There was an issue with during using cython falling back to python.')
    
        nv=np.empty((len(neifile['neighbours'])*2,3))    
        
        neighbours=copy.deepcopy(neifile['neighbours'])

        kk=0
        for i in range(neifile['nnodes']-2):
            nei_cnt=1
            for ii in range(neifile['maxnei']-1):
                if neighbours[i,ii+1]==0:
                    break
                nei_cnt=ii+1    
                if neighbours[i,ii]<=(i+1):
                    continue
                if neighbours[i,ii+1]<=(i+1):
                    continue   
                for j in range(neifile['maxnei']):
                    if neighbours[neighbours[i,ii]-1,j]!=neighbours[i,ii+1]:
                        continue
                    nv[kk,:]=[i+1,neighbours[i,ii],neighbours[i,ii+1]]
                    kk=kk+1
                    break

            if (nei_cnt>1):
                for j in range(neifile['maxnei']):
                    if neighbours[i,0]<=(i+1):
                        break
                    if neighbours[i,nei_cnt]<=(i+1):
                        break
                    if neighbours[neighbours[i,0]-1,j] ==0:
                        break    
                    if neighbours[neighbours[i,0]-1,j] !=neighbours[i,nei_cnt]:
                        continue
                    nv[kk,:]=[i+1,neighbours[i,nei_cnt],neighbours[i,0] ]
                    kk=kk+1
                    break
                     
        nv=np.delete(nv,np.s_[kk:],axis=0)
        neifile['nv']=(nv-1).astype(int)  
        neifile['trigrid'] = mplt.Triangulation(neifile['lon'], neifile['lat'],neifile['nv'])   
        
      
                
    return neifile
    
    
def get_sidelength(data):
    """
        Takes an FVCOM dictionary and returns it with the average element sidelength added.
    """
    sl=np.zeros([len(data['nv']),])
    sidemin=np.zeros([len(data['nv']),])+100000000
    sidemax=np.zeros([len(data['nv']),])
    
    for i in range(0,len(data['nv'])):
        slmin=0
        for j in range(3):
            slmin=np.sqrt((data['nodexy'][data['nv'][i,j-1],0]-data['nodexy'][data['nv'][i,j],0])**2+(data['nodexy'][data['nv'][i,j-1],1]-data['nodexy'][data['nv'][i,j],1])**2)+slmin
            sidemin[i]=np.min([np.sqrt((data['nodexy'][data['nv'][i,j-1],0]-data['nodexy'][data['nv'][i,j],0])**2+(data['nodexy'][data['nv'][i,j-1],1]-data['nodexy'][data['nv'][i,j],1])**2),sidemin[i]])
            sidemax[i]=np.max([np.sqrt((data['nodexy'][data['nv'][i,j-1],0]-data['nodexy'][data['nv'][i,j],0])**2+(data['nodexy'][data['nv'][i,j-1],1]-data['nodexy'][data['nv'][i,j],1])**2),sidemax[i]])
        sl[i]=slmin/3
        
    data['sl']=sl
    data['slmin']=sidemin
    data['slmax']=sidemax
    
    return data
 
    
def get_dhh(data):
    dh=np.zeros([len(data['nv']),])
    for i in range(0,len(data['nv'])):
        one=data['h'][data['nv'][i,0]]
        two=data['h'][data['nv'][i,1]]
        three=data['h'][data['nv'][i,2]]
        hmin=np.min([one,two,three])
        
        #control points close to zero to avoid division by small numbers
        if ((hmin>=0) and (hmin < 1)):
            hmin=1
        if ((hmin<0) and (hmin > -1)):
            hmin=-1
        
        first=np.fabs(np.fabs(one-two)/hmin)
        second=np.fabs(np.fabs(two-three)/hmin)
        thrid=np.fabs(np.fabs(three-one)/hmin)
	
        dh[i]=np.max([first,second,thrid]);
            
    data['dhh']=dh
    return data

    
 
def save_segfile(segfile,outfile=None):
    """
    Saves a seg file. 
    """


    if outfile==None:
        print('save_segfile requires a filename to save.')
        return
    try:
        fp=open(outfile,'w')
    except IOError:
        print('save_segfile: invalid filename.')
        return

    for seg in segfile:
        fp.write('%s %d\n' % (seg,len(segfile[seg]) ) )
        for i in range(len(segfile[seg])):
            fp.write('%d %f %f\n' % (i+1,segfile[seg][i,0],segfile[seg][i,1] ) )
    fp.close()

    return 

    
def save_seg2nc(segfile,outname):
    
    try:
        import netCDF4 as n4
    except ImportError:
        print("netCDF4 is not installed, please install netCDF4.")
        return

    ncid = n4.Dataset(outname, 'w',format='NETCDF3_CLASSIC')

    tlen=0
    for seg in segfile:
        tlen+=len(segfile[seg])
    numkey=len(segfile.keys())

    #create dimensions
    ncid.createDimension('nlines',numkey)
    ncid.createDimension('npoints',tlen) 

    #define variables
    lat = ncid.createVariable('lat','d',('npoints',))
    lon = ncid.createVariable('lon','d',('npoints',))
    start = ncid.createVariable('start','i4',('nlines',))
    count = ncid.createVariable('count','i4',('nlines',))

    START=np.empty((numkey,))
    COUNT=np.empty((numkey,))
    LON=np.empty((tlen,))
    LAT=np.empty((tlen,))
    
    START[0]=0
    for i,seg in enumerate(segfile):
        COUNT[i]=len(segfile[seg])   
        if i<(numkey-1):
            START[i+1]=START[i]+COUNT[i]    
        LON[int(START[i]):int(START[i]+COUNT[i])]=segfile[seg][:,0]
        LAT[int(START[i]):int(START[i]+COUNT[i])]=segfile[seg][:,1]
        
    start[:]=START
    count[:]=COUNT
    lon[:]=LON
    lat[:]=LAT
    
    ncid.__setattr__('description','Coastline for Xscan in nc format')
    ncid.__setattr__('history','Created ' +time.ctime(time.time()) )

    ncid.close()

    
def sort_boundary(neifile,boundary=1):

    nn=copy.deepcopy(neifile['nodenumber'][neifile['bcode']==boundary]).astype(int)
    nnei=copy.deepcopy(neifile['neighbours'][neifile['bcode']==boundary]).astype(int)
    
    #find the neighbour of the first node
    idx=np.argwhere(nnei==nn[0])[0][0]
    
    #have to use temp values with copy as the standard swap doesn't work when things are swapped again and again.
    #there must be a more python way to hand that....
    tmpval=nn[1].copy()
    nn[1]=nn[idx]
    nn[idx]=tmpval    
    tmpval=nnei[1,:].copy()
    nnei[1,:]=nnei[idx,:]
    nnei[idx,:]=tmpval
   
    for i in range(1,len(nn)-1):
        for j in range(neifile['maxnei']):
            nei=nnei[i,j]
            if nei==0: continue
            idx=np.argwhere(nn[(i+1):]==nei)

            if len(idx)==1:
                tmpval=nn[(i+1)].copy()
                nn[(i+1)]=nn[(idx+i+1)]
                nn[(idx+i+1)]=tmpval                
                tmpval=nnei[(i+1),:].copy()
                nnei[(i+1),:]=nnei[(idx+i+1),:]
                nnei[(idx+i+1),:]=tmpval
                break
                
                
                
    return nn
    
    
def save_elobc(elobc,outname):
    
    try:
        import netCDF4 as n4
    except ImportError:
        print("netCDF4 is not installed, please install netCDF4.")
        return

    ncid = n4.Dataset(outname, 'w',format='NETCDF3_CLASSIC')


    #create dimensions
    ncid.createDimension('nobc',len(elobc['obc_nodes']))
    ncid.createDimension('tidal_components',len(elobc['tide_period'])) 
    ncid.createDimension('TideLen',np.shape(elobc['equilibrium_tide_type'])[1])
    ncid.createDimension('DateStrLen',len(elobc['time_origin']))

    #define variables
    obc_nodes = ncid.createVariable('obc_nodes','i4',('nobc',))    
    tide_period = ncid.createVariable('tide_period','f',('tidal_components',))
    tide_Eref = ncid.createVariable('tide_Eref','f',('nobc',))
    tide_Ephase = ncid.createVariable('tide_Ephase','f',('tidal_components','nobc'))
    tide_Eamp = ncid.createVariable('tide_Eamp','f',('tidal_components','nobc'))
    equilibrium_tide_Eamp = ncid.createVariable('equilibrium_tide_Eamp','f',('tidal_components',))
    equilibrium_beta_love = ncid.createVariable('equilibrium_beta_love','f',('tidal_components',))
    equilibrium_tide_type = ncid.createVariable('equilibrium_tide_type','c',('tidal_components','TideLen'))
    time_origin = ncid.createVariable('time_origin','c',('DateStrLen',))

    obc_nodes[:] = elobc['obc_nodes']   
    obc_nodes.__setattr__('long_name','Open Boundary Node Number')
    obc_nodes.__setattr__('grid','obc_grid')
    
    tide_period[:] = elobc['tide_period']
    tide_period.__setattr__('long_name','tide angular period')
    tide_period.__setattr__('units','seconds')
    
    tide_Eref[:] = elobc['tide_Eref']
    tide_Eref.__setattr__('long_name','tidal elevation reference level')
    tide_Eref.__setattr__('units','meters')
    
    tide_Ephase[:] = elobc['tide_Ephase']
    tide_Ephase.__setattr__('long_name','tidal elevation phase angle')
    tide_Ephase.__setattr__('units','degrees, time of maximum elevation with respect to chosen time origin')
    
    tide_Eamp[:] = elobc['tide_Eamp']
    tide_Eamp.__setattr__('long_name','tidal elevation amplitude')
    tide_Eamp.__setattr__('units','meters')
    
    equilibrium_tide_Eamp[:] = elobc['equilibrium_tide_Eamp']
    equilibrium_tide_Eamp.__setattr__('long_name','equilibrium tidal elevation amplitude')
    equilibrium_tide_Eamp.__setattr__('units','meters')
    
    equilibrium_beta_love[:] = elobc['equilibrium_beta_love']
    equilibrium_beta_love.__setattr__('formula','beta=1+klove-hlove')
    
    equilibrium_tide_type[:] = elobc['equilibrium_tide_type']
    equilibrium_tide_type.__setattr__('long_name','formula')
    equilibrium_tide_type.__setattr__('units','beta=1+klove-hlove')

    
    time_origin[:] = elobc['time_origin']
    time_origin.__setattr__('long_name','time')
    time_origin.__setattr__('units','yyyy-mm-dd HH:MM:SS')
    time_origin.__setattr__('time_zone','UTC')
    time_origin.__setattr__('comments','tidal harmonic origin_date')
    

    


    
    ncid.__setattr__('type','FVCOM SPECTRAL ELEVATION FORCING FILE')
    ncid.__setattr__('history','Created ' +time.ctime(time.time()) )

    ncid.close()    
    
    
def load_nei2fvcom(filename,sidelength=True):
    """
    Loads a .nei file and returns the data as a dictionary that mimics the structure of fvcom output as closely as possible. 
    """
    
    # Load the neifile
    data=load_neifile(filename)
    
    # Use lcc projection get x,y data
    data['x'],data['y'],data['proj']=pjt.lcc(data['lon'],data['lat'])
    
    # Get nv for grid
    data=get_nv(data)
    
    # ncdatasort to make typically structures
    data=dt.ncdatasort(data)
    
    # get the model sidelength
    if sidelength:
        data=get_sidelength(data)       
        
    return data
    
def nei2seg(neifile):
    """
    Convert the boundaries from an neifile to a segfile.
    """
    
    segfile=collections.OrderedDict()
    segfileidx=collections.OrderedDict()
    
    bcode=neifile['bcode']  
    nbound=np.unique(bcode) 
        
    for j in range(1,len(nbound)):
        idx=sort_boundary(neifile,boundary=j)-1
        segfile[str(j)]=np.vstack([neifile['lon'][idx],neifile['lat'][idx]]).T          

    return segfile
    
    
def nan2seg(datain):
    """
    Convert a nan separated array to a seg dict
    """
    
    nanidx=np.argwhere(np.isnan(datain[:,0]))
    
    #Add start and end points
    nanidx=np.append(0, nanidx)
    nanidx=np.append(nanidx,len(datain[:,0])-1)
    #Remove no unique points
    nanidx=np.unique(nanidx)
    
    segfile = collections.OrderedDict()
    
    for i in range(len(nanidx)-1):
        segfile[str(i+1)] = datain[nanidx[i]+1:nanidx[i+1],]
    
    
    return segfile
    

def mergesegfiles(seg1,seg2):
    """
    Merge two seg dicts
    """
    
    maxseg=int(list(seg1.keys())[-1])
    
    for seg in seg2:
        maxseg+=1
        seg1[str(maxseg)]=seg2[seg]
            
    return seg1   
    
    
def merge_segments(segfile,segnum1,segnum2,flip1=False,flip2=False):
    """
    Merge two segments in a segfile
    """
    
    if flip1:
        seg1=np.flipud(segfile[segnum1])
    else:
        seg1=segfile[segnum1]
    if flip2:
        seg2=np.flipud(segfile[segnum2])
    else:
        seg2=segfile[segnum2]
    
    segfile[segnum1]=np.vstack([seg1,seg2])
    del segfile[segnum2]    
    
    return segfile
    

def load_kml2seg(filename):
    """
    Loads a coastline kml as a seg dict
    """
    
    data=collections.OrderedDict()
    cnt=1

    ds = ogr.Open(filename)
    for lyr in ds:
        for feat in lyr:
            geom = feat.GetGeometryRef()
            if (geom != None) and (geom.GetGeometryName() == 'LINESTRING'):
                data[str(cnt)]=np.array(geom.GetPoints())
                cnt+=1
    
    return data

    

    

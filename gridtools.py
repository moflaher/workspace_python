from __future__ import division,print_function
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import os, sys, time
import datatools as dt
import misctools as mt
import plottools as pt
import interptools as ipt
import projtools as pjt
np.set_printoptions(precision=16,suppress=True,threshold=sys.maxsize)
from scipy.io import netcdf
import bisect
import collections
import copy
import pyproj as pyp



"""
Front Matter
=============

Created in 2014

Author: Mitchell O'Flaherty-Sproul

A bunch of functions dealing with finite element grids and there construction. All FVCOM particular code should be in fvcomtools

           
"""

################################################################################
#
# Code to load files related to finite element grids
#
################################################################################

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
    
    
    
################################################################################
#
# Code to save files related to finite element grids 
#
################################################################################

def save_neifile(neifilename=None,neifile=None):
    """
    Save an .neifile 

 
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
        
def save_array(data,filename=None):
    """
    Saves a array as a file. 
    """
    
    if len(data.shape)==1:
        data=np.atleast_2d(data).T
    if len(data.shape)>2:
        print('Cannot print 3d+ array')
    
    if filename==None:
        print('save_array requires a filename to save.')
        return
    try:
        fp=open(filename,'w')
    except IOError:
        print('Can''t make ' + filename)
        return

    sout = ''
    for i in range(data.shape[1]):
        sout += '{} '
    sout = sout[:-1] + '\n'

    for i in range(len(data)):
        fp.write(sout.format(*data[i,:]))

    fp.close()
    

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



def save_mshfile(neifile=None, outfile=None):
    """
    Saves a grid in gmsh format.

 
    """
    print('This doesnt work right. Need to figure out element ordering stuff.')
    return
    
    if outfile==None:
        print('save_mshfile requires a filename to save.')
        return
    try:
        fp=open(outfile,'w')
    except IOError:
        print('Can''t make ' + outfile)
        return

    if neifile==None:
        print('No neifile dict given.')
        return



    fp.write('$MeshFormat\n2.2 0 8\n$EndMeshFormat\n$Nodes\n')
    fp.write('{}\n'.format(neifile['nnodes']))
    for i in range(neifile['nnodes']):
        fp.write('{} {} {} {}\n'.format(i+1, neifile['nodell'][i,0], neifile['nodell'][i,1], neifile['h'][i]))
    fp.write('$EndNodes\n$Elements\n')
    fp.write('{}\n'.format(len(neifile['nv'])))
    for i in range(len(neifile['nv'])):
        fp.write('{} 1 2 0 {} {} {}\n'.format(i+1, neifile['nv'][i,0], neifile['nv'][i,1], neifile['nv'][i,2]))
    fp.write('$EndElements\n')
    fp.close()


################################################################################
#
# Code to process stuff for finite element grids
#
################################################################################

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

    idx=get_elements(data,region)
    common=np.in1d(host,idx)

    return np.unique(host[common].flatten())


def regioner(data,region=None,nidx=None,subset=False):   
    
    if region is None and nidx is None:
        print('Must specify a region or nidx')
        return
        
    if region is not None:     
        nidx=get_nodes(data,region)
    

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
    data['eidx_sub']=np.arange(len(eidx))[eidx]
    data['nv_sub']=nv_new

    if subset==True:  
        data['zeta']=data['zeta'][:,nidx_uni]
        data['ua']=data['ua'][:,eidx]
        data['va']=data['va'][:,eidx]
        data['u']=data['u'][:,:,eidx]
        data['v']=data['v'][:,:,eidx]
        data['ww']=data['ww'][:,:,eidx]
        
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
            nnf['neighbours']=np.vstack([nnf['neighbours'],np.zeros((1,neifile['maxnei']),dtype=int)])
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
    

def get_elements(data, region, isll=True):
    """
    Takes uvnodeXX and a region (specified by the corners of a
    rectangle) and determines the elements of uvnode that lie within the
    region
    """
    if isll:
        keystr = 'uvnodell'
    else:
        keystr = 'uvnodexy'
    
    idx = np.argwhere((data[keystr][:,0] >= region['region'][0]) &
                      (data[keystr][:,0] <= region['region'][1]) & 
                      (data[keystr][:,1] >= region['region'][2]) & 
                      (data[keystr][:,1] <= region['region'][3]))

    return idx
    

def get_nodes(data, region, isll=True):
    """
    Takes nodeXX and a region (specified by the corners of a rectangle)
    and determines the nodes that lie in the region
    """
   
    if isll:
        keystr = 'nodell'
    else:
        keystr = 'nodexy'
    
    idx = np.argwhere((data[keystr][:,0] >= region['region'][0]) &
                      (data[keystr][:,0] <= region['region'][1]) & 
                      (data[keystr][:,1] >= region['region'][2]) & 
                      (data[keystr][:,1] <= region['region'][3]))

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

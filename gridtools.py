from __future__ import division
import numpy as np
import matplotlib as mpl
import scipy as sp
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
from StringIO import StringIO

from datatools import *
from regions import makeregions
np.set_printoptions(precision=16,suppress=True,threshold=np.nan)
import bisect


"""
Front Matter
=============

Created in 2014

Author: Mitchell O'Flaherty-Sproul

A bunch of functions dealing with finite element grids.

Requirements
===================================
Absolutely Necessary:


Optional, but recommended:


Functions
=========
regions -   given no input regions returns a list of regions, given a valid location it returns long/lat of the region and the passage name in file format and title format.
            
"""



def regions(regionname=None):
    """Returns region locations and full names

    :Parameters:
    	regionname

 
    """

    allregions=makeregions()

    if regionname==None:
        print 'Valid regions are'
        return allregions.keys()        
    else:
        tmpregion=allregions[regionname]
        tmpregion['center']=[(tmpregion['region'][0]+tmpregion['region'][1])/2,(tmpregion['region'][2]+tmpregion['region'][3])/2]
        return tmpregion


def loadnei(neifilename=None):
    """
    Loads a .nei file and returns the data as a dictionary.

 
    """
    
    if neifilename==None:
        print 'loadnei requires a filename to load.'
        return
    try:
        fp=open(neifilename,'r')
    except IOError:
        print 'Can not find ' + neifilename
        return

    nnodes=int(fp.readline())
    maxnei=int(fp.readline())
    llminmax=np.genfromtxt(StringIO(fp.readline()))
    t_data=np.loadtxt(neifilename,skiprows=3,dtype='float64')
    fp.close()

    neifile={}

    neifile['nnodes']=nnodes
    neifile['maxnei']=maxnei
    neifile['llminmax']=llminmax

    neifile['nodenumber']=t_data[:,0]
    neifile['nodell']=t_data[:,1:3]
    neifile['bcode']=t_data[:,3]
    neifile['h']=t_data[:,4]
    neifile['neighbours']=t_data[:,5:]
    
    return neifile


def find_land_nodes(neifile=None):
    """
    Given an neifile dictionary from loadnei. 
    This fuction returns a list of nodes which are constructed from only boundary nodes.

 
    """

    if neifile==None:
        print 'find_land_nodes requires a neifile dictionary.'
        return

    idx=np.where(neifile['bcode']!=0)[0]
    idx2=np.where(neifile['neighbours'][idx]!=0)
    y=np.histogram(idx[idx2[0]],bins=neifile['nnodes'])

    nodes=np.where(y[0]==2)[0]+1

    return nodes


def savenei(neifilename=None,neifile=None):
    """
    Loads a .nei file and returns the data as a dictionary.

 
    """
    
    if neifilename==None:
        print 'savenei requires a filename to save.'
        return
    try:
        fp=open(neifilename,'w')
    except IOError:
        print 'Can''t make ' + neifilename
        return

    if neifile==None:
        print 'No neifile dict given.'
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
        print 'Need proper data structure'
        return
    if elenum==None:
        print 'Need to specify an element'
        return
    
    a=data['nodell'][data['nv'][elenum,0],]
    b=data['nodell'][data['nv'][elenum,1],]
    c=data['nodell'][data['nv'][elenum,2],]

    return np.max(sp.spatial.distance.pdist(np.array([a,b,c])))


def fvcom_savecage(filename=None,nodes=None,drag=None,depth=None):
    """
    Saves a fvcom cage file.

 
    """
    #Check for filename and open, catch expection if it can't create file.
    if filename==None:
        print 'fvcom_savecage requires a filename to save.'
        return
    try:
        fp=open(filename,'w')
    except IOError:
        print 'Can''t make ' + filename
        return

    #Make sure all arrays were given
    if ((nodes==None) or (drag==None) or (depth==None)):
        print 'Need to gives arrays of nodes,drag, and depth.'
        fp.close()
        return
    #Make sure they are all the same size
    if ((nodes.size!=drag.size) or (nodes.size!=depth.size)):
        print 'Arrays are not the same size.'
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

    centerele=np.argsort((data['uvnodell'][:,1]-(region['region'][3]+region['region'][2])/2)**2+(data['uvnodell'][:,0]-(region['region'][1]+region['region'][0])/2)**2)
    xhalf=0.75*np.fabs(region['region'][1]-region['region'][0])*112200
    yhalf=0.75*np.fabs(region['region'][3]-region['region'][2])*112200

    #xmultiplier=np.floor(np.fabs(xhalf*2)/spacing)
    #ymultiplier=np.floor(np.fabs(yhalf*2)/spacing)    

    XI=np.arange((data['uvnode'][centerele[1],0]-xhalf),(data['uvnode'][centerele[1],0]+xhalf),spacing)
    YI=np.arange((data['uvnode'][centerele[1],1]-yhalf),(data['uvnode'][centerele[1],1]+yhalf),spacing)

    xv,yv=np.meshgrid(XI,YI)
    xytrigrid = mplt.Triangulation(data['x'], data['y'],data['nv'])
    host=xytrigrid.get_trifinder().__call__(xv.reshape(-1,1),yv.reshape(-1,1))

    idx=get_elements(data,region)

    common=np.in1d(host,idx)

    return np.unique(host[common].flatten())



def regionll2xy(data,region):
    """
    Take an FVCOM data dictionary, a region dictionary and return a region dictionary with regionxy added which best approximates the ll region in xy.
 
    """

    left=np.argmin(np.sqrt((data['uvnodell'][:,0]-region['region'][0])**2+(data['uvnodell'][:,1]-(region['region'][2]+region['region'][3])*.5)**2))
    right=np.argmin(np.sqrt((data['uvnodell'][:,0]-region['region'][1])**2+(data['uvnodell'][:,1]-(region['region'][2]+region['region'][3])*.5)**2))
    
    top=np.argmin(np.sqrt((data['uvnodell'][:,1]-region['region'][3])**2+(data['uvnodell'][:,0]-(region['region'][0]+region['region'][1])*.5)**2))
    bottom=np.argmin(np.sqrt((data['uvnodell'][:,1]-region['region'][2])**2+(data['uvnodell'][:,0]-(region['region'][0]+region['region'][1])*.5)**2))

    region['regionxy']=[data['uvnode'][left,0],data['uvnode'][right,0],data['uvnode'][bottom,1],data['uvnode'][top,1]]


    return region






def regioner(data,region,subset=False):
    #subset code not finished yet

    if subset==True:    
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

        data['trigrid'] = mplt.Triangulation(data['lon'][nidx_uni], data['lat'][nidx_uni],nv_new)
        data['nidx_sub']=nidx_uni
        data['eidx_sub']=eidx

        #for key in data.keys():
        #    try:
        #        np.where((np.ravel(data[key].shape)==209890)==1)[0]
        #    except AttributeError:
        #        pass

        data['zeta']=data['zeta'][:,nidx_uni]
        data['ua']=data['ua'][:,eidx]
        data['va']=data['va'][:,eidx]
        data['u']=data['u'][:,:,eidx]
        data['v']=data['v'][:,:,eidx]
        data['ww']=data['ww'][:,:,eidx]


        return data

    else:
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
        data['eidx_sub']=eidx

        return data



@profile
def interp_vel(data,loc,layer=None):
    host=data['trigrid_finder'].__call__(loc[0],loc[1])
    if host==-1:
        print 'Point at: (' + ('%f'%loc[0]) + ', ' +('%f'%loc[1]) + ') is external to the grid.'
        out=np.empty(shape=data['va'][:,0].shape)
        out[:]=np.nan
        return out,out

    xi=loc[0]
    yi=loc[1]
    interp_x = mpl.tri.LinearTriInterpolator(data['trigrid'], data['nodexy'][:,0])
    interp_y = mpl.tri.LinearTriInterpolator(data['trigrid'], data['nodexy'][:,1])
    loc[0] = interp_x(xi, yi)
    loc[1] = interp_y(xi, yi)

    if layer==None:
        x0c=loc[0]-data['uvnode'][host,0];
        y0c=loc[1]-data['uvnode'][host,0];  
        e0=data['nbe'][host,0]
        e1=data['nbe'][host,1]
        e2=data['nbe'][host,2]
        
        u_e=data['ua'][:,host]
        v_e=data['va'][:,host]

        if e0==-1:
            u_0=np.zeros(shape=u_e.shape,dtype=u_e.dtype)
            v_0=np.zeros(shape=u_e.shape,dtype=u_e.dtype)
        else:
            u_0=data['ua'][:,e0]
            v_0=data['va'][:,e0]

        if e1==-1:
            u_1=np.zeros(shape=u_e.shape,dtype=u_e.dtype)
            v_1=np.zeros(shape=u_e.shape,dtype=u_e.dtype)
        else:
            u_1=data['ua'][:,e1]
            v_1=data['va'][:,e1]

        if e2==-1:
            u_2=np.zeros(shape=u_e.shape,dtype=u_e.dtype)
            v_2=np.zeros(shape=u_e.shape,dtype=u_e.dtype)
        else:
            u_2=data['ua'][:,e2]
            v_2=data['va'][:,e2]

        dudx= data['a1u'][0,host]*u_e+data['a1u'][1,host]*u_0+data['a1u'][2,host]*u_1+data['a1u'][3,host]*u_2;
        dudy= data['a2u'][0,host]*u_e+data['a2u'][1,host]*u_0+data['a2u'][2,host]*u_1+data['a2u'][3,host]*u_2;
        dvdx= data['a1u'][0,host]*v_e+data['a1u'][1,host]*v_0+data['a1u'][2,host]*v_1+data['a1u'][3,host]*v_2;
        dvdy= data['a2u'][0,host]*v_e+data['a2u'][1,host]*v_0+data['a2u'][2,host]*v_1+data['a2u'][3,host]*v_2;

        ua= u_e + dudx*x0c + dudy*y0c;
        va= v_e + dvdx*x0c + dvdy*y0c;

    else:
        print testing
        





    return ua,va















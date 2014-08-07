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

def regions(regionname=None):
    """Returns region locations and full names

    :Parameters:
    	regionname

 
    """

    allregions=makeregions()

    if regionname==None:
        print 'Valid regions are'
        print allregions.keys()        
    else:
        return allregions[regionname]


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
    xhalf=0.5*np.fabs(region['region'][1]-region['region'][0])*112200
    yhalf=0.5*np.fabs(region['region'][3]-region['region'][2])*112200

    #xmultiplier=np.floor(np.fabs(xhalf*2)/spacing)
    #ymultiplier=np.floor(np.fabs(yhalf*2)/spacing)    

    XI=np.arange((data['uvnode'][centerele[1],0]-xhalf),(data['uvnode'][centerele[1],0]+xhalf),spacing)
    YI=np.arange((data['uvnode'][centerele[1],1]-yhalf),(data['uvnode'][centerele[1],1]+yhalf),spacing)

    xv,yv=np.meshgrid(XI,YI)
    xytrigrid = mplt.Triangulation(data['x'], data['y'],data['nv'])
    host=xytrigrid.get_trifinder().__call__(xv.reshape(-1,1),yv.reshape(-1,1))

    idx=get_elements(data,region)

    common=np.in1d(host,idx)

    return host[common]





































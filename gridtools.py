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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)

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

    nnodes=int(fp.readline())
    maxnei=int(fp.readline())
    llminmax=np.genfromtxt(StringIO(fp.readline()))
    t_data=np.loadtxt(neifilename,skiprows=3)
    fp.close()

    neifile={}

    neifile['nnodes']=nnodes
    neifile['maxnei']=maxnei
    neifile['llminmax']=llminmax

    neifile['nodell']=t_data[:,1:3]
    neifile['bcode']=t_data[:,3]
    neifile['h']=t_data[:,4]
    neifile['neighbours']=t_data[:,5:-1]
    
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



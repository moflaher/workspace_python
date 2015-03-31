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
from gridtools import *
from regions import makeregions
np.set_printoptions(precision=16,suppress=True,threshold=np.nan)



def runstats(datain=None):
    """Takes an array and returns basic stats on it. Max,Min,Mean,Std

    :Parameters:
    

 
    """

   

    if datain==None:
        print 'Need to pass in data array'  
    else:
        maxval=np.max(datain)
        minval=np.min(datain)
        meanval=np.mean(datain)
        stdval=np.std(datain)

        return maxval,minval,meanval,stdval



def ne_fv(casename,h=False,is31=False):
    
    depdata=load_nodfile(casename+'.nod',h)
    grddata=load_elefile(casename+'.ele')
    save_grdfile(grddata,depdata,casename+'_grd.dat',is31)
    save_depfile(depdata,casename+'_dep.dat',is31)



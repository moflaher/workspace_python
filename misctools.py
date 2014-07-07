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
    """Takes an array and returns basic stats on it. Min,Max,Mean,Std

    :Parameters:
    

 
    """

   

    if datain==None:
        print 'Need to pass data an array'  
    else:
        maxval=np.max(datain)
        minval=np.min(datain)
        meanval=np.mean(datain)
        stdval=np.std(datain)

        return maxval,minval,meanval,stdval

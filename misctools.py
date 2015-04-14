from __future__ import division
import numpy as np
import matplotlib as mpl
import scipy as sp
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
from StringIO import StringIO
import gridtools as gt
import datatools as dt
import plottools as pt
np.set_printoptions(precision=16,suppress=True,threshold=np.nan)
import pandas as pd


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
    
    depdata=gt.load_nodfile(casename+'.nod',h)
    grddata=gt.load_elefile(casename+'.ele')
    gt.save_grdfile(grddata,depdata,casename+'_grd.dat',is31)
    gt.save_depfile(depdata,casename+'_dep.dat',is31)


def dic_shape(indic):
    df=pd.DataFrame([str(np.shape(indic[key])) for key in indic.keys()],indic.keys())
    print df

















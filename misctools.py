from __future__ import division
import numpy as np
import matplotlib as mpl
import scipy as sp
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
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
        print('Need to pass in data array')
    else:
        maxval=np.nanmax(datain)
        minval=np.nanmin(datain)
        meanval=np.nanmean(datain)
        stdval=np.nanstd(datain)
        np.sum(np.isnan(datain))

        return maxval,minval,meanval,stdval,np.sum(np.isnan(datain))/np.size(datain)


def ne_fv(casename,h=False,is31=False):    
    depdata=gt.load_nodfile(casename+'.nod',h)
    grddata=gt.load_elefile(casename+'.ele')
    gt.save_grdfile(grddata,depdata,casename+'_grd.dat',is31)
    gt.save_depfile(depdata,casename+'_dep.dat',is31)


def dic_shape(indic):
    df=pd.DataFrame([str(np.shape(indic[key])) for key in indic.keys()],indic.keys())
    print(df)


def speeder(ua,va):
    return np.sqrt(ua**2+va**2)

def myprint(d):
  """
    Print nested dictionaries in a readable manner.
    Code from Stack overflow - Scharron
    
  """  
    
  for k, v in d.iteritems():
    if isinstance(v, dict):
      myprint(v)
    else:
      print("{0} : {1}".format(k, v))



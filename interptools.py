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

A bunch of functions dealing with fvcom interpolation.

Requirements
===================================
Absolutely Necessary:


Optional, but recommended:


Functions
=========

            
"""

def interpE_at_loc(data,varname,loc,layer=None,ll=True):
    loc=np.array(loc)
    host=data['trigrid_finder'].__call__(loc[0],loc[1])
    if host==-1:
        print 'Point at: (' + ('%f'%loc[0]) + ', ' +('%f'%loc[1]) + ') is external to the grid.'
        out=np.empty(shape=data['va'][:,0].shape)
        out[:]=np.nan
        return out,out

    #code for ll adapted from mod_utils.F
    if ll==True:
        TPI=111194.92664455874
        y0c = TPI * (loc[1] - data['uvnodell'][host,1])
        dx_sph = loc[0] - data['uvnodell'][host,0]
        if (dx_sph > 180.0):
            dx_sph=dx_sph-360.0
        elif (dx_sph < -180.0):
            dx_sph =dx_sph+360.0
        x0c = TPI * np.cos(np.deg2rad(loc[1] + data['uvnodell'][host,1])*0.5) * dx_sph
    else:       
        x0c=loc[0]-data['uvnode'][host,0]
        y0c=loc[1]-data['uvnode'][host,1] 

    e0=data['nbe'][host,0]
    e1=data['nbe'][host,1]
    e2=data['nbe'][host,2]

    if (layer==None and loc.size==2):
        var_e=data[varname][:,host]  

        if e0==-1:
            var_0=np.zeros(shape=var_e.shape,dtype=var_e.dtype)
        else:
            var_0=data[varname][:,e0]

        if e1==-1:
            var_1=np.zeros(shape=var_e.shape,dtype=var_e.dtype)
        else:
            var_1=data[varname][:,e1]

        if e2==-1:
            var_2=np.zeros(shape=var_e.shape,dtype=var_e.dtype)
        else:
            var_2=data[varname][:,e2]



    if (layer!=None and loc.size==2):        
        var_e=data[varname][:,layer,host]

        if e0==-1:
            var_0=np.zeros(shape=var_e.shape,dtype=var_e.dtype)
        else:
            var_0=data[varname][:,layer,e0]

        if e1==-1:
            var_1=np.zeros(shape=var_e.shape,dtype=var_e.dtype)
        else:
            var_1=data[varname][:,layer,e1]

        if e2==-1:
            var_2=np.zeros(shape=var_e.shape,dtype=var_e.dtype)
        else:
            var_2=data[varname][:,layer,e2]



    dvardx= data['a1u'][0,host]*var_e+data['a1u'][1,host]*var_0+data['a1u'][2,host]*var_1+data['a1u'][3,host]*var_2;
    dvardy= data['a2u'][0,host]*var_e+data['a2u'][1,host]*var_0+data['a2u'][2,host]*var_1+data['a2u'][3,host]*var_2;

    var= var_e + dvardx*x0c + dvardy*y0c;
        
    return var


   
    






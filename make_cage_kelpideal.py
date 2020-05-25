from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
import netCDF4 as n4
import scipy.interpolate as interp
from gridtools import _load_nc
import copy


# Define names and types of data
casename='kelpchannel'
filename='kelpchannel.nei'
filepath='data/kelp_ideal/xy_6/makerun/kelpchannel_clean/input/'

#load grid
neifile=loadnei(filepath+filename)
neifile=get_nv(neifile)

#convert grid to xy using the projection in make_channel2.py
projstr='lcc +lon_0=2 +lat_0=2.0 +lat_1=1 +lat_2=3'
proj=pyp.Proj(proj=projstr)
neifile['x'],neifile['y']=proj(neifile['lon'],neifile['lat'])
neifile=ncdatasort(neifile)


#define cage region (square)
region={}
region['region']=np.array([-250,250,-25,25])
#find the elements
eidx=get_elements_xy(neifile,region)
print(len(eidx))
fvcom_savecage('data/kelp_ideal/xy_6/makerun/kelpchannel_cage_500x50.dat',(eidx+1).astype(int),np.zeros(shape=eidx.shape)+0.018,np.zeros(shape=eidx.shape)+20)



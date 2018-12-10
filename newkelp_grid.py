# -*- coding: utf-8 -*-
"""
Front Matter
=============

Created on 

Author: Mitchell O'Flaherty-Sproul

Requirements
===================================
Absolutely Necessary:

* Numpy
* SciPy
* Matplotlib 


Optional, but recommended:

Functions
=========
"""
#load modules
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from math import pi
from datatools import *
from gridtools import *
from misctools import *
import scipy as sp
import matplotlib as mpl
np.set_printoptions(precision=16,suppress=True,threshold=np.nan)
import sys

import h5py as h5
import spectral.io.envi as envi




# Define names and types of data
name='kit4_kelp_newbathy_test'
grid='kit4_kelp'
#name='kit4_45days_3'
#grid='kit4'
regionname='kit4_4island'

starttime=0
plotspeed=False


### load the .nc file #####
data = loadnc('runs/' +grid+'/' + name + '/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data,trifinder=True)
print('done sort')







img=envi.open('data/kelp_data/NDVI_1999-2013_autumn-mean.hdr','data/kelp_data/NDVI_1999-2013_autumn-mean.img')


A=np.squeeze(img[:,:]).T




startx=432105
starty=5928375





Asize=A.shape

print Asize


x=np.linspace(startx,startx+Asize[0]*30,Asize[0],dtype=int,endpoint=False)
y=np.linspace(starty,starty-Asize[1]*30,Asize[1],dtype=int,endpoint=False)

xx,yy=np.meshgrid(x,y)

np.savetxt('data/kelp_data/newkelp_xy.dat',np.vstack([xx.flatten(),yy.flatten()]).T,fmt='%12.12f %12.12f')










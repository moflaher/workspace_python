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
import scipy as sp
import matplotlib as mpl
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import sys






data = loadnc('/media/moflaher/My Book/kitimat3_runs/kitimat3_56_0.25_45day/output/')
data=ncdatasort(data)

tempdic={}

tempdic['trigrid']=data['nv']+1
tempdic['lon']=data['lon']
tempdic['lat']=data['lat']
tempdic['lonc']=data['uvnodell'][:,0]
tempdic['latc']=data['uvnodell'][:,1]
tempdic['h']=data['h']
tempdic['hc']= (data['h'][data['nv'][:,0]] + data['h'][data['nv'][:,1]] + data['h'][data['nv'][:,2]]) / 3.0


sio.savemat('kitgrid.mat',mdict=tempdic)



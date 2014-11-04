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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import sys




infile='data/oil_locations_sdl050'

tempdic={}
sio.loadmat(infile+'.mat',mdict=tempdic)
np.savetxt(infile+'.dat',np.hstack([tempdic['lonmap'],tempdic['latmap']]),fmt='%12.12f %12.12f')




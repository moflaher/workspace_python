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







xyz=np.genfromtxt('kit4.xyz')
savepath='figures/png/kitimat4/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)





plt.scatter(xyz[:,0],xyz[:,1],c=xyz[:,2], lw = 0,s=.5)
#plt.colorbar()
plt.grid()
plt.title('Scatter plot of kit4 grid/depth')
plt.savefig(savepath + 'kit4_scatter_depth.png',dpi=600)
plt.close()


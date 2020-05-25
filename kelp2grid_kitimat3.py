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
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
import sys






data = loadnc('/media/moflaher/My Book/kitimat3_runs/kitimat3_56_0.25_45day/output/')
kelp=np.genfromtxt('kelplocations.dat')
savepath='figures/png/kitimat3/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)

host=data['trigrid'].get_trifinder().__call__(kelp[:,0],kelp[:,1])
host=np.unique(host)
host=host[host !=-1]

np.savetxt('kelptriangles.dat',host+1,fmt='%i')

trihost=np.zeros([data['nv'].shape[0],])
trihost[host]=1


plt.tripcolor(data['trigrid'],trihost)
plt.colorbar()
plt.grid()
plt.title('Locations with kelp')
plt.savefig(savepath + 'kelp_host_locations.png',dpi=1200)
plt.close()


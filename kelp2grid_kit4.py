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






data = loadnc('/media/moflaher/My Book/kit4/kit4_45days_3/output/')
data =ncdatasort(data)
kelp=np.genfromtxt('kelplocations.dat')

maxdepth=20
mindepth=5


savepath='figures/png/kit4/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)

host=data['trigrid'].get_trifinder().__call__(kelp[:,0],kelp[:,1])
#host=np.unique(host)
#host=host[host !=-1]

newhost=host


    
        
newhost=np.unique(newhost)
newhost=newhost[newhost !=-1]     

host_lt_depth=np.where((data['uvh'][newhost]<=maxdepth) & (data['uvh'][newhost]>=mindepth))[0]
newhostbool=np.zeros(shape=newhost.shape,dtype=bool)
newhostbool[host_lt_depth]=True

newhost=newhost[host_lt_depth.flatten()]

tempdic={}
tempdic['kelp_elements']=newhost
sio.savemat('kelp_elements_kit4.mat',mdict=tempdic)


np.savetxt('kelpnodes_kit4.dat',newhost+1,fmt='%i')

drag=np.zeros([newhost.shape[0],])+0.018
depth=np.zeros([newhost.shape[0],])+40

fvcom_savecage('kit4_cage.dat',newhost+1,drag,depth)

trihost=np.zeros([data['uvnodell'].shape[0],])
trihost[newhost]=1

plt.close()
plt.tripcolor(data['trigrid'],trihost)
plt.colorbar()
plt.grid()
plt.title('Locations with kelp')
plt.savefig(savepath + 'kelp_host_locations.png',dpi=1200)
plt.close()


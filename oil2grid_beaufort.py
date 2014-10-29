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




# Define names and types of data
name='try16'
grid='beaufort3'
datatype='2d'
regionname='beaufort3'



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)

cages=sio.loadmat('oil_locations.mat')

cageloc=np.hstack([cages['lonmap'],cages['latmap']])

#region=regions('musq')

savepath='figures/png/beaufort3/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)




host=data['trigrid'].get_trifinder().__call__(cageloc[:,0],cageloc[:,1])


newhost=host


    
        
newhost=np.unique(newhost)
newhost=newhost[newhost !=-1]     

#host_lt_depth=data['uvh'][newhost]<depth



#newhost=newhost[host_lt_depth.flatten()]

tempdic={}
tempdic['cage_elements']=newhost+1
sio.savemat('oil_elements_beaufort3.mat',mdict=tempdic)


np.savetxt('oil_elements_beaufort3.dat',newhost+1,fmt='%i')

#drag=np.zeros([newhost.shape[0],])+0.6
#depth=np.zeros([newhost.shape[0],])+10

#fvcom_savecage('sfm6_musq2_cage.dat',newhost+1,drag,depth)

trihost=np.zeros([data['uvnodell'].shape[0],])
trihost[newhost]=1

plt.close()
plt.tripcolor(data['trigrid'],trihost)
plt.triplot(data['trigrid'],lw=.2)
plt.colorbar()
plt.grid()
#plt.axis([-66.925, -66.8,45.0,45.075])
plt.title('Locations with oil')
plt.savefig(savepath + 'oil_locations.png',dpi=2400)
plt.close()


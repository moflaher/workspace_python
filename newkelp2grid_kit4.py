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

import h5py as h5
import spectral.io.envi as envi




# Define names and types of data
name='kit4_kelp_newbathy_test'
grid='kit4_kelp'
#name='kit4_45days_3'
#grid='kit4'
regionname='kit4_4island'
datatype='2d'
starttime=0
plotspeed=False


### load the .nc file #####
data = loadnc('runs/' +grid+'/' + name + '/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data,trifinder=True)
print 'done sort'




fileload=h5.File('data/kelp_data/latlon_WGS84.mat')
fileload.keys()
newkelp={}
for i in fileload.keys():
    newkelp[i]=fileload[i].value





img=envi.open('data/kelp_data/NDVI_LatLong/NDVI_1999-2013_autumn-mean_LL.hdr','data/kelp_data/NDVI_LatLong/NDVI_1999-2013_autumn-mean_LL.img')


A=np.squeeze(img[:,:]).T

#newkelp['A']=np.flipud(newkelp['A'])
A=np.fliplr(A)


idx=A>=0.15
lon=newkelp['lon'][idx]
lat=newkelp['lat'][idx]


plt.tripcolor(data['trigrid'],trihost)
plt.colorbar()
plt.grid()
plt.scatter(lon+0.00044685879,lat+.00026957498,s=10,c=A[idx],edgecolor='None')
plt.colorbar()
plt.show()



kelp=np.vstack([lon,lat]).T



maxdepth=20
mindepth=0


savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)

region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)


host=data['trigrid_finder'].__call__(kelp[:,0],kelp[:,1])
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
#sio.savemat('kelp_elements_kit4.mat',mdict=tempdic)


np.savetxt('data/grid_stuff/kelpnodes_'+grid+'.dat',newhost+1,fmt='%i')

drag=np.zeros([newhost.shape[0],])+0.018
depth=np.zeros([newhost.shape[0],])+40

fvcom_savecage('data/cage_files/'+grid+'_cage_'+("%d"%mindepth)+'m_'+("%d"%maxdepth)+'m.dat',newhost+1,drag,depth)

trihost=np.zeros([data['uvnodell'].shape[0],])
trihost[newhost]=1

plt.close()
plt.tripcolor(data['trigrid'],trihost)
plt.colorbar()
plt.grid()
plt.axis(region['region'])
plt.title('Locations with kelp')
plt.savefig(savepath +grid+'_'+regionname+ '_newkelp_host_locations.png',dpi=1200)
plt.close()


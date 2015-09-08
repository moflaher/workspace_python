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
datatype='2d'
starttime=0
plotspeed=False


### load the .nc file #####
data = loadnc('runs/' +grid+'/' + name + '/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data,trifinder=True)
print('done sort')



maxdepth=20
mindepth=0


savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)

region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)





ll=np.loadtxt('data/kelp_data/newkelp_ll_nad.dat')
np.save('data/kelp_data/newkelp_ll_nad.npy',ll)

ll=np.load('data/kelp_data/newkelp_ll_nad.npy')

img=envi.open('data/kelp_data/NDVI_1999-2013_winter-mean.hdr','data/kelp_data/NDVI_1999-2013_winter-mean.img')

#img2=envi.open('data/kelp_data/NDVI_1999-2013_summer-mean.hdr','data/kelp_data/NDVI_1999-2013_summer-mean.img')
#A2=(np.squeeze(img2[:,:]).T)
#indata = np.genfromtxt('data/kelp_data/NDVI_1999-2013_summer-mean_LL.txt',skip_header=5)
#A=indata[:,2]

A=(np.squeeze(img[:,:]).T)
lonin=ll[:,0]
latin=ll[:,1]

lonin2=lonin.reshape(A.T.shape).T
latin2=latin.reshape(A.T.shape).T

#lonin2=indata[:,0]
#latin2=indata[:,1]

idx=A<-.15
lon=lonin2[idx]
lat=latin2[idx]
Ain=A[idx]

idx2=np.where((lon>region['region'][0]) & (lon<region['region'][1]) & (lat>region['region'][2]) & (lat<region['region'][3]) )

lon2=lon[idx2]
lat2=lat[idx2]
A2=Ain[idx2]


#bc=np.loadtxt('data/kelp_data/bc_coastline.txt')

plt.triplot(data['trigrid'],lw=.25)
#plt.colorbar()
plt.grid()
scax=plt.scatter(lon2,lat2,s=10,c=A2,edgecolor='None')
#plt.scatter(bc[:,0],bc[:,1],s=20,c='y')
#plt.scatter(lon2+0.0004468575527881*2,lat2+0.0002695749834487/2,s=10,c=A2,edgecolor='None')
#plt.scatter(lon,lat,s=10,edgecolor='None')
plt.colorbar(scax)
plt.axis(region['region'])
plt.show()
kill

kelp=np.vstack([lon,lat]).T





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


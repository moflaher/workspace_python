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
name='kit4_kelp_newbathy_test'
grid='kit4_kelp'
regionname='kit4_4island'
datatype='2d'
starttime=0
plotspeed=False


### load the .nc file #####
data = loadnc('runs/' +grid+'/' + name + '/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data,trifinder=True)
print 'done sort'

kelp=np.genfromtxt('kelplocations.dat')

yd=.0004499640029
xd=.0007168554972
spacing=8
multi=4

nkx=np.empty((len(kelp)*spacing**2,))
nky=np.empty((len(kelp)*spacing**2,))

for i in range(0,len(kelp)):
    xi=np.linspace(kelp[i,0]-xd*multi, kelp[i,0]+xd*multi, spacing)
    yi=np.linspace(kelp[i,1]-yd*multi, kelp[i,1]+yd*multi, spacing)
    XI,YI=np.meshgrid(xi,yi)
    nkx[((i)*spacing**2):((i+1)*spacing**2)]=XI.flatten()
    nky[((i)*spacing**2):((i+1)*spacing**2)]=YI.flatten()  
    

kelpold=kelp.copy()
kelp=np.vstack([nkx,nky]).T


maxdepth=20
mindepth=5


savepath='figures/png/' + grid + '_' + datatype + '/fakekelp/'
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
plt.title('Locations with kelp')
plt.savefig(savepath +grid+'_kelp_host_locations_2_spacing_'+("%d"%spacing)+'_multi_'+("%d"%multi)+'.png',dpi=1200)
plt.axis(region['region'])
plt.savefig(savepath +grid+'_'+regionname+ '_kelp_host_locations_2_spacing_'+("%d"%spacing)+'_multi_'+("%d"%multi)+'.png',dpi=1200)
plt.close()


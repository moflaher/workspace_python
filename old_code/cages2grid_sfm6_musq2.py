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
from plottools import *
from projtools import *
import scipy as sp
import matplotlib as mpl
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import sys






data = loadnc('runs/sfm6_musq2/sfm6_musq2_all_cages/output/',singlename='sfm6_musq2_0001.nc')
data =ncdatasort(data)
cages=np.load('data/misc/fishcage/farmlocations.npy')
cages=cages[()]

cageloc=np.vstack([cages['lon'],cages['lat']]).T


savepath='figures/png/sfm6_musq2/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)




host=data['trigrid'].get_trifinder().__call__(cageloc[:,0],cageloc[:,1])


newhost=host


    
        
newhost=np.unique(newhost)
newhost=newhost[newhost !=-1]     

#host_lt_depth=data['uvh'][newhost]<depth



#newhost=newhost[host_lt_depth.flatten()]

tempdic={}
tempdic['cage_elements']=newhost+1
sio.savemat('data/misc/fishcage/cage_elements_sfm6_musq2.mat',mdict=tempdic)


np.savetxt('data/misc/fishcage/cage_elements_sfm6_musq2.dat',newhost+1,fmt='%i')

drag=np.zeros([newhost.shape[0],])+0.6
depth=np.zeros([newhost.shape[0],])+10

fvcom_savecage('data/misc/fishcage/sfm6_musq2_cage.dat',newhost+1,drag,depth)

trihost=np.zeros([data['uvnodell'].shape[0],])
trihost[newhost]=1

f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
triax=plt.tripcolor(data['trigrid'],trihost)
ax.triplot(data['trigrid'],lw=.2)
region={}
region['region']=np.array([-66.925, -66.8,45.0,45.075])
prettyplot_ll(ax,setregion=region,grid=True)
plt.title('Locations with cages')

#eidx=get_elements(data,region)
#for ele in eidx:
    #ax.text(data['uvnodell'][ele,0],data['uvnodell'][ele,1],"{}".format(ele+1))

f.savefig(savepath + 'cage_host_locations_new.png',dpi=2400)
plt.close(f)


remove=np.array([7090,7210,7209,6970,7211,19545,16462,25848,25889,25887,25886,
            24865,24867,24863,24864,24861,23829,23826,22850,22848,22851,
            23828,23830,23833,23814,22832,22829])
            
add=np.array([18808,19495])

for val in remove:
    idx=np.argwhere(val==(newhost+1))
    newhost=np.delete(newhost,idx)
    
    
newhost=np.append(newhost,add-1)
    
drag=np.zeros([newhost.shape[0],])+0.6
depth=np.zeros([newhost.shape[0],])+10
fvcom_savecage('data/misc/fishcage/sfm6_musq2_cage_manual.dat',newhost+1,drag,depth)

trihost=np.zeros([data['uvnodell'].shape[0],])
trihost[newhost]=1


f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
triax=plt.tripcolor(data['trigrid'],trihost)
ax.triplot(data['trigrid'],lw=.2)
region={}
region['region']=np.array([-66.925, -66.8,45.0,45.075])
prettyplot_ll(ax,setregion=region,grid=True)
plt.title('Locations with cages')

#eidx=get_elements(data,region)
#for ele in eidx:
    #ax.text(data['uvnodell'][ele,0],data['uvnodell'][ele,1],"{}".format(ele+1))

f.savefig(savepath + 'cage_host_locations_new_manual.png',dpi=2400)
plt.close(f)










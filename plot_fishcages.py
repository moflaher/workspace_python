from __future__ import division
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import scipy.io as sio
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
from StringIO import StringIO
from gridtools import *
from datatools import *
from misctools import *
from plottools import *
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)

from scipy.spatial import ConvexHull



# Define names and types of data
name='sfm6_musq2_old_cages'
grid='sfm6_musq2'
regionname='musq_cage'
datatype='2d'


### load the .nc file #####
data = loadnc('/media/moflaher/My Book/cages/' + name + '/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

cages=np.genfromtxt('/media/moflaher/My Book/cages/' +name+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)


region=regions(regionname)
savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)

ncages=np.unique(data['nv'][cages,:])



cv=ConvexHull(data['nodell'][ncages,:])

trueidx=ncages[cv.vertices]


plt.close()
plt=prettyplot_ll(plt,setregion=region,grid=True)
plt.triplot(data['trigrid'],color='black',lw=.1,label='Mesh')
for i in cages:
    tnodes=data['nv'][i,:]    
    plt.plot(data['nodell'][tnodes[[0,1]],0],data['nodell'][tnodes[[0,1]],1],'r',lw=.4,label='Cage')
    plt.plot(data['nodell'][tnodes[[1,2]],0],data['nodell'][tnodes[[1,2]],1],'r',lw=.4,label='Cage')
    plt.plot(data['nodell'][tnodes[[0,2]],0],data['nodell'][tnodes[[0,2]],1],'r',lw=.4,label='Cage')

handles, labels = plt.gca().get_legend_handles_labels()
handles=handles[::-1]
labels=labels[::-1]
legend=plt.legend(handles[1:3], labels[0:2])

t=legend.get_lines()
t[0].set_color('black')

for label in legend.get_lines():
    label.set_linewidth(2.5)

#plt.plot(data['uvnodell'][cages,0],data['uvnodell'][cages,1],'b.',markersize=2)




plt.savefig(savepath + grid + '_' +name+ '_' + regionname +'_cage_outline.png',dpi=1200)

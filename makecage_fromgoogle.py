from __future__ import division,print_function
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
from projtools import *
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)




# Define names and types of data
name='sfm6_musq2_half_cages'
grid='sfm6_musq2'
datatype='2d'


### load the .nc file #####
data = loadnc('runs/sfm6_musq2/' + name + '/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data,trifinder=True)
print('done sort')

cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
if np.shape(cages)!=():
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2]],0],data['nodell'][data['nv'][i,[0,1,2]],1])) for i in cages ]
    color='g'

tcages=np.load('data/misc/fishcage/googlefishcage_all.npy')
tcages=tcages[()]



lseg=PC(tmparray,facecolor = 'g',edgecolor='None')

f=plt.figure()
ax=f.add_axes([.1,.125,.775,.8])
ax.triplot(data['trigrid'],lw=.25,color='k')
plotcoast(ax,filename='mid_nwatl6c.nc',color='None',fill=True)
ax.add_collection(lseg)
for key in tcages:
    ax.plot(tcages[key][:,0],tcages[key][:,1],'r')

f.show()

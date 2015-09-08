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
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)




# Define names and types of data
name='kit4_kelp_0.05'
grid='kit4'
datatype='2d'
regionname='kelparea'

region=regions(regionname)
regionf=[.1,.11,.85,.85]


### load the .nc file #####
data = loadnc('/media/moe46/My Passport/kit4_runs/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

cages=np.genfromtxt('/media/moe46/My Passport/kit4_runs/' +name+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)








savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)

#create plot and plot whole sfm grid with contours (make it look like jasons gmt)
f=plt.figure()
ax01=plt.axes(regionf)

ax01.triplot(data['trigrid'],color='black',lw=.1)
ax01.axis(region['region'])
prettyplot_ll(ax01,setregion=region,grid=True)

for i in cages:
    tnodes=data['nv'][i,:]    
    ax01.plot(data['nodell'][tnodes[[0,1]],0],data['nodell'][tnodes[[0,1]],1],'r',lw=.6,label='Mesh')
    ax01.plot(data['nodell'][tnodes[[1,2]],0],data['nodell'][tnodes[[1,2]],1],'r',lw=.6,label='Cages')
    ax01.plot(data['nodell'][tnodes[[0,2]],0],data['nodell'][tnodes[[0,2]],1],'r',lw=.6,label='Single Cage')










plt.savefig(savepath + grid + '_' +name+ '_'+regionname+'_mesh_and_cage_outline.png',dpi=600)


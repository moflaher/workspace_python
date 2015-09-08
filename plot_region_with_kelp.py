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
namek='kit4_kelp_0.1'
name='kit4_45days_3'
grid='kit4'
regionname='kelparea'
datatype='2d'


### load the .nc file #####
data = loadnc('/media/moflaher/My Book/kit4_runs/' + name + '/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

cages=np.genfromtxt('/media/moflaher/My Book/kit4_runs/' +namek+ '/input/kit4_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)


region=regions(regionname)
savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)


plt.close()
plt.triplot(data['trigrid'],lw=.1)
plt=prettyplot_ll(plt,setregion=region,grid=True)
plt.plot(data['uvnodell'][cages,0],data['uvnodell'][cages,1],'r.',markersize=2)



plt.savefig(savepath + grid + '_' + regionname +'_with_kelp.png',dpi=1200)

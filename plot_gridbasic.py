from __future__ import division
import numpy as np
import matplotlib as mpl
import scipy as sp
from datatools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os


### load a timeslice from an .nc file #####
data = loadnc('/media/moflaher/My Book/kit4_runs/kitimat4_clean/output/',singlename='kit4_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

grid='kit4'





savepath='figures/png/' + grid + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)

#### Spatial plots

plt.close()
plt.tripcolor(data['trigrid'],np.zeros([len(data['nv']),1]))
plt.grid()
plt.title(grid + ' Grid')
plt.savefig(savepath + grid +'_grid.png',dpi=600)
plt.close()




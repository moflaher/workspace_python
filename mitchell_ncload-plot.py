from __future__ import division
import numpy as np
from datatools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os

### load a timeslice from an .nc file #####
data1 = load_timeslice('/home/moflaher/workspace_matlab/runs/beaufort3/3d/try16/output/',0,100,singlename='beaufort3_0001.nc',dim='3D')
print 'done load'
data1 = ncdatasort(data1)
print 'done sort'

#### Grand passage region #####
#data1 = regioner([-66.320543,-66.360025,44.242371,44.290312],data1,dim='3D')

#load quantities
time,ua,va,el = data1['time'],data1['ua'],data1['va'],data1['zeta']


#Calculate total speed
speed = np.sqrt(ua**2+va**2)



#### Spatial plots
for i in xrange(speed.shape[0]):
    #plt.gca().set_aspect('equal')
    grid = data1['trigrid']
    plt.tripcolor(grid,speed[i,:],vmin=0,vmax=0.6)
    plt.colorbar()
    plt.grid()
    plt.title('Velocity')
    #plt.savefig('figures/arctic/speed/speed_' + str(i) + '.png',dpi=600)
    plt.show()    
    plt.close()


for i in xrange(el.shape[0]):
	#plt.gca().set_aspect('equal')
	grid = data1['trigrid']
	plt.tripcolor(grid,el[i,:],vmin=-0.5,vmax=0.5)
	plt.colorbar()
	plt.grid()
	plt.title('Velocity')
	plt.savefig('figures/arctic/el/el_' + str(i) + '.png',dpi=600)
	plt.close()


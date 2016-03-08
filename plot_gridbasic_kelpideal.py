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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name='kelp_channel'
grid='kelp_channel'
datatype='2d'



### load the mesh files #####
data=loadnei('data/kelp_ideal/xy_4/makerun/' +name+ '.nei')
data['x'],data['y'],proj=lcc(data['lon'],data['lat'])
data=get_nv(data)
data=ncdatasort(data)
data=get_sidelength(data)
data=get_dhh(data)

savepath='figures/png/' + grid + '_' + datatype + '/gridbasic/' +name + '/'
if not os.path.exists(savepath): os.makedirs(savepath)





# Plot mesh
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
ax.triplot(data['trigridxy'],lw=.2,color='k')
ax.grid()
ax.axis('equal')
f.savefig(savepath + grid + '_' + name +'_grid.png',dpi=300)
plt.close(f)

# Plot depth
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigridxy'],data['h'])
cb=plt.colorbar(triax)
cb.set_label('Depth (m)')
ax.axis('equal')
f.savefig(savepath + grid + '_' + name +'_depth.png',dpi=600)
plt.close(f)

# Plot depth percentile
clims=np.percentile(data['h'],[5,95])
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigridxy'],data['h'],vmin=clims[0],vmax=clims[1])
cb=plt.colorbar(triax)
cb.set_label('Depth (m)')
ax.axis('equal')
f.savefig(savepath + grid + '_' + name +'_depth_percentile.png',dpi=600)
plt.close(f)


# Plot dh/h
clims=np.percentile(data['dhh'],[1,99])
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigridxy'],data['dhh'],vmin=clims[0],vmax=clims[1])
cb=plt.colorbar(triax)
cb.set_label('dhh')
ax.axis('equal')
f.savefig(savepath + grid + '_' + name +'_dhh.png',dpi=600)
plt.close(f)


# Plot sidelength
clims=np.percentile(data['sl'],[1,99])
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigridxy'],data['sl'],vmin=clims[0],vmax=clims[1])
cb=plt.colorbar(triax)
cb.set_label('Sidelength (m)')
ax.axis('equal')
f.savefig(savepath + grid + '_' + name +'_sidelength.png',dpi=600)
plt.close(f)



















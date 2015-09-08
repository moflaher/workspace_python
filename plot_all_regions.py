from __future__ import division,print_function,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'
regionlist=regions()
datatype='2d'


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

savepath='figures/png/' + grid + '_' + datatype + '/regions_all/'
if not os.path.exists(savepath): os.makedirs(savepath)
plt.close()

# Plot mesh
for i in range(0,len(regionlist)):
    regionname=regionlist[i]
    region=regions(regionname)
    nidx=get_nodes(data,region)
    if len(nidx)!=0:
        print('Printing - ' + region['regionname'])
        f=plt.figure()
        ax=plt.axes([.125,.1,.8,.8])
        ax.triplot(data['trigrid'],lw=.5)
        prettyplot_ll(ax,setregion=region,grid=True)
        f.savefig(savepath + grid + '_' + regionname +'_mesh.png',dpi=150)
        #f.savefig(savepath + grid + '_' + regionname +'_mesh.png',dpi=300)
        plt.close(f)































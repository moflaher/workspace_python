from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)


# Define names and types of data
name='kit4_kelp_20m_0.018'
grid='kit4'
regionlist=['kit4_kelp_tight3','kit4_kelp_tight4','kit4_kelp_tight5','kit4_kelp_tight6']

starttime=384
endtime=450
cmin=0
cmax=1


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')



savepath='figures/png/' + grid + '_'  + '/regions/'
if not os.path.exists(savepath): os.makedirs(savepath)
plt.close()

# Plot mesh
for i in range(0,len(regionlist)):
    print i 
    regionname=regionlist[i]
    region=regions(regionname)
    f=plt.figure()
    ax=plt.axes([.125,.1,.8,.8])
    ax.triplot(data['trigrid'],lw=.5)
    prettyplot_ll(ax,setregion=region,grid=True)
    f.savefig(savepath + grid + '_' + regionname +'_mesh.png',dpi=150)
    #f.savefig(savepath + grid + '_' + regionname +'_mesh.png',dpi=300)
    plt.close(f)































from __future__ import division
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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)



# Define names and types of data
name='kit4_kelp_0.05'
grid='kit4'
regionname='fasttip'
datatype='2d'
starttime=384
endtime=450


### load the .nc file #####
data = loadnc('/media/moe46/My Passport/kit4_runs/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'


region=regions(regionname)

savepath='figures/timeseries/' + grid + '_' + datatype + '/zeta/' + name + '_' + regionname + '/'
if not os.path.exists(savepath): os.makedirs(savepath)
plt.close()

nidx=get_nodes(data,region)

# Plot mesh
for i in range(starttime,endtime):
    print i

    f=plt.figure()
    ax=plt.axes([.1,.1,.7,.85])
    triax=ax.tripcolor(data['trigrid'],data['zeta'][i,:],vmin=data['zeta'][i,nidx].min(),vmax=data['zeta'][i,nidx].max())
    prettyplot_ll(ax,setregion=region,cblabel='Elevation (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_zeta_' + ("%04d" %(i)) + '.png',dpi=300)
    plt.close(f)































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
regionname='gilisland'
datatype='2d'
starttime=384
endtime=450
cmin=-.01
cmax=.01




### load the .nc file #####
data = loadnc('/media/moe46/My Passport/kit4_runs/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'


region=regions(regionname)

savepath='figures/timeseries/' + grid + '_' + datatype + '/curl/' + name + '_' + regionname + '_' +("%f" %cmin) + '_' + ("%f" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)
plt.close()




# Plot mesh
for i in range(starttime,endtime):
    print i
    ua=np.hstack([data['ua'][i,:],0])
    va=np.hstack([data['va'][i,:],0])
    dudy= data['a2u'][0,:]*ua[0:-1]+data['a2u'][1,:]*ua[data['nbe'][:,0]]+data['a2u'][2,:]*ua[data['nbe'][:,1]]+data['a2u'][3,:]*ua[data['nbe'][:,2]];
    dvdx= data['a1u'][0,:]*va[0:-1]+data['a1u'][1,:]*va[data['nbe'][:,0]]+data['a1u'][2,:]*va[data['nbe'][:,1]]+data['a1u'][3,:]*va[data['nbe'][:,2]];
    
    #print np.mean(dvdx-dudy)
    #print np.min(dvdx-dudy)
    #print np.max(dvdx-dudy)
    #print np.std(dvdx-dudy)
    f=plt.figure()
    ax=plt.axes([.1,.1,.7,.85])
    triax=ax.tripcolor(data['trigrid'],dvdx-dudy,vmin=cmin,vmax=cmax)
    prettyplot_ll(ax,setregion=region,cblabel='Curl',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_curl_' + ("%04d" %(i)) + '.png',dpi=600)
    plt.close(f)
































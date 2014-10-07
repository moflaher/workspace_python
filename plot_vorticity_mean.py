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
name='kit4_kelp_20m_0.018'
grid='kit4'
regionname='kit4_ftb'
datatype='2d'
starttime=384
endtime=624





### load the .nc file #####
data = loadnc('/media/moe46/My Passport/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'


region=regions(regionname)

savepath='figures/png/' + grid + '_' + datatype + '/curl/'
if not os.path.exists(savepath): os.makedirs(savepath)
plt.close()

eidx=get_elements(data,region)

curl=np.zeros((endtime-starttime,len(data['nv'])))

idx=0;
# Plot mesh
for i in range(starttime,endtime):
    print i
    ua=np.hstack([data['ua'][i,:],0])
    va=np.hstack([data['va'][i,:],0])
    dudy= data['a2u'][0,:]*ua[0:-1]+data['a2u'][1,:]*ua[data['nbe'][:,0]]+data['a2u'][2,:]*ua[data['nbe'][:,1]]+data['a2u'][3,:]*ua[data['nbe'][:,2]]
    dvdx= data['a1u'][0,:]*va[0:-1]+data['a1u'][1,:]*va[data['nbe'][:,0]]+data['a1u'][2,:]*va[data['nbe'][:,1]]+data['a1u'][3,:]*va[data['nbe'][:,2]]
    curl[idx,:]=dvdx-dudy
    idx=idx+1

mcurl=curl.mean(axis=0)

f=plt.figure()
ax=plt.axes([.15,.1,.7,.85])
triax=ax.tripcolor(data['trigrid'],mcurl,vmin=mcurl[eidx].min(),vmax=mcurl[eidx].max())
prettyplot_ll(ax,setregion=region,cblabel='Mean Curl',cb=triax)
f.savefig(savepath + grid + '_' +name + '_'+ regionname +'_curl_mean.png',dpi=600)
plt.close(f)
































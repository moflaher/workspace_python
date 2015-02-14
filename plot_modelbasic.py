from __future__ import division
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
name='kit4_kelp_newbathy_test'
grid='kit4_kelp'
regionname='kit4_4island'
datatype='2d'
starttime=0
plotspeed=False


### load the .nc file #####
data = loadnc('runs/' +grid+'/' + name + '/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'


region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)



savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)


# Plot mesh
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
ax.triplot(data['trigrid'],lw=.1)
prettyplot_ll(ax,setregion=region,grid=True,title=grid + ' Grid')
f.savefig(savepath + grid + '_' + regionname +'_grid.png',dpi=600)
plt.close(f)

# Plot depth
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigrid'],data['h'],vmin=data['h'][nidx].min(),vmax=data['h'][nidx].max())
prettyplot_ll(ax,setregion=region,grid=True,cblabel='Depth (m)',cb=triax)
f.savefig(savepath + grid + '_' + regionname +'_depth.png',dpi=600)
plt.close(f)


# Plot depth percentile
clims=np.percentile(data['h'][nidx],[1,99])
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigrid'],data['h'],vmin=clims[0],vmax=clims[1])
prettyplot_ll(ax,setregion=region,grid=True,cblabel='Depth (m)',cb=triax)
f.savefig(savepath + grid + '_' + regionname +'_depth_percentile.png',dpi=600)
plt.close(f)


# Plot dh/h
dh=np.zeros([len(data['nv']),])
for i in range(0,len(data['nv'])):
    one=data['h'][data['nv'][i,0]]
    two=data['h'][data['nv'][i,1]]
    three=data['h'][data['nv'][i,2]]
    hmin=np.min([one,two,three])
    first=np.absolute(one-two)/hmin
    second=np.absolute(two-three)/hmin
    thrid=np.absolute(three-one)/hmin
	
    if ( (first > 0) or (second >0) or (thrid> 0) ):
        dh[i]=np.max([first,second,thrid]);
clims=np.percentile(dh[nidx],[1,99])
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigrid'],dh,vmin=clims[0],vmax=clims[1])
prettyplot_ll(ax,setregion=region,grid=True,cblabel=r'$\frac{\delta H}{H}$',cb=triax)
f.savefig(savepath + grid + '_' + regionname +'_dhh.png',dpi=600)
plt.close(f)


# Plot sidelength
sl=np.zeros([len(data['nv']),])
sidemin=1000000
sidemax=0
for i in range(0,len(data['nv'])):
    slmin=0
    for j in range(3):
        slmin=np.sqrt((data['nodexy'][data['nv'][i,j-1],0]-data['nodexy'][data['nv'][i,j],0])**2+(data['nodexy'][data['nv'][i,j-1],1]-data['nodexy'][data['nv'][i,j],1])**2)+slmin
        sidemin=np.min([np.sqrt((data['nodexy'][data['nv'][i,j-1],0]-data['nodexy'][data['nv'][i,j],0])**2+(data['nodexy'][data['nv'][i,j-1],1]-data['nodexy'][data['nv'][i,j],1])**2),sidemin])
        sidemax=np.max([np.sqrt((data['nodexy'][data['nv'][i,j-1],0]-data['nodexy'][data['nv'][i,j],0])**2+(data['nodexy'][data['nv'][i,j-1],1]-data['nodexy'][data['nv'][i,j],1])**2),sidemax])
    sl[i]=slmin/3
print sidemin
print sidemax
clims=np.percentile(sl[eidx],[1,99])
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigrid'],sl,vmin=clims[0],vmax=clims[1])
prettyplot_ll(ax,setregion=region,grid=True,cblabel=r'Sidelength (m)',cb=triax)
f.savefig(savepath + grid + '_' + regionname +'_sidelength.png',dpi=600)
plt.close(f)


if plotspeed==True:
    # Plot mean speed
    meanspeed=(np.sqrt(data['ua'][starttime:,]**2 +data['va'][starttime:,]**2)).mean(axis=0)
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],meanspeed,vmin=meanspeed[eidx].min(),vmax=meanspeed[eidx].max())
    prettyplot_ll(ax,setregion=region,grid=True,cblabel=r'Mean Speed (ms$^{-1}$)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_DA_meanspeed.png',dpi=600)
    plt.close(f)



    # Plot mean speed percentile
    clims=np.percentile(meanspeed[eidx],[1,99])
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],meanspeed,vmin=clims[0],vmax=clims[1])
    prettyplot_ll(ax,setregion=region,grid=True,cblabel=r'Mean Speed (ms$^{-1}$)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_DA_meanspeed_percentile.png',dpi=600)
    plt.close(f)



    # Plot max speed
    maxspeed=(np.sqrt(data['ua'][starttime:,]**2 +data['va'][starttime:,]**2)).max(axis=0)
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],maxspeed,vmin=maxspeed[eidx].min(),vmax=maxspeed[eidx].max())
    prettyplot_ll(ax,setregion=region,grid=True,cblabel=r'Max Speed (ms$^{-1}$)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_DA_maxspeed.png',dpi=600)
    plt.close(f)



    # Plot max speed percentile
    clims=np.percentile(maxspeed[eidx],[1,99])
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],maxspeed,vmin=clims[0],vmax=clims[1])
    prettyplot_ll(ax,setregion=region,grid=True,cblabel=r'Max Speed (ms$^{-1}$)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_DA_maxspeed_percentile.png',dpi=600)
    plt.close(f)































from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from misctools import *
from plottools import *
from projtools import *
from interptools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from scipy.interpolate import interp1d


# Define names and types of data
name='2012-02-01_2012-03-01_0.01_0.001'
grid='vh_high'
datatype='2d'
region={}
region['region']=np.array([-123.19,-123.09,49.27,49.34])
stime=100

savepath='figures/png/' + grid + '_' + datatype + '/shippath/'
if not os.path.exists(savepath): os.makedirs(savepath)

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

seg=load_segfile('data/misc/shippath_fake_vh_2.seg')
locs=np.array([])
for key in seg.keys():
    locs=np.append(locs,np.array([seg[key][:,0],seg[key][:,1]]).T)
locs=locs.reshape(-1,2)

#Plot obs location
f=plt.figure()
ax=f.add_axes([.125,.1,.75,.8])
ax.triplot(data['trigrid'],lw=.2)
prettyplot_ll(ax,setregion=region)
plotcoast(ax,filename='pacific_harbour.nc',color='None',fcolor='darkgreen',fill=True)
ax.plot(locs[:,0],locs[:,1],'r',lw=2)        
f.savefig(savepath + grid + '_shippath.png',dpi=300)
plt.close(f)



f=plt.figure()
ax=f.add_axes([.125,.1,.75,.8])
prettyplot_ll(ax,setregion=region)
plotcoast(ax,filename='pacific_harbour.nc',color='None',fcolor='darkgreen',fill=True)
ax.plot(locs[:,0],locs[:,1],'r',lw=2)

proj=gridproj(grid)
x,y=proj(locs[:,0],locs[:,1])
dx=np.diff(x)
dy=np.diff(y)
d=np.sqrt(dx**2+dy**2)

np.random.seed(10)
sspeed=np.round(np.random.rand(len(locs)-1)*4)+1  
times=np.append(data['time'][stime],np.cumsum(np.divide(d,sspeed)/(24*60*60))+data['time'][stime])
idx=np.argwhere(((data['time']<=times.max()) & (data['time']>=times.min()))).ravel()
if idx.min()!=0:
    idx=np.append(idx[0]-1,idx)
idx=np.append(idx,idx[-1]+1)

mtimes=data['time'][idx]
sua=np.empty((len(locs),))
sva=np.empty((len(locs),))
for i,time in enumerate(times):
    
    lidx=np.argwhere(mtimes<=time).max()
    lua=interpEfield_locs(data,'ua',locs[i,:],lidx,ll=True)    
    lva=interpEfield_locs(data,'va',locs[i,:],lidx,ll=True)  
     
    uidx=np.argwhere(mtimes>time).min()
    uua=interpEfield_locs(data,'ua',locs[i,:],uidx,ll=True)    
    uva=interpEfield_locs(data,'va',locs[i,:],uidx,ll=True)   
    
    u1 = interp1d(mtimes[[lidx,uidx]], np.array([lua,uua]).flatten())
    sua[i] = u1(time)
    v1 = interp1d(mtimes[[lidx,uidx]], np.array([lva,uva]).flatten())
    sva[i] = v1(time)

qax=ax.quiver(locs[:,0],locs[:,1],sua,sva,angles='xy',scale_units='xy',scale=50,width=0.003)
qax.set_zorder(20)
qaxk=ax.quiverkey(qax,.125,.85,0.5, r'0.5 ms')

        
f.savefig(savepath + grid + '_shippath_arrows.png',dpi=300)
plt.close(f)


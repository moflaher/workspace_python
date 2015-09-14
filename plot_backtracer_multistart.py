from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
from interptools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import time
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import matplotlib.path as path

# Define names and types of data
name='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'
datatype='2d'
regionname='kit4_kelp_tight2'
starttime=396
runtime=120



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
if np.shape(cages)!=():
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.1
    ls='solid'


region=regions(regionname)
region=regionll2xy(data,region)
nidx=get_nodes(data,region)


f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.triplot(data['trigrid'],lw=.5)
#clims=np.percentile(data['h'][nidx],[1,99])
#trip=ax.tripcolor(data['trigrid'],data['h'],vmin=clims[0],vmax=clims[1])
#prettyplot_ll(ax,setregion=region,cb=trip,cblabel='Depth (m)',grid=True)
#plotcoast(ax,color='k',fill=True)
if np.shape(cages)!=():   
    lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    ax.add_collection(lseg_t) 
ax.axis(region['region'])
#f.savefig(savepath + grid + '_' + regionname+'_current_variance_magnitude_ratio.png',dpi=600)
vec=f.ginput(n=-1,timeout=-1)
plt.close(f)

print(len(vec))

locs=np.zeros((len(vec)*12,runtime+1,2))+np.nan


proj=gridproj(grid)
dt=np.diff(data['time'])[0]*24*60*60

x=np.array([val[0] for val in vec])
y=np.array([val[1] for val in vec])


for i,step in enumerate(range(starttime,starttime-runtime,-1)):
    if i<12:
        locs[i::12,i,0],locs[i::12,i,1]=proj(x,y)
    ua=interpEfield_locs(data,'ua',locs[:,i,:],step)
    va=interpEfield_locs(data,'va',locs[:,i,:],step)    
    locs[:,i+1,0]=locs[:,i,0]-(ua*dt)
    locs[:,i+1,1]=locs[:,i,1]-(va*dt)

idx=np.where((locs[:,:,0]==0)&(locs[:,:,1]==0))
locs[idx]=np.nan

f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
clims=np.percentile(data['h'][nidx],[1,99])
trip=ax.tripcolor(data['trigridxy'],data['h'],vmin=clims[0],vmax=clims[1])
#prettyplot_ll(ax,setregion=region,cb=trip,cblabel='Depth (m)',grid=True)
#plotcoast(ax,color='k',fill=True)
#if np.shape(cages)!=():   
#    lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
#    ax.add_collection(lseg_t) 
for i in range(len(vec)*12):
    ax.plot(locs[i,:,0],locs[i,:,1],'w',lw=.5)
    #ax.plot(locs[i,:,0],locs[i,:,1],'r.')

ax.plot(locs[:,0,0],locs[:,0,1],'w*')
ax.plot(locs[:,-1,0],locs[:,-1,1],'k*')
box=np.array([np.nanmin(locs[:,:,0]),np.nanmax(locs[:,:,0]),np.nanmin(locs[:,:,1]),np.nanmax(locs[:,:,1])])
#ax.axis(region['regionxy'])
ax.axis(box)
f.show()




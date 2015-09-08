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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import scipy.io as sio
import bisect
import h5py as h5
from matplotlib.collections import PolyCollection as PC

# Define names and types of data
name='try16'
grid='beaufort3'
datatype='2d'
regionname='beaufort3'



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)

#region=regions(regionname)


if 'savelag' not in globals():
    print "Loading savelag"
    fileload=h5.File('/home/moflaher/workspace_matlab/lagtracker/savedir/'+grid+'/oilstarts_50pp_s0.mat')
    savelag={}
    for i in fileload['savelag'].keys():
            if (i=='u' or i=='v' or i=='w' or i=='sig'):
                continue
            savelag[i]=fileload['savelag'][i].value.T


starts=sio.loadmat('/home/moflaher/workspace_matlab/lagtracker/element_starts/oil_elements_beaufort3.mat')['cage_elements']
startsbool=np.ones((len(data['nv']),))
startsbool[starts-1]=0
unidx=np.flatnonzero(startsbool)


idx=np.where(data['trigrid'].neighbors==-1)
tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2]],0],data['nodell'][data['nv'][i,[0,1,2]],1])) for i in idx[0] ]
modelcoast=PC(tmparray,facecolor = 'g',edgecolor='None')





#f=plt.figure()
#ax=f.add_axes([.125,.1,.8,.8])
#ax.add_collection(modelcoast)
#ax.triplot(data['trigrid'],lw=.5)
#f.show()




host=data['trigridxy'].get_trifinder().__call__(savelag['x'],savelag['y'])
whenall=np.in1d(host,idx[0]).reshape(host.shape)
when=np.argmax(whenall[:,1:],axis=1)
whenidx=np.where((when==0) & (np.sum(whenall,axis=1)==0))[0]


trihost=np.zeros((len(data['nv']),))
tricnt=np.zeros((len(data['nv']),))
for i in range(len(host[:,0])):
    trihost[host[i,0]]=trihost[host[i,0]]+when[i]
    tricnt[host[i,0]]=tricnt[host[i,0]]+1

tridiv=trihost.copy()
tridiv[tricnt!=0]=np.divide(trihost[tricnt!=0],tricnt[tricnt!=0])

f=plt.figure()
ax=f.add_axes([.125,.1,.8,.8])

clims=np.percentile(tridiv[tricnt!=0],[2,98])

triaxis=ax.tripcolor(data['trigridxy'],tridiv,vmin=clims[0],vmax=clims[1])
tmparray=[list(zip(data['nodexy'][data['nv'][i,[0,1,2]],0],data['nodexy'][data['nv'][i,[0,1,2]],1])) for i in np.unique(np.hstack([unidx,np.flatnonzero(tridiv==0)]))]
modelcoast=PC(tmparray,facecolor = 'w',edgecolor='None')
ax.add_collection(modelcoast)
plt.colorbar(triaxis)
#for i in (idx[0]+1):
#    ax.plot(savelag['x'][i,:],savelag['y'][i,:])
#ax.axis([-140,-127,68.5,71])
ax.plot(savelag['x'][:,0],savelag['y'][:,0],'k.',markersize=4)
ax.plot(savelag['x'][when>0,0],savelag['y'][when>0,0],'g.',markersize=6)

f.show()





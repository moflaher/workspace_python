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
regionname='beaufort3_southcoast'
lname='southcoast_10pp_s0'


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

region=regions(regionname)

savepath='figures/png/' + grid + '_' + datatype + '/lagtracker/percent2coast/'
if not os.path.exists(savepath): os.makedirs(savepath)

if 'savelag' not in globals():
    print "Loading savelag"
    fileload=h5.File('savedir/'+grid+'/'+lname+'.mat')
    savelag={}
    for i in fileload['savelag'].keys():
            if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
                continue
            savelag[i]=fileload['savelag'][i].value.T





idx=np.where(data['trigrid'].neighbors==-1)
#tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2]],0],data['nodell'][data['nv'][i,[0,1,2]],1])) for i in idx[0] ]
#modelcoast=PC(tmparray,facecolor = 'g',edgecolor='None')





#f=plt.figure()
#ax=f.add_axes([.125,.1,.8,.8])
#ax.add_collection(modelcoast)
#ax.triplot(data['trigrid'],lw=.5)
#f.show()




host=data['trigridxy'].get_trifinder().__call__(savelag['x'],savelag['y'])
whenall=np.in1d(host,idx[0]).reshape(host.shape)
when=np.argmax(whenall,axis=1)
whenidx=np.where((when==0) & (np.sum(whenall,axis=1)==0))[0]


trihost=np.zeros((len(data['nv']),))
trihost2=np.zeros((len(data['nv']),))
tricnt=np.zeros((len(data['nv']),))
for i in range(len(host[:,0])):
    trihost[host[i,0]]=trihost[host[i,0]]+when[i]
    tricnt[host[i,0]]=tricnt[host[i,0]]+1
    if (when[i]!=0):
        trihost2[host[i,0]]=trihost2[host[i,0]]+1

tridiv=trihost.copy()
tridiv[tricnt!=0]=np.divide(trihost[tricnt!=0],tricnt[tricnt!=0])
tridiv2=np.divide(trihost2,10)
tridiv2[idx[0]]=1

f=plt.figure()
ax=f.add_axes([.125,.1,.8,.8])

clims=np.percentile(tridiv[tricnt!=0],[2,98])

triaxis=ax.tripcolor(data['trigrid'],tridiv2*100)
#tmparray=[list(zip(data['nodexy'][data['nv'][i,[0,1,2]],0],data['nodexy'][data['nv'][i,[0,1,2]],1])) for i in np.unique(np.hstack([unidx,np.flatnonzero(tridiv==0)]))]
tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2]],0],data['nodell'][data['nv'][i,[0,1,2]],1])) for i in np.flatnonzero(tridiv2==0)]
modelcoast=PC(tmparray,facecolor = 'w',edgecolor='k',linewidth=.5)
ax.add_collection(modelcoast)
cb=plt.colorbar(triaxis)
cb.set_label('Percent of particles to reach coastal element')
#for i in (idx[0]+1):
#    ax.plot(savelag['x'][i,:],savelag['y'][i,:])
ax.axis(region['region'])
#ax.plot(savelag['x'][:,0],savelag['y'][:,0],'k.',markersize=4)
#ax.plot(savelag['x'][when>0,0],savelag['y'][when>0,0],'g.',markersize=6)
plotcoast(ax,filename='world_GSHHS_f_L1.nc',color='k')

box={}
box['region']=[-141,-131.5,68,71.5]
plot_box(ax,box,'g',lw=2)

ax.set_xticklabels(-1*(ax.get_xticks()))
ax.set_xlabel(r'Longitude ($^{\circ}$W)')
ax.set_ylabel(r'Latitude ($^{\circ}$N)')


#f.show()
f.savefig(savepath +''+name+'_'+regionname+'_'+lname+'_percent2coast.png',dpi=600)
plt.close(f)





from __future__ import division,print_function
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
from mytools import *
import os, sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name='test_river_utc'
grid='sjh_lr_v1_sub'
loc=np.array([-66.723517, 44.718500])

loc=np.array([-66.04, 45.235])

### load the .nc file #####
data = loadnc('/media/moflaher/runs/sjh_lr_v1_sub/test_river_utc/output/',singlename=grid + '_0001.nc')
print('done load')

savepath='{}/png/{}/variogram4loc/{}/'.format(figpath,grid,name)
if not os.path.exists(savepath): os.makedirs(savepath)


speed=np.sqrt(data['ua']**2+data['va']**2)
mspeed=np.max(speed,axis=0)
pspeed=np.percentile(speed,95,axis=0)
bspeed=.1
bpspeed=copy.deepcopy(pspeed)
bpspeed[bpspeed<=bspeed]=np.nan

eidx=closest_element(data,loc)


x,y=data['proj'](loc[0],loc[1])
lon,lat=data['proj']([x-5000,x+5000],[y-5000,y+5000],inverse=True)

ratio=bpspeed/bpspeed[eidx]
#dist=np.sqrt((data['xc']-data['xc'][i])**2 +(data['yc']-data['yc'][i])**2)




f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8])    
plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc', filepath=coastpath, color='k', fill=True,zorder=50)   
triax=ax.tripcolor(data['trigrid'],ratio,vmin=-1,vmax=3,cmap=mpl.cm.seismic)    
cb=plt.colorbar(triax)
ax.plot(loc[0],loc[1],'r*',zorder=70)
ax.plot(data['lon'][data['nv'][eidx,[0,1,2,0]]],data['lat'][data['nv'][eidx,[0,1,2,0]]],'k',lw=2)
ax.set_xlabel(r'Longitude ($^{\circ}$)')
ax.set_ylabel(r'Latitude ($^{\circ}$)')
ax.axis([lon[0],lon[1],lat[0],lat[1]])

#ax.annotate('{} {}'.format(data['Time'][i][:10],data['Time'][i][11:19]),xy=region['textloc'],xycoords='axes fraction')
for label in ax.get_xticklabels()[::2]:
    label.set_visible(False)
#f.savefig('{}{}_{}_{}_{}_{:05d}.png'.format(savepath,grid,name,region['regionname'],field,i),dpi=300)
#plt.close(f)
f.show()













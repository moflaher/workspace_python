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
from mpl_toolkits.mplot3d.axes3d import Axes3D





# Define names and types of data
name='sfm6_musq2_all_cages'
grid='sfm6_musq2'
regionname='musq_cage'
datatype='2d'



### load the .nc file #####
data = loadnc('/media/moflaher/My Book/cages/' + name +'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

trigridxy = mplt.Triangulation(data['x'], data['y'],data['nv'])
region=regions(regionname)

savelag=(sio.loadmat('/home/moflaher/workspace_matlab/lagtracker/savedir/test_240i.mat',squeeze_me=True,struct_as_record=False))['savelag']



#plt.triplot(trigridxy,lw=.3)
whichtri=3151
whichtri=-39
whichtri=2936
whichtri=5


l=savelag.x.shape[1]


#fig = plt.figure(figsize=(14,6))
f, ax = plt.subplots(nrows=1,ncols=2)
#ax.plot_trisurf(trigridxy,data['h'])
#ax.axis([-100000,-300000,200000,400000])
#plt.plot(savelag.x[whichtri,0],savelag.z[whichtri,0],'r*')
ax[0].plot(savelag.time,savelag.z[whichtri,:],'b')
ax[0].plot(savelag.time,-savelag.h[whichtri,:],'g')
#plt.show()


ax[1].tripcolor(trigridxy,data['h'],vmin=-5,vmax=40)
ax[1].plot(savelag.x[whichtri,:],savelag.y[whichtri,:],'r')
ax[1].plot(savelag.x[whichtri,0],savelag.y[whichtri,0],'b*')
ax[1].plot(savelag.x[whichtri,-1],savelag.y[whichtri,-1],'k*')
last=np.max(np.flatnonzero(~np.isnan(savelag.x[whichtri,:])))
tdiff=savelag.time[2]-savelag.time[1]
newx=savelag.x[whichtri,last]+savelag.u[whichtri,last]*tdiff
newy=savelag.y[whichtri,last]+savelag.v[whichtri,last]*tdiff
ax[1].plot(newx,newy,'m*',markersize=16)

ax[1].axis([np.nanmin(savelag.x[whichtri,:])*1.01, np.nanmax(savelag.x[whichtri,:])*.99, np.nanmin(savelag.y[whichtri,:])*.99, np.nanmax(savelag.y[whichtri,:])*1.01])
#plt.show()

#ax[i]=prettyplot_ll(ax[i],setregion=region,grid=True,title='Day '+ ("%d"% (48*3*i/48)))


f.show()
    
    #f.savefig(savepath + grid + '_' +name1+ '_'+name2+'_currents_at_' +("%d"%idx[i])+ '.png',dpi=1200)

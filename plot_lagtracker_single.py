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

savelag=(sio.loadmat('/home/moflaher/workspace_matlab/lagtracker/savedir/25_particles_all_cages/all_cages_25part_per_ele_sfm6_musq2_all_cages_6_noclass.mat',squeeze_me=True,struct_as_record=False))['savelag']



#plt.triplot(trigridxy,lw=.3)
whichtri=200


host=trigridxy.get_trifinder().__call__(savelag.x[whichtri,:],savelag.y[whichtri,:])



fig = plt.figure(figsize=(14,6))
ax = fig.add_subplot(1,1,1,projection='3d')
ax.plot_trisurf(trigridxy,data['h'])
ax.axis([-100000,-300000,200000,400000])
#plt.plot(savelag.x[whichtri,0],savelag.z[whichtri,0],'r*')
#plt.plot(savelag.x[whichtri,:],savelag.z[whichtri,:],'g')
#plt.plot(savelag.x[whichtri,:],-data['uvh'][host])
plt.show()

#ax[i]=prettyplot_ll(ax[i],setregion=region,grid=True,title='Day '+ ("%d"% (48*3*i/48)))



    
    #f.savefig(savepath + grid + '_' +name1+ '_'+name2+'_currents_at_' +("%d"%idx[i])+ '.png',dpi=1200)

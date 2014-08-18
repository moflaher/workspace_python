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

testi=0
region['region']=[np.nanmin(savelag.x[:,3*testi*48]),np.nanmax(savelag.x[:,3*testi*48]),np.nanmin(savelag.y[:,3*testi*48]),np.nanmax(savelag.y[:,3*testi*48])]


f, ax = plt.subplots(nrows=3,ncols=3, sharex=True, sharey=True)
ax=ax.flatten()

for i in range(0,len(ax)):
    ax[i].triplot(trigridxy,lw=.3)
    plotidx=np.where(((savelag.x[:,3*i*48]-savelag.x[:,3*(i-1)*48])!=0) & ((savelag.x[:,3*i*48]-savelag.x[:,3*(i-1)*48])!=np.nan))
    ax[i].plot(savelag.x[plotidx,3*i*48],savelag.y[plotidx,3*i*48],'g.')
    ax[i].axis(region['region'])
    ax[i].set_title('Day '+ ("%d"% (48*3*i/48)))
    #ax[i]=prettyplot_ll(ax[i],setregion=region,grid=True,title='Day '+ ("%d"% (48*3*i/48)))



    
    #f.savefig(savepath + grid + '_' +name1+ '_'+name2+'_currents_at_' +("%d"%idx[i])+ '.png',dpi=1200)

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

savelag=(sio.loadmat('/home/moflaher/workspace_matlab/lagtracker/savedir/testzf.mat',squeeze_me=True,struct_as_record=False))['savelag']

daysi=1
lph=24*2
testi=0
region['region']=[np.nanmin(savelag.x[:,daysi*testi*lph]),np.nanmax(savelag.x[:,daysi*testi*lph]),np.nanmin(savelag.y[:,daysi*testi*lph]),np.nanmax(savelag.y[:,daysi*testi*lph])]



f, ax = plt.subplots(nrows=3,ncols=4, sharex=True, sharey=True)
ax=ax.flatten()

for i in range(0,len(ax)):
    print i
    ax[i].triplot(trigridxy,lw=.3)
    plotidx=np.where(np.isnan(savelag.x[:,daysi*i*lph]) & ((savelag.x[:,daysi*i*lph]-savelag.x[:,daysi*(i-1)*lph])!=0))
    plotidxb=np.zeros(shape=(savelag.x.shape[0],), dtype=bool)
    plotidxb[plotidx]=1
    ax[i].plot(savelag.x[plotidxb,daysi*i*lph],savelag.y[plotidxb,daysi*i*lph],'g.')
    ax[i].plot(savelag.x[~plotidxb,daysi*i*lph],savelag.y[~plotidxb,daysi*i*lph],'r.')
    #ax[i].plot(savelag.x[:,daysi*i*lph],savelag.y[:,daysi*i*lph],'g.')
    
    #plotidx2=np.where(np.fabs(savelag.z[:,daysi*i*lph]-data['uvh'][trigridxy.get_trifinder().__call__(savelag.x[:,daysi*i*lph],savelag.y[:,daysi*i*lph])])<=1 )
    #ax[i].plot(savelag.x[plotidx2,daysi*i*lph],savelag.y[plotidx2,daysi*i*lph],'y.')

    ax[i].axis(region['region'])
    ax[i].set_title('Day '+ ("%d"% (48*daysi*i/48)))
    #ax[i]=prettyplot_ll(ax[i],setregion=region,grid=True,title='Day '+ ("%d"% (48*daysi*i/48)))



    
    #f.savefig(savepath + grid + '_' +name1+ '_'+name2+'_currents_at_' +("%d"%idx[i])+ '.png',dpi=1200)

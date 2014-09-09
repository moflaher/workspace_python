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
name='kit4_45days_3'
grid='kit4'
regionname='mostchannels'
datatype='2d'
lfolder='kit4_kelp_0.0'
lname='kit4_kelp_0.0_0'
spacing=10



### load the .nc file #####
data = loadnc('/media/moflaher/My Book/kit4_runs/' + name +'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

savepath='figures/png/' + grid + '_' + datatype + '/lagtracker/' + lfolder + '/singles/'
if not os.path.exists(savepath): os.makedirs(savepath)

trigridxy = mplt.Triangulation(data['x'], data['y'],data['nv'])
region=regions(regionname)


savelag=(sio.loadmat('/home/moflaher/workspace_matlab/lagtracker/savedir/'+lfolder+'/'+lname+'.mat',squeeze_me=True,struct_as_record=False))['savelag']



#plt.triplot(trigridxy,lw=.3)
whichtri=3151
whichtri=-39
whichtri=2936
whichtri=5

for whichtri in range(0,len(savelag.x),spacing):
    region={}
    region['region']=[np.nanmin(savelag.x[whichtri,:]), np.nanmax(savelag.x[whichtri,:]), np.nanmin(savelag.y[whichtri,:]), np.nanmax(savelag.y[whichtri,:])]


    l=savelag.x.shape[1]



    #f, ax = plt.subplots(nrows=1,ncols=2)

    f=plt.figure()    
    ax0 = plt.subplot2grid((1,4),(0, 0),colspan=2)
    ax1 = plt.subplot2grid((1,4),(0, 2),colspan=2)


    ax0.plot(savelag.time,savelag.z[whichtri,:],'b')
    ax0.plot(savelag.time,-savelag.h[whichtri,:],'g')
    ax0.set_xticklabels((ax0.get_xticks())/100000,rotation=90)



    nidx=get_nodes_xy(data,region)

    ax1tri=ax1.tripcolor(trigridxy,data['h'],vmin=data['h'][nidx].min(),vmax=data['h'][nidx].max())
    plt.colorbar(ax1tri,ax=ax1)
    ax1.plot(savelag.x[whichtri,:],savelag.y[whichtri,:],'k')
    ax1.plot(savelag.x[whichtri,0],savelag.y[whichtri,0],'b*',markersize=12)
    ax1.plot(savelag.x[whichtri,-1],savelag.y[whichtri,-1],'k*')
    last=np.max(np.flatnonzero(~np.isnan(savelag.x[whichtri,:])))
    tdiff=savelag.time[2]-savelag.time[1]
    newx=savelag.x[whichtri,last]+savelag.u[whichtri,last]*tdiff
    newy=savelag.y[whichtri,last]+savelag.v[whichtri,last]*tdiff
    ax1.plot(newx,newy,'m*',markersize=16)
    ax1.axis(region['region'])
    ax1.set_xticklabels((ax1.get_xticks())/1000,rotation=90)
    ax1.set_yticklabels((ax1.get_yticks())/1000)



    #f.show()
    f.tight_layout(pad=0.4)
    f.savefig(savepath + grid + '_' +name+ '_'+lname+'_particle_path_'+("%05d"%whichtri)+'.png',dpi=300)
    plt.close(f)



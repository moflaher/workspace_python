from __future__ import division,print_function
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
import h5py as h5




# Define names and types of data
name='try16'
grid='beaufort3'
regionname='beaufort3_southcoast'
datatype='2d'
lname='southcoast_10pp_s0'
spacing=1000



### load the .nc file #####
data = loadnc('runs/'+grid+'/' + name +'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

savepath='figures/png/' + grid + '_' + datatype + '/lagtracker/singles/'
if not os.path.exists(savepath): os.makedirs(savepath)


region=regions(regionname)
region=regionll2xy(data,region)


if 'savelag' not in globals():
    print "Loading savelag"
    fileload=h5.File('savedir/'+grid+'/'+lname+'.mat')
    savelag={}
    for i in fileload['savelag'].keys():
            if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
                continue
            savelag[i]=fileload['savelag'][i].value.T


whichtri=3151
whichtri=-39
whichtri=2936
whichtri=5

for whichtri in range(0,len(savelag['x']),spacing):
    region={}
    minmax=[np.nanmin(savelag['x'][whichtri,:]), np.nanmax(savelag['x'][whichtri,:]), np.nanmin(savelag['y'][whichtri,:]), np.nanmax(savelag['y'][whichtri,:])]
    region['regionxy']=[minmax[0]-(minmax[1]-minmax[0])*2,minmax[1]+(minmax[1]-minmax[0])*2,minmax[2]-(minmax[3]-minmax[2])*2,minmax[3]+(minmax[3]-minmax[2])*2]


    l=savelag['x'].shape[1]



    #f, ax = plt.subplots(nrows=1,ncols=2)

    f=plt.figure()    
    ax = f.add_axes([.125,.1,.8,.8])
   
    ax.triplot(data['trigridxy'],lw=.5)
    ax.plot(savelag['x'][whichtri,:],savelag['y'][whichtri,:],'r')
    ax.plot(savelag['x'][whichtri,0],savelag['y'][whichtri,0],'b*',markersize=12)
    ax.axis(region['regionxy'])
    ax.set_xticklabels((ax.get_xticks())/1000)
    ax.set_yticklabels((ax.get_yticks())/1000)

    ax.set_xlabel('x (km)')
    ax.set_ylabel('y (km)')
    #f.show()

    f.savefig(savepath + grid + '_' +name+ '_'+lname+'_particle_path_'+("%05d"%whichtri)+'.png',dpi=300)
    plt.close(f)



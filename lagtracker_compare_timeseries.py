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
import h5py as h5
from matplotlib.collections import PolyCollection as PC



# Define names and types of data
name='kit4_45days_3'
name2='kit4_kelp_20m_0.018'
grid='kit4'
regionname='kit4_kelp_tight6'
datatype='2d'
lfolder='kit4_kelp_0.0'
lname='kit4_kelp_0.0_0_all_in_a_box'


### load the .nc file #####
data = loadnc('runs/'+grid+'/' + name +'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

savepath='figures/timeseries/' + grid + '_' + datatype + '/lagtracker/' + name + '_'+name2+'/'
if not os.path.exists(savepath): os.makedirs(savepath)

data['trigridxy'] = mplt.Triangulation(data['x'], data['y'],data['nv'])
region=regions(regionname)
region=regionll2xy(data,region)


if 'savelag1' not in locals():
    fileload=h5.File('/home/moflaher/workspace_matlab/lagtracker/savedir/'+name+'/allelements_s0in_aristazabal_west.mat')
    savelag1={}
    for i in fileload['savelag'].keys():
            savelag1[i]=fileload['savelag'][i].value.T

if 'savelag2' not in locals():
    fileload=h5.File('/home/moflaher/workspace_matlab/lagtracker/savedir/'+name2+'/allelements_s0in_aristazabal_west.mat')
    savelag2={}
    for i in fileload['savelag'].keys():
            savelag2[i]=fileload['savelag'][i].value.T


cages=np.genfromtxt('runs/'+grid+'/' +name2+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)


tmparray=[list(zip(data['nodexy'][data['nv'][i,[0,1,2]],0],data['nodexy'][data['nv'][i,[0,1,2]],1])) for i in cages ]
sidx=np.where((savelag1['x'][:,0]>region['regionxy'][0])&(savelag1['x'][:,0]<region['regionxy'][1])&(savelag1['y'][:,0]>region['regionxy'][2])&(savelag1['y'][:,0]<region['regionxy'][3]))

expand=10000
region['regionxy']=[region['regionxy'][0]-expand,region['regionxy'][1]+expand,region['regionxy'][2]-expand,region['regionxy'][3]+expand]

for i in range(0,100,10):
    f = plt.figure()
    ax=f.add_axes([.125,.1,.8,.8])


    #plotcoast(ax,filename='pacific.nc',color='k')
    ax.triplot(data['trigridxy'],lw=.25)
    ax.axis(region['regionxy'])
    lseg1=PC(tmparray,facecolor = 'g',edgecolor='None')
    ax.add_collection(lseg1)

    ax.plot(savelag1['x'][sidx,i],savelag1['y'][sidx,i],'.k',markersize=4)
    ax.plot(savelag2['x'][sidx,i],savelag2['y'][sidx,i],'.r',markersize=4)
    
    f.savefig(savepath +'_'+name+'_'+name2+'_'+regionname+'_timestep_'+("%d"%i)+'.png',dpi=300)
    plt.close(f)




















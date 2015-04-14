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
name='kit4_kelp_nodrag'
name2='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'
datatype='2d'


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

cages=loadcage('runs/'+grid+'/' +name2+ '/input/' +grid+ '_cage.dat')
if np.shape(cages)!=():
    tmparray=[list(zip(data['nodexy'][data['nv'][i,[0,1,2]],0],data['nodexy'][data['nv'][i,[0,1,2]],1])) for i in cages ]
    color='g'
    lw=.1
    ls='solid'



for i in range(0,24,3):
    lname='kit4_kelp_tight2_kelpfield_3elements_200x200_1000pp_s' + ("%d"%i)




    print "Loading savelag1"
    fileload=h5.File('savedir/'+name+'/'+lname+'.mat')
    savelag1={}
    for i in fileload['savelag'].keys():
        if (i=='x' or i=='y' or i=='time'):
            savelag1[i]=fileload['savelag'][i].value.T

    print "Loading savelag2"
    fileload=h5.File('savedir/'+name2+'/'+lname+'.mat')
    savelag2={}
    for i in fileload['savelag'].keys():
        if (i=='x' or i=='y'):
            savelag2[i]=fileload['savelag'][i].value.T


    subset=1000

    savedic={}
    for sub in range(int(savelag1['x'].shape[0]/subset)):
        print "Subset " +("%d"%sub)
        print

        savedic['sigma_nodrag']=np.sqrt(np.nanvar(savelag1['x'][(subset*sub):(subset*(sub+1)),:],axis=0,ddof=1)+np.nanvar(savelag1['y'][(subset*sub):(subset*(sub+1)),:],axis=0,ddof=1))
        savedic['dis_rate_nodrag']=np.diff(savedic['sigma_nodrag'])/60
        savedic['sigma_drag']=np.sqrt(np.nanvar(savelag2['x'][(subset*sub):(subset*(sub+1)),:],axis=0,ddof=1)+np.nanvar(savelag2['y'][(subset*sub):(subset*(sub+1)),:],axis=0,ddof=1))
        savedic['dis_rate_drag']=np.diff(savedic['sigma_drag'])/60
        savedic['time']=savelag1['time']

        
        sio.savemat('data/dis_rate/'+name+'_'+name2+'_'+lname+'_sigma_and_disrate_'+("%05d"%(subset*sub))+'_'+("%05d"%(subset*(sub+1)))+'.mat',mdict=savedic)
        









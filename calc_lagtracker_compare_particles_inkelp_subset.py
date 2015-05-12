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
from projtools import *
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
data = ncdatasort(data,trifinder=True)
print 'done sort'

lcages=loadcage('runs/'+grid+'/' +name2+ '/input/' +grid+ '_cage.dat')
if np.shape(lcages)!=():
    tmparray=[list(zip(data['nodexy'][data['nv'][i,[0,1,2]],0],data['nodexy'][data['nv'][i,[0,1,2]],1])) for i in lcages ]
    color='g'
    lw=.1
    ls='solid'



for i in range(0,25,1):
    lname='kit4_kelp_tight5_1elements_250x150_1000pp_s' + ("%d"%i)




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

        regionname='kit4'

#        if sub>2:
#            regionname='kit4_kelp_tight5_A2'
#        else:
#            regionname='kit4_kelp_tight5_A6'


        region=regions(regionname)
        region=regionll2xy(data,region)
        eidx=get_elements(data,region)
        #comment out this line for any kelp not just kelp in the start box
        cages=eidx[np.in1d(eidx,lcages)]


        sidx=np.arange(subset*sub,subset*(sub+1))
        npts=savelag1['x'][(subset*sub):(subset*(sub+1)),:].shape[0]


        #find particles in kelp from region start
        numberin1=np.sum(np.in1d(data['trigridxy_finder'].__call__(savelag1['x'][sidx,:],savelag1['y'][sidx,:]),cages).reshape(savelag1['x'][sidx,:].shape),axis=0)/npts
        numberin2=np.sum(np.in1d(data['trigridxy_finder'].__call__(savelag2['x'][sidx,:],savelag2['y'][sidx,:]),cages).reshape(savelag2['x'][sidx,:].shape),axis=0)/npts


        savedic['kelpratio_nodrag']=numberin1
        savedic['kelpratio_drag']=numberin2
        savedic['time']=savelag1['time']


        
        sio.savemat('data/kelp_ratio/'+name+'_'+name2+'_'+regionname+'_'+lname+'_kelp_ratio_'+("%05d"%(subset*sub))+'_'+("%05d"%(subset*(sub+1)))+'.mat',mdict=savedic)
        









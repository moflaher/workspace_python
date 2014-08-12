# -*- coding: utf-8 -*-
"""
Front Matter
=============

Created on 

Author: Mitchell O'Flaherty-Sproul

Requirements
===================================
Absolutely Necessary:

* Numpy
* SciPy
* Matplotlib 


Optional, but recommended:

Functions
=========
"""
#load modules
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from math import pi
from datatools import *
import scipy as sp
import matplotlib as mpl
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import sys





# Define names and types of data
name='kit4_45days_3'
grid='kit4'
datatype='2d'
starttime=384
interpheight=1

### load the .nc file #####
data = loadnc('/media/moflaher/My Book/kit4_runs/' + name + '/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'
base_dir = os.path.dirname(__file__)

tempdic={}

tempdic['trigrid']=data['nv']+1
tempdic['lon']=data['lon']
tempdic['lat']=data['lat']
tempdic['lonc']=data['uvnodell'][:,0]
tempdic['latc']=data['uvnodell'][:,1]
tempdic['h']=data['h']
tempdic['hc']= (data['h'][data['nv'][:,0]] + data['h'][data['nv'][:,1]] + data['h'][data['nv'][:,2]]) / 3.0
tempdic['siglay']=data['siglay'][:,0]
tempdic['siglev']=data['siglev'][:,0]




sio.savemat(os.path.join(base_dir,'data', grid +'_basic.mat'),mdict=tempdic)



tempdic['ua']=data['ua'][384:,:]
tempdic['va']=data['va'][384:,:]
tempdic['time']=data['time'][384:]
tempdic['zeta']=data['zeta'][384:,:]

sio.savemat(os.path.join(base_dir,'data',grid+'_currents.mat'),mdict=tempdic)





filename='_' + grid + '_' +name+ '_' + ("%d" %interpheight) + 'm.npy'
if (os.path.exists(os.path.join(base_dir,'data', 'u' + filename)) & os.path.exists(os.path.join(base_dir,'data', 'v' + filename))):
    print 'Loading old interpolated currents'
    tempdic['u_interp']=np.load(os.path.join(base_dir,'data', 'u' + filename))
    tempdic['v_interp']=np.load(os.path.join(base_dir,'data', 'v' + filename))
    print 'Loaded old interpolated currents'
else:
    print 'Interpolate currents first'
    sys.exit(0)

tempdic['comments']='The *_interp data is interpolated to ' + ("%d"%interpheight) + 'm.'

sio.savemat(os.path.join(base_dir,'data',grid+'_currents_and_interp.mat'),mdict=tempdic)




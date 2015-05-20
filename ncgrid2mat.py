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
name='kit4_kelp_nodrag'
grid='kit4_kelp'
datatype='2d'
starttime=384
interpheight=1

### load the .nc file #####
data = loadnc('runs/'+grid+'/' + name + '/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

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
sio.savemat('data/ncgrid2mat/'+grid +'_basic.mat',mdict=tempdic)


#empdic['ua']=data['ua'][384:,:]
#tempdic['va']=data['va'][384:,:]
tempdic['time']=data['time'][384:]
#tempdic['zeta']=data['zeta'][384:,:]
#sio.savemat('data/ncgrid2mat/'+grid +'_'+name+'_currents.mat',mdict=tempdic)


tempdic['ww']=data['ww'][384:456,:,:]
sio.savemat('data/ncgrid2mat/'+grid +'_'+name+'_vertical_currents.mat',mdict=tempdic)




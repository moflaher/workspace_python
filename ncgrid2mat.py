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
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
import sys





# Define names and types of data
name='kit4_baroclinic_new_322'
grid='kit4'

starttime=96
interpheight=1

### load the .nc file #####
data = loadnc('runs/'+grid+'/' + name + '/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')


tempdic={}
tempdic['trigrid']=data['nv']+1
tempdic['lon']=data['lon']
tempdic['lat']=data['lat']
tempdic['lonc']=data['uvnodell'][:,0]
tempdic['latc']=data['uvnodell'][:,1]
tempdic['x']=data['x']
tempdic['y']=data['y']
tempdic['xc']=data['uvnode'][:,0]
tempdic['yc']=data['uvnode'][:,1]
tempdic['h']=data['h']
tempdic['hc']= (data['h'][data['nv'][:,0]] + data['h'][data['nv'][:,1]] + data['h'][data['nv'][:,2]]) / 3.0
tempdic['siglay']=data['siglay'][:,0]
tempdic['siglev']=data['siglev'][:,0]
sio.savemat('data/ncgrid2mat/'+grid +'_basic.mat',mdict=tempdic)

#tempdic['ua']=data['ua'][starttime:,:]
#tempdic['va']=data['va'][starttime:,:]
#tempdic['time']=data['time'][starttime:]
#tempdic['zeta']=data['zeta'][starttime:,:]
#sio.savemat('data/ncgrid2mat/'+grid +'_'+name+'_currents.mat',mdict=tempdic)

tempdic={}
#tempdic['trigrid']=data['nv']+1
#tempdic['lon']=data['lon']
#tempdic['lat']=data['lat']
#tempdic['lonc']=data['uvnodell'][:,0]
#tempdic['latc']=data['uvnodell'][:,1]
#tempdic['x']=data['x']
#tempdic['y']=data['y']
#tempdic['xc']=data['uvnode'][:,0]
#tempdic['yc']=data['uvnode'][:,1]
#tempdic['h']=data['h']
#tempdic['hc']= (data['h'][data['nv'][:,0]] + data['h'][data['nv'][:,1]] + data['h'][data['nv'][:,2]]) / 3.0
#tempdic['siglay']=data['siglay'][:,0]
#tempdic['siglev']=data['siglev'][:,0]

tempdic['time']=data['time'][starttime:]
tempdic['u']=data['u'][starttime:,-1,:]
tempdic['v']=data['v'][starttime:,-1,:]
#tempdic['ww']=data['ww'][starttime:,-1,:]

sio.savemat('data/ncgrid2mat/'+grid +'_'+name+'_uv_bottom_currents.mat',mdict=tempdic)


#tempdic={}
#tempdic['trigrid']=data['nv']+1
#tempdic['lon']=data['lon']
#tempdic['lat']=data['lat']
#tempdic['lonc']=data['uvnodell'][:,0]
#tempdic['latc']=data['uvnodell'][:,1]
#tempdic['x']=data['x']
#tempdic['y']=data['y']
#tempdic['xc']=data['uvnode'][:,0]
#tempdic['yc']=data['uvnode'][:,1]
#tempdic['h']=data['h']
#tempdic['hc']= (data['h'][data['nv'][:,0]] + data['h'][data['nv'][:,1]] + data['h'][data['nv'][:,2]]) / 3.0
#tempdic['siglay']=data['siglay'][:,0]
#tempdic['siglev']=data['siglev'][:,0]

#tempdic['salinity']=data['salinity'][starttime:(starttime+30),:,:]
#tempdic['temp']=data['temp'][starttime:(starttime+30),:,:]

#sio.savemat('data/ncgrid2mat/'+grid +'_'+name+'_temp_sal.mat',mdict=tempdic)


#tempdic={}
#tempdic['trigrid']=data['nv']+1
#tempdic['lon']=data['lon']
#tempdic['lat']=data['lat']
#tempdic['lonc']=data['uvnodell'][:,0]
#tempdic['latc']=data['uvnodell'][:,1]
#tempdic['x']=data['x']
#tempdic['y']=data['y']
#tempdic['xc']=data['uvnode'][:,0]
#tempdic['yc']=data['uvnode'][:,1]
#tempdic['h']=data['h']
#tempdic['hc']= (data['h'][data['nv'][:,0]] + data['h'][data['nv'][:,1]] + data['h'][data['nv'][:,2]]) / 3.0
#tempdic['siglay']=data['siglay'][:,0]
#tempdic['siglev']=data['siglev'][:,0]

#tempdic['km']=data['km'][starttime:(starttime+30),:,:]
#tempdic['kh']=data['kh'][starttime:(starttime+30),:,:]

#sio.savemat('data/ncgrid2mat/'+grid +'_'+name+'_temp_sal.mat',mdict=tempdic)

















# -*- coding: utf-8 -*-
"""
Front Matter
=============

Created on April 4 2014

Author: Mitchell O'Flaherty-Sproul


Requirements
===================================
Absolutely Necessary:

* Numpy
* SciPy
* Matplotlib version 1.3.0


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
np.set_printoptions(precision=8,suppress=True)



import sys
sys.path.append('/home/moflaher/Desktop/workspace_python/ttide_py/ttide/')
import t_tide as tt
reload(tt)

import t_predic as tp


fileDir='/media/moflaher/My Book/kitimat3_runs/kitimat3_56_0.25_45day/output/'

data = loadnc(fileDir)
data= ncdatasort(data)

#testel=np.genfromtxt('kiti_118836.csv', dtype=None, delimiter=',')
#print np.absolute(data['zeta'][199:-1,118836]-testel).min()
#print np.absolute(data['zeta'][199:-1,118836]-testel).max()
#[nameu, fu, tidecon, xout]=tt.t_tide(data['zeta'][199:-1,118836])
#[nameu, fu, tidecon, xout]=tt.t_tide(data['zeta'][199:-1,118836],data['time'][0],dt=.5)

#[nameu, fu, tidecon, xout]=tt.t_tide(data['ua'][199:-1,149999]+1j*data['va'][199:-1,149999],stime=data['time'][0])
#[nameu, fu, tidecon2, xout]=tt.t_tide(data['ua'][199:-1,149999]+1j*data['va'][199:-1,149999],stime=data['time'][0],dt=0.5)

#[nameu, fu, tidecon, xout]=tt.t_tide(data['zeta'][199:-1,118836],stime=data['time'][0],dt=0.5,lat=data['nodell'][118836,1])







#[nameu, fu, tidecon2, xout]=tt.t_tide(data['zeta'][199:-1,118836],stime=data['time'][0])
[nameu, fu, tidecon, xout]=tt.t_tide(data['zeta'][199:-1,118836],stime=data['time'][0],lat=data['nodell'][118836,1])
[nameu, fu, tidecon, xout]=tt.t_tide(data['zeta'][199:-1,118836],stime=data['time'][0],lat=data['nodell'][118836,1],constitnames=np.array([['M2  '],['N2  ']]))
#print tp.t_predic(data['time'][0:10],nameu,fu,tidecon)














#print tidecon-tidecon2

#mtidecon=np.genfromtxt('tidecon.csv', dtype=None, delimiter=',')


#diff=tidecon-mtidecon


#print diff[:,[0,1,2,3]]
#print
#print diff[:,[4,5,6,7]]


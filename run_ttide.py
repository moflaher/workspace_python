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





fileDir='/media/moflaher/My Book/kitimat3_runs/kitimat3_56_0.25_45day/output/'

data = loadnc(fileDir)
data= ncdatasort(data)

testel=np.genfromtxt('kiti_118836.csv', dtype=None, delimiter=',')
print np.absolute(data['zeta'][199:-1,118836]-testel).min()
print np.absolute(data['zeta'][199:-1,118836]-testel).max()
#[nameu, fu, tidecon, xout]=tt.t_tide(data['zeta'][199:-1,118836])
[nameu, fu, tidecon, xout]=tt.t_tide(data['zeta'][199:-1,118836],data['time'][0])
#[nameu, fu, tidecon, xout]=tt.t_tide(testel)

mtidecon=np.genfromtxt('tidecon.csv', dtype=None, delimiter=',')


print tidecon-mtidecon



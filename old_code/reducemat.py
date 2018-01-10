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
import h5py as h5



name='sfm6_musq2_all_cages'
lname='sfm6_musq2_all_cages_1_10000pp_s6_sink_0mm_29day'

print("Loading savelag1")
fileload=h5.File('savedir/'+name+'/'+lname+'.mat')
savelag1={}
for key in fileload['savelag'].keys():
    if 21421 in fileload['savelag'][key].shape:
        print(key)
        print(fileload['savelag'][key].shape)
        if key=='time':
            savelag1[key]=fileload['savelag'][key][:,range(0,21421,5)]
        else:
            savelag1[key]=fileload['savelag'][key][range(0,21421,5),:]        
    else:
        savelag1[key]=fileload['savelag'][key][:]
    #if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z' or i=='saverandomstate'):
        #continue



print('Saving Mat-file')
sio.savemat('savedir/'+name+'/'+lname+'_small.mat',mdict=savelag1)
print('Finished Saving')











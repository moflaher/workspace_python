# -*- coding: utf-8 -*-
"""
Front Matter
=============

Created on April 3 2014

Author: Mitchell O'Flaherty-Sproul

Load data from anal_comp.c and plot polar figure and display data below 

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


path='/home/moflaher/Desktop/anal_comp_test_case/'
name='M2'

data=np.genfromtxt(path+name+'.out',delimiter=' ',skip_footer=(1),usecols=(0,1,2,3,4,5,6,7,8))
names=np.genfromtxt(path+name+'.out',dtype=None,delimiter=' ',skip_footer=(1),usecols=(9))




fig=plt.figure()
ax=fig.add_subplot(1,1,1,polar=True)
#ax.set_theta_direction(-1)
#ax.set_theta_zero_location("N")


for x in range(0, len(data[:,1])):
  plt.plot(pi/180 *data[x,5:7],data[x,1:3],c='black')


plt.scatter(pi/180 *data[:,6],data[:,2],c='r')
plt.scatter(pi/180 *data[:,5],data[:,1],c='b',marker='x')




t=plt.title(name)
t.set_y(1.09) 
plt.subplots_adjust(top=0.86) 

fig.show()

fig.savefig('figures/png/' +name + '.png',dpi=600)

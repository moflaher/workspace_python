from __future__ import division,print_function
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
sys.path.append('/home/moe46/Desktop/school/workspace_python/ttide_py/ttide/')
sys.path.append('/home/moflaher/Desktop/workspace_python/ttide_py/ttide/')
from t_tide import t_tide
from t_predic import t_predic




oldelobc=loadnc('data/grid_stuff/',singlename='kit4_kelp_non_julian_obc.nc')
newelobc=loadnc('data/misc/baroclinic/kit4-spring-convert/',singlename='kit4-20140401-el_obc.nc')





means=np.empty((153,))
means_old=np.empty((153,))
means_new=np.empty((153,))
for i in range(153):

    tmp_tidecon=np.zeros((5,4))
    tmp_tidecon[:,0]=oldelobc['tide_Eamp'][:,i]
    tmp_tidecon[:,2]=oldelobc['tide_Ephase'][:,i]
    tp_old=t_predic(np.arange(1000),np.atleast_2d(np.array(['S2  ','M2  ','N2  ','K1  ','O1  '])).T,np.divide(1.0,oldelobc['tide_period']/3600),tmp_tidecon,synth=0)


    idx=np.array([0,1,2,4,6])
    idx=np.array([0,1,2,3,4,5,6,7])
    tmp_tidecon=np.zeros((len(idx),4))

    tmp_tidecon[:,0]=newelobc['tide_Eamp'][idx,i]
    tmp_tidecon[:,2]=newelobc['tide_Ephase'][idx,i]
    tp_new=t_predic(np.arange(1000),np.atleast_2d(np.array(['S2  ','M2  ','N2  ','K2  ','K1  ','P1  ','O1  ','Q1  '])).T,np.divide(1.0,newelobc['tide_period'][idx]/3600),tmp_tidecon,synth=0)

    means[i]=np.mean(tp_old-tp_new)
    means_old[i]=np.mean(tp_old)
    means_new[i]=np.mean(tp_new)

f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.plot(means_old,'b')
f.show()

f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.plot(means_new,'r')
f.show()

#plt.plot(means)
#plt.show()






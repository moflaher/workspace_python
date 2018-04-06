from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from folderpath import *
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pandas as pd
import netCDF4 as n4
import copy
import matplotlib.dates as dates


# Define names and types of data
namelist=['test01']
grid='sjh_lr_v1'
datatype='2d'



for name in namelist:
    print('')
    print(name)	
    try:
	out={}
        data = loadnc('/gpfs/fs1/dfo/dfo_odis/yow001/BoF/{}/output/'.format(name),grid + '_0001_SST.nc')

        savepath='{}/{}_{}/buoy/{}/'.format(datapath,grid,datatype,name)
        if not os.path.exists(savepath): os.makedirs(savepath)

	loc=[-66.096800,  45.208650]
	
	idx=closest_node(data,loc)

	out['time']=data['time']
	out['temp']=data['temp'][:,0,idx]
	np.save('{}{}_buoy_temp.npy'.format(savepath,name),out)
    except:
        continue
	









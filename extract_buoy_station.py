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
namelist=['test_fvcom41_spechum']
grid='sjh_lr_v1'
datatype='2d'



for name in namelist:
    print('')
    print(name)	
    try:
	out={}
        data = loadnc('/fs/vnas_Hdfo/odis/suh001/scratch/sjh_lr_v1/runs/{}/output/'.format(name),grid + '_station_timeseries.nc',False)

        savepath='{}/{}_{}/buoy/{}/'.format(datapath,grid,datatype,name)
        if not os.path.exists(savepath): os.makedirs(savepath)

	if 'time_JD' in data.keys():
            out['time']=678576+data['time_JD']+data['time_second']/(24*3600.0)
	else:
	    out['time']=678576+data['time']

	out['temp']=data['temp'][:,0,0]
	np.save('{}{}_buoy_temp.npy'.format(savepath,name),out)
    except:
        continue
	









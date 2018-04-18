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
name1='sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1'
grid='sjh_lr_v1'
datatype='2d'

### load the .nc file #####
data1 = loadnc('/fs/vnas_Hdfo/odis/suh001/scratch/sjh_lr_v1/runs/{}/output/'.format(name1),grid + '_station_timeseries.nc',False)

data2 = loadnc('/fs/vnas_Hdfo/odis/suh001/scratch/sjh_lr_v1/runs/sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1_jcool0/output/',grid + '_station_timeseries.nc',False)
data3 = loadnc('/fs/vnas_Hdfo/odis/suh001/scratch/sjh_lr_v1/runs/sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1_origriver_jcool0/output/',grid + '_station_timeseries.nc',False)
data4 = loadnc('/fs/vnas_Hdfo/odis/suh001/scratch/sjh_lr_v1/runs/sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1_origriver_jcool1/output/',grid + '_station_timeseries.nc',False)
data5 = loadnc('/fs/vnas_Hdfo/odis/suh001/scratch/sjh_lr_v1/runs/sjh_lr_v1_year_wet_phase1b/output/',grid + '_station_timeseries.nc',False)
data6 = loadnc('/fs/vnas_Hdfo/odis/suh001/scratch/sjh_lr_v1/runs/sjh_lr_v1_year_origbc_wet_hfx100/output/',grid + '_station_timeseries.nc',False)


f=plt.figure(figsize=(15,5))
ax=f.add_axes([.125,.1,.775,.8])
ax.plot(data1['temp'][::900,0,0],'k',label='newriver_jcool1')
ax.plot(data2['temp'][::900,0,0],'b',label='newriver_jcool0')
ax.plot(data3['temp'][::900,0,0],'r',label='oldriver_jcool0')
ax.plot(data4['temp'][::900,0,0],'g',label='oldriver_jcool1')
ax.plot(data5['temp'][::900,0,0],'m',label='wet_phase1b')
ax.plot(data6['temp'][::900,0,0],'y',label='wet_phase1a')
ax.legend()
f.savefig('figures/misc/buoy_runs.png',dpi=300)














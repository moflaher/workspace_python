from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from folderpath import *
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
from stattools import *
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
#from collections import OrderedDict


# Define names and types of data

name='sjh_lr_v1_year_wet_phase1b'
grid='sjh_lr_v1'
#name='test_wu'
#grid='sjh_lr_v1_sub'
#name='sjh_lr_v1_year_sigma_uniform_61'
#grid='sjh_lr_v1'
datatype='2d'


modpath='/mnt/drive_0/misc/gpscrsync/dataout/{}_{}/ctd/{}/'.format(grid,datatype,name)
obspath='/mnt/drive_1/obs_data/east/ctd/ctd_wcts/'
ctdnum=np.genfromtxt(obspath+'NEMO-FVCOM_SaintJohn_BOF_Observations_ctd_SABS.txt',skip_header=1,dtype=int)[:,0]

savepath='{}png/{}_{}/t_vs_s/{}/'.format(figpath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)

other={}
other['grid']=grid
other['name']=name

Tstats={}
Sstats={}
vT=OrderedDict()
f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8]);
plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc', filepath=coastpath, color='k', fill=True)
for num in ctdnum:
    print(num)
    try:
        mod=load_ctd_mod('{}ctd_timeseries_{}.txt'.format(modpath,num))
        obs=load_ctd_obs('{}{}_ctd.dat'.format(obspath,num))
        other['dt']=(mod['arrays']['time'][0,1]-mod['arrays']['time'][0,0])*24*60
        other['num']=num
        tidx=np.argmin(np.fabs(mod['arrays']['time'][0,:]-obs['time']))
        other['tidx']=tidx
        
        #for i in range(mod['arrays']['depth'].shape[1]):
        Tmod=ipt.interp1d(-1*mod['arrays']['depth'][:,tidx],mod['arrays']['temperature'][:,tidx],obs['Depth'])
        Smod=ipt.interp1d(-1*mod['arrays']['depth'][:,tidx],mod['arrays']['salinity'][:,tidx],obs['Depth'])

        cTmod, cTobs = remove_common_nan(Tmod,obs['Temp'])
        cSmod, cSobs = remove_common_nan(Smod,obs['Salinity'])

       
        other['filename']='{}ctd_t_vs_s_{}.png'.format(savepath,num)
        #plot_tsmap2(mod,obs,other,Tstats,Sstats)

        
        f=plt.figure(figsize=(4,4))
        ax=f.add_axes([.15,.15,.75,.75])
        ax.plot(mod['arrays']['temperature'],mod['arrays']['salinity'],'b')
        ax.plot(obs['Temp'],obs['Salinity'],'r')
        f.savefig(other['filename'],dpi=300)
        plt.close('all')
        
       
    except:
        print('Pass on {}'.format(num))
        pass


	








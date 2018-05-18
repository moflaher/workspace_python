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
#namelist=['sjh_lr_v1_year_coare3','sjh_lr_v1_year_coare3_wu_mixing','sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1','sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1_jcool0']
namelist=['test_fvcom41_spechum']
grid='sjh_lr_v1'
datatype='2d'


st=2208
st=0
cut=13700
df=pd.read_csv('~/scratch/obs/misc/SA_Saint_John_Buoy_03152015_04302016.csv')
time=np.array(dates.datestr2num(df.values[st:cut,0].astype(str)))
temp=df.values[st:cut,8].astype(float)

months = dates.MonthLocator()
monthsFmt = dates.DateFormatter('%b')

for name in namelist:
    try:
        print('')
        print(name)

        savepath='{}png/{}_{}/buoy/{}/'.format(figpath,grid,datatype,name)
	if not os.path.exists(savepath): os.makedirs(savepath)
	
        
        inpath='{}/{}_{}/buoy/{}/'.format(datapath,grid,datatype,name)
        out=np.load('{}{}_buoy_temp.npy'.format(inpath,name))
        out=out[()]

        
        idx=np.argwhere((out['time']>=time[0])&(out['time']<=time[-1]))
        timed=out['time'][idx]        
        tempd=out['temp'][idx]

        itemp=ipt.interp1d(time[~np.isnan(temp)],temp[~np.isnan(temp)],timed)

        f=plt.figure(figsize=(15,5))
        ax=f.add_axes([.125,.1,.775,.8])
        ax.plot(timed, itemp,'k',label='Buoy')
        ax.plot(timed,tempd,lw=.5,label=name)
        ax.xaxis.set_major_locator(months)
	ax.xaxis.set_major_formatter(monthsFmt)
	ax.legend()
	#ax.set_ylabel('SST ($^{\circ}C$)')
	#ax.set_xlabel('2015-2016')
        f.savefig('{}{}_buoy_compare.png'.format(savepath,name),dpi=300)

	diff=itemp-tempd

	print(np.fabs(diff).mean())
	print(diff.mean())

    except:
        continue
	










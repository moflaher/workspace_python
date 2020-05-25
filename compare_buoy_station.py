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
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
import pandas as pd
import netCDF4 as n4
import copy
import matplotlib.dates as dates
from collections import OrderedDict

# Define names and types of data
#namelist=['sjh_lr_v1_year_coare3','sjh_lr_v1_year_coare3_wu_mixing','sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1','sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1_jcool0']
name='test_1'
grid='sjh_lr_v1_sub'



st=2208
st=0
cut=13700
df=pd.read_csv('data/nemofvcom/SA_Saint_John_Buoy_03152015_04302016.csv')

time=np.array(dates.datestr2num(df.values[:,0].astype(str)))
temp=df.values[:,8].astype(float)


st=dates.datestr2num('20150501')
et=dates.datestr2num('20151228')
idx=np.argwhere((time>=st) & (time<=et))

time=time[idx]
temp=temp[idx]

time=time[~np.isnan(temp)]
temp=temp[~np.isnan(temp)]


inpath='{}/{}_{}/buoy/{}/'.format(datapath,grid,datatype,name)
out=np.load('{}{}_buoy_temp.npy'.format(inpath,name))
out=out[()]



mod=ipt.interp1d(out['time'],out['temp'],time)
obs=temp


stats={}
stats['fvcom_1m']=OrderedDict()
stats['fvcom_1m']=residual_stats(mod,obs)


timeh=dates.drange(dates.num2date(time[0]),dates.num2date(time[-1]),dates.datetime.timedelta(0,3600))
modh=ipt.interp1d(out['time'],out['temp'],timeh)
obsh=ipt.interp1d(time,temp,timeh)

stats['fvcom_60m']=OrderedDict()
stats['fvcom_60m']=residual_stats(modh,obsh)


stats['nemo']=OrderedDict()
stats['nemo']['meansl']=.07
stats['nemo']['stdsl']=1.04
stats['nemo']['rmsesl']=1.04
stats['nemo']['relaverr']=5.7
stats['nemo']['corsl']=.94
stats['nemo']['skewsl']=-.15
stats['nemo']['skill']=.97

stats['fvcom']=OrderedDict()
stats['fvcom']['meansl']=.83
stats['fvcom']['stdsl']=.89
stats['fvcom']['rmsesl']=1.22
stats['fvcom']['relaverr']=7.96
stats['fvcom']['corsl']=.96
stats['fvcom']['skewsl']=-.29
stats['fvcom']['skill']=.96

stats['riops']=OrderedDict()
stats['riops']['meansl']=.01
stats['riops']['stdsl']=1.63
stats['riops']['rmsesl']=1.63
stats['riops']['relaverr']=12.24
stats['riops']['corsl']=.89
stats['riops']['skewsl']=-.36
stats['riops']['skill']=.94


print(name)

df=pd.DataFrame(stats).T#,columns=['meansl','stdsl','rmsesl','relaverr','corsl','skewsl','skill']).T
df=df[['meansl','stdsl','rmsesl','relaverr','corsl','skewsl','skill']]
df=df.reindex(['nemo','fvcom','riops','fvcom_1m','fvcom_60m'])
print(df.round(2))

savepath='{}png/{}_{}/buoy/{}/'.format(figpath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)
months = dates.MonthLocator()
monthsFmt = dates.DateFormatter('%b')


f=plt.figure(figsize=(10,5))
ax=f.add_axes([.125,.1,.775,.8])
ax.plot(time, temp,'k',lw=.5,label='Buoy')
ax.plot(time,mod,'b',lw=.5,label=name)
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
ax.legend()
#ax.set_ylabel('SST ($^{\circ}C$)')
#ax.set_xlabel('2015-2016')
f.savefig('{}{}_buoy_stats.png'.format(savepath,name),dpi=300)


	








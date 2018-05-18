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
from collections import OrderedDict


# Define names and types of data
name='sjh_lr_v1_year_origbc_wet_hfx100'
#name='sjh_hr_v3_year_wet'
grid='sjh_lr_v1'
datatype='2d'
print(name)

### load the .nc file #####
data = loadnc('/mnt/drive_0/misc/gpscrsync/sjh_lr_v1_year_origbc_wet_hfx100/output/',grid + '_station_timeseries.nc',False)
#data = loadnc('/fs/vnas_Hdfo/odis/mif001/scratch/sjh_lr_v1_sub/{}/output/'.format(name),grid + '_station_timeseries.nc',False)
#data = loadnc('/gpfs/fs1/dfo/dfo_odis/yow001/BoF/{}/output/'.format(name),grid + '_station_timeseries.nc',False)
data['lon']=data['lon']-360
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])

print('done load')

print('processing time')
#for j in range(int((len(data['time_JD'])/10000)+1)):
#    test=np.divide(data['time_second'][j*10000:(j+1)*10000],86400.0)
#    print(j)
if 'time_JD' in data.keys():
    #num=int(len(data['time_JD'])/len(np.arange(0,86400,60)))
    #ts=np.append(np.arange(data['time_second'][0],86400,60)/86400.0,np.tile(np.arange(0,86400,60)/86400.0,num))
    #lmin=np.hstack([len(data['time_JD']),len(ts)]).min()-10
    #data['time']=data['time_JD'][:lmin]+ts[:lmin]+678576
    data['time']=data['time_JD']+(data['time_second']/86400.0)+678576
    data['dTimes']=dates.num2date(data['time'])
    data['Time']=np.array([ct.isoformat(sep=' ')[:19] for ct in data['dTimes']])
else:
    data['time']=data['time']+678576
    data['dTimes']=dates.num2date(data['time'])
    data['Time']=np.array([ct.isoformat(sep=' ')[:19] for ct in data['dTimes']])


print('done time')

filenames=glob.glob('/mnt/drive_1/obs_data/east/adcp/*.npy')
filenames.sort()

savepath='{}/{}_{}/adcp/{}/'.format(datapath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)

names=np.array([''.join(data['name_station'][j,:]).strip() for j,n in enumerate(data['name_station'])])

for i,filename in enumerate(filenames):
    print('='*80)
    print(i)
    print(filename)
    
    adcp = np.load(filename)
    adcp = adcp[()]
    
    lon=adcp['lon'][0,0]
    lat=adcp['lat'][0,0]  
    time=dates.datestr2num(adcp['time']['Times'])
    
    #idx=np.argmin(((data['lon']-lon)**2 + (data['lat']-lat)**2))
    try:
        idx=np.argwhere(names=='ADCP_{}'.format(adcp['metadata']['ADCP_number']))[0,0]
    except:
        continue
    #expand time window by +-3 hours, should means this works for ctd as well
    tidx=np.argwhere((data['time']>=(time[0]-(3.0/24.0)))&(data['time']<=(time[-1]+(3.0/24.0))))
    
    name=''.join(data['name_station'][idx,:])
    print(name)
    if name[5:8]!=str(adcp['metadata']['ADCP_number']):
        print('Bad ADCP_number match skipping')
        continue
    
    out=OrderedDict()
    out['time']=data['time'][tidx]
    out['Time']=data['Time'][tidx]
    print('Extracted time')
    
    out['h']=data['h'][idx]
    out['zeta']=data['zeta'][tidx,idx]
    out['ua']=data['ua'][tidx,idx]
    out['va']=data['va'][tidx,idx]
    print('Extracted 2d')
    
    out['u']=data['u'][tidx,:,idx]
    out['v']=data['v'][tidx,:,idx]
    out['ww']=data['ww'][tidx,:,idx]
    out['temp']=data['temp'][tidx,:,idx]
    out['salinity']=data['salinity'][tidx,:,idx]
    print('Extracted 3d')
    
    out['siglev']=data['siglev'][:,idx]
    out['siglay']=data['siglay'][:,idx]
    out['lon']=data['lon'][idx]
    out['lat']=data['lat'][idx]
    out['name_station']=data['name_station'][idx,:]
    print('Extracted misc')
    
    for key in out:
        out[key]=np.squeeze(out[key])
    
    savepath2='{}{}'.format(savepath,''.join(data['name_station'][idx,:]).strip())
    if not os.path.exists(savepath2): os.makedirs(savepath2)
    np.save('{}/{}_model_ministation.npy'.format(savepath2,''.join(data['name_station'][idx,:]).strip()),out)
    print('Saved')








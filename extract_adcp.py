from __future__ import division,print_function
import numpy as np
import scipy as sp
from mytools import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import os, sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pandas as pd
import matplotlib.dates as dates
import argparse
from collections import OrderedDict



parser = argparse.ArgumentParser()
parser.add_argument("grid", help="name of the grid", type=str)
parser.add_argument("name", help="name of the run", type=str)
parser.add_argument("--fvcom", help="switch to fvcom instead of station", default=False,action='store_true')
parser.add_argument("-ncfile", help="manual specify ncfile", type=str, default=None)
args = parser.parse_args()

print("The current commandline arguments being used are")
print(args)

name=args.name
grid=args.grid
datatype='2d'


### load the .nc file #####
if args.fvcom:
    tag='0001.nc'
else:
    tag='station_timeseries.nc'

if args.ncfile is None:
    args.ncfile='{}/{}/runs/{}/output/{}_{}'.format(grid,tag)

ncfile=args.ncfile
ncloc=ncfile.rindex('/')

if args.fvcom:
    data = loadnc(ncfile[:ncloc+1],ncfile[ncloc+1:])
else:
    data = loadnc(ncfile[:ncloc+1],ncfile[ncloc+1:],False)
    data['lon']=data['lon']-360
    data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
print('done load')

if 'time_JD' in data.keys():
    data['time']=data['time_JD']+(data['time_second']/86400.0)+678576
else:
    data['time']=data['time']+678576
    
if not 'Time' in data.keys():
    data['dTimes']=dates.num2date(data['time'])
    data['Time']=np.array([ct.isoformat(sep=' ')[:19] for ct in data['dTimes']])
print('done time')

filenames=glob.glob('{}east/adcp/*.npy'.format(obspath))
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
        idx=np.argwhere(names=='{}'.format(adcp['metadata']['ADCP_number']))[0,0]
    except:
	print('ADCP not found')        
	continue
    #expand time window by +-3 hours, should means this works for ctd as well
    tidx=np.argwhere((data['time']>=(time[0]-(3.0/24.0)))&(data['time']<=(time[-1]+(3.0/24.0))))
    
    name=''.join(data['name_station'][idx,:])
    print(name)
    if name[:3]!=str(adcp['metadata']['ADCP_number']):
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
    
    savepath2='{}ADCP_{}'.format(savepath,''.join(data['name_station'][idx,:]).strip())
    if not os.path.exists(savepath2): os.makedirs(savepath2)
    np.save('{}/ADCP_{}_model_ministation.npy'.format(savepath2,''.join(data['name_station'][idx,:]).strip()),out)
    print('Saved')








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
parser.add_argument("ncfile", help="specify ncfile", type=str)
parser.add_argument("--station", help="switch to station output instead of fvcom output", default=False,action='store_true')
parser.add_argument("-dist", help="max distance from obs to be allowed", type=float,default=10000)
args = parser.parse_args()

print("The current commandline arguments being used are")
print(args)

name=args.name
grid=args.grid
ncfile=args.ncfile
ncloc=ncfile.rindex('/')

if args.station:
    data = loadnc(ncfile[:ncloc+1],ncfile[ncloc+1:],False)
    data['lon']=data['lon']-360
    data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
    x,y=data['x'],data['y']
    lon,lat=data['lon'],data['lat']
    tag='station'
    if 'time' in data:
        data['time']=data['time']+678576
    #older station files    
    if 'time_JD' in data:
        data['time']=data['time_JD']+(data['time_second']/86400.0)+678576        
    data['dTimes']=dates.num2date(data['time'])
    data['Time']=np.array([ct.isoformat(sep=' ')[:19] for ct in data['dTimes']])
else:
    data = loadnc(ncfile[:ncloc+1],ncfile[ncloc+1:])
    lon,lat=data['lonc'],data['latc']
    x,y=data['xc'],data['yc']
    tag='fvcom'   

print('done load')

# find adcp ncfiles
filenames=glob.glob('{}east/all/adcp_*.nc'.format(obspath))
filenames.sort()

#create location to save model ncfiles
savepath='{}/{}/adcp/{}/'.format(datapath,grid,name)
if not os.path.exists(savepath): os.makedirs(savepath)


for i,filename in enumerate(filenames):
    print('='*80)
    print(i)
    print(filename)
    
    adcp = loadnc('',filename,False)

    lona=adcp['lon']
    lata=adcp['lat'] 
    time=adcp['time']
    adcp['x'],adcp['y']=data['proj'](lona,lata)

    dist=np.sqrt((x-adcp['x'])**2+(y-adcp['y'])**2)
    idx=np.argmin(dist)

    #expand time window by +-3 hours, to ensure we have all we need
    tidx=np.argwhere((data['time']>=(time[0]-(3.0/24.0)))&(data['time']<=(time[-1]+(3.0/24.0))))
    
    #skip observation if no matching time or to far away
    if dist[idx]>args.dist:
        print('Skipping {}, over {} away'.format(filename.split('/')[-1],args.dist))
        continue
    if len(tidx)==0:
        print('Skipping {}, no time match'.format(filename.split('/')[-1]))
        continue
    
    out=OrderedDict()
    out['time']=data['time'][tidx]
    out['Time']=data['Time'][tidx]
    print('Extracted time')
    
    if 'station' in tag:
        out['h']=data['h'][idx].mean()
        out['zeta']=data['zeta'][tidx,idx].mean(axis=1)   
    else:
        out['h']=data['h'][data['nv'][idx,:]].mean()
        out['zeta']=data['zeta'][tidx,data['nv'][idx,:]].mean(axis=1)
    out['ua']=data['ua'][tidx,idx]
    out['va']=data['va'][tidx,idx]
    print('Extracted 2d')
    
    out['u']=data['u'][tidx,:,idx]
    out['v']=data['v'][tidx,:,idx]
    out['ww']=data['ww'][tidx,:,idx]
    #out['temp']=data['temp'][tidx,:,data['nv'][:,idx]].mean(axis=1)
    #out['salinity']=data['salinity'][tidx,:,data['nv'][:,idx]].mean(axis=1)
    print('Extracted 3d')
    
    #out['siglev']=data['siglev'][:,idx]
    out['siglay']=data['siglay'][:,0]
    out['lon']=lon[idx]
    out['lat']=lat[idx]
    out['ADCP_number']=filename.split('.')[0].split('/')[-1].split('_')[-1]
    out['dist']=dist[idx]    
    print('Extracted misc')
    
    for key in out:
        out[key]=np.squeeze(out[key])
    
    savepath2='{}{}_{}.nc'.format(savepath,filename.split('.')[0].split('/')[-1],tag)
    save_adcpnc(out,savepath2)
    
    print('Saved')







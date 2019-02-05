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
parser.add_argument("-fake", help="define a fake adcp", type=str,default=None,nargs=4)
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
    lon,lat=data['lon'],data['lat']
    x,y=data['x'],data['y']
    tag='fvcom'   

print('done load')


# find adcp ncfiles
if args.fake is None:
    filenames=glob.glob('{}east/all/tg_*.nc'.format(obspath))
    filenames.sort()
else:
    print('Using specified fake tg')
    filenames=['fake_tg_{}_{}_{}_{}.nc'.format(args.fake[0],args.fake[1],args.fake[2],args.fake[3])]


#create location to save model ncfiles
savepath='{}/{}/tg/{}/'.format(datapath,grid,name)
if not os.path.exists(savepath): os.makedirs(savepath)


for i,filename in enumerate(filenames):
    print('='*80)
    print(i)
    print(filename)
    
    if args.fake is None:    
        tg = loadnc('',filename,False)
    else:
        tg={}
        tg['lon']=args.fake[0]
        tg['lat']=args.fake[1]
        tg['time']=np.array([dates.datestr2num(args.fake[2]),dates.datestr2num(args.fake[3])])
    
    lona=tg['lon']
    lata=tg['lat'] 
    time=tg['time']
    tg['x'],tg['y']=data['proj'](lona,lata)

    dist=np.sqrt((x-tg['x'])**2+(y-tg['y'])**2)
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
    
    out['h']=data['h'][idx]
    out['zeta']=data['zeta'][tidx,idx]
    print('Extracted 2d')
    
    out['lon']=lon[idx]
    out['lat']=lat[idx]
    out['tg_number']=filename.split('.')[0].split('/')[-1].split('_')[-1]
    out['dist']=dist[idx]    
    print('Extracted misc')
    
    for key in out:
        out[key]=np.squeeze(out[key])
    
    savepath2='{}{}_{}.nc'.format(savepath,filename[:filename.rfind('.')].split('/')[-1],tag)
    save_tgnc(out,savepath2)
    
    print('Saved')







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
parser.add_argument("-snr", help="signal to noise ratio value used for constituent cutoff", type=float,default=2.0)
args = parser.parse_args()

print("The current commandline arguments being used are")
print(args)

name=args.name
grid=args.grid
ncfile=args.ncfile
ncloc=ncfile.rindex('/')
snr=args.snr

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

# find wlev ncfiles
filenames=glob.glob('{}east/all/wlev_*.nc'.format(obspath))
filenames.sort()

#create location to save model ncfiles
savepath='{}/{}/wlev/{}/'.format(datapath,grid,name)
if not os.path.exists(savepath): os.makedirs(savepath)


for i,filename in enumerate(filenames):
    print('='*80)
    print(i)
    print(filename)
    
    wlev = loadnc('',filename,False)

    lona=wlev['lon']
    lata=wlev['lat'] 
    days=wlev['days']
    wlev['x'],wlev['y']=data['proj'](lona,lata)

    dist=np.sqrt((x-wlev['x'])**2+(y-wlev['y'])**2)
    idx=np.argmin(dist)

    #skip observation if no matching time or to far away
    if dist[idx]>args.dist:
        print('Skipping {}, over {} away'.format(filename.split('/')[-1],args.dist))
        continue

    #remove first 2 weeks to ensure spin up
    tidxall=np.argwhere(data['time']>=data['time'][0]+14.0).flatten()
    
    #find the total days    
    totaldays=data['time'][tidxall[-1]]-data['time'][tidxall[0]]
    
    outpre=run_ttide(data['time'][tidxall],data['zeta'][tidxall,idx],data['lat'][idx])
    outall=dict(run_ttide(data['time'][tidxall],data['zeta'][tidxall,idx],data['lat'][idx],outpre['nameu'][outpre['snr']>=snr]))
    
    d3=np.floor(days/3)
    dr=np.floor(totaldays/d3)
    print('Running ttide for {} days of {} days every {} days, {} times'.format(days,totaldays,d3,dr))
    
    cons=np.array([])
    for i in range(dr):
        tidx=np.argwhere((data['time']>=data['time'][0]+14.0+(i*d3)) & (data['time']<=data['time'][0]+14.0+(i*d3)+days)).flatten()
        if data['time'][tidx[-1]]-data['time'][tidx[0]] == days:
            o=run_ttide(data['time'][tidx],data['zeta'][tidx,idx],data['lat'][idx])
            cons=np.unique(np.append(cons,o['nameu'][o['snr']>=snr]))
    
    os={}
    for i in range(dr):
        print(i)
        tidx=np.argwhere((data['time']>=data['time'][0]+14.0+(i*d3)) & (data['time']<=data['time'][0]+14.0+(i*d3)+days)).flatten()
        if data['time'][tidx[-1]]-data['time'][tidx[0]] == days:
            os[str(i)]=dict(run_ttide(data['time'][tidx],data['zeta'][tidx,idx],data['lat'][idx],cons))
            
            
    #rtide=np.stack([os[key]['tidecon'] for key in os])

    
    out=OrderedDict()
    out['time']=data['time'][tidxall]
    out['Time']=data['Time'][tidxall]
    print('Extracted time')
    
    out['h']=data['h'][idx]
    out['zeta']=data['zeta'][tidxall,idx]
    print('Extracted 2d')
    
    out['lon']=lon[idx]
    out['lat']=lat[idx]
    out['wlev_number']=filename.split('.')[0].split('/')[-1].split('_')[-1]
    out['dist']=dist[idx]   
    out['snr']=snr 
    print('Extracted misc')
    
    for key in out:
        out[key]=np.squeeze(out[key])
    
    out['ttideall']=outall
    out['rtide']=os   
    print('Calculated ttide')
    

    
    savepath2='{}{}_{}_snr_{}.nc'.format(savepath,filename.split('.')[0].split('/')[-1],tag,snr)
    save_wlevnc(out,savepath2)
    
    print('Saved')






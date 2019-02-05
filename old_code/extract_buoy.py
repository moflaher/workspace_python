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


savepath='{}/{}_{}/buoy/{}/'.format(datapath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)



out={}
out['time']=data['time']

loc=np.array([-66.0968,45.20865])
idx=np.argmin((data['lon']-loc[0])**2+(data['lat']-loc[1])**2)

out['temp']=data['temp'][:,0,idx]

np.save('{}{}_buoy_temp.npy'.format(savepath,name),out)

	









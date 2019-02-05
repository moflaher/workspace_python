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


ctdbio=pd.read_csv('/home/suh001/data/NEMO-FVCOM_SaintJohn_BOF_Observations_ctd_BIO.txt',delimiter=' ')
ctdsabs=pd.read_csv('/home/suh001/data/NEMO-FVCOM_SaintJohn_BOF_Observations_ctd_SABS.txt',delimiter=' ')

lon=np.append(ctdbio['lon'],ctdsabs['lon'])
lat=np.append(ctdbio['lat'],ctdsabs['lat'])
deploy=np.append(ctdbio['deploy'],ctdsabs['deploy'])
Time=np.append(['{} {}'.format(ctdbio['date'][i],ctdbio['time'][i]) for i in range(len(ctdbio['lon']))],
                ['{} {}'.format(ctdsabs['date'][i],ctdsabs['time'][i]) for i in range(len(ctdsabs['lon']))])
time=dates.datestr2num(Time)


savepath='{}/{}_{}/ctd/{}/'.format(datapath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)


for i,dep in enumerate(deploy):
    print('='*80)
    print(i)
    print(dep)
    xloc,yloc = data['proj'](lon[i],lat[i])

    dist=np.sqrt((data['x']-xloc)**2+(data['y']-yloc)**2)
    asort=np.argsort(dist)
    node=asort[0]

    print(node)
    print(dist[node])

    #extract timeseries
    tidx=np.argwhere((data['time']>=time[i]-3/24.0) &(data['time']<=time[i]+3/24.0) )
    temp=data['temp'][tidx,:,node]
    sal=data['salinity'][tidx,:,node]
    d=(data['zeta'][tidx,node]+data['h'][node])*data['siglay'][:,0]
    
    fp=open('{}ctd_timeseries_{}.txt'.format(savepath,deploy[i]),'w')
    fp.write('node it latitude longitue date time depth temperature salinity\n')
    for k,t in enumerate(tidx):
        for j,tem in enumerate(temp[k,0,]):
            fp.write('{} {} {} {} {} {} {} {} {}\n'.format(node+1,t[0],data['lat'][node],data['lon'][node],data['Time'][t[0]][:10],data['Time'][t[0]][11:19],d[k,j],temp[k,0,j],sal[k,0,j]))
    fp.close()


    #extract single profile
    tidx=np.argmin(np.fabs(data['time']-time[i]))
    temp=data['temp'][tidx,:,node]
    sal=data['salinity'][tidx,:,node]
    d=(data['zeta'][tidx,node]+data['h'][node])*data['siglay'][:,0]
    
    fp=open('{}ctd_{}.txt'.format(savepath,deploy[i]),'w')
    fp.write('node latitude longitue date time depth temperature salinity\n')
    for j,tem in enumerate(temp):
        fp.write('{} {} {} {} {} {} {} {}\n'.format(node+1,data['lat'][node],data['lon'][node],data['Time'][tidx][:10],data['Time'][tidx][11:19],d[j],temp[j],sal[j]))
    fp.close()



    #extract zeta
    tidx=np.argwhere((data['time']>=time[i]-1.0) &(data['time']<=time[i]+1.0) )
    z=data['zeta'][tidx,node]
    print(z.shape)
    fp=open('{}ctd_zeta_{}.txt'.format(savepath,deploy[i]),'w')
    fp.write('node it latitude longitue date time zeta\n')
    for k,t in enumerate(tidx):
        fp.write('{} {} {} {} {} {} {}\n'.format(node+1,t[0],data['lat'][node],data['lon'][node],data['Time'][t[0]][:10],data['Time'][t[0]][11:19],z[k][0]))
    fp.close()






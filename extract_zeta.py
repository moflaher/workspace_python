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


wetnodes=data['wet_nodes'][:]
time=data['time'][:]
zeta=data['zeta'][:]
locations=np.loadtxt('tcon.csv')

savepath='{}/{}_{}/zeta/{}/'.format(datapath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)


for i,loc in enumerate(locations):
    print('='*80)
    print(i)
    xloc,yloc = data['proj'](loc[2],loc[1])
    #xl,yl = data['proj'](xloc-5000,yloc-5000,inverse=True)
    #xr,yr = data['proj'](xloc+5000,yloc+5000,inverse=True)
    #region={}
    #region['region']=np.array([xl,xr,yl,yr])


    dist=np.sqrt((data['x']-xloc)**2+(data['y']-yloc)**2)
    asort=np.argsort(dist)
    close=0
    while np.sum(wetnodes[:,asort[close]])<len(time):
	close+=1

    node=asort[close]

    print(close)
    print(dist[node])

    #nidx=get_nodes(data,region)
    #if len(nidx)==0:
    #    f,ax=plottri(data,data['h'],show=False)
    #else:	
    #    f,ax=plottri(data,data['h'],minmax=[data['h'][nidx].min(), data['h'][nidx].max()],show=False)
    #prettyplot_ll(ax,setregion=region)
    #plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc',filepath=coastpath, color='k', fcolor='0.75', fill=True)  
    #ax.plot(loc[2],loc[1],'k*',markersize=10)
    #ax.plot(data['lon'][node],data['lat'][node],'r*',markersize=10,alpha=.5)
    #f.savefig('{}{}_{}_{}_dist_{:.2f}_depth.png'.format(savepath,loc[0].astype(int),loc[2],loc[1],dist[node]),dpi=600)
    #plt.close(f)

    #zeta=ipt.interpN_at_loc(data,'zeta',[loc[2],loc[1]])
    #zetac=zeta[starttime:endtime]
    zetac=zeta[:,node]

    df=pd.DataFrame(np.vstack([tclean,zetac]).T,columns=['time','zeta'])
    df.to_csv('{}{}_{}_{}_dist_{:.2f}_{}.csv'.format(savepath,loc[0].astype(int),loc[2],loc[1],dist[node],node))
























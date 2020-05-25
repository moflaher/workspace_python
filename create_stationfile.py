from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from folderpath import *
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
from stattools import *
from fvcomtools import *
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
import argparse




parser = argparse.ArgumentParser()
parser.add_argument("neifile", help="neifile (path name)", type=str)
parser.add_argument("stationfile", help="stationfile (path name)", type=str)
parser.add_argument("-dist", help="max distance allowed", type=float,default=10000)
parser.add_argument("-type", help="stationfile (path name)", type=str,default='cell')
args = parser.parse_args()

print("The current commandline arguments being used are")
print(args)

filenames=glob.glob('{}east/all/*.nc'.format(obspath))
filenames.sort()
data=load_nei2fvcom(args.neifile)
name=args.stationfile[:args.stationfile.find('.')]


sdata=OrderedDict()

if 'cell' in args.type:
    lon=data['uvnodell'][:,0]
    lat=data['uvnodell'][:,1]
else:
    lon=data['nodell'][:,0]
    lat=data['nodell'][:,1]  
    
x,y,proj=lcc(lon,lat)

for i,filename in enumerate(filenames):
    
    odata=loadnc('',filename,False)
    xo,yo = proj(odata['lon'],odata['lat'])
    
    
    dist=np.sqrt((x-xo)**2+(y-yo)**2)
    idx=np.argmin(dist)
    
    if dist[idx]>args.dist:
        continue
    
    key=filename.split('/')[-1].split('.')[0] 
    sdata[key]=np.array([lon[idx],lat[idx],idx+1,dist[idx]])
    
    print(100*(i+1)/len(filenames))



f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.triplot(data['trigrid'],color='k',lw=.05)
for key in sdata:
    cax=ax.scatter(sdata[key][0],sdata[key][1],c=sdata[key][3],s=10,edgecolor=None,vmin=0,vmax=args.dist,zorder=100)    
plt.colorbar(cax)
f.savefig('{}_obs_dist.png'.format(name),dpi=600)




f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.triplot(data['trigrid'],color='k',lw=.05)

keys=sdata.keys()
ll=np.array([s[1][:2] for s in sdata.items()])

idx=np.array(['adcp' in k for k in keys])
ax.plot(ll[idx,0],ll[idx,1],'r*',markersize=5,zorder=100,label='adcp')
idx=np.array(['tg' in k for k in keys])
ax.plot(ll[idx,0],ll[idx,1],'.',color='darkgreen',markersize=5,zorder=110,label='tg',markeredgecolor='k')
idx=np.array(['wlev' in k for k in keys])
ax.plot(ll[idx,0],ll[idx,1],'>',color='darkgreen',markersize=5,zorder=80,label='wlev')
idx=np.array(['ctd' in k for k in keys])
ax.plot(ll[idx,0],ll[idx,1],'d',color='b',markersize=5,zorder=90,label='ctd')   
idx=np.array(['buoy' in k for k in keys])
ax.plot(ll[idx,0],ll[idx,1],'.',color='m',markersize=5,zorder=120,label='buoy') 
ax.legend()
f.savefig('{}_obs_types.png'.format(name),dpi=600)




save_stationfile(sdata,args.stationfile)










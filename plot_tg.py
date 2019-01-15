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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pandas as pd
import netCDF4 as n4
import copy
import matplotlib.dates as dates
import argparse




parser = argparse.ArgumentParser()
parser.add_argument("grid", help="name of the grid", type=str)
parser.add_argument("name", help="name of the run", type=str,default=None, nargs='?')
parser.add_argument("--station", help="switch to station output instead of fvcom output", default=False,action='store_true')
parser.add_argument("-dates", help="specify start and end date",type=str,nargs=2,default=None)
args = parser.parse_args()

print("The current commandline arguments being used are")
print(args)


name=args.name
grid=args.grid


if args.station:
    tag='station'
else:
    tag='fvcom'  

# find tg ncfiles


months = dates.MonthLocator()
monthsFmt = dates.DateFormatter('%b')

savepath='{}png/{}/tg/{}/'.format(figpath,grid,name)
if not os.path.exists(savepath): os.makedirs(savepath)


inpath='{}{}/tg/{}/'.format(datapath,grid,name)
filenames=glob.glob('{}tg_*_{}.nc'.format(inpath,tag))
filenames.sort()


#tg_*.nc'.format(obspath)

for i,filename in enumerate(filenames):
    print('='*80)
    print(i)
    print(filename)
    
    tgm = loadnc('',filename,False)    
    tgo = loadnc('{}east/all/'.format(obspath),'tg_{:05d}.nc'.format(tgm['tgnumber'][0]),False)


    if args.dates is not None:
        din=dates.datestr2num(args.dates)
        figstr='{}{}_{}_tg_{:05d}_{}_to_{}.png'.format(savepath,grid,name,tgm['tgnumber'][0],args.dates[0],args.dates[1])
    else:
        din=np.array([tgo['time'][0],tgo['time'][-1]])
        figstr='{}{}_{}_tg_{:05d}.png'.format(savepath,grid,name,tgm['tgnumber'][0])
        
    idx=np.argwhere((tgo['time']>=din[0]) & (tgo['time']<=din[1]))

    time1,data1,data2=interp_clean_common(tgo['time'][idx],tgo['zeta'][idx],tgm['time'],tgm['zeta'],500,-500)
    stats=residual_stats(data2-np.mean(data2), data1-np.mean(data1))
    a=pd.DataFrame(stats,index=[0]).round(2).T[0]

    f=plt.figure(figsize=(15,5)); 
    ax=f.add_axes([.125,.1,.775,.8]);
    ax.plot(time1,data1-np.mean(data1),'k',label='TG: {:05d}'.format(tgm['tgnumber'][0]))
    ax.plot(time1,data2-np.mean(data2),'r',lw=.5,label='{}'.format(name))
    ax.legend()    
    f.suptitle('Removed TG means - Obs: {}     Model: {}\n Bias: {}   Std: {}   RMSE: {}   RAE: {}   Corr: {}   Skew: {}   Skill: {}'.format(np.mean(data1),np.mean(data2),a[0],a[1],a[2],a[3],a[4],a[5],a[6]))
    f.savefig(figstr,dpi=600)
    
    
    #kill














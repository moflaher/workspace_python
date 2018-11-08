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
import argparse




parser = argparse.ArgumentParser()
parser.add_argument("grid", help="name of the grid", type=str)
parser.add_argument("name", help="name of the run", type=str,default=None, nargs='?')
args = parser.parse_args()

print("The current commandline arguments being used are")
print(args)


grid=args.grid
if args.name is None:
    tempa='ls {}/{}_{}/ctd/'.format(datapath,grid,'2d')
    print('\n Model names available:')
    os.system('{}'.format(tempa))
    print('\n')
    sys.exit()
else:
    name=args.name

datatype='2d'


st=2208
st=0
cut=13700
df=pd.read_csv('{}/misc/SA_Saint_John_Buoy_03152015_04302016.csv'.format(obspath))
time=np.array(dates.datestr2num(df.values[st:cut,0].astype(str)))
temp=df.values[st:cut,8].astype(float)

months = dates.MonthLocator()
monthsFmt = dates.DateFormatter('%b')

savepath='{}png/{}_{}/buoy/{}/'.format(figpath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)


inpath='{}/{}_{}/buoy/{}/'.format(datapath,grid,datatype,name)
out=np.load('{}{}_buoy_temp.npy'.format(inpath,name))
out=out[()]


idx=np.argwhere((out['time']>=time[0])&(out['time']<=time[-1]))
timed=out['time'][idx]        
tempd=out['temp'][idx]

itemp=ipt.interp1d(time[~np.isnan(temp)],temp[~np.isnan(temp)],timed)

f=plt.figure(figsize=(15,5))
ax=f.add_axes([.125,.1,.775,.8])
ax.plot(timed, itemp,'k',label='Buoy')
ax.plot(timed,tempd,lw=.5,label=name)
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
ax.legend()
#ax.set_ylabel('SST ($^{\circ}C$)')
#ax.set_xlabel('2015-2016')
f.savefig('{}{}_buoy_compare.png'.format(savepath,name),dpi=300)

diff=itemp-tempd

print(np.fabs(diff).mean())
print(diff.mean())












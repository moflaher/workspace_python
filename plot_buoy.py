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
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
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


grid=args.grid
if args.name is None:
    tempa='ls {}{}/buoy/'.format(datapath,grid)
    print('\n Model names available:')
    os.system('{}'.format(tempa))
    print('\n')
    sys.exit()
else:
    name=args.name


if args.station:
    tag='station'
else:
    tag='fvcom'  


st=2208
st=0
cut=13700
df=pd.read_csv('{}/east/buoy/SA_Saint_John_Buoy_03152015_04302016.csv'.format(obspath))
time=np.array(dates.datestr2num(df.values[st:cut,0].astype(str)))
temp=df.values[st:cut,8].astype(float)


months = dates.MonthLocator()
monthsFmt = dates.DateFormatter('%b')

savepath='{}png/{}/buoy/{}/'.format(figpath,grid,name)
if not os.path.exists(savepath): os.makedirs(savepath)


figstr='{}{}_buoy_compare_{}.png'.format(savepath,name,tag)
if args.dates is not None:
    din=dates.datestr2num(args.dates)
    idx=np.argwhere((time>=din[0]) & (time<=din[1]))
    time=np.ravel(time[idx])
    temp=np.ravel(temp[idx])
    figstr='{}{}_buoy_compare_{}_{}_to_{}.png'.format(savepath,name,tag,args.dates[0],args.dates[1])


inpath='{}/{}/buoy/{}/'.format(datapath,grid,name)
out=np.load('{}{}_buoy_temp.npy'.format(inpath,name))
out=out[()]


idx=np.argwhere((out['time']>=time[0])&(out['time']<=time[-1]))
timed=out['time'][idx]        
tempd=out['temp'][idx]

itemp=ipt.interp1d(time[~np.isnan(temp)],temp[~np.isnan(temp)],timed)

test=residual_stats(tempd,itemp)

f=plt.figure(figsize=(15,5))
ax=f.add_axes([.125,.1,.775,.8])
ax.plot(timed, itemp,'k',label='Buoy')
ax.plot(timed,tempd,lw=.5,label=name)
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
ax.legend()

#f.suptitle(pd.DataFrame(test).round(2).T.to_string()[15:].replace(' ','').replace('\n',' '))
a=pd.DataFrame(test,index=[0]).round(2).T[0]
f.suptitle('Bias: {}   Std: {}   RMSE: {}   RAE: {}   Corr: {}   Skew: {}   Skill: {}'.format(a[0],a[1],a[2],a[3],a[4],a[5],a[6]))
#ax.set_ylabel('SST ($^{\circ}C$)')
#ax.set_xlabel('2015-2016')
f.savefig(figstr,dpi=300)

#diff=itemp-tempd


#print(np.fabs(diff).mean())
#print(diff.mean())

print(pd.DataFrame(test).round(2).T)











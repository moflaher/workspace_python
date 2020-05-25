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
try:
    import ttide
    tide=True
except:
    print('No ttide')
    tide=False


parser = argparse.ArgumentParser()
parser.add_argument("grid", help="name of the grid", type=str)
parser.add_argument("name", help="name of the run", type=str,default=None, nargs='?')
parser.add_argument("--station", help="switch to station output instead of fvcom output", default=False,action='store_true')
parser.add_argument("-dates", help="specify start and end date",type=str,nargs=2,default=None)
parser.add_argument("-snr", help="signal to noise ratio value used for constituent cutoff", type=float,default=2.0)
parser.add_argument("-skipdays", help="number of days to skip at start of timeseries", type=float,default=14.0)
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
savepath2='{}png/{}/tg/{}/csv/'.format(figpath,grid,name)
if not os.path.exists(savepath2): os.makedirs(savepath2)

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
        figstr2='{}{}_{}_tg_{:05d}_residual_{}_to_{}.png'.format(savepath,grid,name,tgm['tgnumber'][0],args.dates[0],args.dates[1])
        figstr3='{}{}_{}_tg_{:05d}_{}_to_{}'.format(savepath2,grid,name,tgm['tgnumber'][0],args.dates[0],args.dates[1])
    else:
        din=np.array([tgm['time'][0]+args.skipdays,tgm['time'][-1]])
        figstr='{}{}_{}_tg_{:05d}.png'.format(savepath,grid,name,tgm['tgnumber'][0])
        figstr2='{}{}_{}_tg_{:05d}_residual.png'.format(savepath,grid,name,tgm['tgnumber'][0])
        figstr3='{}{}_{}_tg_{:05d}'.format(savepath2,grid,name,tgm['tgnumber'][0])
        
    idx=np.argwhere((tgo['time']>=din[0]) & (tgo['time']<=din[1]))
    idx=np.ravel(idx)
    

    time1,data1,data2=interp_clean_common(tgo['time'][idx],tgo['zeta'][idx],tgm['time'],tgm['zeta'],500,-500)
    stats=residual_stats(data2-np.mean(data2), data1-np.mean(data1))
    a=pd.DataFrame(stats,index=[0]).round(2).T[0]

    f=plt.figure(figsize=(15,5)); 
    ax=f.add_axes([.125,.1,.775,.8]);
    ax.plot(time1,data1-np.mean(data1),'k',label='TG: {:05d}'.format(tgm['tgnumber'][0]))
    ax.plot(time1,data2-np.mean(data2),'r',lw=.5,label='{}'.format(name))
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
    ax.legend() 
    ax.set_ylabel('Elevation (m)')   
    f.suptitle('Removed TG means - Obs: {}     Model: {}\n Bias: {}   Std: {}   RMSE: {}   RAE: {}   Corr: {}   Skew: {}   Skill: {}'.format(np.mean(data1),np.mean(data2),a[0],a[1],a[2],a[3],a[4],a[5],a[6]))
    f.savefig(figstr,dpi=600)
    
    if tide:
        time=np.arange(time1[0],time1[-1]+1/24.0,1/24.0)
        tgm_int=ipt.interp1d(tgm['time'],tgm['zeta'],time)
        tgonan=tgo['zeta'][idx]
        tgonan[tgonan>500]=np.nan
        tgo_int=ipt.interp1d(tgo['time'][idx],tgonan,time)
        
        tgm_tcon_pre=ttide.t_tide(tgm_int,stime=time[0],lat=tgm['lat'],dt=(time[1]-time[0])*24.0,out_style=None)
        tgo_tcon_pre=ttide.t_tide(tgo_int,stime=time[0],lat=tgm['lat'],dt=(time[1]-time[0])*24.0,out_style=None)
        
        tgm_tcon=ttide.t_tide(tgm_int,stime=time[0],lat=tgm['lat'],dt=(time[1]-time[0])*24.0,constitnames=tgm_tcon_pre['nameu'][tgm_tcon_pre['snr']>=args.snr],out_style=None)
        tgo_tcon=ttide.t_tide(tgo_int,stime=time[0],lat=tgm['lat'],dt=(time[1]-time[0])*24.0,constitnames=tgo_tcon_pre['nameu'][tgo_tcon_pre['snr']>=args.snr],out_style=None)
    
        f=plt.figure(figsize=(15,5)); 
        ax=f.add_axes([.125,.1,.775,.8]);
        ax.plot(time[:len(tgo_tcon['xres'])],tgo_tcon['xres']-np.nanmean(tgo_tcon['xres']),'k',label='TG: {:05d}'.format(tgm['tgnumber'][0]))
        ax.plot(time[:len(tgm_tcon['xres'])],tgm_tcon['xres']-np.nanmean(tgm_tcon['xres']),'r',lw=.5,label='{}'.format(name))
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        ax.legend()    
        ax.set_ylabel('Residual Elevation (m)')
        o,m=remove_common_nan(tgo_tcon['xres']-np.nanmean(tgo_tcon['xres']), tgm_tcon['xres']-np.nanmean(tgm_tcon['xres']))
        stats=residual_stats(o,m)
        a=pd.DataFrame(stats,index=[0]).round(2).T[0]
        f.suptitle('Removed TG means - Obs: {}     Model: {}\n Bias: {}   Std: {}   RMSE: {}   RAE: {}   Corr: {}   Skew: {}   Skill: {}'.format(np.nanmean(tgo_tcon['xres']),np.nanmean(tgm_tcon['xres']),a[0],a[1],a[2],a[3],a[4],a[5],a[6]))
        f.savefig(figstr2,dpi=600)
        
        
        
        df=pd.DataFrame(tgm_tcon['tidecon'],columns=['Amp','AmpE','Phase','PhaseE'],index=tgm_tcon['nameu']).round(2).sort_values('Amp',ascending=False)
        df.to_csv('{}_model_full.csv'.format(figstr3))
        
        df=pd.DataFrame(tgo_tcon['tidecon'],columns=['Amp','AmpE','Phase','PhaseE'],index=tgo_tcon['nameu']).round(2).sort_values('Amp',ascending=False)
        df.to_csv('{}_obs_full.csv'.format(figstr3))
        
        
        namesm=tgm_tcon['nameu']
        cnames=np.array([])
        for namea in namesm:
            if namea in tgo_tcon['nameu']:
                cnames=np.append(cnames,namea)
                
        oidx=np.in1d(tgo_tcon['nameu'],cnames)
        midx=np.in1d(tgm_tcon['nameu'],cnames)
        
        diff=np.vstack([tgo_tcon['tidecon'][oidx,0],tgm_tcon['tidecon'][midx,0],tgo_tcon['tidecon'][oidx,0]-tgm_tcon['tidecon'][midx,0],
                   tgo_tcon['tidecon'][oidx,2],tgm_tcon['tidecon'][midx,2],tgo_tcon['tidecon'][oidx,2]-tgm_tcon['tidecon'][midx,2]]).T
        
        df=pd.DataFrame(diff,columns=['AmpObs','AmpMod','AmpDiff','PhaseObs','PhaseMod','PhaseDiff'],index=cnames).round(2).sort_values('AmpObs',ascending=False)
        df.to_csv('{}_obsmod_common_diff.csv'.format(figstr3))
        
       
    
    #kill














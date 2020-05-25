from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from mytools import *
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
from collections import OrderedDict
import ttide
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("grid", help="name of the grid", type=str)
parser.add_argument("name", help="name of the run", type=str,default=None, nargs='?')
parser.add_argument("levels", help="levels to look at in meters ex. 2 5 10", nargs='+', type=int)
parser.add_argument("--station", help="switch to station output instead of fvcom output", default=False,action='store_true')
args = parser.parse_args()

print("The current commandline arguments being used are")
print(args)

lvl=args.levels
grid=args.grid
if args.name is None:
    tempa='ls {}/{}/adcp/'.format(datapath,grid)
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


#location of save model ncfiles
modpath='{}/{}/adcp/{}/'.format(datapath,grid,name)
filenames=glob.glob('{}adcp_*_{}.nc'.format(modpath,tag))
filenames.sort()

# loadpath='{}{}/adcp/{}/'.format(datapath,grid,name)
# dt=dates.datetime.timedelta(0,60)


def plot_fun1(time,obs,mod,savepath,pname,level):
    #months = dates.MonthLocator()
    monthsFmt = dates.DateFormatter('%b %d')
    
    f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8]);
    ax.plot(time,obs,'r',label='Obs')
    ax.plot(time,mod,'b',lw=.5,label='Mod')   
    ax.legend()
    #ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
    ax.set_xlabel('Time')
    ax.set_ylabel('{} (m/s)'.format(pname.replace("_"," ")))
    f.savefig('{}{}_timeseries_at_{}m.png'.format(savepath,pname,level),dpi=150)
    #plot a subset of time
    dt=time.max()-time.min()
    ax.set_xlim([time.min()+dt*.25,time.max()-dt*.25])
    f.savefig('{}{}_timeseries_at_{}m_subset.png'.format(savepath,pname,level),dpi=150)
    #plot another subset but just 3 days centered on the middle
    ax.set_xlim([time.min()+dt*.5-1.5,time.min()+dt*.5+1.5])
    f.savefig('{}{}_timeseries_at_{}m_3days.png'.format(savepath,pname,level),dpi=150)
    
    plt.close(f)


def plot_fun2(mod_u,mod_v,obs_u,obs_v,savepath,level,lbc,ptag='',zoom=True):
    #u vs v
    amin=np.nanmin(np.hstack([obs_u,obs_v,mod_u,mod_v]))*1.2
    amax=np.nanmax(np.hstack([obs_u,obs_v,mod_u,mod_v]))*1.2
    omin=np.nanmin(np.hstack([obs_u,obs_v]))*1.2
    omax=np.nanmax(np.hstack([obs_u,obs_v]))*1.2
    f=plt.figure(figsize=(4,4)); ax=f.add_axes([.2,.175,.725,.725])
    ax.axvline(0,linestyle='--',color='k',lw=.5)
    ax.axhline(0,linestyle='--',color='k',lw=.5)
    ax.plot(obs_u,obs_v,lbc[1],label=lbc[0],markersize=.5,alpha=.3)
    ax.plot(mod_u,mod_v,lbc[3],label=lbc[2],markersize=.5,alpha=.3)   
    ax.legend(markerscale=20)
    ax.set_xlabel('u (m/s)')
    ax.set_ylabel('v (m/s)')
    ax.axis([amin,amax,amin,amax])
    f.savefig('{}u_vs_v_{}timeseries_at_{}m.png'.format(savepath,ptag,level),dpi=150)
    if zoom:
        ax.axis([omin,omax,omin,omax])
        f.savefig('{}u_vs_v_{}timeseries_at_{}m_zoom.png'.format(savepath,ptag,level),dpi=150)
    plt.close(f)
    


for i,filename in enumerate(filenames):
    print('='*80)
    print(i)
    print(filename)
    
    # Load the ncfiles for extract model and obs
    adcpm = loadnc('',filename,False)
    adcpo = loadnc('{}east/all/'.format(obspath),'adcp_{}.nc'.format(adcpm['adcpnumber'][0]),False)
    num=adcpm['adcpnumber'][0]
    
    
    # Interpolate model to levels
    mup=np.empty((len(lvl),len(adcpm['time'])))
    mvp=np.empty((len(lvl),len(adcpm['time'])))
    for i in range(len(adcpm['time'])):
        mup[:,i]=ipt.interp1d(-1*adcpm['siglay']*(adcpm['zeta'][i]+adcpm['h']),adcpm['u'][i,],lvl)
        mvp[:,i]=ipt.interp1d(-1*adcpm['siglay']*(adcpm['zeta'][i]+adcpm['h']),adcpm['v'][i,],lvl)
    
    # Interpolate obs to levels
    oup=np.empty((len(lvl),len(adcpo['time'])))
    ovp=np.empty((len(lvl),len(adcpo['time'])))
    for i in range(len(adcpo['time'])):
        oup[:,i]=ipt.interp1d(adcpo['zetah'][i,:],adcpo['u'][i,],lvl)
        ovp[:,i]=ipt.interp1d(adcpo['zetah'][i,:],adcpo['v'][i,],lvl)
    
    # Interpolate model and obs to model time and remove common nans
    mu=OrderedDict(); mv=OrderedDict(); ou=OrderedDict(); ov=OrderedDict();
    for i,l in enumerate(lvl):
        sl=str(l)
        time,mu[sl],ou[sl]=interp_common(adcpm['time'],mup[i,],adcpo['time'],oup[i,])
        time,mv[sl],ov[sl]=interp_common(adcpm['time'],mvp[i,],adcpo['time'],ovp[i,])
    
            
    for i,l in enumerate(lvl): 
        # Maybe add a nan check or something
        # if time==0:
            # print('Could not process {} at level {}'.format(num,l))
            # continue
         
        sl=str(l)
        mod_u=mu[sl]; mod_v=mv[sl]
        obs_u=ou[sl]; obs_v=ov[sl]
        zeta=ipt.interp1d(adcpm['time'],adcpm['zeta'],time)        
        
        savepath='{}png/{}/adcp/{}/adcp_{}/{}/'.format(figpath,grid,name,num,sl)
        if not os.path.exists(savepath): os.makedirs(savepath)
        
        ztf=np.gradient(zeta)>0
    
        # time vs field
        plot_fun1(time,mod_u,obs_u,savepath,'u',sl)
        plot_fun1(time,mod_v,obs_v,savepath,'v',sl)
        plot_fun1(time,speeder(mod_u,mod_v),speeder(obs_u,obs_v),savepath,'speed',sl)
        #plot_fun1(time,mod_u_res,obs_u_res,savepath,'u_res',sl)
        #plot_fun1(time,mod_v_res,obs_v_res,savepath,'v_res',sl)
        #plot_fun1(time,speeder(mod_u_res,mod_v_res),speeder(obs_u_res,obs_v_res),savepath,'speed_res',sl)
    
        # u vs v
        plot_fun2(mod_u,mod_v,obs_u,obs_v,savepath,sl,['Obs','r.','Mod','b.'])
        #plot_fun2(mod_u_res,mod_v_res,obs_u_res,obs_v_res,savepath,sl,['Obs_res','r.','Mod_res','b.'])
    
        # u vs v for ebbfld
        plot_fun2(mod_u[ztf],mod_v[ztf],mod_u[~ztf],mod_v[~ztf],savepath,sl,['Flood','m.','Ebb','g.'],'ebbfld_mod_',False)
        plot_fun2(obs_u[ztf],obs_v[ztf],obs_u[~ztf],obs_v[~ztf],savepath,sl,['Flood','m.','Ebb','g.'],'ebbfld_obs_',False)
        #plot_fun2(mod_u_res[ztf],mod_v_res[ztf],mod_u_res[~ztf],mod_v_res[~ztf],savepath,sl,['Flood_res','m.','Ebb_res','g.'],'_res_ebbfld_mod_')
        #plot_fun2(obs_u_res[ztf],obs_v_res[ztf],obs_u_res[~ztf],obs_v_res[~ztf],savepath,sl,['Flood_res','m.','Ebb_res','g.'],'_res_ebbfld_obs_')


        # and zeta for fun? maybe later
    

 
    
   
    

    
    
    

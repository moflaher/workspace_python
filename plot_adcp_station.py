from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from mytools import *
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
from collections import OrderedDict
import ttide
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("grid", help="name of the grid", type=str)
parser.add_argument("name", help="name of the run", type=str)
args = parser.parse_args()

print("The current commandline arguments being used are")
print(args)

name=args.name
grid=args.grid

## Define names and types of data
#name='year_fvcom41_wet'
##name='sjh_hr_v3_year_wet'
#grid='sjh_lr_v2_double'
datatype='2d'
#print(name)

filenames=glob.glob('{}east/adcp/*.npy'.format(obspath))
filenames.sort()
loadpath='{}/{}_{}/adcp/{}/'.format(datapath,grid,datatype,name)
dt=dates.datetime.timedelta(0,60)

#savepath='{}/{}_{}/adcp/{}/'.format(datapath,grid,datatype,name)
#if not os.path.exists(savepath): os.makedirs(savepath)

#months = dates.MonthLocator()
monthsFmt = dates.DateFormatter('%b %d')

for i,filename in enumerate(filenames):
    print('='*80)
    print(i)
    print(filename)
    
    adcp = np.load(filename)
    adcp = adcp[()]
    try:
        lpath='{}ADCP_{}/'.format(loadpath,adcp['metadata']['ADCP_number'])
        model = np.load('{}ADCP_{}_model_ministation.npy'.format(lpath,adcp['metadata']['ADCP_number']))
        model = model[()]
        zdf=pd.read_csv('{}ADCP_{}_zeta_timeseries.csv'.format(lpath,adcp['metadata']['ADCP_number']))
        savepath='{}png/{}_{}/adcp/{}/ADCP_{}/'.format(figpath,grid,datatype,name,adcp['metadata']['ADCP_number'])
        if not os.path.exists(savepath): os.makedirs(savepath)
    except:
        print('Failed to load {}'.format(adcp['metadata']['ADCP_number']))
        continue
    
    lvl=np.array([2,5,10])
    for j,level in enumerate(lvl):
        try:    
            df=pd.read_csv('{}ADCP_{}_timeseries_at_{}m.csv'.format(lpath,adcp['metadata']['ADCP_number'],level))
        except:
            print('Failed to load {} at {}'.format(adcp['metadata']['ADCP_number'],level))
            continue

       # '{}ctd_timeseries_{}.png'.format(savepath,num)
        tl=len(df.time)
        if tl>40320:
            st=df.time[int(tl*.25)]
            et=df.time[int(tl*.25)+7*24*60]
        else:
            st=df.time[0]
            et=df.time[7*24*60]
            
        ztf=np.gradient(df.zeta)>0

        plots=['u','v','u_res','v_res']        
        for pname in plots:
            f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8]);
            ax.plot(df.time,df['obs_{}'.format(pname)],'r',label='Obs')
            ax.plot(df.time,df['mod_{}'.format(pname)],'b',lw=.5,label='Mod')   
            ax.legend()
            #ax.xaxis.set_major_locator(months)
            ax.xaxis.set_major_formatter(monthsFmt)
            f.savefig('{}{}_timeseries_at_{}m.png'.format(savepath,pname,level),dpi=150)
            ax.set_xlim([st,et])
            f.savefig('{}{}_timeseries_at_{}m_subset.png'.format(savepath,pname,level),dpi=150)
            plt.close(f)
            

        ################################################################
        #speed plots
        f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8])
        ax.plot(df.time,np.sqrt(df.obs_u**2+df.obs_v**2),'r',label='Obs')
        ax.plot(df.time,np.sqrt(df.mod_u**2+df.mod_v**2),'b',lw=.5,label='Mod')   
        ax.legend()
        #ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        f.savefig('{}speed_timeseries_at_{}m.png'.format(savepath,level),dpi=150)
        ax.set_xlim([st,et])
        f.savefig('{}speed_timeseries_at_{}m_subset.png'.format(savepath,level),dpi=150)
        plt.close(f)

        f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8])
        ax.plot(df.time,np.sqrt(df.obs_u_res**2+df.obs_v_res**2),'r',label='Obs')
        ax.plot(df.time,np.sqrt(df.mod_u_res**2+df.mod_v_res**2),'b',lw=.5,label='Mod')   
        ax.legend()
        #ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        f.savefig('{}speed_res_timeseries_at_{}m.png'.format(savepath,level),dpi=150)
        ax.set_xlim([st,et])
        f.savefig('{}speed_res_timeseries_at_{}m_subset.png'.format(savepath,level),dpi=150)
        plt.close(f)
        

        ################################################################
        #u vs v
        amin=np.nanmin([df.obs_u,df.obs_v,df.mod_u,df.mod_v])*1.1
        amax=np.nanmax([df.obs_u,df.obs_v,df.mod_u,df.mod_v])*1.1
        f=plt.figure(figsize=(4,4)); ax=f.add_axes([.125,.1,.775,.8])
        ax.plot(df.obs_u,df.obs_v,'r.',label='Obs',markersize=.5,alpha=.3)
        ax.plot(df.mod_u,df.mod_v,'b.',label='Mod',markersize=.5,alpha=.3)   
        ax.legend(markerscale=20)
        ax.axis([amin,amax,amin,amax])
        f.savefig('{}u_vs_v_timeseries_at_{}m.png'.format(savepath,level),dpi=150)
        plt.close(f)


        amin=np.nanmin([df.obs_u_res,df.obs_v_res,df.mod_u_res,df.mod_v_res])*1.1
        amax=np.nanmax([df.obs_u_res,df.obs_v_res,df.mod_u_res,df.mod_v_res])*1.1
        f=plt.figure(figsize=(4,4)); ax=f.add_axes([.125,.1,.775,.8])
        ax.plot(df.obs_u_res,df.obs_v_res,'r.',label='Obs',markersize=.5,alpha=.3)
        ax.plot(df.mod_u_res,df.mod_v_res,'b.',label='Mod',markersize=.5,alpha=.3)   
        leg=ax.legend(markerscale=20)
        ax.axis([amin,amax,amin,amax])
        f.savefig('{}u_res_vs_v_res_timeseries_at_{}m.png'.format(savepath,level),dpi=150)
        plt.close(f)


        ################################################################
        #u vs v ebbfld for obs
        amin=np.nanmin([df.obs_u,df.obs_v])*1.1
        amax=np.nanmax([df.obs_u,df.obs_v])*1.1
        f=plt.figure(figsize=(4,4)); ax=f.add_axes([.125,.1,.775,.8])
        ax.plot(df.obs_u[ztf],df.obs_v[ztf],'m.',label='Flood',markersize=.5,alpha=.3)
        ax.plot(df.obs_u[~ztf],df.obs_v[~ztf],'g.',label='Ebb',markersize=.5,alpha=.3)   
        ax.legend(markerscale=20)
        ax.axis([amin,amax,amin,amax])
        f.savefig('{}u_vs_v_ebbfld_obs_timeseries_at_{}m.png'.format(savepath,level),dpi=150)
        plt.close(f)

        amin=np.nanmin([df.obs_u_res,df.obs_v_res])*1.1
        amax=np.nanmax([df.obs_u_res,df.obs_v_res])*1.1
        f=plt.figure(figsize=(4,4)); ax=f.add_axes([.125,.1,.775,.8])
        ax.plot(df.obs_u_res[ztf],df.obs_v_res[ztf],'m.',label='Flood',markersize=.5,alpha=.3)
        ax.plot(df.obs_u_res[~ztf],df.obs_v_res[~ztf],'g.',label='Ebb',markersize=.5,alpha=.3)   
        ax.legend(markerscale=20)
        ax.axis([amin,amax,amin,amax])
        f.savefig('{}u_res_vs_v_res_ebbfld_obs_timeseries_at_{}m.png'.format(savepath,level),dpi=150)
        plt.close(f)


        ################################################################
        #u vs v ebbfld for obs        
        amin=np.nanmin([df.mod_u,df.mod_v])*1.1
        amax=np.nanmax([df.mod_u,df.mod_v])*1.1
        f=plt.figure(figsize=(4,4)); ax=f.add_axes([.125,.1,.775,.8])
        ax.plot(df.mod_u[ztf],df.mod_v[ztf],'m.',label='Flood',markersize=.5,alpha=.3)
        ax.plot(df.mod_u[~ztf],df.mod_v[~ztf],'g.',label='Ebb',markersize=.5,alpha=.3)   
        ax.legend(markerscale=20)
        ax.axis([amin,amax,amin,amax])
        f.savefig('{}u_vs_v_ebbfld_mod_timeseries_at_{}m.png'.format(savepath,level),dpi=150)
        plt.close(f)

        amin=np.nanmin([df.mod_u_res,df.mod_v_res])*1.1
        amax=np.nanmax([df.mod_u_res,df.mod_v_res])*1.1
        f=plt.figure(figsize=(4,4)); ax=f.add_axes([.125,.1,.775,.8])
        ax.plot(df.mod_u_res[ztf],df.mod_v_res[ztf],'m.',label='Flood',markersize=.5,alpha=.3)
        ax.plot(df.mod_u_res[~ztf],df.mod_v_res[~ztf],'g.',label='Ebb',markersize=.5,alpha=.3)   
        ax.legend(markerscale=20)
        ax.axis([amin,amax,amin,amax])
        f.savefig('{}u_res_vs_v_res_ebbfld_mod_timeseries_at_{}m.png'.format(savepath,level),dpi=150)
        plt.close(f)

    
        ################################################################
        #zeta
        plots=['zeta']        
        for pname in plots:
            f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8]);
            ax.plot(zdf.time,zdf['obs_{}'.format(pname)],'r',label='Obs')
            ax.plot(zdf.time,zdf['mod_{}'.format(pname)],'b',lw=.5,label='Mod')   
            ax.legend()
            #ax.xaxis.set_major_locator(months)
            ax.xaxis.set_major_formatter(monthsFmt)
            f.savefig('{}{}_timeseries_at_{}m.png'.format(savepath,pname,level),dpi=150)
            ax.set_xlim([st,et])
            f.savefig('{}{}_timeseries_at_{}m_subset.png'.format(savepath,pname,level),dpi=150)
            plt.close(f)

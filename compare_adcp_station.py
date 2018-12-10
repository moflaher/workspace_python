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
from collections import OrderedDict
import ttide
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("grid", help="name of the grid", type=str)
parser.add_argument("name", help="name of the run", type=str)
parser.add_argument("levels", help="levels to look at in meters ex. 2 5 10", nargs='+', type=int)
parser.add_argument("--noplot", help="call plotting script afterwards", action="store_false", default=True)
args = parser.parse_args()

print("The current commandline arguments being used are")
print(args)

name=args.name
grid=args.grid
lvl=args.levels


## Define names and types of data
#name='year_fvcom41_wet'
##name='sjh_hr_v3_year_wet'
#grid='sjh_lr_v2_double'
datatype='2d'
#print(name)
np.random.seed(25938123)

filenames=glob.glob('{}east/adcp/*.npy'.format(obspath))
filenames.sort()
loadpath='{}/{}_{}/adcp/{}/'.format(datapath,grid,datatype,name)
dt=dates.datetime.timedelta(0,60)

#savepath='{}/{}_{}/adcp/{}/'.format(datapath,grid,datatype,name)
#if not os.path.exists(savepath): os.makedirs(savepath)


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
    except:
        print('Failed to load {}'.format(adcp['metadata']['ADCP_number']))
        continue
    
    obs={}
    mod={}    
    
    #lvl=np.array([2,5,10])
    obs['rtime']=dates.datestr2num(adcp['time']['Times'])
    obs['rzeta']=adcp['pres']['surf']
    obs['rv']=np.empty((len(obs['rtime']),len(lvl)))
    obs['ru']=np.empty((len(obs['rtime']),len(lvl)))
    for i in range(len(obs['rtime'])):
        obs['rv'][i,]=ipt.interp1d(adcp['pres']['topheight'][i,:],adcp['data']['north_vel'][i,:],lvl)
        obs['ru'][i,]=ipt.interp1d(adcp['pres']['topheight'][i,:],adcp['data']['east_vel'][i,:],lvl)

    mod['rtime']=model['time']
    mod['rzeta']=model['zeta']
    mod['rv']=np.empty((len(mod['rtime']),len(lvl)))
    mod['ru']=np.empty((len(mod['rtime']),len(lvl)))  
    for i in range(len(mod['rtime'])):
        mod['rv'][i,]=ipt.interp1d(-1*model['siglay']*(model['zeta'][i]+model['h']),model['v'][i,],lvl)
        mod['ru'][i,]=ipt.interp1d(-1*model['siglay']*(model['zeta'][i]+model['h']),model['u'][i,],lvl)

    
    
    

    

    timeshift=dates.drange(dates.num2date(obs['rtime'][0]),dates.num2date(obs['rtime'][-1]),dt)
    try:
        oz=ipt.interp1d(obs['rtime'],obs['rzeta'],timeshift)

        mz=ipt.interp1d(mod['rtime'],mod['rzeta'],timeshift)
        
        nidx=np.isnan(oz)
        mz[nidx]=np.nan
        
        oz=oz-np.nanmean(oz)
        mz=mz-np.nanmean(mz)

    
        r1z=residual_stats(mz[~nidx],oz[~nidx])

    
        print('T_tide zeta obs')
        oout=ttide.t_tide(oz,dt=60.0/3600.0,stime=timeshift[0],lat=adcp['lat'],out_style=None)
        osnr=0
        clist=oout['nameu'][oout['snr']>2]
        nsnr=len(clist)
        while(osnr!=nsnr):
            #print('looping')
            oout2=ttide.t_tide(oz,dt=60.0/3600.0,stime=timeshift[0],lat=adcp['lat'],constitnames=clist,out_style=None)
            osnr=nsnr
            clist=oout2['nameu'][oout2['snr']>2]
            nsnr=len(clist)

        
        print('T_tide zeta mod')
        mout=ttide.t_tide(mz,dt=60.0/3600.0,stime=timeshift[0],lat=model['lat'],out_style=None)
        osnr=0
        clist=mout['nameu'][mout['snr']>2]
        nsnr=len(clist)
        while(osnr!=nsnr):
            #print('looping')
            mout2=ttide.t_tide(mz,dt=60.0/3600.0,stime=timeshift[0],lat=model['lat'],constitnames=clist,out_style=None)
            osnr=nsnr
            clist=mout2['nameu'][mout2['snr']>2]
            nsnr=len(clist)
        
        nidx=np.isnan(oout2['xres'])
        r2z=residual_stats(mout2['xres'][~nidx],oout2['xres'][~nidx])
        

        #save it all here
        rstats=pd.DataFrame([r1z,r2z],index=['zeta_stats','zeta_res_stats'])
        rstats.to_csv('{}ADCP_{}_zeta_timeseries_stats.csv'.format(lpath,adcp['metadata']['ADCP_number']))
        
        df=pd.DataFrame([timeshift,oz,mz,oout2['xres'],mout2['xres']],index=['time','obs_zeta','mod_zeta','obs_zeta_res','mod_zeta_res']).T
        df.to_csv('{}ADCP_{}_zeta_timeseries.csv'.format(lpath,adcp['metadata']['ADCP_number']),na_rep='NaN')
        
        ostr,odf='{}ADCP_{}_obs_zeta_ttide_output.txt'.format(lpath,adcp['metadata']['ADCP_number']),'{}ADCP_{}_obs_zeta_ttide_tidecon.csv'.format(lpath,adcp['metadata']['ADCP_number'])        
        oout2.pandas_style(ostr,odf)

        mstr,mdf='{}ADCP_{}_mod_zeta_ttide_output.txt'.format(lpath,adcp['metadata']['ADCP_number']),'{}ADCP_{}_mod_zeta_ttide_tidecon.csv'.format(lpath,adcp['metadata']['ADCP_number'])
        mout2.pandas_style(mstr,mdf)
    except:
        print('Failed zeta for ADCP {}'.format(adcp['metadata']['ADCP_number']))

    
    for j,level in enumerate(lvl):
        try:
            print('calculating level {}'.format(level))
            ov=ipt.interp1d(obs['rtime'],obs['rv'][:,j],timeshift)
            ou=ipt.interp1d(obs['rtime'],obs['ru'][:,j],timeshift)

            mv=ipt.interp1d(mod['rtime'],mod['rv'][:,j],timeshift)
            mu=ipt.interp1d(mod['rtime'],mod['ru'][:,j],timeshift)
            zeta=ipt.interp1d(mod['rtime'],mod['rzeta'],timeshift)

            nidx=np.isnan(ov)
            nidx2=np.isnan(ov)
            mv[nidx]=np.nan
            mu[nidx]=np.nan
        
            r1v=residual_stats(mv[~nidx],ov[~nidx])
            r1u=residual_stats(mu[~nidx],ou[~nidx])

        
            print('T_tide obs')
            oout=ttide.t_tide(ou+1j*ov,dt=60.0/3600.0,stime=timeshift[0],lat=adcp['lat'],out_style=None)
            osnr=0
            clist=oout['nameu'][oout['snr']>2]
            nsnr=len(clist)
            while(osnr!=nsnr):
                #print('looping')
                oout2=ttide.t_tide(ou+1j*ov,dt=60.0/3600.0,stime=timeshift[0],lat=adcp['lat'],constitnames=clist,out_style=None)
                osnr=nsnr
                clist=oout2['nameu'][oout2['snr']>2]
                nsnr=len(clist)


            print('T_tide mod')
            mout=ttide.t_tide(mu+1j*mv,dt=60.0/3600.0,stime=timeshift[0],lat=model['lat'],out_style=None)
            osnr=0
            clist=mout['nameu'][mout['snr']>2]
            nsnr=len(clist)
            while(osnr!=nsnr):
                #print('looping')
                mout2=ttide.t_tide(mu+1j*mv,dt=60.0/3600.0,stime=timeshift[0],lat=model['lat'],constitnames=clist,out_style=None)
                osnr=nsnr
                clist=mout2['nameu'][mout2['snr']>2]
                nsnr=len(clist)

            nidx=np.isnan(oout2['xres'])
            r2v=residual_stats(np.imag(mout2['xres'])[~nidx],np.imag(oout2['xres'])[~nidx])
            r2u=residual_stats(np.real(mout2['xres'])[~nidx],np.real(oout2['xres'])[~nidx])
            
            rcomp=residual_stats(np.real(mout2['xres'])[~nidx],np.real(oout2['xres'])[~nidx])
            for key in rcomp:
                rcomp[key]=np.nan
            mod1=mu[~nidx2]+1j*mv[~nidx2]
            obs1=ou[~nidx2]+1j*ov[~nidx2]
            rcomp['skill']=1-(np.sum(np.abs(mod1-obs1)**2)/(np.sum((np.abs(mod1-mod1.mean())+np.abs(obs1-obs1.mean()))**2)))

            #save it all here
            rstats=pd.DataFrame([r1u,r1v,r2u,r2v,rcomp],index=['u_stats','v_stats','u_res_stats','v_res_stats','complex'])
            rstats.to_csv('{}ADCP_{}_timeseries_stats_at_{}m.csv'.format(lpath,adcp['metadata']['ADCP_number'],level),na_rep='NaN')
            
            df=pd.DataFrame([timeshift,zeta,ou,ov,mu,mv,np.real(oout2(timeshift)),np.imag(oout2(timeshift)),np.real(mout2(timeshift)),np.imag(mout2(timeshift))],index=['time','zeta','obs_u','obs_v','mod_u','mod_v','obs_u_res','obs_v_res','mod_u_res','mod_v_res']).T
            df.to_csv('{}ADCP_{}_timeseries_at_{}m.csv'.format(lpath,adcp['metadata']['ADCP_number'],level),na_rep='NaN')
            
            ostr,odf='{}ADCP_{}_obs_ttide_output_at_{}m.txt'.format(lpath,adcp['metadata']['ADCP_number'],level),'{}ADCP_{}_obs_ttide_tidecon_at_{}m.csv'.format(lpath,adcp['metadata']['ADCP_number'],level)        
            oout2.pandas_style(ostr,odf)

            mstr,mdf='{}ADCP_{}_mod_ttide_output_at_{}m.txt'.format(lpath,adcp['metadata']['ADCP_number'],level),'{}ADCP_{}_mod_ttide_tidecon_at_{}m.csv'.format(lpath,adcp['metadata']['ADCP_number'],level)
            mout2.pandas_style(mstr,mdf)


        except:
            print('could not calculate level {}'.format(level))


if args.noplot:
    os.system("python plot_adcp.py {} {} 2 5 10".format(grid,name))

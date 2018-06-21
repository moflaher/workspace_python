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


# Define names and types of data
name='sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1_jcool0'
#name='sjh_hr_v3_year_wet'
grid='sjh_lr_v1'
datatype='2d'
print(name)


filenames=glob.glob('/mnt/drive_1/obs_data/east/adcp/*.npy')
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
    
    obs['rtime']=dates.datestr2num(adcp['time']['Times'])
    obs['rzeta']=adcp['pres']['surf']

    mod['rtime']=model['time']
    mod['rzeta']=model['zeta']
    
    

    timeshift=dates.drange(dates.num2date(obs['rtime'][0]),dates.num2date(obs['rtime'][-1]),dt)
    try:
        oz=ipt.interp1d(obs['rtime'],obs['rzeta'],timeshift)

        mz=ipt.interp1d(mod['rtime'],mod['rzeta'],timeshift)
        
        nidx=np.isnan(oz)
        mz[nidx]=np.nan
        
        oz=oz-np.nanmean(oz)
        mz=mz-np.nanmean(mz)

    
        r1z=residual_stats(mz[~nidx],oz[~nidx])

    
        print('T_tide obs')
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

        
        print('T_tide mod')
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
        
        df=pd.DataFrame([timeshift,oz,mz],index=['time','obs_zeta','mod_zeta']).T
        df.to_csv('{}ADCP_{}_zeta_timeseries.csv'.format(lpath,adcp['metadata']['ADCP_number']),na_rep='NaN')
        
        ostr,odf='{}ADCP_{}_obs_zeta_ttide_output.txt'.format(lpath,adcp['metadata']['ADCP_number']),'{}ADCP_{}_obs_zeta_ttide_tidecon.csv'.format(lpath,adcp['metadata']['ADCP_number'])        
        oout2.pandas_style(ostr,odf)

        mstr,mdf='{}ADCP_{}_mod_zeta_ttide_output.txt'.format(lpath,adcp['metadata']['ADCP_number']),'{}ADCP_{}_mod_zeta_ttide_tidecon.csv'.format(lpath,adcp['metadata']['ADCP_number'])
        mout2.pandas_style(mstr,mdf)

    except:
        print('could not calculate zeta for {}'.format(adcp['metadata']['ADCP_number']))



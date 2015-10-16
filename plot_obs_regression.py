from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from misctools import *
from plottools import *
from projtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import scipy.io as sio
import scipy.fftpack as fftp
import pandas as pd
from datetime import timedelta


# Define names and types of data
namelist=['2012-02-01_2012-03-01_0.01_0.001', '2012-02-01_2012-03-01_0.01_0.01', '2012-02-01_2012-03-01_0.02_0.001', '2012-02-01_2012-03-01_0.02_0.01', '2012-02-01_2012-03-01_0.03_0.001', '2012-02-01_2012-03-01_0.03_0.01']
namelist=['2012-02-01_2012-03-01_0.01_0.001','2012-02-01_2012-03-01_0.03_0.01']

#name='2012-02-01_2012-03-01_0.01_0.01'
grid='vh_high'
datatype='2d'
regionname='secondnarrows'
region=regions(regionname)

obspath='data/misc/vhfr_obs/VancouverBC_Harbour_Currents/'
obsname='04100_20110621'
obs=loadcur(obspath+obsname+'*')
#shifttime because PST
for key in obs:
    obs[key]['time']=obs[key]['time']


savepath='figures/png/' + grid + '_' + datatype + '/obs_speed_linreg/' +obsname + '/'
if not os.path.exists(savepath): os.makedirs(savepath)


       
     



for name in namelist:

    ### load the .nc file #####
    data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
    print('done load')
    data = ncdatasort(data,trifinder=True)
    print('done sort')
    
    nidx=get_nodes(data,region)
    eidx=get_elements(data,region)

    for key in obs:

        ua=ipt.interpE_at_loc(data,'ua',[obs[key]['lon'],obs[key]['lat']]) 
        va=ipt.interpE_at_loc(data,'va',[obs[key]['lon'],obs[key]['lat']]) 
        zeta=ipt.interpN_at_loc(data,'zeta',[obs[key]['lon'],obs[key]['lat']]) 

        modelin={}
        modelin['time']=data['time']
        modelin['pts']=ua        
        obsin={}
        obsin['time']=obs[key]['time']
        obsin['pts']=obs[key]['u']
        
        #removenan
        removethis=~np.isnan(obsin['pts'])
        obsin['time']=obsin['time'][removethis]
        obsin['pts']=obsin['pts'][removethis]
        mu,ou,time,dt=interpol(modelin,obsin)
    
        modelin['pts']=va 
        obsin['pts']=obs[key]['v']
        obsin['pts']=obsin['pts'][removethis]
        mv,ov,time,dt=interpol(modelin,obsin)

        
        ms=speeder(mu,mv)
        os=speeder(ou,ov)
        
        lru=linReg(mu,ou)
        lrv=linReg(mv,ov)
        lrs=linReg(ms,os)
        
        plotlinreg(mu,ou,lru,savepath + grid + '_' + name +'_'+obsname+'_bin_'+("%d"%key)+'_model_obs_linreg_u.png')
        plotlinreg(mv,ov,lrv,savepath + grid + '_' + name +'_'+obsname+'_bin_'+("%d"%key)+'_model_obs_linreg_v.png')
        plotlinreg(ms,os,lrs,savepath + grid + '_' + name +'_'+obsname+'_bin_'+("%d"%key)+'_model_obs_linreg_speed.png')
        
        
        

















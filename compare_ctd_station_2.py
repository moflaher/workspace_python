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
#from collections import OrderedDict


# Define names and types of data

name='sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1_jcool0'
grid='sjh_lr_v1'
name='test_1'
grid='sjh_lr_v1_sub'
#name='sjh_lr_v1_year_sigma_uniform_61'
#grid='sjh_lr_v1'
datatype='2d'


modpath='/mnt/drive_0/misc/gpscrsync/dataout/{}_{}/ctd/{}/'.format(grid,datatype,name)
obspath='/mnt/drive_1/obs_data/east/ctd/ctd_wcts/'
ctdnum=np.genfromtxt(obspath+'NEMO-FVCOM_SaintJohn_BOF_Observations_ctd_SABS.txt',skip_header=1,dtype=int)[:,0]

savepath='{}png/{}_{}/ctd2/{}/'.format(figpath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)

other={}
other['grid']=grid
other['name']=name

Tstats={}
Sstats={}
vT=OrderedDict()
f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8]);
plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc', filepath=coastpath, color='k', fill=True)
for num in ctdnum:
    print(num)
    try:
        mod=load_ctd_mod('{}ctd_timeseries_{}.txt'.format(modpath,num))
        zeta=load_ctd_zeta_mod('{}ctd_zeta_{}.txt'.format(modpath,num))
        obs=load_ctd_obs('{}{}_ctd.dat'.format(obspath,num))
        other['dt']=(mod['arrays']['time'][0,1]-mod['arrays']['time'][0,0])*24*60
        other['num']=num
        tidx=np.argmin(np.fabs(mod['arrays']['time'][0,:]-obs['time']))
        other['tidx']=tidx
        
        #for i in range(mod['arrays']['depth'].shape[1]):
        Tmod=ipt.interp1d(-1*mod['arrays']['depth'][:,tidx],mod['arrays']['temperature'][:,tidx],obs['Depth'])
        Smod=ipt.interp1d(-1*mod['arrays']['depth'][:,tidx],mod['arrays']['salinity'][:,tidx],obs['Depth'])

        cTmod, cTobs = remove_common_nan(Tmod,obs['Temp'])
        cSmod, cSobs = remove_common_nan(Smod,obs['Salinity'])

        Tstats['{}'.format(num)]=residual_stats(cTmod, cTobs)
        Sstats['{}'.format(num)]=residual_stats(cSmod, cSobs)
                
        other['filename']='{}ctd_timeseries_{}.png'.format(savepath,num)
        #plot_tsmap2(mod,obs,other,Tstats,Sstats)

        #compute stats for all times
        Tstatst=OrderedDict()
        Tmodt=np.empty((len(obs['Depth']),mod['arrays']['depth'].shape[1]))
        Sstatst=OrderedDict()
        Smodt=np.empty((len(obs['Depth']),mod['arrays']['depth'].shape[1]))
        for i in range(mod['arrays']['depth'].shape[1]):
            Tmodt[:,i]=ipt.interp1d(-1*mod['arrays']['depth'][:,i],mod['arrays']['temperature'][:,i],obs['Depth'])
            cTmodt, cTobst = remove_common_nan(Tmodt[:,i],obs['Temp'])    
            
            Smodt[:,i]=ipt.interp1d(-1*mod['arrays']['depth'][:,i],mod['arrays']['salinity'][:,i],obs['Depth'])
            cSmodt, cSobst = remove_common_nan(Smodt[:,i],obs['Salinity'])   

            Tstatst['{}'.format(i)]=residual_stats(cTmodt, cTobst)
            Sstatst['{}'.format(i)]=residual_stats(cSmodt, cSobst)


        #put them in an array 
        bTstats=np.empty((7,len(Tstatst.keys())))
        bSstats=np.empty((7,len(Sstatst.keys())))
        for i,key in enumerate(Tstatst.keys()):
            for j,key2 in enumerate(Tstatst[key].keys()):
                bTstats[j,i]=Tstatst[key][key2]
                bSstats[j,i]=Sstatst[key][key2]


        #find the "best"
        Tidx=np.argmin(np.fabs(bTstats),axis=1)
        #fix the ones where "best" isnt the min
        Tidx2=np.argmin(np.fabs(bTstats-1),axis=1)
        Tidx[4]=Tidx2[4]
        Tidx[6]=Tidx2[6]

        #find the "best"
        Sidx=np.argmin(np.fabs(bSstats),axis=1)
        #fix the ones where "best" isnt the min
        Sidx2=np.argmin(np.fabs(bSstats-1),axis=1)
        Sidx[4]=Sidx2[4]
        Sidx[6]=Sidx2[6]
        

        #plot_tsmap2(mod,obs,zeta,other,Tstats,Sstats,bTstats,bSstats,Tidx,Sidx)
        
        TstatsV=OrderedDict()
        SstatsV=OrderedDict()
        for i,h in enumerate(np.arange(-7,7.1,.1)):
            Tmod=ipt.interp1d(-1*(mod['arrays']['depth'][:,tidx]+h),mod['arrays']['temperature'][:,tidx],obs['Depth'])
            Smod=ipt.interp1d(-1*(mod['arrays']['depth'][:,tidx]+h),mod['arrays']['salinity'][:,tidx],obs['Depth'])

            cTmod, cTobs = remove_common_nan(Tmod,obs['Temp'])
            cSmod, cSobs = remove_common_nan(Smod,obs['Salinity'])

            TstatsV['{}'.format(i)]=residual_stats(cTmod, cTobs)
            SstatsV['{}'.format(i)]=residual_stats(cSmod, cSobs)
        
        bTstatsV=np.empty((7,len(TstatsV.keys())))
        bSstatsV=np.empty((7,len(SstatsV.keys())))
        for i,key in enumerate(TstatsV.keys()):
            for j,key2 in enumerate(TstatsV[key].keys()):
                bTstatsV[j,i]=TstatsV[key][key2]
                bSstatsV[j,i]=SstatsV[key][key2]
                
        #for k in range(7):
            #f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8]); ax.plot(bTstatsV[k,:]); f.show()
        VidxT=np.argmin(bTstatsV[3,:])
        VidxS=np.argmin(bSstatsV[3,:])
        ht=np.arange(-7,7.1,.1)[VidxT]
        Tmod=ipt.interp1d(-1*(mod['arrays']['depth'][:,tidx]+ht),mod['arrays']['temperature'][:,tidx],obs['Depth'])
        hs=np.arange(-7,7.1,.1)[VidxS]
        Smod=ipt.interp1d(-1*(mod['arrays']['depth'][:,tidx]+hs),mod['arrays']['salinity'][:,tidx],obs['Depth'])

        cTmod, cTobs = remove_common_nan(Tmod,obs['Temp'])
        cSmod, cSobs = remove_common_nan(Smod,obs['Salinity'])
        
        
        plot_tsmap2(mod,obs,zeta,other,Tstats,Sstats,bTstats,bSstats,Tidx,Sidx,ht)
        
        pdf=OrderedDict()
        print('T Vshift of {}'.format(ht))
        vT[str(num)]=ht
        if ht>=-1 and ht<=-.6:
            ax.plot(obs['Lon'],obs['Lat'],'*r',markersize=10)
        else:
            ax.plot(obs['Lon'],obs['Lat'],'*b',markersize=10)
        print('T hshift of {}'.format(bTstatsV[0,VidxT]))
        print('S Vshift of {}'.format(hs))
        print('S hshift of {}'.format(bSstatsV[0,VidxS]))
        pdf['vT']=residual_stats(cTmod, cTobs)
        pdf['hT']=residual_stats(cTmod-bTstatsV[0,VidxT], cTobs)
        pdf['vS']=residual_stats(cSmod, cSobs)
        pdf['hS']=residual_stats(cSmod-bSstatsV[0,VidxS], cSobs)
        df=pd.DataFrame(pdf).round(2).T
        print(df[['meansl','stdsl','rmsesl','relaverr','corsl','skewsl','skill']])
        print()
        print()
    except:
        print('Pass on {}'.format(num))
        pass



#f.show()
    



dfT=pd.DataFrame(Tstats).T
dfT=dfT[['meansl','stdsl','rmsesl','relaverr','corsl','skewsl','skill']]
dfS=pd.DataFrame(Sstats).T
dfS=dfS[['meansl','stdsl','rmsesl','relaverr','corsl','skewsl','skill']]



	








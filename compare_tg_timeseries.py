from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from projtools import *
from folderpath import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from ttide import t_tide



# Define names and types of data
namelist=['sjh_lr_v1_jul2015_wet_riverspg_geometric_wu_origdep']
grid='sjh_lr_v1'
datatype='2d'
starttime=900
endtime=-1

savepath='{}/png/{}_{}/compare_tg_timeseries/'.format(figpath,grid,datatype)
if not os.path.exists(savepath): os.makedirs(savepath)

tg65=np.load('/home/mif001/scratch/obs/tg/tg65_clean.npy')

for name in namelist:
    ### load the .nc file #####
    data = loadnc('/fs/vnas_Hdfo/odis/suh001/scratch/sjh_lr_v1/runs/{}/output/'.format(name),singlename=grid + '_0001.nc')
    print('done load')

    time=data['time'][starttime:endtime]-4/24.0
    zeta=data['zeta'][starttime:endtime,25086]-np.mean(data['zeta'][starttime:endtime,25086])
    zeta=data['zeta'][starttime:endtime,55468]-np.mean(data['zeta'][starttime:endtime,55468])
     
    
    idx=np.argwhere((tg65[:,0]>=(time[0]-1/24.0)) & (tg65[:,0]<=(time[-1]+1/24.0)))

    tgtime=tg65[idx,0]
    tgzeta=tg65[idx,1]-np.nanmean(tg65[idx,1])
    tgtime=tgtime[~np.isnan(tgzeta)]
    tgzeta=tgzeta[~np.isnan(tgzeta)]	

    mtgzeta=ipt.interp1d(tgtime.flatten(),tgzeta.flatten(),time)

    rmse=np.sqrt(np.nanmean((mtgzeta-zeta)**2))

    r=np.corrcoef(mtgzeta,zeta)[0,1]
    r2=r**2
    maxdiff=np.max(mtgzeta-zeta)
    mindiff=np.min(mtgzeta-zeta)
    meandiff=np.mean(mtgzeta-zeta)


    print(name)	
    print(rmse)
    print(r2)
    print(maxdiff)
    print(mindiff)
    print(meandiff)

    f=plt.figure(figsize=(20,5))
    ax=f.add_axes([.125,.1,.775,.8])
    ax.plot(time,mtgzeta,'r',lw=2,label='TG')
    ax.plot(time,zeta,'b',lw=1,label='Model')
    ax.legend()
    f.suptitle('RMSE: {}    R2: {}    MinDiff: {}    MaxDiff: {}    MeanDiff: {}'.format(rmse,r2,mindiff,maxdiff,meandiff))
    f.savefig('{}{}_{}_{}_compare_tg_timeseries.png'.format(savepath,name,starttime,endtime),dpi=300)
    plt.close(f)


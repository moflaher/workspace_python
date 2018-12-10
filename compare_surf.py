from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
from folderpath import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)

name='drifter_2015-10-07'
grid='sjh_lr_v1'

regionname='stjohn_harbour'
starttime=0
endtime=2851
cmin=0
cmax=2



data=loadnc('/fs/hnas1-evs1/Ddfo/dfo_odis/suh001/sjh_lr_v1/drifter/sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1/{}/output/'.format(name),'sjh_lr_v1_0001.nc')


surf=loadnc('/fs/hnas1-evs1/Ddfo/dfo_odis/suh001/sjh_lr_v1/drifter/sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1/for_guillaume/','{}.nc'.format(name),False)

region=regions(regionname)

savepath='{}timeseries/{}_{}/compare_surf_speed/{}_{}_{:.3f}_{:.3f}/'.format(figpath,grid,datatype,name,region['regionname'],cmin,cmax)
if not os.path.exists(savepath): os.makedirs(savepath)



for k in range(starttime,endtime):
    print(k)
    f=plt.figure(figsize=(10,5))#(nrows=1,ncols=2,sharex=True,sharey=True)
    s1=np.sqrt(data['u'][k,0,:]**2+data['v'][k,0,:]**2)
    s2=np.sqrt(surf['usurf'][k,:]**2+surf['vsurf'][k,:]**2)
    ax0=f.add_axes([.125,.1,.35,.8])
    ax1=f.add_axes([.5,.1,.35,.8])
    cax=f.add_axes([.875,.1,.025,.8])
    ax0.tripcolor(data['trigrid'],s1,vmin=cmin,vmax=cmax)
    triax=ax1.tripcolor(data['trigrid'],s2,vmin=cmin,vmax=cmax)
    plt.colorbar(triax,cax)
    ax0.axis(region['region'])
    ax1.axis(region['region'])
    ax1.yaxis.set_tick_params(labelleft='off')
    for label in ax0.get_xticklabels()[::2]:
        label.set_visible(False)
    for label in ax1.get_xticklabels()[::2]:
        label.set_visible(False)
    f.savefig('{}{}_{}_{}_surf_speed_compare_{:05d}.png'.format(savepath,grid,name,region['regionname'],k),dpi=300)
    plt.close(f)
#np.savetxt('data/stracker_input/helens_work_200mx100m_4locs.dat',locs,fmt='%.12f')

    

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


# Define names and types of data
name='vhfr_low_20120201_0.02_0.01'
grid='vhfr_low'
datatype='2d'
regionname='secondnarrows'



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data,trifinder=True)
print('done sort')

region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)

obspath='data/misc/vhfr_obs/VancouverBC_Harbour_Currents/'
obsname='04100_20110621'
obs=loadcur(obspath+obsname+'*')
#shifttime because PST
for key in obs:
    obs[key]['time']=obs[key]['time']+(4.0/24)


savepath='figures/png/' + grid + '_' + datatype + '/obs_speed/' +obsname + '/'
if not os.path.exists(savepath): os.makedirs(savepath)


for key in obs:
    #Plot obs location
    clims=np.percentile(data['h'][nidx],[5,95])
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],data['h'],vmin=clims[0],vmax=clims[1])
    ax.plot(obs[key]['lon'],obs[key]['lat'],'*',markersize=12)
    prettyplot_ll(ax,setregion=region,grid=True,cblabel='Depth (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_obs_location_'+obsname+'_bin_'+("%d"%key)+'.png',dpi=600)
    plt.close(f)


    ua=ipt.interpE_at_loc(data,'ua',[obs[key]['lon'],obs[key]['lat']]) 
    va=ipt.interpE_at_loc(data,'va',[obs[key]['lon'],obs[key]['lat']]) 
    zeta=ipt.interpN_at_loc(data,'zeta',[obs[key]['lon'],obs[key]['lat']]) 

    #there seems to be a shift in the time of 21 tidal cycles. have to find if it is real and where it is from.
    time=data['time'][0]+(np.arange(len(data['time']))*(5.0/(24*60)))-(21*12.42/24)
    limit=[0,-1]


    f=plt.figure(figsize=(25,5))
    ax0=plt.subplot2grid((10,50),(0,0),colspan=50,rowspan=7)
    ax1=plt.subplot2grid((10,50),(7,0),colspan=50,rowspan=3,sharex=ax0)

    ax0.plot(obs[key]['time'],np.sqrt(obs[key]['u']**2+obs[key]['v']**2),'r',label='Obs')
    ax0.plot(time,np.sqrt(ua**2+va**2),'b',lw=.5,label='Model')
    ax0.legend()
    ax0.set_xlim([time[limit[0]:limit[1]].min(),time[limit[0]:limit[1]].max()])
    ax0.xaxis.get_label().set_visible(False)
    ax0.grid()

    ax1.plot(time,zeta,'b',lw=.5,label='Model')
    ax1.grid()


    f.savefig(savepath + grid + '_' + name +'_'+obsname+'_bin_'+("%d"%key)+'_model_obs_compare.png',dpi=300)
    plt.close(f)


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
import glob


# Define names and types of data
name='vhfr_low_20120201_0.02_0.01'
grid='vhfr_low'
datatype='2d'

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data,trifinder=True)
print('done sort')



obspath='data/misc/vhfr_obs/slev/'
files=glob.glob(obspath+'*.csv')

for ifile in files:
    print(ifile)
    obs=loadslev(ifile)
    obsname=ifile.replace(obspath,'').replace('.csv','')
    #shifttime because PST
    obs['time']=obs['time']+(4/24)


    savepath='figures/png/' + grid + '_' + datatype + '/obs_zeta/' +obsname + '/'
    if not os.path.exists(savepath): os.makedirs(savepath)

    idx=closest_node(data,[obs['lon'],obs['lat']])
    zeta=data['zeta'][:,idx]
    #zeta=ipt.interpN_at_loc(data,'zeta',[obs['lon'],obs['lat']]) 
    
    region={}
    region['region']=np.array([obs['lon'],obs['lon'],obs['lat'],obs['lat']])
    region=expand_region(region,dist=5000)
    nidx=get_nodes(data,region)
    eidx=get_elements(data,region)

    #there seems to be a shift in the time of 21 tidal cycles. have to find if it is real and where it is from.
    time=data['time'][0]+(np.arange(len(data['time']))*(5.0/(24*60)))-(21*12.42/24)
    limit=[0,-1]


    #Plot obs location
    clims=np.percentile(data['h'][nidx],[5,95])
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],data['h'],vmin=clims[0],vmax=clims[1])
    ax.plot(obs['lon'],obs['lat'],'*',markersize=12)
    prettyplot_ll(ax,setregion=region,grid=True,cblabel='Depth (m)',cb=triax)
    f.savefig(savepath + grid + '_obs_location_'+obsname+'.png',dpi=600)
    plt.close(f)




    f=plt.figure(figsize=(25,5))
    ax=plt.axes([.125,.1,.775,.8])


    ax.plot(obs['time'],obs['zeta']-obs['zeta'].mean(),'r',label='Obs')
    ax.plot(time,zeta,'b',lw=.5,label='Model')
    ax.legend()
    ax.set_xlim([time[limit[0]:limit[1]].min(),time[limit[0]:limit[1]].max()])
    ax.grid()


    f.savefig(savepath + grid + '_' + name +'_'+obsname+'_model_obs_compare.png',dpi=300)
    plt.close(f)


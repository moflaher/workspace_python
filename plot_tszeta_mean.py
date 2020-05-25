from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from folderpath import *
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
import pandas as pd

# Define names and types of data
name='sjh_hr_v2_newwind'
grid='sjh_hr_v2'

starttime=960
endtime=-1


### load the .nc file #####
#data = loadnc(runpath+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data = loadnc('/home/mif001/scratch/susan/sjh_hr_v2/runs/sjh_hr_v2_newwind/output/',singlename=grid + '_0001.nc')
data['lon']=data['lon']-360
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
print('done load')
del data['trigrid']
data = ncdatasort(data)
print('done sort')


savepath='{}/png/{}_{}/misc/'.format(figpath,grid,datatype)
if not os.path.exists(savepath): os.makedirs(savepath)


#mtemp=data['temp'][starttime:endtime,0,:].mean(axis=0)
#msal=data['salinity'][starttime:endtime,0,:].mean(axis=0)
#mzeta=data['zeta'][starttime:endtime,:].mean(axis=0)
mspeed=np.sqrt(data['u'][starttime:endtime,0,:]**2+data['v'][starttime:endtime,0,:]**2).mean(axis=0)

regionlist=['sfmwhole','bof_nemo','stjohn_nemo']

for regionname in regionlist:

    region=regions(regionname)
    nidx=get_nodes(data,region)
    eidx=get_elements(data,region)

    #clim=np.percentile(mtemp,[20,80])
    #f,ax,cax=setplot(region)
    #plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc',filepath=coastpath, color='k', fcolor='0.75', fill=True)
    #triax=ax.tripcolor(data['trigrid'],mtemp,vmin=clim[0], vmax=clim[1],cmap=mpl.cm.jet)
    #cb=plt.colorbar(triax,cax=cax)
    #cb.set_label(r'Temperature')
    #f.savefig('{}{}_{}_surface_temp_mean.png'.format(savepath,name,regionname),dpi=600)
    #plt.close(f)

    #clim=np.percentile(msal,[20,80])
    #f,ax,cax=setplot(region)
    #plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc',filepath=coastpath, color='k', fcolor='0.75', fill=True)
    #triax=ax.tripcolor(data['trigrid'],msal,vmin=clim[0], vmax=clim[1],cmap=mpl.cm.jet)
    #cb=plt.colorbar(triax,cax=cax)
    #cb.set_label(r'Salinity') 
    #f.savefig('{}{}_{}_surface_salinity_mean.png'.format(savepath,name,regionname),dpi=600)
    #plt.close(f)

    #clim=np.percentile(mzeta,[20,80])
    #f,ax,cax=setplot(region)
    #plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc',filepath=coastpath, color='k', fcolor='0.75', fill=True)
    #triax=ax.tripcolor(data['trigrid'],mzeta,vmin=clim[0], vmax=clim[1],cmap=mpl.cm.jet)
    #cb=plt.colorbar(triax,cax=cax)
    #cb.set_label(r'Elevation')  
    #f.savefig('{}{}_{}_surface_zeta_mean.png'.format(savepath,name,regionname),dpi=600)
    #plt.close(f)

    clim=np.percentile(mspeed[eidx],[5,99])
    f,ax,cax=setplot(region)
    plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc',filepath=coastpath, color='k', fcolor='0.75', fill=True)
    triax=ax.tripcolor(data['trigrid'],mspeed,vmin=clim[0], vmax=clim[1],cmap=mpl.cm.jet)
    cb=plt.colorbar(triax,cax=cax)
    cb.set_label(r'Speed')  
    f.savefig('{}{}_{}_surface_speed_mean.png'.format(savepath,name,regionname),dpi=600)
    plt.close(f)
















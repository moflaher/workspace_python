from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC

# Define names and types of data
name='2012-02-01_2012-03-01_0.01_0.001'
grid='vh_high'
regionlist=['firstnarrows','secondnarrows']
regionlist=['vh_whole']

starttime=0
endtime=2785
clim_min=10
clim_max=90



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')


cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
if np.shape(cages)!=():
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.1
    ls='solid'




savepath='figures/png/' + grid + '_'  + '/zeta_mmm_range_var/' + name + '/'
if not os.path.exists(savepath): os.makedirs(savepath)

zdiff=data['zeta'][starttime:(endtime+1),:]
zeta_mean=np.mean(zdiff,axis=0)
zeta_max=np.max(zdiff,axis=0)
zeta_min=np.min(zdiff,axis=0)
zeta_std=np.std(zdiff,axis=0)

for regionname in regionlist:
    print('Plotting region:' + regionname)
    region=regions(regionname)
    nidx=get_nodes(data,region)

    # Plot zeta difference mean
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    clims=np.percentile(zeta_mean[nidx],[clim_min,clim_max])
    triax=ax.tripcolor(data['trigrid'],zeta_mean,vmin=clims[0],vmax=clims[1])
    plotcoast(ax,filename='pacific_harbour.nc',color='k',fill=True)
    if cages!=None:   
        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        ax.add_collection(lseg_t) 
    prettyplot_ll(ax,setregion=region,cblabel='Elevation (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_zeta_mean.png',dpi=300)
    plt.close(f)

    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    clims=np.percentile(zeta_max[nidx],[clim_min,clim_max])
    triax=ax.tripcolor(data['trigrid'],zeta_max,vmin=clims[0],vmax=clims[1])
    plotcoast(ax,filename='pacific_harbour.nc',color='k',fill=True)
    if cages!=None:   
        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        ax.add_collection(lseg_t) 
    prettyplot_ll(ax,setregion=region,cblabel='Elevation (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_zeta_max.png',dpi=300)
    plt.close(f)

    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    clims=np.percentile(zeta_min[nidx],[clim_min,clim_max])
    triax=ax.tripcolor(data['trigrid'],zeta_min,vmin=clims[0],vmax=clims[1])
    plotcoast(ax,filename='pacific_harbour.nc',color='k',fill=True)
    if cages!=None:   
        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        ax.add_collection(lseg_t) 
    prettyplot_ll(ax,setregion=region,cblabel='Elevation (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_zeta_min.png',dpi=300)
    plt.close(f)
    
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    clims=np.percentile(zeta_max[nidx]-zeta_min[nidx],[clim_min,clim_max])
    triax=ax.tripcolor(data['trigrid'],zeta_max-zeta_min,vmin=clims[0],vmax=clims[1])
    plotcoast(ax,filename='pacific_harbour.nc',color='k',fill=True)
    if cages!=None:   
        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        ax.add_collection(lseg_t) 
    prettyplot_ll(ax,setregion=region,cblabel='Elevation (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_zeta_range.png',dpi=300)
    plt.close(f) 

    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    clims=np.percentile(zeta_std[nidx],[clim_min,clim_max])
    triax=ax.tripcolor(data['trigrid'],zeta_std,vmin=clims[0],vmax=clims[1])
    plotcoast(ax,filename='pacific_harbour.nc',color='k',fill=True)
    if cages!=None:   
        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        ax.add_collection(lseg_t) 
    prettyplot_ll(ax,setregion=region,cblabel='Elevation (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_zeta_std.png',dpi=300)
    plt.close(f)























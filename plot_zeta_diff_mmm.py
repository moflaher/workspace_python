from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC

# Define names and types of data
name1='kit4_kelp_nodrag'
name2='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'
regionlist=['kit4_ftb','kit4_crossdouble','kit4_kelp_tight2_small','kit4_kelp_tight5','kit4_kelp_tight2_kelpfield']
datatype='2d'
starttime=621
endtime=1081



### load the .nc file #####
data1 = loadnc('runs/'+grid+'/'+name1+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')
print('done load')
data1 = ncdatasort(data1)
data2 = ncdatasort(data2)
print('done sort')


cages=loadcage('runs/'+grid+'/' +name_change+ '/input/' +grid+ '_cage.dat')
if np.shape(cages)!=():
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.1
    ls='solid'




savepath='figures/png/' + grid + '_' + datatype + '/zeta_diff_mmm/' + name1 + '_' +name2 + '/'
if not os.path.exists(savepath): os.makedirs(savepath)

zdiff=data1['zeta'][starttime:(endtime+1),:]-data2['zeta'][starttime:(endtime+1),:]
zeta_mean=np.mean(zdiff,axis=0)
zeta_max=np.max(zdiff,axis=0)
zeta_min=np.min(zdiff,axis=0)

for regionname in regionlist:
    print 'Plotting region:' + regionname
    region=regions(regionname)
    nidx=get_nodes(data1,region)

    # Plot zeta difference mean
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data1['trigrid'],zeta_mean,vmin=zeta_mean[nidx].min(),vmax=zeta_mean[nidx].max())
    plotcoast(ax,filename='pacific.nc',color='k',fill=True)
    if cages!=None:   
        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        ax.add_collection(lseg_t) 
    prettyplot_ll(ax,setregion=region,cblabel='Elevation (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_zetadiff_mean.png',dpi=300)
    plt.close(f)

    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data1['trigrid'],zeta_max,vmin=zeta_max[nidx].min(),vmax=zeta_max[nidx].max())
    plotcoast(ax,filename='pacific.nc',color='k',fill=True)
    if cages!=None:   
        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        ax.add_collection(lseg_t) 
    prettyplot_ll(ax,setregion=region,cblabel='Elevation (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_zetadiff_max.png',dpi=300)
    plt.close(f)

    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data1['trigrid'],zeta_min,vmin=zeta_min[nidx].min(),vmax=zeta_min[nidx].max())
    plotcoast(ax,filename='pacific.nc',color='k',fill=True)
    if cages!=None:   
        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        ax.add_collection(lseg_t) 
    prettyplot_ll(ax,setregion=region,cblabel='Elevation (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_zetadiff_min.png',dpi=300)
    plt.close(f)
























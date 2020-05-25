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
import multiprocessing



global grid
global regionname
global region
global tmparray
global savepath
global data1
global data2
global cmin
global cmax
global cages
global lw
global ls
global color



# Define names and types of data
name_orig='kit4_kelp_baroclinic_nodrag'
name_change='kit4_kelp_baroclinic_drag_0.018'
grid='kit4_kelp'

regionname='kit4_kelp_tight5'
starttime=400
endtime=640
cmin=-1
cmax=1


### load the .nc file #####
data1 = loadnc('runs/' + grid + '/' + name_orig +'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/' + grid + '/' + name_change +'/output/',singlename=grid + '_0001.nc')
print('done load')
data1 = ncdatasort(data1)
data2 = ncdatasort(data2)
print('done sort')


cages=loadcage('runs/'+grid+'/' +name_change+ '/input/' +grid+ '_cage.dat')
if cages!=None:
    tmparray=[list(zip(data2['nodell'][data2['nv'][i,[0,1,2,0]],0],data2['nodell'][data2['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.2
    ls='solid'


region=regions(regionname)

savepath='figures/timeseries/' + grid + '_'  + '/speed_difference_relative/' + name_orig + '_' +name_change + '_' + regionname + '_' +("%f" %cmin) + '_' + ("%f" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)


def myplot(i):
    print i
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    speed1=np.sqrt(data1['ua'][i,:]**2+data1['va'][i,:]**2)+.01
    speed2=np.sqrt(data2['ua'][i,:]**2+data2['va'][i,:]**2)+.01
    divco=np.divide((speed2-speed1),speed1)
    divco[np.isnan(divco)]=0
    triax=ax.tripcolor(data1['trigrid'],divco,vmin=cmin,vmax=cmax,cmap=mpl.cm.seismic)
    #plotcoast(ax,color='k',fill=True)
    if cages!=None:   
        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        ax.add_collection(lseg_t) 
    vidx=equal_vectors(data2,region,300)
    Q1=ax.quiver(data2['uvnodell'][vidx,0],data2['uvnodell'][vidx,1],data2['ua'][i,vidx],data2['va'][i,vidx],angles='xy',scale_units='xy',scale=50,zorder=10)    
    aqk1=ax.quiverkey(Q1,.1,.95,0.5, r'0.5 m/s', labelpos='E',fontproperties={'size': 10})
    aqk1.set_zorder(30)
    prettyplot_ll(ax,setregion=region,cblabel=r'Speed Rel Diff. (ms$^{-1}$)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_speed_reldiff_' + ("%04d" %(i)) + '.png',dpi=150)
    plt.close(f)



pool = multiprocessing.Pool()
pool.map(myplot,range(starttime,endtime))

































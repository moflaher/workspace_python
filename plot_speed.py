from __future__ import division
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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import multiprocessing


global name
global grid
global regionname
global region
global tmparray
global savepath
global data
global cmin
global cmax



# Define names and types of data
name='test_interp_bathymetry'
grid='smallcape_force'
datatype='2d'
regionname='mp'
starttime=0
endtime=100
cmin=0
cmax=5


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data,trifinder=False,uvhset=False)
print 'done sort'


cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
if cages!=None:
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.2
    ls='solid'


region=regions(regionname)

savepath='figures/timeseries/' + grid + '_' + datatype + '/speed/' + name + '_' + regionname + '_' +("%f" %cmin) + '_' + ("%f" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)


def speed_plot(i):
    print i
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],np.sqrt(data['ua'][i,:]**2+data['va'][i,:]**2),vmin=cmin,vmax=cmax)
#    plotcoast(ax,color='k',fill=True)
#    if cages!=None:   
#        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
#        ax.add_collection(lseg_t) 
    prettyplot_ll(ax,setregion=region,cblabel=r'Speed (ms$^{-1}$)',cb=triax,grid=True)
    f.savefig(savepath + grid + '_' + regionname +'_speed_' + ("%04d" %(i)) + '.png',dpi=150)
    plt.close(f)



pool = multiprocessing.Pool(8)
pool.map(speed_plot,range(starttime,endtime))































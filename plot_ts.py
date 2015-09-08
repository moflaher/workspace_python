from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
from misctools import *
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




# Define names and types of data
name='kit4_kelp_baroclinic_2'
grid='kit4_kelp'
regionname='kit4'
datatype='2d'
starttime=0
endtime=20


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data,trifinder=False,uvhset=False)
print('done sort')


cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
if cages!=None:
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.2
    ls='solid'


region=regions(regionname)

savepath_t='figures/timeseries/' + grid + '_' + datatype + '/temp/' + name + '_' + regionname + '/'
if not os.path.exists(savepath_t): os.makedirs(savepath_t)
savepath_s='figures/timeseries/' + grid + '_' + datatype + '/sal/' + name + '_' + regionname + '/'
if not os.path.exists(savepath_s): os.makedirs(savepath_s)


def ts_plot(i):
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],data['temp'][i,0,:])
#    plotcoast(ax,color='k',fill=True)
#    if cages!=None:   
#        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
#        ax.add_collection(lseg_t) 
    prettyplot_ll(ax,setregion=region,cblabel=r'Temp (degree)',cb=triax,grid=True)
    f.savefig(savepath_t + grid + '_' + regionname +'_temp_' + ("%04d" %(i)) + '.png',dpi=150)
    plt.close(f)

    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],data['salinity'][i,0,:])
#    plotcoast(ax,color='k',fill=True)
#    if cages!=None:   
#        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
#        ax.add_collection(lseg_t) 
    prettyplot_ll(ax,setregion=region,cblabel=r'Salinity',cb=triax,grid=True)
    f.savefig(savepath_s + grid + '_' + regionname +'_sal_' + ("%04d" %(i)) + '.png',dpi=150)
    plt.close(f)


pool = multiprocessing.Pool()
pool.map(ts_plot,range(starttime,endtime))































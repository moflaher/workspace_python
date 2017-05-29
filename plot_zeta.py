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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import multiprocessing

global name
global grid
global regionname
global region
global tmparray
global savepath
global data
global nidx



# Define names and types of data
name='sjh_hr_v2_test_03'
grid='sjh_hr_v2'
datatype='2d'
regionname='stjohn_harbour'
starttime=768
endtime=864


### load the .nc file #####
data = loadnc('/fs/vnas_Hdfo/odis/mif001/scratch/'+grid+'/'+name+'/output',singlename=grid + '_0001.nc')
data['lon']=data['lon']-360
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
print('done load')
data = ncdatasort(data)
print('done sort')

cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
if cages!=None:
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.2
    ls='solid'


region=regions(regionname)
nidx=get_nodes(data,region)

savepath='figures/timeseries/' + grid + '_' + datatype + '/zeta/' + name + '_' + regionname + '/'
if not os.path.exists(savepath): os.makedirs(savepath)


def zeta_plot(i):
    print(i)
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    nidxh=data['zeta'][i,nidx]
    her=np.percentile(nidxh,[5,95])
    triax=ax.tripcolor(data['trigrid'],data['zeta'][i,:],vmin=her[0],vmax=her[1])
#    plotcoast(ax,color='k',fill=True)
#    if cages!=None:   
#        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
#        ax.add_collection(lseg_t) 
    prettyplot_ll(ax,setregion=region,cblabel='Elevation (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_zeta_' + ("%04d" %(i)) + '.png',dpi=600)
    plt.close(f)


trange=range(len(data['time']))
starttime=trange[starttime]
endtime=trange[endtime]
#pool = multiprocessing.Pool(1)
#pool.map(zeta_plot,range(starttime,endtime))
for i in range(starttime,endtime):
    zeta_plot(i)




























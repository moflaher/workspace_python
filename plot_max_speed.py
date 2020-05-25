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
name='2012-02-01_2012-03-01'
grid='fr_high'
regionlist=['fr_mouth']

starttime=0
endtime=2785
clim_min=2
clim_max=98



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




savepath='figures/png/' + grid + '_'  + '/max_speed/' + name + '/'
if not os.path.exists(savepath): os.makedirs(savepath)


for regionname in regionlist:
    print('Plotting region:' + regionname)
    region=regions(regionname)
    eidx=get_elements(data,region)
    
    mspeed=np.zeros((data['nele'],))
    mspeed[eidx]=np.max(np.sqrt(data['ua'][starttime:endtime,eidx]**2+data['va'][starttime:endtime,eidx]**2),axis=0)

    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    clims=np.percentile(mspeed[eidx],[clim_min,clim_max])
    triax=ax.tripcolor(data['trigrid'],mspeed,vmin=clims[0],vmax=clims[1])
    plotcoast(ax,filename='pacific_harbour.nc',fcolor='darkgreen',color='None',fill=True)
    if np.shape(cages)!=():   
        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        ax.add_collection(lseg_t)         
    prettyplot_ll(ax,setregion=region,cblabel=r'Max Speed (ms$^{-1}$)',cb=triax)
    f.savefig(savepath + grid + '_' + region['regionname'] +'_maxspeed.png',dpi=300)
    plt.close(f)



from __future__ import division,print_function
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import scipy.io as sio
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
from StringIO import StringIO
from gridtools import *
from datatools import *
from misctools import *
from plottools import *
from projtools import *
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name='kit4_baroclinic'
grid='kit4'
regionname='kit4_area5'
datatype='2d'
starttime=384
endtime=450
interpheight=1

### load the .nc file #####
data = loadnc('runs/'+grid+'/' + name + '/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')


region=regions(regionname)


savepath='figures/timeseries/' + grid + '_' + datatype + '/currents_' + ("%d" %interpheight)+ 'm/' +region['regionname']+'/'
if not os.path.exists(savepath): os.makedirs(savepath)

print('Loading old interpolated currents')
currents=np.load('data/interp_currents/'+ grid + '_' +name+ '_' + ("%d" %interpheight) + 'm.npy')
currents=currents[()]
print('Loaded old interpolated currents')



vectorspacing=250
vector_scale=100
cmin=0
cmax=1


vidx=equal_vectors(data,region,vectorspacing)



for i in range(starttime,endtime):
    print(i)
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],np.sqrt(currents['u'][i,:]**2+currents['v'][i,:]**2),vmin=cmin,vmax=cmax)
    plotcoast(ax,color='k',fill=True)
    #if np.shape(cages)!=():   
        #lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        #ax.add_collection(lseg_t) 
    Q1=ax.quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],1,1,angles='xy',scale_units='xy',scale=vector_scale,zorder=100,width=.0025)           
    prettyplot_ll(ax,setregion=region,cblabel=r'Speed (ms$^{-1}$)',cb=triax)
    f.savefig(savepath + grid + '_' + region['regionname'] +'_speed_' + ("%04d" %(i)) + '.png',dpi=150)
    plt.close(f)

























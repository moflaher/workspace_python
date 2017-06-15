from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from folderpath import *
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
import pymp


global name
global grid
global regionname
global region
global tmparray
global savepath
global data
global cmin
global cmax
global vectorflag
global uniformvectorflag
global coastflag
global vidx
global vector_scale



# Define names and types of data
name='2011-08-25_2011-09-08_0.0025'
grid='acadia_force_2d'
datatype='2d'
regionname='mp'
starttime=0
endtime=100
layer='da'
cmin=0
cmax=4



### load the .nc file #####
data = loadnc(runpath+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data,trifinder=False,uvhset=False)
print('done sort')

vectorflag=False
coastflag=True
uniformvectorflag=False
vector_spacing=125
vector_scale=50


region=regions(regionname)
vidx=equal_vectors(data,region,vector_spacing)


savepath='{}timeseries/{}_{}/speed/{}_{}_{}_{:.3f}_{:.3f}/'.format(figpath,grid,datatype,name,region['regionname'],layer,cmin,cmax)
if not os.path.exists(savepath): os.makedirs(savepath)


def speed_plot(i):
    print(i)
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])    
    if coastflag:
        plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc', filepath=coastpath, color='k', fcolor='darkgreen', fill=True)
    
    if layer is 'da':
        speed=np.sqrt(data['ua'][i,:]**2+data['va'][i,:]**2)
    else:
        speed=np.sqrt(data['u'][i,layer,:]**2+data['v'][i,layer,:]**2)
    
    triax=ax.tripcolor(data['trigrid'],speed,vmin=cmin,vmax=cmax)

    if vectorflag:
        Q1=ax.quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],data['ua'][i,vidx],data['va'][i,vidx],angles='xy',scale_units='xy',scale=vector_scale,zorder=100,width=.001)    
    if uniformvectorflag:
        norm=np.sqrt(data['ua'][i,vidx]**2+data['va'][i,vidx]**2)
        Q1=ax.quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],np.divide(data['ua'][i,vidx],norm),np.divide(data['va'][i,vidx],norm),angles='xy',scale_units='xy',scale=vector_scale,zorder=100,width=.002,color='k')  
        
    prettyplot_ll(ax,setregion=region,cblabel=r'Speed (ms$^{-1}$)',cb=triax)
    f.savefig(savepath + grid + '_' + region['regionname'] +'_speed_' + ("%04d" %(i)) + '.png',dpi=150)
    plt.close(f)



#pool = multiprocessing.Pool()
#pool.map(speed_plot,range(starttime,endtime))

with pymp.Parallel(4) as p:
    for i in p.range(starttime,endtime):
        speed_plot(i)





























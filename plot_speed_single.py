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
name='sjh_hr_v2_newriver_0.5'
grid='sjh_hr_v2'
datatype='2d'
regionname='stjohn_harbour'
starttime=0
endtime=2000
cmin=0
cmax=3
layer='da'


### load the .nc file #####
data = loadnc(runpath+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data['lon']=data['lon']-360
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
print('done load')
del data['trigrid']
data = ncdatasort(data)
print('done sort')






region=regions(regionname)


savepath='{}timeseries/{}_{}/speed/{}_{}_{}_{:.3f}_{:.3f}/'.format(figpath,grid,datatype,name,region['regionname'],layer,cmin,cmax)
if not os.path.exists(savepath): os.makedirs(savepath)



f=plt.figure()
ax=plt.axes([.125,.1,.775,.8]) 
plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc',filepath=coastpath, color='k', fcolor='0.75', fill=True)  
_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
ax.yaxis.set_major_formatter(_formatter)
ax.xaxis.set_major_formatter(_formatter)
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: -1*x))
ax.set_xlabel(r'Longitude ($^{\circ}$W)')
ax.set_ylabel(r'Latitude ($^{\circ}$N)')
ax.axis(region['region'])
ax.set_aspect(get_aspectratio(region),anchor='SW')
f.canvas.draw()


#Find the bounding box and if its too big for a colorbar then reduce size
box=ax.get_position()
cbarwidth=box.xmax+0.1+0.1
if cbarwidth>1.0:
    resize=cbarwidth-1.0+.01
    box.set_points(np.array([[box.xmin,box.ymin],[box.xmax-resize,box.ymax]]))
    ax.set_position(box)
    f.canvas.draw()
    
box=ax.get_position()
cax=f.add_axes([box.xmax + .025, box.ymin, .025, box.height])

i=starttime
if layer is 'da':
    speed=np.sqrt(data['ua'][i,:]**2+data['va'][i,:]**2)
else:
    speed=np.sqrt(data['u'][i,layer,:]**2+data['v'][i,layer,:]**2)
triax=ax.tripcolor(data['trigrid'],speed,vmin=cmin,vmax=cmax)
cb=plt.colorbar(triax,cax=cax)
cb.set_label(r'Speed (ms$^{-1}$)',fontsize=10)

f.canvas.draw()
background = f.canvas.copy_from_bbox(ax.bbox)
 
for i in range(starttime+1,endtime):
    print(i)
    f.canvas.restore_region(background)
    if layer is 'da':
        speed=np.sqrt(data['ua'][i,:]**2+data['va'][i,:]**2)
    else:
        speed=np.sqrt(data['u'][i,layer,:]**2+data['v'][i,layer,:]**2)    
    triax.set_array(speed)
    ax.draw_artist(triax)
    f.canvas.blit(ax.bbox)
    f.savefig('{}{}_{}_speed_{:05d}.png'.format(savepath,grid,region['regionname'],i),dpi=600)




























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
name='sjh_hr_v1_test_01'
grid='sjh_hr_v1'
datatype='2d'
regionname='stjohn_harbour_tight'
starttime=1000
endtime=1010
cmin=0
cmax=0.4


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')






region=regions(regionname)


savepath='figures/timeseries/' + grid + '_' + datatype + '/speed/' + name + '_' + region['regionname'] + '_' +("%f" %cmin) + '_' + ("%f" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)



f=plt.figure()
ax=plt.axes([.125,.1,.775,.8]) 
plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc',color='k', fcolor='darkgreen', fill=True)  
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
triax=ax.tripcolor(data['trigrid'],np.sqrt(data['ua'][i,:]**2+data['va'][i,:]**2),vmin=cmin,vmax=cmax)
cb=plt.colorbar(triax,cax=cax)
cb.set_label(r'Speed (ms$^{-1}$)',fontsize=10)

f.canvas.draw()
background = f.canvas.copy_from_bbox(ax.bbox)
 
for i in range(starttime+1,endtime):
    print(i)
    f.canvas.restore_region(background)
    triax.set_array(np.sqrt(data['ua'][i,:]**2+data['va'][i,:]**2))
    ax.draw_artist(triax)
    f.canvas.blit(ax.bbox)
    f.savefig(savepath + grid + '_' + region['regionname'] +'_speed_' + ("%04d" %(i)) + '.png',dpi=150)
#plt.close(f)



#pool = multiprocessing.Pool()
#pool.map(speed_plot,range(starttime,endtime))































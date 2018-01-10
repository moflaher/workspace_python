from __future__ import division,print_function
import matplotlib as mpl
mpl.use('Agg')
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
name='jul2015_nest_lowdif'
grid='sjh_hr_v3'
datatype='2d'
regionname='bof_nemo'
starttime=1008
endtime=1508
cmin=-200
cmax=600



### load the .nc file #####
data = loadnc('/fs/vnas_Hdfo/odis/suh001/scratch/sjh_hr_v3_clean/runs/{}/output/'.format(name),singlename=grid + '_0001.nc')
print('done load')

region=regions(regionname)


savepath='{}timeseries/{}_{}/netheat/{}_{}_{}_{}/'.format(figpath,grid,datatype,name,region['regionname'],cmin,cmax)
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
#ax.set_aspect(get_aspectratio(region),anchor='SW')
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
heat=data['net_heat_flux'][i,:]
triax=ax.tripcolor(data['trigrid'],heat,vmin=cmin,vmax=cmax)
cb=plt.colorbar(triax,cax=cax)
cb.set_label(r'Net Heat Flux',fontsize=10)

f.canvas.draw()
background = f.canvas.copy_from_bbox(ax.bbox)


def speed_plot(i):
    print(i)
    f.canvas.restore_region(background)
    heat=np.mean(data['net_heat_flux'][i,data['nv']],axis=1)
    triax.set_array(heat)
    ax.draw_artist(triax)
    f.canvas.blit(ax.bbox)
    f.savefig('{}{}_{}_netheatflux_{:05d}.png'.format(savepath,grid,region['regionname'],i),dpi=300)


with pymp.Parallel(4) as p:
    for i in p.range(starttime,endtime):
        speed_plot(i)





























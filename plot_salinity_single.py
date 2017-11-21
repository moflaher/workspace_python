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
import pymp

# Define names and types of data
name='sjh_lr_v1_year_origbc_wet_hfx100'
grid='sjh_lr_v1'
datatype='2d'
regionname='bof_nemo'
starttime=0
endtime=10909
cmin=8
cmax=31
layer=0


### load the .nc file #####
data = loadnc('/fs/vnas_Hdfo/odis/suh001/scratch/sjh_lr_v1/runs/{}/output/'.format(name),singlename=grid + '_0001.nc')
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
print('done load')
data = ncdatasort(data)
print('done sort')


coast=False

region=regions(regionname)


savepath='{}timeseries/{}_{}/salinity/{}_{}_{}_{:.3f}_{:.3f}/'.format(figpath,grid,datatype,name,region['regionname'],layer,cmin,cmax)
if not os.path.exists(savepath): os.makedirs(savepath)



f=plt.figure()
ax=plt.axes([.125,.1,.775,.8]) 
if coast:
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
triax=ax.tripcolor(data['trigrid'],data['salinity'][i,layer,:],vmin=cmin,vmax=cmax)
cb=plt.colorbar(triax,cax=cax)
cb.set_label(r'Salinity',fontsize=10)

f.canvas.draw()
background = f.canvas.copy_from_bbox(ax.bbox)

#for i in range(starttime+1,endtime):
def plot_salinity(i):
    print(i)
    f.canvas.restore_region(background)
    fcolors=np.mean(data['salinity'][i,layer,data['nv']],axis=1)
    triax.set_array(fcolors)
    ax.draw_artist(triax)
    f.canvas.blit(ax.bbox)
    f.savefig('{}{}_{}_salinity_{:05d}.png'.format(savepath,grid,region['regionname'],i),dpi=600)

with pymp.Parallel(4) as p:
    for i in p.range(starttime+1,endtime):
        plot_salinity(i)




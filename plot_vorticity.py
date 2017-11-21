from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from folderpath import *
from datatools import *
from gridtools import *
from plottools import *
from misctools import *
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
regionname='stjohn_harbour'
starttime=2000
endtime=2500
cmin=-.025
cmax=.025


### load the .nc file #####
data = loadnc('/fs/vnas_Hdfo/odis/suh001/scratch/sjh_lr_v1/runs/{}/output/'.format(name),singlename=grid + '_0001.nc')
print('done load')

savepath='figures/timeseries/' + grid + '_' + datatype + '/curl/' + name + '_' + regionname + '_' +("%f" %cmin) + '_' + ("%f" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)


region=regions(regionname)


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
dudy= data['a2u'][0,:]*data['ua'][i,:]+data['a2u'][1,:]*data['ua'][i,data['nbe'][:,0]]+data['a2u'][2,:]*data['ua'][i,data['nbe'][:,1]]+data['a2u'][3,:]*data['ua'][i,data['nbe'][:,2]]
dvdx= data['a1u'][0,:]*data['va'][i,:]+data['a1u'][1,:]*data['va'][i,data['nbe'][:,0]]+data['a1u'][2,:]*data['va'][i,data['nbe'][:,1]]+data['a1u'][3,:]*data['va'][i,data['nbe'][:,2]]
curl=dvdx-dudy
triax=ax.tripcolor(data['trigrid'],curl,vmin=cmin,vmax=cmax,cmap=mpl.cm.seismic)
cb=plt.colorbar(triax,cax=cax)
cb.set_label(r'Curl',fontsize=10)

f.canvas.draw()
background = f.canvas.copy_from_bbox(ax.bbox)


def speed_plot(i):
    print(i)
    f.canvas.restore_region(background)
    dudy= data['a2u'][0,:]*data['ua'][i,:]+data['a2u'][1,:]*data['ua'][i,data['nbe'][:,0]]+data['a2u'][2,:]*data['ua'][i,data['nbe'][:,1]]+data['a2u'][3,:]*data['ua'][i,data['nbe'][:,2]]
    dvdx= data['a1u'][0,:]*data['va'][i,:]+data['a1u'][1,:]*data['va'][i,data['nbe'][:,0]]+data['a1u'][2,:]*data['va'][i,data['nbe'][:,1]]+data['a1u'][3,:]*data['va'][i,data['nbe'][:,2]]
    curl=dvdx-dudy
    triax.set_array(curl)
    ax.draw_artist(triax)
    f.canvas.blit(ax.bbox)
    f.savefig('{}{}_{}_curl_{:05d}.png'.format(savepath,grid,region['regionname'],i),dpi=300)


with pymp.Parallel(4) as p:
    for i in p.range(starttime,endtime):
        speed_plot(i)
































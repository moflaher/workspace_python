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
import multiprocessing
import pymp
import seawater as sw
import argparse




parser = argparse.ArgumentParser()
parser.add_argument("grid", help="name of the grid", type=str)
parser.add_argument("name", help="name of the run", type=str)
#parser.add_argument("field", help="field to plot from ncfile", type=str, default=None, nargs='?')
parser.add_argument("times", help="specify start and end step",type=int,nargs=2)
#parser.add_argument("minmax", help="specify colorbar limits",type=float,nargs=2)
parser.add_argument("ncfile", help="specify ncfile", type=str)
parser.add_argument("-dpi", help="dpi of plot",type=int, default=150)
parser.add_argument("-zoom", help="specify zoom axis",type=float,nargs=4,default=None)
parser.add_argument("-region", help="specify predefined region",type=str,default=None)
parser.add_argument("-layer", help="specify layer to plot",type=str,default='da')
parser.add_argument("--coastline", help="disable coastline",type=bool,default=True)
#parser.add_argument("--vectorflag", help="disable coastline",type=bool,default=True)
parser.add_argument("-cmap", help="specify colormap",type=str,default='viridis')
args = parser.parse_args()

print("The current commandline arguments being used are")
print(args)


# Define names and types of data
name=args.name
grid=args.grid
field=args.field
starttime=args.times[0]
endtime=args.times[1]
cmin=args.minmax[0]
cmax=args.minmax[1]
ncfile=args.ncfile
ncloc=ncfile.rindex('/')
if args.layer!='da':
    layer=int(args.layer)
else:
    layer=args.layer
coastflag=args.coastline
# if field is None:
    # print('Please specify one of the following field:')  
    # print(['temp','salinity','speed','u','v','vorticity','density','zeta'])
    # sys.exit()
regionname=args.region
region=regions(regionname)

### load the .nc file #####
data = loadnc(ncfile[:ncloc+1],ncfile[ncloc+1:])
print('done load')

farmslat=np.array([[44,39,27.69],
		   [44,39,28.17],
		   [44,39,22.82],
                   [44,38,59.59],
                   [44,38,58.53],
                   [44,39,18.77]])
farmslon=np.array([[65,45,24.29],
		   [65,45,15.70],
		   [65,45,12.46],
                   [65,45,09.59],
                   [65,45,26.32],
                   [65,45,27.03]])

farmsoldlat=np.array([[44,39,20.34],
		   [44,39,20.40],
		   [44,39,08.76],
                   [44,39,05.52],
                   [44,39,05.40]])
farmsoldlon=np.array([[65,45,27.36],
		   [65,45,20.10],
		   [65,45,17.64],
                   [65,45,17.58],
                   [65,45,27.06]])
lat=farmslat[:,0]+farmslat[:,1]/60.0+farmslat[:,2]/3600.0
lon=farmslon[:,0]+farmslon[:,1]/60.0+farmslon[:,2]/3600.0
latold=farmsoldlat[:,0]+farmsoldlat[:,1]/60.0+farmsoldlat[:,2]/3600.0
lonold=farmsoldlon[:,0]+farmsoldlon[:,1]/60.0+farmsoldlon[:,2]/3600.0

lat=np.append(lat,lat[0])
lon=np.append(lon,lon[0])
latold=np.append(latold,latold[0])
lonold=np.append(lonold,lonold[0])


# vectorflag=False
# coastflag=True
# vector_spacing=800
# vector_scale=100

# #region=regions(regionname)
# vidx=equal_vectors(data,region,vector_spacing)

# nodefile=glob.glob('/mnt/drive_0/misc/gpscrsync/dataout/{}_2d/monthly_mean_surface/{}/node*'.format(grid,name))
# cellfile=glob.glob('/mnt/drive_0/misc/gpscrsync/dataout/{}_2d/monthly_mean_surface/{}/cell*'.format(grid,name))

# filenames=np.hstack([cellfile,nodefile]).T


savepath='{}png/{}/max_speed/{}/{}/'.format(figpath,grid,name,region['regionname'])
if not os.path.exists(savepath): os.makedirs(savepath)



f=plt.figure(figsize=region['figsize'])
ax=plt.axes(region['axes'])    
if coastflag:
    plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc', filepath=coastpath, color='k', fill=True)


idx=get_elements(data,region)

tidx=np.argwhere((data['time']>=data['time'][args.minmax[0]])&(data['time']<=data['time'][args.minmax[1]]))
speed=np.sqrt(data['ua'][tidx,:]**2+data['va'][tidx,:]**2)
maxspeed=speed.max(axis=0)

clim=np.percentile(maxspeed[idx.flatten()],[5,95])
triax=ax.tripcolor(data['trigrid'],maxspeed,vmin=clim[0],vmax=clim[1])
ax.plot(-1*lon,lat,'k',lw=2,zorder=100)
ax.plot(-1*lonold,latold,'r',lw=2,zorder=50)

# if vectorflag:
    # Q1=ax.quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],data['u'][i,layer,vidx],data['v'][i,layer,vidx],angles='xy',scale_units='xy',scale=vector_scale,zorder=100,width=.001)    
    # qaxk=ax.quiverkey(Q1,.775,.9,2, r'2 ms$^{-1}$')

cb=plt.colorbar(triax)
cb.set_label(field,fontsize=10)    
ax.set_xlabel(r'Longitude ($^{\circ}$)')
ax.set_ylabel(r'Latitude ($^{\circ}$)')
ax.axis(region['region'])
#ax.annotate('{}'.format(filename[136:-4]),xy=(.425,.93),xycoords='axes fraction')
for label in ax.get_xticklabels()[::2]:
    label.set_visible(False)
f.savefig('{}{}_{}_{}_{}_{:05d}.png'.format(savepath,grid,name,region['regionname'],'maxspeed',i),dpi=300)
plt.close(f)
































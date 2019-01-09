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
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
#import multiprocessing
#import pymp
import seawater as sw
import argparse




parser = argparse.ArgumentParser()
parser.add_argument("grid", help="name of the grid", type=str)
parser.add_argument("name", help="name of the run", type=str)
parser.add_argument("field", help="field to plot from ncfile", type=str, default=None, nargs='?')
parser.add_argument("times", help="specify start and end step",type=int,nargs=2)
parser.add_argument("minmax", help="specify zoom axis",type=float,nargs=2)
parser.add_argument("ncfile", help="specify ncfile", type=str)
parser.add_argument("-dpi", help="dpi of plot",type=int, default=150)
parser.add_argument("-zoom", help="specify zoom axis",type=float,nargs=4,default=None)
parser.add_argument("-region", help="specify predefined region",type=str,default=None)
parser.add_argument("-layer", help="specify layer to plot",type=str,default='da')
parser.add_argument("--coastline", help="disable coastline",type=bool,default=True)
#parser.add_argument("--vectorflag", help="disable coastline",type=bool,default=True)
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
if field is None:
    print('Please specify one of the following field:')  
    print(['temp','salinity','speed','u','v','vorticity','density','zeta'])
    sys.exit()
regionname=args.region



# vectorflag=False
# uniformvectorflag=False
# vector_spacing=800
# vector_scale=100


### load the .nc file #####
data = loadnc(ncfile[:ncloc+1],ncfile[ncloc+1:])
print('done load')

if endtime==-1:
    endtime=len(data['time'])
    print('Plotting {} timesteps'.format(endtime-starttime))
    
if regionname is not None:
    region=regions(regionname)
else:
    if args.zoom is not None:
        region={'region':np.array([args.zoom])}
    else:
        region={'region': np.array([data['lon'].min(),data['lon'].max(),data['lat'].min(),data['lat'].max()])}
    region['regionname']='zoom_'+array2str(region['region'])[:-1]
    region['figsize']=(4,3)
    region['axes']=[.125,.1,.775,.8]
    region['coast']='mid_nwatl6c_sjh_lr.nc'

#region['region']=np.array([1.5,2.5,1.9,2.1])
#vidx=equal_vectors(data,region,vector_spacing)

savepath='{}timeseries/{}/{}/{}/{}_{}_{:.4f}_{:.4f}/'.format(figpath,grid,field,name,region['regionname'],layer,cmin,cmax)
if not os.path.exists(savepath): os.makedirs(savepath)



def plot_fun(i):
    print(i)
    
    fieldout, fieldname = select_field(data, field, i, layer) 

    f=plt.figure(figsize=region['figsize'])
    ax=f.add_axes(region['axes'])    
    if coastflag:
        plotcoast(ax,filename=region['coast'], filepath=coastpath, color='k', fill=True)   
    
    triax=ax.tripcolor(data['trigrid'],fieldout,vmin=cmin,vmax=cmax)    
    
    # if vectorflag:
        # Q1=ax.quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],data['ua'][i,vidx],data['va'][i,vidx],angles='xy',scale_units='xy',scale=vector_scale,zorder=100,width=.001)    
        # qaxk=ax.quiverkey(Q1,.775,.9,.5, r'.5 ms$^{-1}$')
    # if uniformvectorflag:
        # norm=np.sqrt(data['u'][i,layer,vidx]**2+data['v'][i,layer,vidx]**2)
        # Q1=ax.quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],np.divide(data['u'][i,layer,vidx],norm),np.divide(data['v'][i,layer,vidx],norm),angles='xy',scale_units='xy',scale=vector_scale,zorder=100,width=.002,color='k')  
    
    cb=plt.colorbar(triax)
    cb.set_label(fieldname,fontsize=10)    
    ax.set_xlabel(r'Longitude ($^{\circ}$)')
    ax.set_ylabel(r'Latitude ($^{\circ}$)')
    ax.axis(region['region'])
    #ax.annotate('{} {}'.format(data['Time'][i][:10],data['Time'][i][11:19]),xy=region['textloc'],xycoords='axes fraction')
    for label in ax.get_xticklabels()[::2]:
        label.set_visible(False)
    f.savefig('{}{}_{}_{}_{}_{:05d}.png'.format(savepath,grid,name,region['regionname'],field,i),dpi=300)
    plt.close(f)



for i in range(starttime,endtime):
    plot_fun(i)

#pool = multiprocessing.Pool(30)
#pool.map(plot_fun,range(starttime,endtime))

#with pymp.Parallel(4) as p:
    #for i in p.range(starttime,endtime):
        #plot_fun(i)





























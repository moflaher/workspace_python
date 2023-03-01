from __future__ import division,print_function,print_function
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


# Define names and types of data
gridname='passbay_v5_pre'


regionlist=regions(group='bof')+regions(group='aquaculture')
data = load_nei2fvcom('/media/moflaher/data/grids/passbay_v5/fix_musq_23_r.nei')


savepath='figures/png/{}/regions_all/'.format(gridname)
if not os.path.exists(savepath): os.makedirs(savepath)


# Plot mesh
savepathmesh='figures/png/{}/regions_all/mesh/'.format(gridname)
if not os.path.exists(savepathmesh): os.makedirs(savepathmesh)

for i in range(0,len(regionlist)):
    regionname=regionlist[i]
    region=regions(regionname)
    nidx=get_nodes(data,region)
    if len(nidx)!=0:
        print('Printing mesh - ' + region['regionname'])
        f=plt.figure()
        ax=plt.axes([.125,.1,.8,.8])
        ax.triplot(data['trigrid'],lw=.5,color='k')
        ax.axis(region['region'])
        #prettyplot_ll(ax,setregion=region,grid=True)
        f.savefig(savepathmesh + gridname + '_' + regionname +'_mesh.png',dpi=150)
        #f.savefig(savepath + grid + '_' + regionname +'_mesh.png',dpi=300)
        plt.close(f)



# Plot bathy
savepathbathy='figures/png/{}/regions_all/bathy/'.format(gridname)
if not os.path.exists(savepathbathy): os.makedirs(savepathbathy)

for i in range(0,len(regionlist)):
    regionname=regionlist[i]
    region=regions(regionname)
    nidx=get_nodes(data,region)
    if len(nidx)!=0:
        print('Printing bathy - ' + region['regionname'])
        clim=np.percentile(data['h'][nidx],[10,90])
        f=plt.figure()
        ax=plt.axes([.125,.1,.8,.8])
        cax=ax.tripcolor(data['trigrid'],data['h'],vmin=clim[0],vmax=clim[1])
        ax.axis(region['region'])
        plt.colorbar(cax)
        #prettyplot_ll(ax,setregion=region,grid=True)
        f.savefig(savepathbathy + gridname + '_' + regionname +'_bathy.png',dpi=150)
        #f.savefig(savepath + grid + '_' + regionname +'_mesh.png',dpi=300)


        plt.close(f)





# Plot sidelength
savepathsl='figures/png/{}/regions_all/sidelength/'.format(gridname)
if not os.path.exists(savepathsl): os.makedirs(savepathsl)

for i in range(0,len(regionlist)):
    regionname=regionlist[i]
    region=regions(regionname)
    eidx=get_elements(data,region)
    if len(nidx)!=0:
        print('Printing sidelength - ' + region['regionname'])
        clim=np.percentile(data['sl'][eidx],[10,90])
        f=plt.figure()
        ax=plt.axes([.125,.1,.8,.8])
        cax=ax.tripcolor(data['trigrid'],data['sl'],vmin=clim[0],vmax=clim[1])
        ax.axis(region['region'])
        plt.colorbar(cax)
        #prettyplot_ll(ax,setregion=region,grid=True)
        f.savefig(savepathsl + gridname + '_' + regionname +'_sidelength.png',dpi=150)
        #f.savefig(savepath + grid + '_' + regionname +'_mesh.png',dpi=300)


        plt.close(f)





















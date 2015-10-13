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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name='vhfr_low'
grid='vhfr_low'
#regionlist=regions()
regionlist=['fr_whole','fr_mouth','pitt_lake','fr_area1','fr_area2','vh_whole','firstnarrows','secondnarrows','vhfr_whole']
regionlist=['vh_whole']
#regionlist=['firstnarrows','secondnarrows']
datatype='2d'



### load the mesh files #####
#data=load_fvcom_files('runs/'+grid+'/'+name+'/input',grid)
#data.update(loadnei('runs/'+grid+'/'+name+'/input/' +grid+ '.nei'))
data=loadnei('runs/'+grid+'/vhfr_low_clean_hpc/input/' +name+ '.nei')
data['x'],data['y'],proj=lcc(data['lon'],data['lat'])
data=get_nv(data)
data=ncdatasort(data)
data=get_sidelength(data)
data=get_dhh(data)

savepath='figures/png/' + grid + '_' + datatype + '/gridbasic/' +name + '/'
if not os.path.exists(savepath): os.makedirs(savepath)



for regionname in regionlist:
    
    region=regions(regionname)
    nidx=get_nodes(data,region)
    eidx=get_elements(data,region)

    if ((len(nidx)==0) or (len(eidx)==0)):
        continue
    
    print('plotting region: ' +regionname)


    # Plot mesh
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    ax.triplot(data['trigrid'],lw=.1)
    prettyplot_ll(ax,setregion=region,grid=True,title=regionname)
    f.savefig(savepath + grid + '_' + regionname +'_grid.png',dpi=300)
    plt.close(f)
    
    # Plot mesh
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    ax.triplot(data['trigrid'],lw=.1)
    prettyplot_ll(ax,setregion=region)
    plotcoast(ax,filename='pacific_harbour.nc',color='0.75',fill=True)
    f.savefig(savepath + grid + '_' + regionname +'_grid_pretty.png',dpi=300)
    plt.close(f)


    # Plot depth
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],data['h'],vmin=data['h'][nidx].min(),vmax=data['h'][nidx].max())
    prettyplot_ll(ax,setregion=region,grid=True,cblabel='Depth (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_depth.png',dpi=600)
    plt.close(f)

    # Plot depth shallow
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],data['h'],vmin=data['h'][nidx].min(),vmax=10)
    prettyplot_ll(ax,setregion=region,grid=True,cblabel='Depth (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_depth_shallow.png',dpi=1200)
    plt.close(f)


    # Plot depth percentile
    clims=np.percentile(data['h'][nidx],[5,95])
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],data['h'],vmin=clims[0],vmax=clims[1])
    prettyplot_ll(ax,setregion=region,grid=True,cblabel='Depth (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_depth_percentile.png',dpi=600)
    plt.close(f)


    # Plot dh/h
    clims=np.percentile(data['dhh'][nidx],[1,99])
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],data['dhh'],vmin=clims[0],vmax=clims[1])
    prettyplot_ll(ax,setregion=region,grid=True,cblabel=r'$\frac{\delta H}{H}$',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_dhh.png',dpi=600)
    plt.close(f)


    # Plot sidelength
    clims=np.percentile(data['sl'][eidx],[1,99])
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],data['sl'],vmin=clims[0],vmax=clims[1])
    prettyplot_ll(ax,setregion=region,grid=True,cblabel=r'Sidelength (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_sidelength.png',dpi=600)
    plt.close(f)



















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
name1='sjh_hr_v1_20150701-20150907'
grid1='sjh_hr_v1'
name2='sfm5m_sjr_baroclinic_20150615-20150905'
grid2='sfm5m_sjr'
regionlist=regions()
#regionlist=['fr_whole','fr_mouth','pitt_lake','fr_area1','fr_area2','vh_whole','firstnarrows','secondnarrows','vhfr_whole']
#regionlist=['kelp_channel']
regionlist=['gp','pp','gp_tight','dg','dg_upper','sfmwhole','bof','mp','pp','blackrock','blackrock_ebb','blackrock_fld','capedor','northgrid','northgrid_cape']
regionlist=['stjohn_harbour']#,'sjr_kl']#,'stjohn_harbour']
datatype='2d'



### load the mesh files #####
#data=load_neifile('runs/sfm5m_sjr/sfm5m_sjr_baroclinic_20150615-20150905/input/sjh_hr_v1.nei')
#data['x'],data['y'],proj=lcc(data['lon'],data['lat'])
#data=get_nv(data)
data1=loadnc('runs/'+grid1+'/'+name1+'/output/',singlename=grid1 + '_0001.nc')
data1=ncdatasort(data)
data1=get_sidelength(data)

data2=loadnc('runs/'+grid2+'/'+name2+'/output/',singlename=grid2 + '_0001.nc')
data2=ncdatasort(data)
data2=get_sidelength(data)

savepath='figures/png/grid_compare/' +grid1 + '_' +grid2 + '/'
if not os.path.exists(savepath): os.makedirs(savepath)



for regionname in regionlist:
    
    region=regions(regionname)
     
    print('plotting region: ' +regionname)

    
    # Plot mesh
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    ax.triplot(data['trigrid'],lw=.1,color='k')
    prettyplot_ll(ax,setregion=region,axlabels=False)
    plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc',color='k',fill=True,lw=.5)
    f.savefig(savepath + grid + '_' + regionname +'_grid_pretty.png',dpi=300)
    plt.close(f)


    # Plot depth
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],data['h'],vmin=-5,vmax=75)
    prettyplot_ll(ax,setregion=region,cblabel='Depth (m)',cb=triax,axlabels=False)
    plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc',color='k',fill=True,lw=.5)
    f.savefig(savepath + grid + '_' + regionname +'_depth.png',dpi=300)
    plt.close(f)

 

    # Plot dh/h
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],data['dhh'],vmin=0,vmax=1)
    prettyplot_ll(ax,setregion=region,cblabel=r'$\frac{\delta H}{H}$',cb=triax,axlabels=False)
    plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc',color='k',fill=True,lw=.5)
    f.savefig(savepath + grid + '_' + regionname +'_dhh.png',dpi=300)
    plt.close(f)


    # Plot sidelength
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],data['sl'],vmin=25,vmax=500)
    prettyplot_ll(ax,setregion=region,cblabel=r'Sidelength (m)',cb=triax,axlabels=False)
    plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc',color='k',fill=True,lw=.5)
    f.savefig(savepath + grid + '_' + regionname +'_sidelength.png',dpi=300)
    plt.close(f)



















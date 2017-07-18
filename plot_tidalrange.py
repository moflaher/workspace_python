from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from folderpath import *
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pandas as pd

# Define names and types of data
name='sjh_hr_v2_spg_100x'
grid='sjh_hr_v2'
datatype='2d'
starttime=960
endtime=-1


### load the .nc file #####
#data = loadnc(runpath+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data = loadnc('/fs/vnas_Hdfo/odis/mif001/scratch/test_dme/sjh_hr_v2_spg_100x/output/',singlename=grid + '_0001.nc')
data['lon']=data['lon']-360
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
print('done load')
del data['trigrid']
data = ncdatasort(data)
print('done sort')


savepath='{}/png/{}_{}/misc/'.format(figpath,grid,datatype)
if not os.path.exists(savepath): os.makedirs(savepath)


mzeta=data['zeta'][starttime:endtime,:].max(axis=0)-data['zeta'][starttime:endtime,:].min(axis=0)

regionlist=['sfmwhole','bof_nemo','stjohn_nemo','sjr_kl']

for regionname in regionlist:

    region=regions(regionname)
    nidx=get_nodes(data,region)

    clim=np.percentile(mzeta[nidx],[5,95])
    f,ax,cax=setplot(region)
    plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc',filepath=coastpath, color='k', fcolor='0.75', fill=True)
    triax=ax.tripcolor(data['trigrid'],mzeta,vmin=clim[0], vmax=clim[1])
    cb=plt.colorbar(triax,cax=cax)
    cb.set_label(r'Tidal Range (m)')  
    f.savefig('{}{}_{}_tidal_range.png'.format(savepath,name,regionname),dpi=600)
    plt.close(f)














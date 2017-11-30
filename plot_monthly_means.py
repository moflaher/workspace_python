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




# Define names and types of data
name='sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1'
grid='sjh_lr_v1'
datatype='2d'
regionname='stjohn_harbour'

region={}
region['region']=np.array([-66.45,-65.55,44.9,45.325])
region['regionname']='nemofvcom_100m_grid'

### load the .nc file #####
data = loadnc('/mnt/drive_1/runs/{}/{}_15mins/output/'.format(grid,name),singlename=grid + '_0001.nc')
print('done load')


vectorflag=False
coastflag=True
vector_spacing=800
vector_scale=100

#region=regions(regionname)
vidx=equal_vectors(data,region,vector_spacing)

nodefile=glob.glob('/mnt/drive_0/misc/gpscrsync/dataout/{}_2d/monthly_mean_surface/{}/node*'.format(grid,name))
cellfile=glob.glob('/mnt/drive_0/misc/gpscrsync/dataout/{}_2d/monthly_mean_surface/{}/cell*'.format(grid,name))

filenames=np.hstack([cellfile,nodefile]).T


savepath='{}png/{}_{}/monthly_means_nemofvcom/{}_{}/'.format(figpath,grid,datatype,name,region['regionname'])
if not os.path.exists(savepath): os.makedirs(savepath)

for filename in filenames:

    print(filename)
    loaded=pd.read_csv(filename,delimiter=' ')

    for field in ['surf_speed','zeta','temp','sal']:
        if field not in loaded.keys():
            continue
    
        f=plt.figure(figsize=(25/2.539,15/2.536))
        ax=plt.axes([.13,.11,.8825,.8125])    
        if coastflag:
            plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc', filepath=coastpath, color='k', fill=True)
        
        if field=='surf_speed':
            idx=get_elements(data,region)
        else:
            idx=get_nodes(data,region)
        
        clim=np.percentile(loaded[field][idx.flatten()],[5,95])
        triax=ax.tripcolor(data['trigrid'],loaded[field],vmin=clim[0],vmax=clim[1])

        if vectorflag:
            Q1=ax.quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],data['u'][i,layer,vidx],data['v'][i,layer,vidx],angles='xy',scale_units='xy',scale=vector_scale,zorder=100,width=.001)    
            qaxk=ax.quiverkey(Q1,.775,.9,2, r'2 ms$^{-1}$')
       
        cb=plt.colorbar(triax)
        cb.set_label(field,fontsize=10)    
        ax.set_xlabel(r'Longitude ($^{\circ}$)')
        ax.set_ylabel(r'Latitude ($^{\circ}$)')
        ax.axis(region['region'])
        ax.annotate('{}'.format(filename[136:-4]),xy=(.425,.93),xycoords='axes fraction')
        for label in ax.get_xticklabels()[::2]:
            label.set_visible(False)
        f.savefig(savepath + grid + '_' + region['regionname'] +'_{}_monthly_mean_nemofvcom_{}'.format(field,filename[136:-4].replace(':',''))+ '.png',dpi=300)
        plt.close(f)
































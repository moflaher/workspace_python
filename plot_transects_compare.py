from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from misctools import *
from plottools import *
from projtools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
from scipy.interpolate import interp1d
from matplotlib import patches as pp
from osgeo import osr, gdal
from matplotlib.colors import LinearSegmentedColormap
import collections
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Define names and types of data
name='vh_high_3d_profile'
grid='vh_high'





### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')
mlay=20
sigh=data['siglay'][:,0]

trans=np.load('data/misc/vhfr_obs/transects/VH_5x1m_corrected.npy')
trans=trans[()]

mtrans=np.load('data/misc/vhfr_obs/transects/VH_5x1m_corrected_model_vh_high_2.npy')
mtrans=mtrans[()]


savepath='figures/png/' + grid + '_'  + '/transects_compare/'
if not os.path.exists(savepath): os.makedirs(savepath)



for key in trans.keys():
    print('')
    print(key)
    
    loc=trans[key]['Bin_Position']
    dist=np.array([np.sqrt(np.sum((loc[0,:]-tloc)**2)) for tloc in loc])
    depth=-1*trans[key]['Depth']
    
    

    
    line='LineA'
    mspeeda=np.sqrt(mtrans[key][line]['v']**2+mtrans[key][line]['u']**2)
    speeda=np.sqrt(trans[key][line]['East']**2+trans[key][line]['North']**2)
    line='LineB'
    mspeedb=np.sqrt(mtrans[key][line]['v']**2+mtrans[key][line]['u']**2) 
    speedb=np.sqrt(trans[key][line]['East']**2+trans[key][line]['North']**2) 
    
    allspeed=np.vstack([mspeeda,speeda,mspeedb,speedb])
    cspeed=allspeed[~np.isnan(allspeed)]
    if len(cspeed)==0:
        continue
    
    clim=np.percentile(cspeed,[5,95])
    
    line='LineA'
    f = plt.figure(figsize=(15,5))
    s=.075
    w=.24
    start=.055
    ax1 = f.add_axes([start,.1,w,.79])
    ax2 = f.add_axes([start+w+s,.1,w,.79])
    ax3 = f.add_axes([start+(w+s)*2,.1,w,.79])
    

    cbax1=ax1.pcolormesh(dist,depth,mspeeda,vmin=clim[0],vmax=clim[1])
    cbax2=ax2.pcolormesh(dist,depth,speeda,vmin=clim[0],vmax=clim[1])
    
    lim=np.nanmax(np.fabs(np.hstack([mspeeda-speeda,mspeedb-speedb])))*.95
    cbax3=ax3.pcolormesh(dist,depth,mspeeda-speeda,vmin=-lim,vmax=lim,cmap=mpl.cm.seismic)
    
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("right", size="7.5%", pad=0.05)
    cb=plt.colorbar(cbax1,cax=cax)
    cb.set_label('Speed (ms$^{-1}$)')
    
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes("right", size="7.5%", pad=0.05)
    cb=plt.colorbar(cbax2,cax=cax)
    cb.set_label('Speed (ms$^{-1}$)') 
       
    divider = make_axes_locatable(ax3)
    cax = divider.append_axes("right", size="7.5%", pad=0.05)
    cb=plt.colorbar(cbax3,cax=cax)
    cb.set_label('Speed (ms$^{-1}$)')
    
    ax1.set_title('Model')
    ax2.set_title('Observations')
    ax3.set_title('Difference')
    ax1.set_xlabel('Distance (m)')
    ax2.set_xlabel('Distance (m)')
    ax3.set_xlabel('Distance (m)')
    ax1.set_ylabel('Depth (m)')
    f.suptitle('Transect Number: {}    Name: {}    Line: {}'.format(key,trans[key]['Line_Num'],line))

    f.savefig(savepath+'model_transect_'+key+'_'+line+'.png',dpi=300)
    plt.close(f)
    
    
    
    

    line='LineB'
    f = plt.figure(figsize=(15,5))
    s=.075
    w=.24
    start=.055
    ax1 = f.add_axes([start,.1,w,.79])
    ax2 = f.add_axes([start+w+s,.1,w,.79])
    ax3 = f.add_axes([start+(w+s)*2,.1,w,.79])
    

    cbax1=ax1.pcolormesh(dist,depth,mspeedb,vmin=clim[0],vmax=clim[1])
    cbax2=ax2.pcolormesh(dist,depth,speedb,vmin=clim[0],vmax=clim[1])
    cbax3=ax3.pcolormesh(dist,depth,mspeedb-speedb,vmin=-lim,vmax=lim,cmap=mpl.cm.seismic)
    
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("right", size="7.5%", pad=0.05)
    cb=plt.colorbar(cbax1,cax=cax)
    cb.set_label('Speed (ms$^{-1}$)')
    
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes("right", size="7.5%", pad=0.05)
    cb=plt.colorbar(cbax2,cax=cax)
    cb.set_label('Speed (ms$^{-1}$)') 
       
    divider = make_axes_locatable(ax3)
    cax = divider.append_axes("right", size="7.5%", pad=0.05)
    cb=plt.colorbar(cbax3,cax=cax)
    cb.set_label('Speed (ms$^{-1}$)')
    
    ax1.set_title('Model')
    ax2.set_title('Observations')
    ax3.set_title('Difference')
    ax1.set_xlabel('Distance (m)')
    ax2.set_xlabel('Distance (m)')
    ax3.set_xlabel('Distance (m)')
    ax1.set_ylabel('Depth (m)')
    f.suptitle('Transect Number: {}    Name: {}    Line: {}'.format(key,trans[key]['Line_Num'],line))
 
    f.savefig(savepath+'model_transect_'+key+'_'+line+'.png',dpi=300)
    plt.close(f)
    
    
    
    
    

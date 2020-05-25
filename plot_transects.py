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

mtrans=np.load('data/misc/vhfr_obs/transects/VH_5x1m_corrected_model_vh_high.npy')
mtrans=mtrans[()]


savepath='figures/png/' + grid + '_'  + '/transects/'
if not os.path.exists(savepath): os.makedirs(savepath)



for key in trans.keys():
    print('')
    print(key)
    
    loc=trans[key]['Bin_Position']
    dist=np.array([np.sqrt(np.sum((loc[0,:]-tloc)**2)) for tloc in loc])
    plotdist=np.tile(dist,20).reshape(20,-1)
    
    
    speed=np.sqrt(mtrans[key]['LineA']['v']**2+mtrans[key]['LineA']['u']**2)  
    cspeed=speed[~np.isnan(speed)]
    clim=np.percentile(cspeed,[5,95])
    
    line='LineA'
    speeda=np.sqrt(mtrans[key][line]['v']**2+mtrans[key][line]['u']**2)
    ploth=sigh[:,None]*mtrans[key][line]['h'][None,:]    
    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])
    cbax=ax.pcolormesh(plotdist,ploth,speeda,vmin=clim[0],vmax=clim[1])
    cb=plt.colorbar(cbax)
    cb.set_label('Speed (ms$^{-1}$)')
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Depth (m)')
    ax.set_title('Transect Number: {}    Name: {}    Line: {}'.format(key,trans[key]['Line_Num'],line))
    f.savefig(savepath+'model_transect_'+key+'_'+line+'.png',dpi=300)
    plt.close(f)
    
    line='LineB'
    speedb=np.sqrt(mtrans[key][line]['v']**2+mtrans[key][line]['u']**2)
    ploth=sigh[:,None]*mtrans[key][line]['h'][None,:]    
    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])
    cbax=ax.pcolormesh(plotdist,ploth,speeda,vmin=clim[0],vmax=clim[1])
    cb=plt.colorbar(cbax)
    cb.set_label('Speed (ms$^{-1}$)')
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Depth (m)')
    ax.set_title('Transect Number: {}    Name: {}    Line: {}'.format(key,trans[key]['Line_Num'],line))
    f.savefig(savepath+'model_transect_'+key+'_'+line+'.png',dpi=300)
    plt.close(f)
    
    line='difference'
    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])
    cbax=ax.pcolormesh(plotdist,ploth,speeda-speedb,cmap=mpl.cm.seismic)
    cb=plt.colorbar(cbax)
    cb.set_label('Speed (ms$^{-1}$)')
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Depth (m)')
    ax.set_title('Transect Number: {}    Name: {}    Line: {}'.format(key,trans[key]['Line_Num'],line))
    f.savefig(savepath+'model_transect_'+key+'_'+line+'.png',dpi=300)
    plt.close(f)
    
    
    
    
    
    
    
    
    
    

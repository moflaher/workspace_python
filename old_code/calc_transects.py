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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from scipy.interpolate import interp1d
from matplotlib import patches as pp
from osgeo import osr, gdal
from matplotlib.colors import LinearSegmentedColormap
import collections

# Define names and types of data
name='vh_high_3d_profile'
grid='vh_high'
datatype='2d'

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')
mlay=20

trans=np.load('data/misc/vhfr_obs/transects/VH_5x1m_corrected.npy')
trans=trans[()]

savepath='figures/timeseries/' + grid + '_' + datatype + '/transects/'
if not os.path.exists(savepath): os.makedirs(savepath)


#dict to hold transect data
mtrans=collections.OrderedDict()

#short for model time
mtimes=data['time']

for key in trans.keys():
    print('*'*80)
    print(key,len(trans[key]['LineA']['time']))
    # dict to hold lines
    mtrans[key]={}
    for line in ['LineA','LineB']:
        print('-'*80)
        #dict to hold u v
        mtrans[key][line]={}     
        locs=(trans[key]['Bin_Position_ll'][:-1,:]+trans[key]['Bin_Position_ll'][1:,:])/2.0
        mtrans[key][line]['u']=np.empty((mlay,len(locs)))
        mtrans[key][line]['v']=np.empty((mlay,len(locs)))
        mtrans[key][line]['h']=np.empty((len(locs),))
        #transect times
        time=trans[key][line]['time']
        #get model times for all transect
        mt_idx=np.argwhere( (mtimes> time.min()) & (mtimes<time.max()) )
        print(len(mt_idx))
        print('')
        #pass it no model for transect
        if len(mt_idx)==0:
            continue
        #make sure all times are covered
        mt_idx=np.arange(mt_idx.min()-1,mt_idx.max()+2)
        
        cnt=0

        #get data for first time
        lidx=mt_idx[0]
        lu=np.empty((mlay,len(locs)))
        lv=np.empty((mlay,len(locs)))
        lh=np.empty((len(locs),))
        lz=np.empty((len(locs),))
        uu=np.empty((mlay,len(locs)))
        uv=np.empty((mlay,len(locs)))
        uh=np.empty((len(locs),))
        uz=np.empty((len(locs),))
        for layer in range(0,mlay):
            lu[layer,:]=ipt.interpEfield_locs(data,'u',locs,lidx,ll=True,layer=layer)    
            lv[layer,:]=ipt.interpEfield_locs(data,'v',locs,lidx,ll=True,layer=layer)  
        lh=ipt.interpNfield_locs(data,'h',locs,lidx,ll=True)
        lz=ipt.interpNfield_locs(data,'zeta',locs,lidx,ll=True)
        for i in range(len(mt_idx)-1): 
            for layer in range(0,mlay):            
                uu[layer,:]=ipt.interpEfield_locs(data,'u',locs,mt_idx[i+1],ll=True,layer=layer)    
                uv[layer,:]=ipt.interpEfield_locs(data,'v',locs,mt_idx[i+1],ll=True,layer=layer) 
            uh=ipt.interpNfield_locs(data,'h',locs,mt_idx[i+1],ll=True) 
            uz=ipt.interpNfield_locs(data,'zeta',locs,mt_idx[i+1],ll=True)
            t_idx=np.argwhere( (time>=mtimes[mt_idx[i]]) & (time<mtimes[mt_idx[i+1]]) )    
            print(i,len(t_idx))
            for idx in t_idx:
                su = ipt.interp1d(mtimes[[mt_idx[i],mt_idx[i+1]]], np.squeeze(np.array([lu[:,idx],uu[:,idx]])).T, time[idx])
                sv = ipt.interp1d(mtimes[[mt_idx[i],mt_idx[i+1]]], np.squeeze(np.array([lv[:,idx],uv[:,idx]])).T, time[idx])
                sh = ipt.interp1d(mtimes[[mt_idx[i],mt_idx[i+1]]], np.squeeze(np.array([lh[idx],uh[idx]])), time[idx])
                sz = ipt.interp1d(mtimes[[mt_idx[i],mt_idx[i+1]]], np.squeeze(np.array([lz[idx],uz[idx]])), time[idx])
                mtrans[key][line]['u'][:,cnt]=su.flatten()  
                mtrans[key][line]['v'][:,cnt]=sv.flatten()
                mtrans[key][line]['h'][cnt]=sh.flatten()+sz.flatten()               
                cnt+=1 
        
            lu=uu
            lv=uv
            lh=uh
            lz=uz
               

np.save('data/misc/vhfr_obs/transects/VH_5x1m_corrected_model_vh_high.npy',mtrans)

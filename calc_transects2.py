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
sigh=data['siglay'][:,0]

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
        locsm=(trans[key]['Bin_Position_ll'][:-1,:]+trans[key]['Bin_Position_ll'][1:,:])/2.0
        locs=trans[key]['Bin_Position_ll']
        depth=trans[key]['Depth']
        mtrans[key][line]['u']=np.empty((len(depth),len(locsm)))*np.nan
        mtrans[key][line]['v']=np.empty((len(depth),len(locsm)))*np.nan
        mtrans[key][line]['h']=np.empty((len(locs),))
        mtrans[key][line]['hc']=np.empty((len(locsm),))
        #transect times have to adjust to utc from pst
        time=trans[key][line]['time']#+(8/24.0)
        timeh=trans[key][line]['timeh']#+(8/24.0)
        #get model times for all transect
        mt_idx=np.argwhere( (mtimes> timeh.min()) & (mtimes<timeh.max()) )
        print(len(mt_idx))
        print('')
        #pass if no model for transect
        if len(mt_idx)==0:
            continue
        #make sure all times are covered
        mt_idx=np.arange(mt_idx.min()-1,mt_idx.max()+2)
        
        cnt=0


        lidx=mt_idx[0]
        lh=np.empty((len(locs),))
        lz=np.empty((len(locs),))
        uh=np.empty((len(locs),))
        uz=np.empty((len(locs),))        
        
        lh=ipt.interpNfield_locs(data,'h',locs,lidx,ll=True)
        lz=ipt.interpNfield_locs(data,'zeta',locs,lidx,ll=True)

        for i in range(len(mt_idx)-1): 
            uh=ipt.interpNfield_locs(data,'h',locs,mt_idx[i+1],ll=True) 
            uz=ipt.interpNfield_locs(data,'zeta',locs,mt_idx[i+1],ll=True)
            t_idx=np.argwhere( (timeh>=mtimes[mt_idx[i]]) & (timeh<mtimes[mt_idx[i+1]]) )    
            print(i,len(t_idx))
            for idx in t_idx:
                sh = ipt.interp1d(mtimes[[mt_idx[i],mt_idx[i+1]]], np.squeeze(np.array([lh[idx],uh[idx]])), timeh[idx])
                sz = ipt.interp1d(mtimes[[mt_idx[i],mt_idx[i+1]]], np.squeeze(np.array([lz[idx],uz[idx]])), timeh[idx])
                mtrans[key][line]['h'][cnt]=sh.flatten()+sz.flatten()               
                cnt+=1 

            lh=uh
            lz=uz
            
        mtrans[key][line]['hc']=(mtrans[key][line]['h'][:-1]+mtrans[key][line]['h'][1:])/2.0
        hsig=-1*sigh[:,None]*mtrans[key][line]['hc'][None,:] 
        
     
        #get model times for all transect
        mt_idx=np.argwhere( (mtimes> time.min()) & (mtimes<time.max()) )
        print(len(mt_idx))
        print('')
        #pass if no model for transect
        if len(mt_idx)==0:
            continue
        #make sure all times are covered
        mt_idx=np.arange(mt_idx.min()-1,mt_idx.max()+2)
        
        cnt=0     
        
        lu=np.empty((mlay,len(locs)))
        lv=np.empty((mlay,len(locs)))
        uu=np.empty((mlay,len(locs)))
        uv=np.empty((mlay,len(locs)))

        for layer in range(0,mlay):
            lu[layer,:]=ipt.interpEfield_locs(data,'u',locs,lidx,ll=True,layer=layer)    
            lv[layer,:]=ipt.interpEfield_locs(data,'v',locs,lidx,ll=True,layer=layer) 

        for i in range(len(mt_idx)-1): 
            for layer in range(0,mlay):            
                uu[layer,:]=ipt.interpEfield_locs(data,'u',locs,mt_idx[i+1],ll=True,layer=layer)    
                uv[layer,:]=ipt.interpEfield_locs(data,'v',locs,mt_idx[i+1],ll=True,layer=layer) 
            t_idx=np.argwhere( (time>=mtimes[mt_idx[i]]) & (time<mtimes[mt_idx[i+1]]) )    
            print(i,len(t_idx))
            for idx in t_idx:
                su = ipt.interp1d(mtimes[[mt_idx[i],mt_idx[i+1]]], np.squeeze(np.array([lu[:,idx],uu[:,idx]])).T, time[idx])
                sv = ipt.interp1d(mtimes[[mt_idx[i],mt_idx[i+1]]], np.squeeze(np.array([lv[:,idx],uv[:,idx]])).T, time[idx])

                deep=depth<(hsig[:,idx].max())
                ld=np.argwhere(deep==True)
                su = ipt.interp1d(hsig[:,idx].flatten(), su.flatten(), depth[deep])
                sv = ipt.interp1d(hsig[:,idx].flatten(), sv.flatten(), depth[deep])
                
                
                mtrans[key][line]['u'][ld,cnt]=su.reshape(-1,1)
                mtrans[key][line]['v'][ld,cnt]=sv.reshape(-1,1)
               
                cnt+=1 
        
            lu=uu
            lv=uv
            lh=uh
            lz=uz
            
               

np.save('data/misc/vhfr_obs/transects/VH_5x1m_corrected_model_vh_high_2.npy',mtrans)

from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
sys.path.append('/home/moe46/Desktop/school/workspace_python/ttide_py/ttide/')
sys.path.append('/home/moflaher/Desktop/workspace_python/ttide_py/ttide/')
from t_tide import t_tide
from t_predic import t_predic

# Define names and types of data
name='sfm6_musq2_half_cages'
grid='sfm6_musq2'

starttime=0


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')



ttidein=np.load('data/ttide/'+grid+'_'+name+'_'+'_uv_surface_currents_all.npy')
ttidein=ttidein[()]

tidecon=ttidein['tidecon']
nameu=ttidein['nameu']
freq=ttidein['freq']


resu=np.empty((tidecon.shape[0],len(data['time'][starttime:])))
resv=np.empty((tidecon.shape[0],len(data['time'][starttime:])))

for j in range(0,tidecon.shape[0]):
    print( ("%d"%j)+"              "+("%f"%(j/tidecon.shape[0]*100)) )
    tpre=t_predic(data['time'][starttime:],nameu,freq,tidecon[j,:,:])
    resu[j,:]=data['u'][starttime:,19,j]-np.real(tpre).flatten()
    resv[j,:]=data['v'][starttime:,19,j]-np.imag(tpre).flatten()


resmean={}
resmean['resumean']=resu.mean(axis=1)
resmean['resvmean']=resv.mean(axis=1)


np.save('data/ttide/'+grid+'_'+name+'_'+'_uv_surface_currents_all_mean.npy',resmean)









from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
sys.path.append('/home/moflaher/Desktop/workspace_python/ttide_py/ttide/')
sys.path.append('/home/moe46/Desktop/school/workspace_python/ttide_py/ttide/')
from t_tide import t_tide



# Define names and types of data
name='2012-02-01_2012-03-01_0.01_0.001'
grid='vh_high'
datatype='2d'
starttime=0
endtime=2785



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

dt=np.diff(data['time'])[0]*24

tidecon_uv=np.empty([len(data['uvnodell'][:,0]),29,8])
for i in range(0,len(data['uvnodell'][:,0])):
    print(i)
    [nameu, freq, tidecon_uv[i,], xout]=t_tide(data['ua'][starttime:endtime,i]+1j*data['va'][starttime:endtime,i],stime=data['time'][starttime],lat=data['uvnodell'][i,1],output=False,synth=-1,dt=dt)

tidesave={}
tidesave['nameu']=nameu
tidesave['freq']=freq
tidesave['tidecon']=tidecon_uv
np.save('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv_all.npy',tidesave)


tidecon_el=np.empty([len(data['nodell'][:,0]),29,4])
for j in range(0,len(data['nodell'][:,0])):
    print(j)
    [nameu, freq, tidecon_el[j,], xout]=t_tide(data['zeta'][starttime:endtime,j],stime=data['time'][starttime],lat=data['nodell'][j,1],synth=-1,output=False,dt=dt)

tidesave={}
tidesave['nameu']=nameu
tidesave['freq']=freq
tidesave['tidecon']=tidecon_el
np.save('data/ttide/'+grid+'_'+name+'_'+datatype+'_el_all.npy',tidesave)







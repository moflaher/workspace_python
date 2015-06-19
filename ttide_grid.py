from __future__ import division
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
name='sfm6_musq2_all_cages'
grid='sfm6_musq2'
datatype='2d'
starttime=0
endtime=721



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

data['time']=data['time']+55055


tidecon_el=np.empty([len(data['nodell'][:,0]),29,4])
for j in range(0,len(data['nodell'][:,0])):
    print j
    [nameu, freq, tidecon_el[j,], xout]=t_tide(data['zeta'][starttime:endtime,j],stime=data['time'][starttime],lat=data['nodell'][j,1],synth=-1,output=False)

tidesave={}
tidesave['nameu']=nameu
tidesave['freq']=freq
tidesave['tidecon']=tidecon_el
np.save('data/ttide/'+grid+'_'+name+'_'+datatype+'_el_all.npy',tidesave)


#tidecon_uv=np.empty([len(data['uvnodell'][:,0]),29,8])
#for i in range(0,len(data['uvnodell'][:,0])):
    #print i
    #[nameu, freq, tidecon_uv[i,], xout]=t_tide(data['u'][starttime:endtime,0,i]+1j*data['v'][starttime:endtime,0,i],stime=data['time'][starttime],lat=data['uvnodell'][i,1],output=False,synth=-1)

#tidesave={}
#tidesave['nameu']=nameu
#tidesave['freq']=freq
#tidesave['tidecon']=tidecon_uv
#np.save('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv_layer_0_all.npy',tidesave)


#tidecon_uv=np.empty([len(data['uvnodell'][:,0]),29,8])
#for i in range(0,len(data['uvnodell'][:,0])):
    #print i
    #[nameu, freq, tidecon_uv[i,], xout]=t_tide(data['u'][starttime:endtime,19,i]+1j*data['v'][starttime:endtime,19,i],stime=data['time'][starttime],lat=data['uvnodell'][i,1],output=False,synth=-1)

#tidesave={}
#tidesave['nameu']=nameu
#tidesave['freq']=freq
#tidesave['tidecon']=tidecon_uv
#np.save('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv_layer_19_all.npy',tidesave)






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
from ttide.t_tide import t_tide



# Define names and types of data
name='sfm6_musq2_all_cages'
grid='sfm6_musq2'
datatype='2d'
starttime=0
endtime=721



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

data['time']=data['time']-678576+733631.0

dt=np.diff(data['time'])[0]*24

test=np.load('data/interp_currents/sfm6_musq2_sfm6_musq2_all_cages_1m.npy')
test=test[()]


tidecon_uv=np.empty([len(data['uvnodell'][:,0]),29,8])
for i in range(0,len(data['uvnodell'][:,0])):
    print(i)
    [nameu, freq, tidecon_uv[i,], xout]=t_tide(test['u'][starttime:endtime,i]+1j*test['v'][starttime:endtime,i],stime=data['time'][starttime],lat=data['uvnodell'][i,1],output=False,synth=-1,dt=dt)

tidesave={}
tidesave['nameu']=nameu
tidesave['freq']=freq
tidesave['tidecon']=tidecon_uv
np.save('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv_1m_currents_all.npy',tidesave)



#tidecon_uv=np.empty([len(data['uvnodell'][:,0]),29,8])
#for i in range(0,len(data['uvnodell'][:,0])):
    #print(i)
    #[nameu, freq, tidecon_uv[i,], xout]=t_tide(data['u'][starttime:endtime,-1,i]+1j*data['v'][starttime:endtime,-1,i],stime=data['time'][starttime],lat=data['uvnodell'][i,1],output=False,synth=-1,dt=dt)

#tidesave={}
#tidesave['nameu']=nameu
#tidesave['freq']=freq
#tidesave['tidecon']=tidecon_uv
#np.save('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv_bottom_currents_all.npy',tidesave)


#tidecon_uv=np.empty([len(data['uvnodell'][:,0]),29,8])
#for i in range(0,len(data['uvnodell'][:,0])):
    #print(i)
    #[nameu, freq, tidecon_uv[i,], xout]=t_tide(data['ua'][starttime:endtime,i]+1j*data['va'][starttime:endtime,i],stime=data['time'][starttime],lat=data['uvnodell'][i,1],output=False,synth=-1,dt=dt)

#tidesave={}
#tidesave['nameu']=nameu
#tidesave['freq']=freq
#tidesave['tidecon']=tidecon_uv
#np.save('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv_all.npy',tidesave)


#tidecon_el=np.empty([len(data['nodell'][:,0]),29,4])
#for j in range(0,len(data['nodell'][:,0])):
    #print(j)
    #[nameu, freq, tidecon_el[j,], xout]=t_tide(data['zeta'][starttime:endtime,j],stime=data['time'][starttime],lat=data['nodell'][j,1],synth=-1,output=False,dt=dt)

#tidesave={}
#tidesave['nameu']=nameu
#tidesave['freq']=freq
#tidesave['tidecon']=tidecon_el
#np.save('data/ttide/'+grid+'_'+name+'_'+datatype+'_el_all.npy',tidesave)







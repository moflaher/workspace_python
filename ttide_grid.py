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
name='kit4_kelp_20m_0.018'
grid='kit4'
datatype='2d'
starttime=384
endtime=1081



### load the .nc file #####
#data = loadnc('/media/moflaher/My Book/cages/' + name + '/output/',singlename=grid + '_0001.nc')
data = loadnc('/media/moe46/Hardy/spet_18_work/kit4_kelp_20m_0.018/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

data['time']=data['time']





#tidecon_el=np.empty([len(data['nodell'][:,0]),5,4])
#for j in range(0,len(data['nodell'][:,0])):
#    print j
#    [nameu, freq, tidecon_el[j,], xout]=t_tide(data['zeta'][starttime:endtime,j],stime=data['time'][starttime],lat=data['nodell'][j,1],output=False,constitnames=np.array([['M2  '],['N2  '],['S2  '],['K1  '],['O1  ']]))

#tidesave={}
#tidesave['nameu']=nameu
#tidesave['freq']=freq
#tidesave['tidecon']=tidecon_el
#np.save('data/ttide/'+grid+'_'+name+'_'+datatype+'_el.npy',tidesave)


tidecon_uv=np.empty([len(data['uvnodell'][:,0]),5,8])
for i in range(0,len(data['uvnodell'][:,0])):
    print i
    [nameu, freq, tidecon_uv[i,], xout]=t_tide(data['ua'][starttime:endtime,i]+1j*data['va'][starttime:endtime,i],stime=data['time'][starttime],lat=data['uvnodell'][i,1],output=False,constitnames=np.array([['M2  '],['N2  '],['S2  '],['K1  '],['O1  ']]))

tidesave={}
tidesave['nameu']=nameu
tidesave['freq']=freq
tidesave['tidecon']=tidecon_uv
np.save('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv.npy',tidesave)






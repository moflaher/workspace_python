from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from projtools import *
from folderpath import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from ttide import t_tide



# Define names and types of data
name='sjh_hr_v2_newwind'
grid='sjh_hr_v2'
datatype='2d'
starttime=960
endtime=3744



### load the .nc file #####
data = loadnc('/home/mif001/scratch/susan/sjh_hr_v2/runs/sjh_hr_v2_newwind/output/',singlename=grid + '_0001.nc')
data['lon']=data['lon']-360
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
print('done load')
del data['trigrid']
data = ncdatasort(data)
print('done sort')


savepath='{}/{}_{}/ttide/{}/'.format(datapath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)

dt=np.diff(data['time'])[0]*24


tidecon_el=np.empty([len(data['nodell'][:,0]),29,4])
for j in range(0,len(data['nodell'][:,0])):
    print(j)
    out=t_tide(data['zeta'][starttime:endtime,j],stime=data['time'][starttime],lat=data['nodell'][j,1],synth=-1,out_style=None,dt=.25)
    tidecon_el[j,]=out['tidecon']

tidesave={}
tidesave['nameu']=out['nameu']
tidesave['freq']=out['freq']
tidesave['tidecon']=tidecon_el
np.save('{}ttide_grid_el_all.npy'.format(savepath))







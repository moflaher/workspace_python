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
name='sjh_hr_v3_0.03_newnest'
grid='sjh_hr_v3'

starttime=672
endtime=3744



### load the .nc file #####
data = loadnc('/home/mif001/scratch/sjh_hr_v3/test_bfric2/{}/output/'.format(name),singlename=grid + '_0001.nc')
print('done load')


savepath='{}/{}_{}/ttide/{}/'.format(datapath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)

dt=np.diff(data['time'])[0]*24


out=np.empty((len(data['nodell'][:,0]),),dtype=object)
for j in range(0,len(data['nodell'][:,0])):
    print(j)
    out[j]=t_tide(data['zeta'][starttime:endtime,j],stime=data['time'][starttime],lat=data['lat'][j],synth=-1,out_style=None,dt=.25)

np.save('{}{}_{}_{}_ttide_grid_el_all.npy'.format(savepath,name,starttime,endtime),out)







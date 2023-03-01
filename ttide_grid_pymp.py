from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from projtools import *
from folderpath import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
from ttide import t_tide
import pymp

#This was for python 2.7 and an older version of ttide, it may barf.

# Define names and types of data
name='sjh_hr_v3_0.03_newnest'
grid='sjh_hr_v3'

starttime=672
endtime=3744



### load the .nc file #####
data = loadnc('/home/mif001/scratch/sjh_hr_v3/test_bfric2/{}/output/'.format(name),singlename=grid + '_0001.nc')
print('done load')

#where to save the output
savepath='{}/{}_{}/ttide/{}/'.format(datapath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)

#get dt which it looks like I don't use
dt=np.diff(data['time'])[0]*24


# special array to hold the results from using parallel
out=pymp.shared.array((len(data['nodell'][:,0]),35,4))

#run in parallel with 48 cores/threads
with pymp.Parallel(48) as p:
    for j in p.range(len(data['nodell'][:,0])):
        print(j)
        #out_style=None gets rid of the output
        #I have dt set to .25 here so 15 minute output, you will need to adjust it
        out[j,]=t_tide(data['zeta'][starttime:endtime,j],stime=data['time'][starttime],lat=data['lat'][j],synth=-1,out_style=None,dt=.25)['tidecon']

#I have it doing a single output here not sure why... maybe it was to get the shape of the array?
outall=t_tide(data['zeta'][starttime:endtime,j],stime=data['time'][starttime],lat=data['lat'][j],synth=-1,out_style=None,dt=.25)

#save the output
np.save('{}{}_{}_{}_ttide_grid_tidecon_el_all_pymp.npy'.format(savepath,name,starttime,endtime),out)
np.save('{}{}_{}_{}_ttide_grid_singleout_el_all_pymp.npy'.format(savepath,name,starttime,endtime),outall)







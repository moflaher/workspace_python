from __future__ import division,print_function
import matplotlib as mpl
mpl.use('Agg')
import scipy as sp
from datatools import *
from gridtools import *
from projtools import *
from folderpath import *
from plottools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name='sjh_hr_v2_newwind'
grid='sjh_hr_v2'
datatype='2d'
regionname='bof_nemo'
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


region=regions(regionname)
nidx=get_nodes(data,region)




savepath='{}png/{}_{}/ttide/zeta/{}/'.format(figpath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)


el=np.load('{}{}_{}/ttide/{}/ttide_grid_el_all.npy'.format(datapath,grid,datatype,name))
el=el[()]


def plot_field(con):
    print(con)

    conidx=np.argwhere(el['nameu']==con)[0][0]
    print(conidx)

    f,ax,cax = setplot(region)
    clim = np.percentile(el['tidecon'][nidx,conidx,0],[5,99])
    triax=ax.tripcolor(data['trigrid'],el['tidecon'][:,conidx,0],vmin=clim[0],vmax=clim[1])
    cb=plt.colorbar(triax,cax=cax)
    cb.set_label(r'Amp.',fontsize=10)
    f.savefig('{}{}_{}_amp_{}.png'.format(savepath,grid,region['regionname'],con.replace(' ','') ),dpi=600)
    plt.close(f)

    f,ax,cax = setplot(region)
    triax=ax.tripcolor(data['trigrid'],el['tidecon'][:,conidx,2],vmin=0,vmax=360,cmap=mpl.cm.hsv,shading='gouraud')
    cb=plt.colorbar(triax,cax=cax)
    cb.set_label(r'Phase.',fontsize=10)
    f.savefig('{}{}_{}_Phase_{}.png'.format(savepath,grid,region['regionname'],con.replace(' ','') ),dpi=600)
    plt.close(f)


cons=['M2  ','N2  ','S2  ','K1  ','O1  ']
for con in cons:
    plot_field(con)












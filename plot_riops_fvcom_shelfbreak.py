from __future__ import division,print_function
import matplotlib as mpl
mpl.use('Agg')
import scipy as sp
from folderpath import *
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import multiprocessing
import pymp
import seawater as sw




# Define names and types of data
name='sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1_jcool0_15mins'
grid='sjh_lr_v1'
datatype='2d'
starttime=0
endtime=-1



### load the .nc file #####
data = loadnc('/mnt/drive_1/runs/sjh_lr_v1/{}/output/'.format(name),singlename=grid + '_0001.nc')
print('done load')
fname='oce_daily_2016100100.nc'
rdata = loadnc('/mnt/drive_0/misc/misc/',fname,False)

ssavepath='{}png/{}_{}/shelfbreak/{}_salinity_{}/'.format(figpath,grid,datatype,name,fname[10:20])
if not os.path.exists(ssavepath): os.makedirs(ssavepath)
tsavepath='{}png/{}_{}/shelfbreak/{}_temp_{}/'.format(figpath,grid,datatype,name,fname[10:20])
if not os.path.exists(tsavepath): os.makedirs(tsavepath)

lon=np.ravel(rdata['nav_lon'])-360
lat=np.ravel(rdata['nav_lat'])
sal=np.reshape(rdata['vosaline'],(50,-1))
temp=np.reshape(rdata['votemper'],(50,-1))
h=np.ravel(rdata['depth'])

locs=np.array([[-67.91409917,  39.01440626],
       [-59.20714752,  42.62463315],
       [-63.57974549,  40.8734932 ],
       [-61.36157626,  41.74906317],
       [-65.87440332,  39.86598802],
       [-60.50745362,  44.39976132],
       [-68.97219139,  41.06539895],
       [-64.65058581,  43.11639163],
       [-62.26669129,  43.90800284],
       [-67.22570182,  42.08489823]])




for loc in locs:
    ridx=np.argmin(np.fabs((lon-loc[0])**2+(lat-loc[1])**2))
    rpro=sal[:,ridx]
    rrpro=np.ma.masked_array(rpro,rpro>1000)
    hm=np.ma.masked_array(h,rpro>1000)
    fidx=np.argmin(np.fabs((data['lon']-loc[0])**2+(data['lat']-loc[1])**2))
    fpro=data['salinity'][576:673,:,fidx]
    #print(hm)
    
    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])
    ax.plot(fpro.T,-1*data['h'][fidx]*data['siglay'][:,0],'b')
    ax.plot(rrpro,hm,'g')
    f.savefig('{}{}_{}_shelfbreak_salinity_{}_{}.png'.format(ssavepath,grid,name,loc[0],loc[1]),dpi=300)
    plt.close(f)



    ridx=np.argmin(np.fabs((lon-loc[0])**2+(lat-loc[1])**2))
    rpro=temp[:,ridx]
    rrpro=np.ma.masked_array(rpro,rpro>1000)
    hm=np.ma.masked_array(h,rpro>1000)
    fidx=np.argmin(np.fabs((data['lon']-loc[0])**2+(data['lat']-loc[1])**2))
    fpro=data['temp'][576:673,:,fidx]
    #print(hm)
    
    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])
    ax.plot(fpro.T,-1*data['h'][fidx]*data['siglay'][:,0],'b')
    ax.plot(rrpro,hm,'g')
    f.savefig('{}{}_{}_shelfbreak_temp_{}_{}.png'.format(tsavepath,grid,name,loc[0],loc[1]),dpi=300)
    plt.close(f)



















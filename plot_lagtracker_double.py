from __future__ import division,print_function
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import scipy.io as sio
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
from StringIO import StringIO
from gridtools import *
from datatools import *
from misctools import *
from plottools import *
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from mpl_toolkits.mplot3d.axes3d import Axes3D





# Define names and types of data
name='kit4_45days_3'
grid='kit4'
regionname='mostchannels'
datatype='2d'
lfolder1='kit4_kelp_0.025'
lfolder2='kit4_kelp_0.05'
lname1='kit4_kelp_0.025_0'
lname2='kit4_kelp_0.05_0'
spacing=10



### load the .nc file #####
data = loadnc('/media/moflaher/My Book/kit4_runs/' + name +'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

savepath='figures/png/' + grid + '_' + datatype + '/lagtracker/' + lfolder1 + '_' +lfolder2+'_doubles/'
if not os.path.exists(savepath): os.makedirs(savepath)

trigridxy = mplt.Triangulation(data['x'], data['y'],data['nv'])
region=regions(regionname)


savelag1=(sio.loadmat('/home/moflaher/workspace_matlab/lagtracker/savedir/'+lfolder1+'/'+lname1+'.mat',squeeze_me=True,struct_as_record=False))['savelag']
savelag2=(sio.loadmat('/home/moflaher/workspace_matlab/lagtracker/savedir/'+lfolder2+'/'+lname2+'.mat',squeeze_me=True,struct_as_record=False))['savelag']


#plt.triplot(trigridxy,lw=.3)
whichtri=3151
whichtri=-39
whichtri=2936
whichtri=5

for whichtri in range(0,len(savelag1.x),spacing):
    region={}
    region['region']=[np.nanmin([savelag1.x[whichtri,:],savelag2.x[whichtri,:]]), np.nanmax([savelag1.x[whichtri,:],savelag2.x[whichtri,:]]), np.nanmin([savelag1.y[whichtri,:],savelag2.y[whichtri,:]]), np.nanmax([savelag1.y[whichtri,:],savelag2.y[whichtri,:]])]


 



    #f, ax = plt.subplots(nrows=1,ncols=2)

    f=plt.figure()    
    ax0a = plt.subplot2grid((2,3),(0, 0))
    ax0b = plt.subplot2grid((2,3),(1, 0))
    ax1 = plt.subplot2grid((2,3),(0, 1),colspan=2,rowspan=2)


    ax0a.plot(savelag1.time,savelag1.z[whichtri,:],'k')
    ax0a.plot(savelag1.time,-savelag1.h[whichtri,:],'b')
    ax0a.set_xticklabels((ax0a.get_xticks())/100000,rotation=90)
    ax0a.set_title(lname1)
    ax0b.plot(savelag2.time,savelag2.z[whichtri,:],'r')
    ax0b.plot(savelag2.time,-savelag2.h[whichtri,:],'b')
    ax0b.set_xticklabels((ax0b.get_xticks())/100000,rotation=90)
    ax0b.set_title(lname2)


    nidx=get_nodes_xy(data,region)

    ax1tri=ax1.tripcolor(trigridxy,data['h'],vmin=data['h'][nidx].min(),vmax=data['h'][nidx].max(),cmap=plt.cm.winter)
    plt.colorbar(ax1tri,ax=ax1)
    ax1.plot(savelag1.x[whichtri,:],savelag1.y[whichtri,:],'k',label=lname1)
    ax1.plot(savelag1.x[whichtri,0],savelag1.y[whichtri,0],'w*',markersize=12)
    last=np.max(np.flatnonzero(~np.isnan(savelag1.x[whichtri,:])))
    tdiff=savelag1.time[2]-savelag1.time[1]
    newx=savelag1.x[whichtri,last]+savelag1.u[whichtri,last]*tdiff
    newy=savelag1.y[whichtri,last]+savelag1.v[whichtri,last]*tdiff
    ax1.plot(newx,newy,'k*',markersize=16)

    ax1.plot(savelag2.x[whichtri,:],savelag2.y[whichtri,:],'r',label=lname2)
    ax1.plot(savelag2.x[whichtri,0],savelag2.y[whichtri,0],'w*',markersize=12)
    last=np.max(np.flatnonzero(~np.isnan(savelag2.x[whichtri,:])))
    tdiff=savelag2.time[2]-savelag2.time[1]
    newx=savelag2.x[whichtri,last]+savelag2.u[whichtri,last]*tdiff
    newy=savelag2.y[whichtri,last]+savelag2.v[whichtri,last]*tdiff
    ax1.plot(newx,newy,'r*',markersize=16)

   
    
    ax1.axis(region['region'])
    ax1.set_xticklabels((ax1.get_xticks())/1000,rotation=90)
    ax1.set_yticklabels((ax1.get_yticks())/1000)
    ax1.legend(loc=0)


    #f.show()

    f.tight_layout(pad=0.4)
    f.savefig(savepath + grid + '_' +name+ '_'+lname1+'_'+lname2+'_particle_path_'+("%05d"%whichtri)+'.png',dpi=300)
    plt.close(f)



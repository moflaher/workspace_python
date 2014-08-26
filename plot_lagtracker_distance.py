from __future__ import division
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



# Define names and types of data
name='sfm6_musq2_all_cages'
grid='sfm6_musq2'
regionname='musq_cage'
datatype='2d'
lfolder='25_part_all_cage_in60min_time1min_out10min'
lname='all_cages_25_part_sfm6_musq2_6'


### load the .nc file #####
data = loadnc('/media/moflaher/My Book/cages/' + name +'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

savepath='figures/png/' + grid + '_' + datatype + '/lagtracker/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)

trigridxy = mplt.Triangulation(data['x'], data['y'],data['nv'])
region=regions(regionname)


savelag=(sio.loadmat('/home/moflaher/workspace_matlab/lagtracker/savedir/'+lfolder+'/'+lname+'.mat',squeeze_me=True,struct_as_record=False))['savelag']




distance=np.empty([savelag.x.shape[0]])
for i in range(0,savelag.x.shape[0]):
    distance[i]=np.nansum(np.sqrt(np.diff(savelag.x[i,:])**2+np.diff(savelag.y[i,:])**2))

host=trigridxy.get_trifinder().__call__(savelag.x[:,0],savelag.y[:,0])
pltarray=np.zeros([data['nv'].shape[0],])
hostcnt=np.zeros([data['nv'].shape[0],])
for i in range(0,len(host)):
    if ~np.isnan(distance[i]):
        hostcnt[host[i]]+=1
        pltarray[host[i]]=distance[i]+pltarray[host[i]]

final=np.zeros([data['nv'].shape[0],])
for i in np.unique(host):
    if hostcnt[i]!=0:
        final[i]=(pltarray[i]/1000)/hostcnt[i]


plt.close()
plt.tripcolor(data['trigrid'],final)
prettyplot_ll(plt.gca(),setregion=region,grid=True,cblabel=r'Path Travel Distance (km)')
plt.savefig(savepath +lname+'_path_distance.png',dpi=600)




maxdistance=np.zeros([savelag.x.shape[0],1])
for j in range(0,savelag.x.shape[1]):        
    maxdistance=np.nanmax(np.hstack([maxdistance.reshape(-1,1),np.sqrt((savelag.x[:,0]-savelag.x[:,j])**2+(savelag.y[:,0]-savelag.y[:,j])**2).reshape(-1,1)   ]),axis=1)
        
pltarray=np.zeros([data['nv'].shape[0],])
hostcnt=np.zeros([data['nv'].shape[0],])
for i in range(0,len(host)):
    if ~np.isnan(maxdistance[i]):
        hostcnt[host[i]]+=1
        pltarray[host[i]]=maxdistance[i]+pltarray[host[i]]

final=np.zeros([data['nv'].shape[0],])
for i in np.unique(host):
    if hostcnt[i]!=0:
        final[i]=(pltarray[i]/1000)/hostcnt[i]


plt.close()
plt.tripcolor(data['trigrid'],final)
prettyplot_ll(plt.gca(),setregion=region,grid=True,cblabel=r'Max Distance (km)')
plt.savefig(savepath +lname+'_max_distance.png',dpi=600)




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
import h5py as h5
from matplotlib.collections import PolyCollection as PC



# Define names and types of data
name='kit4_45days_3'
name2='kit4_kelp_20m_0.018'
grid='kit4'
regionname='kit4_kelp_tight2'
datatype='2d'
lname='kelpstart_in_kit4_kelp_tight2'


### load the .nc file #####
data = loadnc('runs/'+grid+'/' + name +'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

savepath='figures/png/' + grid + '_' + datatype + '/lagtracker/particles_inkelp/' + name + '_'+name2+'/'
if not os.path.exists(savepath): os.makedirs(savepath)

data['trigridxy'] = mplt.Triangulation(data['x'], data['y'],data['nv'])
region=regions(regionname)
region=regionll2xy(data,region)


if 'savelag1' not in globals():
    print "Loading savelag1"
    fileload=h5.File('/home/moflaher/workspace_matlab/lagtracker/savedir/'+name+'/kit4_kelp_tight2_kelpstart_15mdeep_s0.mat')
    savelag1={}
    for i in fileload['savelag'].keys():
            savelag1[i]=fileload['savelag'][i].value.T
    savelag1['u']=0
    savelag1['v']=0
    savelag1['w']=0

if 'savelag2' not in globals():
    print "Loading savelag2"
    fileload=h5.File('/home/moflaher/workspace_matlab/lagtracker/savedir/'+name2+'/kit4_kelp_tight2_kelpstart_15mdeep_s0.mat')
    savelag2={}
    for i in fileload['savelag'].keys():
            savelag2[i]=fileload['savelag'][i].value.T
    savelag2['u']=0
    savelag2['v']=0
    savelag2['w']=0


cages=np.genfromtxt('runs/'+grid+'/' +name2+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)


tmparray=[list(zip(data['nodexy'][data['nv'][i,[0,1,2]],0],data['nodexy'][data['nv'][i,[0,1,2]],1])) for i in cages ]
sidx=np.where((savelag1['x'][:,0]>region['regionxy'][0])&(savelag1['x'][:,0]<region['regionxy'][1])&(savelag1['y'][:,0]>region['regionxy'][2])&(savelag1['y'][:,0]<region['regionxy'][3]))[0]


host=data['trigridxy'].get_trifinder().__call__(savelag1['x'][sidx,0],savelag1['y'][sidx,0])

cidx=np.in1d(host,cages)

expand=15000
region['regionxy']=[region['regionxy'][0]-expand,region['regionxy'][1]+expand,region['regionxy'][2]-expand,region['regionxy'][3]+expand]

#computed values for each timestep, changed to check all places and reshape much faster
#numberin1=np.empty((len(savelag1['time']),1))
#numberin2=np.empty((len(savelag1['time']),1))
#for i in range(0,len(savelag1['time'])):
#    print ("%d"%i)+"              "+("%f"%(i/len(savelag1['time'])*100)) 
#    numberin1[i]=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag1['x'][sidx,i],savelag1['y'][sidx,i]),cages))
#    numberin2[i]=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag2['x'][sidx,i],savelag2['y'][sidx,i]),cages))



#find particles in kelp from region start
numberin1=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag1['x'][sidx,:],savelag1['y'][sidx,:]),cages).reshape(savelag1['x'][sidx,:].shape),axis=0)
numberin2=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag2['x'][sidx,:],savelag2['y'][sidx,:]),cages).reshape(savelag2['x'][sidx,:].shape),axis=0)

f = plt.figure()
ax=f.add_axes([.125,.1,.8,.8])

ax.plot((savelag1['time']-savelag1['time'].min())/3600,numberin1,'k',label='No drag')
ax.plot((savelag2['time']-savelag2['time'].min())/3600,numberin2,'r',label='Drag')
ax.set_xlim([-10,ax.get_xlim()[1]])

handles, labels = ax.get_legend_handles_labels()
legend=ax.legend(handles, labels)

ax.set_ylabel(r'Number of particles in kelp',fontsize=8)
ax.set_xlabel(r'Time (hour)',fontsize=8)

for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontsize(8)

f.savefig(savepath +''+name+'_'+name2+'_'+regionname+'_'+lname+'_compare_particles_inkelp_regionstart.png',dpi=150)
plt.close(f)



#find particles in kelp from kelp start
numberin1=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag1['x'][sidx[cidx],:],savelag1['y'][sidx[cidx],:]),cages).reshape(savelag1['x'][sidx[cidx],:].shape),axis=0)
numberin2=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag2['x'][sidx[cidx],:],savelag2['y'][sidx[cidx],:]),cages).reshape(savelag2['x'][sidx[cidx],:].shape),axis=0)

f = plt.figure()
ax=f.add_axes([.125,.1,.8,.8])

ax.plot((savelag1['time']-savelag1['time'].min())/3600,numberin1,'k',label='No drag')
ax.plot((savelag2['time']-savelag2['time'].min())/3600,numberin2,'r',label='Drag')
ax.set_xlim([-10,ax.get_xlim()[1]])

handles, labels = ax.get_legend_handles_labels()
legend=ax.legend(handles, labels)

ax.set_ylabel(r'Number of particles in kelp',fontsize=8)
ax.set_xlabel(r'Time (hour)',fontsize=8)

for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontsize(8)

f.savefig(savepath +''+name+'_'+name2+'_'+regionname+'_'+lname+'_compare_particles_inkelp_kelpstart.png',dpi=150)
plt.close(f)















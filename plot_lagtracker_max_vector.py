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
import h5py as h5
from matplotlib.collections import PolyCollection as PC



# Define names and types of data
name='kit4_45days_3'
name2='kit4_kelp_20m_0.018'
grid='kit4'
regionname='kit4_kelp_tight2_small'
datatype='2d'
scale1=75
kl=[.8,.02,.175,.1]
ebbfldscale='15000'

### load the .nc file #####
data = loadnc('runs/'+grid+'/' + name +'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

savepath='figures/png/' + grid + '_' + datatype + '/lagtracker/max_vectors/' + name + '_'+name2+'/'
if not os.path.exists(savepath): os.makedirs(savepath)

data['trigridxy'] = mplt.Triangulation(data['x'], data['y'],data['nv'])
region=regions(regionname)
region=regionll2xy(data,region)


if 'savelag1' not in globals():
    print "Loading savelag1"
    fileload=h5.File('/media/moflaher/Hardy/work_rsync/savedir/'+name+'/allelements_s0in_aristazabal_west.mat')
    savelag1={}
    for i in fileload['savelag'].keys():
            if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
                continue
            savelag1[i]=fileload['savelag'][i].value.T

if 'savelag2' not in globals():
    print "Loading savelag2"
    fileload=h5.File('/media/moflaher/Hardy/work_rsync/savedir/'+name2+'/allelements_s0in_aristazabal_west.mat')
    savelag2={}
    for i in fileload['savelag'].keys():
            if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
                continue
            savelag2[i]=fileload['savelag'][i].value.T


cages=np.genfromtxt('runs/'+grid+'/' +name2+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)


tmparray=[list(zip(data['nodexy'][data['nv'][i,[0,1,2]],0],data['nodexy'][data['nv'][i,[0,1,2]],1])) for i in cages ]
sidx=np.where((savelag1['x'][:,0]>region['regionxy'][0])&(savelag1['x'][:,0]<region['regionxy'][1])&(savelag1['y'][:,0]>region['regionxy'][2])&(savelag1['y'][:,0]<region['regionxy'][3]))[0]

savelag1['dist']=np.empty((len(sidx),len(savelag1['time'])))
savelag2['dist']=np.empty((len(sidx),len(savelag1['time'])))

for i in range(0,len(sidx)):
    j=sidx[i]    
    savelag1['dist'][i,:]=np.sqrt((savelag1['x'][j,:]-savelag1['x'][j,1])**2+(savelag1['y'][j,:]-savelag1['y'][j,1])**2)
    savelag2['dist'][i,:]=np.sqrt((savelag2['x'][j,:]-savelag2['x'][j,1])**2+(savelag2['y'][j,:]-savelag2['y'][j,1])**2)







f = plt.figure()
ax=f.add_axes([.125,.1,.8,.8])


q2x1=(savelag1['x'][sidx,np.argmax(savelag1['dist'],axis=1)])-savelag1['x'][sidx,0]
q2x2=(savelag2['x'][sidx,np.argmax(savelag2['dist'],axis=1)])-savelag2['x'][sidx,0]
q2y1=(savelag1['y'][sidx,np.argmax(savelag1['dist'],axis=1)])-savelag1['y'][sidx,0]
q2y2=(savelag2['y'][sidx,np.argmax(savelag2['dist'],axis=1)])-savelag2['y'][sidx,0]



Q1=ax.quiver(savelag1['x'][sidx,0],savelag1['y'][sidx,0],q2x1,q2y1,angles='xy',scale_units='xy',scale=scale1,zorder=10)
Q2=ax.quiver(savelag2['x'][sidx,0],savelag2['y'][sidx,0],q2x2,q2y2,angles='xy',scale_units='xy',scale=scale1,color='r',zorder=10)
ax.axis(region['regionxy'])

ax.triplot(data['trigridxy'],lw=.25)
lseg=PC(tmparray,facecolor = 'g',edgecolor='None',zorder=5)
ax.add_collection(lseg)

#fix_osw(ax)
#ax.set_aspect(get_aspectratio(region))
#plt.draw()
rec=mpl.patches.Rectangle((kl[0],kl[1]),kl[2],kl[3],transform=ax.transAxes,fc='w',zorder=20)
ax.add_patch(rec)
ax.annotate(r''+ebbfldscale+' m',xy=(kl[0]+.035,kl[1]+.07),xycoords='axes fraction',zorder=30,fontsize=8)
aqk1=ax.quiverkey(Q1,kl[0]+.075,kl[1]+.045,float(ebbfldscale), r'No drag', labelpos='E',fontproperties={'size': 8})
aqk2=ax.quiverkey(Q2,kl[0]+.075,kl[1]+.015,float(ebbfldscale), r'Drag', labelpos='E',fontproperties={'size': 8})
aqk1.set_zorder(30)
aqk2.set_zorder(30)
for label in ax.get_xticklabels()[::2]:
    label.set_visible(False)
plotcoast(ax,filename='pacific_kit4.nc',color='k')


#f.savefig(savepath + grid + '_'+ name+'_'+ name2+'_'+regionname+'_max_particle_vector.png',dpi=600)

#plt.close(f)














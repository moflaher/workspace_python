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
grid='kit4'
regionname='kit4_kelp_tight2'
datatype='2d'



### load the .nc file #####
data = loadnc('runs/'+grid+'/' + name +'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)


region=regions(regionname)


cage1n='kit4_cage_5m_30m'
cage2n='kit4_cage_5m_15m'
cages1=np.genfromtxt('data/cage_files/'+cage1n+'.dat',skiprows=1)
cages1=(cages1[:,0]-1).astype(int)
cages2=np.genfromtxt('data/cage_files/'+cage2n+'.dat',skiprows=1)
cages2=(cages2[:,0]-1).astype(int)

tmparray1=[list(zip(data['nodell'][data['nv'][i,[0,1,2]],0],data['nodell'][data['nv'][i,[0,1,2]],1])) for i in cages1 ]
lseg1=PC(tmparray1,facecolor = 'g',edgecolor='None')
tmparray2=[list(zip(data['nodell'][data['nv'][i,[0,1,2]],0],data['nodell'][data['nv'][i,[0,1,2]],1])) for i in cages2 ]
lseg2=PC(tmparray2,facecolor = 'b',edgecolor='None')

f = plt.figure()
ax=f.add_axes([.125,.1,.8,.8])

plotcoast(ax,filename='pacific.nc',color='k')
ax.triplot(data['trigrid'],lw=.25,zorder=1)
ax.axis(region['region'])
ax.add_collection(lseg1)
ax.add_collection(lseg2)
  
f.savefig(savepath +''+grid+'_'+cage1n+'_'+cage2n+'_'+regionname+'_cage_compare.png',dpi=150)
plt.close(f)





eidx=get_elements(data,region)
newhost=np.in1d(eidx,cages2)
tempdic={}
tempdic['cage_elements']=eidx[newhost]+1
sio.savemat('data/cage_files/kelp_elements_'+cage2n+'_'+regionname+'.mat',mdict=tempdic)














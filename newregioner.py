from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
import scipy.io as sio
import bisect

# Define names and types of data
name='kit4_kelp_20m_0.018'
grid='kit4'

regionname='kit4'



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)

region=regions(regionname)


nidx=get_nodes(data,region)

idx0=np.in1d(data['nv'][:,0],nidx)
idx1=np.in1d(data['nv'][:,1],nidx)
idx2=np.in1d(data['nv'][:,2],nidx)
eidx=idx0+idx1+idx2

nv2 = data['nv'][eidx].flatten(order='F')
nidx_uni=np.unique(nv2)
nv_tmp2=np.empty(shape=nv2.shape)
nv2_sortedind = nv2.argsort()
nv2_sortd = nv2[nv2_sortedind]
 
for i in xrange(len(nidx_uni)):
    i1 = bisect.bisect_left(nv2_sortd, nidx_uni[i])
    i2 = bisect.bisect_right(nv2_sortd,nidx_uni[i])
    inds = nv2_sortedind[i1:i2]
    nv_tmp2[inds] = i

nv_new = np.reshape(nv_tmp2, (-1, 3), 'F')













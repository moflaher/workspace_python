from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
import time
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import matplotlib.path as path

# Define names and types of data
name='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'

regionname='kit4'



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
if np.shape(cages)!=():
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.1
    ls='solid'


region=regions(regionname)
region={}
region['region']=np.array([-129.615566168,-129.215178942,52.44600635,52.83665705])

nidx=get_nodes(data,region)


f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
clims=np.percentile(data['h'][nidx],[1,99])
trip=ax.tripcolor(data['trigrid'],data['h'],vmin=clims[0],vmax=clims[1])
prettyplot_ll(ax,setregion=region,cb=trip,cblabel='Depth (m)',grid=True)
plotcoast(ax,color='k',fill=True)
if np.shape(cages)!=():   
    lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    ax.add_collection(lseg_t) 
#f.savefig(savepath + grid + '_' + regionname+'_current_variance_magnitude_ratio.png',dpi=600)
vec=f.ginput(n=2,timeout=-1)
plt.close(f)


ll1=np.min([vec[0][0],vec[1][0]])
ll2=np.max([vec[0][0],vec[1][0]])
ll3=np.min([vec[1][1],vec[0][1]])
ll4=np.max([vec[1][1],vec[0][1]])

print(vec)
print('')
print('region={}')
print('region[\'region\']=np.array([{},{},{},{}])'.format(ll1,ll2,ll3,ll4))


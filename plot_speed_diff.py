from __future__ import division
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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC

# Define names and types of data
name1='kit4_kelp_nodrag'
name2='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'
regionname='kit4_kelp_tight2_kelpfield'
datatype='2d'
starttime=400
endtime=450
#offset its to account for different starttimes
offset=0
cmin=-0.5
cmax=0.5


### load the .nc file #####
data1 = loadnc('runs/'+grid+'/'+name1+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data1 = ncdatasort(data1)
data2 = ncdatasort(data2)
print 'done sort'


cages=np.genfromtxt('runs/'+grid+'/' +name2+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)


region=regions(regionname)
nidx=get_nodes(data1,region)

savepath='figures/timeseries/' + grid + '_' + datatype + '/speed_diff/' + name1 + '_' +name2 + '_' + regionname + '_' +("%f" %cmin) + '_' + ("%f" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)





# Plot depth and cage locations
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
triax=ax.tripcolor(data1['trigrid'],data1['h'],vmin=data1['h'][nidx].min(),vmax=data1['h'][nidx].max())
ax.plot(data1['uvnodell'][cages,0],data1['uvnodell'][cages,1],'k.',markersize=2)
prettyplot_ll(ax,setregion=region,grid=True,cblabel=r'Depth (m)',cb=triax)
f.savefig(savepath + grid + '_' + regionname +'_cage_locations.png',dpi=1200)
plt.close(f)


# Plot speed difference
for i in range(starttime,endtime):
    print i
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data1['trigrid'],np.sqrt(data1['ua'][i,:]**2+data1['va'][i,:]**2)-np.sqrt(data2['ua'][i+offset,:]**2+data2['va'][i+offset,:]**2),vmin=cmin,vmax=cmax)
    ax.plot(data1['uvnodell'][cages,0],data1['uvnodell'][cages,1],'k.',markersize=.5)
    prettyplot_ll(ax,setregion=region,grid=True,cblabel=r'Speed Difference (ms$^{-1}$)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_speeddiff_' + ("%04d" %(i)) + '.png',dpi=300)
    plt.close(f)





























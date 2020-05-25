from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC


# Define names and types of data
name='1978-03-04_1978-04-06'
grid='fr_high'
regionname1='vhfr_whole'
regionname2='fr_mouth'

#spacing must be even
spacing=250
stype='tanh'



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data,trifinder=True)
print('done sort')

cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
if np.shape(cages)!=():
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2]],0],data['nodell'][data['nv'][i,[0,1,2]],1])) for i in cages ]
    color='g'

savepath='figures/timeseries/' + grid + '_'  + '/zoom/'+regionname1+'_'+regionname2+'_'+stype+'_'+("%d"%spacing)+'/'
if not os.path.exists(savepath): os.makedirs(savepath)


region1=regions(regionname1)  
region2=regions(regionname2)    

f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.triplot(data['trigrid'],lw=.1)
#prettyplot_ll(ax,setregion=region)
#scalebar(ax,region,200)
plotcoast(ax,filename='pacific.nc',color='None',fill=True)
if np.shape(cages)!=():
    lsega=PC(tmparray,facecolor = color,edgecolor='None')
    ax.add_collection(lsega)
_formatter = mpl.ticker.FormatStrFormatter("%.2f")
ax.yaxis.set_major_formatter(_formatter)
ax.xaxis.set_major_formatter(_formatter)

ax.set_xlabel(r'Longitude ($^{\circ}$W)')
ax.set_ylabel(r'Latitude ($^{\circ}$N)')


tempregion={}
if 'linear' in stype:
    #constant speed
    spaces=np.array([s*(region1['region']-region2['region'])/spacing for s in range(spacing)])
if 'quad' in stype:
    #slow then fast
    spaces=(region1['region']-region2['region'])*np.atleast_2d(np.array([s**2 for s in range(spacing)])/(spacing-1.0)**2).T
if 'quadr' in stype:
    #fast then slow
    spaces=(region1['region']-region2['region'])*np.atleast_2d(np.flipud(1-(np.array([s**2 for s in range(spacing)]))/(spacing-1.0)**2)).T
if 'tanh' in stype:
    #slow fast slow
    tanh=np.tanh(np.linspace(2,4,spacing/2))
    speed=np.cumsum(np.hstack([np.flipud(1-tanh),1-tanh]))
    speed=speed/speed.max()
    spaces=(region1['region']-region2['region'])*np.atleast_2d(speed).T


for i in range(spacing):
    print(i)
    tempregion['region']=region1['region']-spaces[i]
    ax.axis(tempregion['region'])
    ax.set_aspect(get_aspectratio(tempregion))
    for label in ax.get_xticklabels()+ax.get_yticklabels():
        label.set_visible(True)
    for label in ax.get_xticklabels()[::2]+ax.get_yticklabels()[::2]:
        label.set_visible(False)
    ax.set_xticklabels(-1*(ax.get_xticks()))

    f.savefig(savepath + grid + '_'+ name +'_'+regionname1+'_'+regionname2+'_'+stype+'_'+'spacing_'+("%d"%spacing)+'_'+("%05d"%i)+'_grid.png',dpi=150)
    #plt.close(f)

for j in range(i,i+50):
    f.savefig(savepath + grid + '_'+ name +'_'+regionname1+'_'+regionname2+'_'+stype+'_'+'spacing_'+("%d"%spacing)+'_'+("%05d"%j)+'_grid.png',dpi=150)



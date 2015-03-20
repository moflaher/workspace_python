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



# Define names and types of data
name='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'
datatype='2d'
regionname='kit4_kelp_tight5'
starttime=400
endtime=450


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
if cages!=None:
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.2
    ls='solid'


region=regions(regionname)
nidx=get_nodes(data,region)

savepath='figures/timeseries/' + grid + '_' + datatype + '/zeta/' + name + '_' + regionname + '/'
if not os.path.exists(savepath): os.makedirs(savepath)


# Plot mesh
for i in range(starttime,endtime):
    print i
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    nidxh=data['zeta'][i,nidx]
    her=nidxh[nidxh!=0]
    triax=ax.tripcolor(data['trigrid'],data['zeta'][i,:],vmin=her.min(),vmax=her.max())
    if cages!=None:   
        ax.plot(data['uvnodell'][cages,0],data['uvnodell'][cages,1],'w.',markersize=1) 
    prettyplot_ll(ax,setregion=region,cblabel='Elevation (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_zeta_' + ("%04d" %(i)) + '.png',dpi=300)
    plt.close(f)































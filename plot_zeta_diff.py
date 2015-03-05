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
cmin=-0.02
cmax=0.02


### load the .nc file #####
data1 = loadnc('runs/'+grid+'/'+name1+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data1 = ncdatasort(data1)
data2 = ncdatasort(data2)
print 'done sort'


cages=None
with open('runs/'+grid+'/' +name2+ '/input/' +grid+ '_cage.dat') as f_in:
    cages=np.genfromtxt(f_in,skiprows=1)
    if len(cages)>0:
        cages=(cages[:,0]-1).astype(int)
    else:
        cages=None



region=regions(regionname)
nidx=get_nodes(data1,region)

savepath='figures/timeseries/' + grid + '_' + datatype + '/zeta_diff/' + name1 + '_' +name2 + '_' + regionname + '_' +("%f" %cmin) + '_' + ("%f" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)




# Plot zeta difference
for i in range(starttime,endtime):
    print i
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data1['trigrid'],data1['zeta'][i,:]-data2['zeta'][i,:],vmin=cmin,vmax=cmax)
    if cages!=None:   
        ax.plot(data2['uvnodell'][cages,0],data2['uvnodell'][cages,1],'w.',markersize=1) 
    prettyplot_ll(ax,setregion=region,cblabel='Elevation (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_zetadiff_' + ("%04d" %(i)) + '.png',dpi=300)
    plt.close(f)




























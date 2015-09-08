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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name1='kit4_45days_3'
name2='kit4_kelp_test'
grid1='kit4'
grid2='kit4_kelp'
regionname='gilisland'
datatype='2d'
starttime=384
endtime=500
#offset its to account for different starttimes
offset=0
cmin=-0.5
cmax=0.5


### load the .nc file #####
data1 = loadnc('runs/'+grid1+'/'+name1+'/output/',singlename=grid1 + '_0001.nc')
data2 = loadnc('runs/'+grid2+'/'+name2+'/output/',singlename=grid2 + '_0001.nc')
print('done load')
data1 = ncdatasort(data1)
data2 = ncdatasort(data2)
print('done sort')


savepath='figures/png/' + grid2 + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)



region=regions(regionname)


interp_h=mpl.tri.LinearTriInterpolator(data1['trigrid'], data1['h'])

new_h=interp_h(data2['nodell'][:,0],data2['nodell'][:,1])


plt.close()
# Plot depth difference
triax=plt.tripcolor(data2['trigrid'],data2['h']-new_h)
prettyplot_ll(plt.gca(),cb=triax,cblabel=r'Depth grid-interp_h (m)')
plt.savefig(savepath + grid2 + '_depth_difference.png',dpi=1200)



plt.close()
# Plot depth difference
triax=plt.tripcolor(data2['trigrid'],data2['h'],vmin=0,vmax=650)
prettyplot_ll(plt.gca(),cb=triax,cblabel=r'Depth (m)')
plt.savefig(savepath + grid2 + '_depth.png',dpi=1200)































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
import time

# Define names and types of data
name_orig='kit4_45days_3'
grid='kit4'
datatype='2d'
regionname='kit4_kelp_tight6'
starttime=384




### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name_orig+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')






region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)




savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)




f, ax = plt.subplots(nrows=2,ncols=2)


ngridx = 500
ngridy = 500

speed=np.sqrt(data['ua'][500,:]**2+data['va'][500,:]**2)

start = time.clock()
xi = np.linspace(region['region'][0],region['region'][1], ngridx)
yi = np.linspace(region['region'][2],region['region'][3], ngridy)
zi=mpl.mlab.griddata(data['uvnodell'][:,0],data['uvnodell'][:,1], speed, xi, yi)
tmpxy=np.meshgrid(xi,yi)
xii=tmpxy[0]
yii=tmpxy[1]
host=data['trigrid'].get_trifinder().__call__(xii,yii)
zi2=speed[host]
diff=zi-zi2
rel=np.divide(zi-zi2,zi2)

Zm = np.ma.masked_where(host==-1,diff)
Zmr = np.ma.masked_where(host==-1,rel)
Zmi = np.ma.masked_where(host==-1,zi)
print ('griddata interp: %f' % (time.clock() - start))


start = time.clock()
axtri1=ax[0,0].tripcolor(data['trigrid'],speed,vmin=speed[eidx].min(),vmax=speed[eidx].max())
plt.colorbar(axtri1,ax=ax[0,0])
ax[0,0].axis(region['region'])
print ('tripcolor: %f' % (time.clock() - start))

start = time.clock()
axtri2a=ax[0,1].pcolor(xi,yi,Zmi)
plt.colorbar(axtri2a,ax=ax[0,1])
print ('pcolor: %f' % (time.clock() - start))

start = time.clock()
axtri2=ax[1,0].pcolor(xi,yi,Zm)
plt.colorbar(axtri2,ax=ax[1,0])
print ('pcolor: %f' % (time.clock() - start))

start = time.clock()
axtri2c=ax[1,1].pcolor(xi,yi,Zmr*100,vmin=-60,vmax=60)
plt.colorbar(axtri2c,ax=ax[1,1])
print ('pcolor: %f' % (time.clock() - start))

fix_osw(ax[0,0])
fix_osw(ax[0,1])
fix_osw(ax[1,0])
fix_osw(ax[1,1])
ax_label_spacer(ax[0,0])
ax_label_spacer(ax[0,1])
ax_label_spacer(ax[1,0])
ax_label_spacer(ax[1,1])


f.tight_layout(pad=1)
f.savefig(savepath + grid + '_' + regionname+'_griddata_compare.png',dpi=600)
plt.close(f)












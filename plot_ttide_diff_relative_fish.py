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
name='sfm6_musq2_no_cages'
nameold='sfm6_musq2_old_cages'
nameall='sfm6_musq2_all_cages'
grid='sfm6_musq2'
regionname='musq_cage'
datatype='2d'

### load the .nc file #####
data = loadnc('/media/moflaher/My Book/cages/' + name + '/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'






region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)


savepath='figures/png/' + grid + '_' + datatype + '/ttide_diff_rel/' + name + '_' + regionname + '/'
if not os.path.exists(savepath): os.makedirs(savepath)

plt.close()


el=np.load('/home/moflaher/Desktop/workspace_python/data/ttide/'+grid+'_'+name+'_'+datatype+'_el.npy')
el=el[()]
uv=np.load('/home/moflaher/Desktop/workspace_python/data/ttide/'+grid+'_'+name+'_'+datatype+'_uv.npy')
uv=uv[()]

elold=np.load('/home/moflaher/Desktop/workspace_python/data/ttide/'+grid+'_'+nameold+'_'+datatype+'_el.npy')
elold=elold[()]
uvold=np.load('/home/moflaher/Desktop/workspace_python/data/ttide/'+grid+'_'+nameold+'_'+datatype+'_uv.npy')
uvold=uvold[()]

elall=np.load('/home/moflaher/Desktop/workspace_python/data/ttide/'+grid+'_'+nameall+'_'+datatype+'_el.npy')
elall=elall[()]
uvall=np.load('/home/moflaher/Desktop/workspace_python/data/ttide/'+grid+'_'+nameall+'_'+datatype+'_uv.npy')
uvall=uvall[()]

_formatter = mpl.ticker.ScalarFormatter(useOffset=False)

# Plot ttide el amp difference for fish cages
f, (ax1, ax2,ax3) = plt.subplots(3, sharex=True, sharey=True)
ax1tri=ax1.tripcolor(data['trigrid'],el['tidecon'][:,3,0],vmin=el['tidecon'][nidx,3,0].min(),vmax=el['tidecon'][nidx,3,0].max())
ax1cb=plt.colorbar(ax1tri,ax=ax1)
ax1cb.set_label(r'Amplitude (m)')
ax1.yaxis.set_major_formatter(_formatter)
ax1.xaxis.set_major_formatter(_formatter)
ax1.set_ylabel(r'Latitude (N$^{\circ}$)')
ax1.annotate("A",xy=(.025,.85),xycoords='axes fraction')

ax2tri=ax2.tripcolor(data['trigrid'],np.divide(el['tidecon'][:,3,0]-elold['tidecon'][:,3,0],el['tidecon'][:,3,0]+.0001),vmin=-1,vmax=1)
ax2cb=plt.colorbar(ax2tri,ax=ax2)
ax2cb.set_label(r'Relative Difference')
ax2.yaxis.set_major_formatter(_formatter)
ax2.xaxis.set_major_formatter(_formatter)
ax2.set_ylabel(r'Latitude (N$^{\circ}$)')
ax2.annotate("B",xy=(.025,.85),xycoords='axes fraction')

ax3tri=ax3.tripcolor(data['trigrid'],np.divide(el['tidecon'][:,3,0]-elall['tidecon'][:,3,0],el['tidecon'][:,3,0]+.0001),vmin=-1,vmax=1)
ax3cb=plt.colorbar(ax3tri,ax=ax3)
ax3cb.set_label(r'Relative Difference')
ax3.yaxis.set_major_formatter(_formatter)
ax3.xaxis.set_major_formatter(_formatter)
ax3.axis(region['region'])
ax3.set_xlabel(r'Longitude (W$^{\circ}$)')
ax3.set_ylabel(r'Latitude (N$^{\circ}$)')
ax3.annotate("C",xy=(.025,.85),xycoords='axes fraction')

f.suptitle(r'M2 Elevation')
f.savefig(savepath + grid + '_' + regionname +'_el_m2_amp_difference_relative.png',dpi=1200)

#ttide el phase difference
f, (ax1, ax2,ax3) = plt.subplots(3, sharex=True, sharey=True)
ax1tri=ax1.tripcolor(data['trigrid'],el['tidecon'][:,3,2],vmin=0,vmax=360,cmap=plt.cm.hsv)
ax1cb=plt.colorbar(ax1tri,ax=ax1)
ax1cb.set_label(r'Phase ($^{\circ}$)')
ax1.yaxis.set_major_formatter(_formatter)
ax1.xaxis.set_major_formatter(_formatter)
ax1.set_ylabel(r'Latitude (N$^{\circ}$)')
ax1.annotate("A",xy=(.025,.85),xycoords='axes fraction')

ax2tri=ax2.tripcolor(data['trigrid'],el['tidecon'][:,3,2]-elold['tidecon'][:,3,2],vmin=(el['tidecon'][nidx,3,2]-elold['tidecon'][nidx,3,2]).min(),vmax=(el['tidecon'][nidx,3,2]-elold['tidecon'][nidx,3,2]).max())
ax2cb=plt.colorbar(ax2tri,ax=ax2)
ax2cb.set_label(r'Difference ($^{\circ}$)')
ax2.yaxis.set_major_formatter(_formatter)
ax2.xaxis.set_major_formatter(_formatter)
ax2.set_ylabel(r'Latitude (N$^{\circ}$)')
ax2.annotate("B",xy=(.025,.85),xycoords='axes fraction')

ax3tri=ax3.tripcolor(data['trigrid'],el['tidecon'][:,3,2]-elall['tidecon'][:,3,2],vmin=(el['tidecon'][nidx,3,2]-elall['tidecon'][nidx,3,2]).min(),vmax=(el['tidecon'][nidx,3,2]-elall['tidecon'][nidx,3,2]).max())
ax3cb=plt.colorbar(ax3tri,ax=ax3)
ax3cb.set_label(r'Difference ($^{\circ}$)')
ax3.yaxis.set_major_formatter(_formatter)
ax3.xaxis.set_major_formatter(_formatter)
ax3.axis(region['region'])
ax3.set_xlabel(r'Longitude (W$^{\circ}$)')
ax3.set_ylabel(r'Latitude (N$^{\circ}$)')
ax3.annotate("C",xy=(.025,.85),xycoords='axes fraction')

f.suptitle(r'M2 Elevation Phase')
f.savefig(savepath + grid + '_' + regionname +'_el_m2_phase_difference.png',dpi=1200)



# Plot ttide uv amp and phase
f, (ax1, ax2,ax3) = plt.subplots(3, sharex=True, sharey=True)
ax1tri=ax1.tripcolor(data['trigrid'],uv['tidecon'][:,3,0],vmin=uv['tidecon'][nidx,3,0].min(),vmax=uv['tidecon'][nidx,3,0].max())
ax1cb=plt.colorbar(ax1tri,ax=ax1)
ax1cb.set_label(r'Amplitude (ms$^{-1}$)')
ax1.yaxis.set_major_formatter(_formatter)
ax1.xaxis.set_major_formatter(_formatter)
ax1.set_ylabel(r'Latitude (N$^{\circ}$)')
ax1.annotate("A",xy=(.025,.85),xycoords='axes fraction')

ax2tri=ax2.tripcolor(data['trigrid'],np.divide(uv['tidecon'][:,3,0]-uvold['tidecon'][:,3,0],uv['tidecon'][:,3,0]+.01),vmin=-1,vmax=1)
ax2cb=plt.colorbar(ax2tri,ax=ax2)
ax2cb.set_label(r'Relative Difference')
ax2.yaxis.set_major_formatter(_formatter)
ax2.xaxis.set_major_formatter(_formatter)
ax2.set_ylabel(r'Latitude (N$^{\circ}$)')
ax2.annotate("B",xy=(.025,.85),xycoords='axes fraction')

ax3tri=ax3.tripcolor(data['trigrid'],np.divide(uv['tidecon'][:,3,0]-uvall['tidecon'][:,3,0],uv['tidecon'][:,3,0]+.01),vmin=-1,vmax=1)
ax3cb=plt.colorbar(ax3tri,ax=ax3)
ax3cb.set_label(r'Relative Difference')
ax3.yaxis.set_major_formatter(_formatter)
ax3.xaxis.set_major_formatter(_formatter)
ax3.axis(region['region'])
ax3.set_xlabel(r'Longitude (W$^{\circ}$)')
ax3.set_ylabel(r'Latitude (N$^{\circ}$)')
ax3.annotate("C",xy=(.025,.85),xycoords='axes fraction')

f.suptitle(r'M2 Current Major Axis')
f.savefig(savepath + grid + '_' + regionname +'_uv_m2_amp_major_difference_relative.png',dpi=1200)


#ttide uv phase difference
f, (ax1, ax2,ax3) = plt.subplots(3, sharex=True, sharey=True)
ax1tri=ax1.tripcolor(data['trigrid'],uv['tidecon'][:,3,6],vmin=0,vmax=360,cmap=plt.cm.hsv)
ax1cb=plt.colorbar(ax1tri,ax=ax1)
ax1cb.set_label(r'Phase ($^{\circ}$)')
ax1.yaxis.set_major_formatter(_formatter)
ax1.xaxis.set_major_formatter(_formatter)
ax1.set_ylabel(r'Latitude (N$^{\circ}$)')
ax1.annotate("A",xy=(.025,.85),xycoords='axes fraction')

ax2tri=ax2.tripcolor(data['trigrid'],uv['tidecon'][:,3,6]-uvold['tidecon'][:,3,6],vmin=-360,vmax=360,cmap=plt.cm.hsv)
ax2cb=plt.colorbar(ax2tri,ax=ax2)
ax2cb.set_label(r'Difference ($^{\circ}$)')
ax2.yaxis.set_major_formatter(_formatter)
ax2.xaxis.set_major_formatter(_formatter)
ax2.set_ylabel(r'Latitude (N$^{\circ}$)')
ax2.annotate("B",xy=(.025,.85),xycoords='axes fraction')

ax3tri=ax3.tripcolor(data['trigrid'],uv['tidecon'][:,3,6]-uvall['tidecon'][:,3,6],vmin=-360,vmax=360,cmap=plt.cm.hsv)
ax3cb=plt.colorbar(ax3tri,ax=ax3)
ax3cb.set_label(r'Difference ($^{\circ}$)')
ax3.yaxis.set_major_formatter(_formatter)
ax3.xaxis.set_major_formatter(_formatter)
ax3.axis(region['region'])
ax3.set_xlabel(r'Longitude (W$^{\circ}$)')
ax3.set_ylabel(r'Latitude (N$^{\circ}$)')
ax3.annotate("C",xy=(.025,.85),xycoords='axes fraction')

f.suptitle(r'M2 Current Phase')
f.savefig(savepath + grid + '_' + regionname +'_uv_m2_phase_difference.png',dpi=1200)




















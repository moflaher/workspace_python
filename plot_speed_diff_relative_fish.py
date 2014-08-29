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
name1='sfm6_musq2_no_cages'
name2='sfm6_musq2_old_cages'
name3='sfm6_musq2_all_cages'
grid='sfm6_musq2'
regionname='musq_cage'
datatype='2d'
starttime=0
endtime=72
#offset its to account for different starttimes
offset=1008
cmin=-1
cmax=1


### load the .nc file #####
data1 = loadnc('/media/moflaher/My Book/cages/' + name1 +'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('/media/moflaher/My Book/cages/' + name2 +'/output/',singlename=grid + '_0001.nc')
data3 = loadnc('/media/moflaher/My Book/cages/' + name3 +'/output/',singlename=grid + '_0001.nc')
print 'done load'
data1 = ncdatasort(data1)
print 'done sort'


cages2=np.genfromtxt('/media/moflaher/My Book/cages/' +name2+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages2=(cages2[:,0]-1).astype(int)
cages3=np.genfromtxt('/media/moflaher/My Book/cages/' +name3+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages3=(cages3[:,0]-1).astype(int)

region=regions(regionname)
nidx=get_nodes(data1,region)

savepath='figures/timeseries/' + grid + '_' + datatype + '/speed_diff_rel_fish/' + name1 + '_' +name2 +'_' +name3 + '_' + regionname + '_' +("%f" %cmin) + '_' + ("%f" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)




_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
plt.close()
# Plot speed difference
for i in range(starttime,endtime):
    print i



    speed1=np.sqrt(data1['ua'][starttime+offset+i,:]**2+data1['va'][starttime+offset+i,:]**2)
    speed2=np.sqrt(data2['ua'][starttime+i,:]**2+data2['va'][starttime+i,:]**2)
    speed3=np.sqrt(data3['ua'][starttime+i,:]**2+data3['va'][starttime+i,:]**2)
    
    # Plot speed difference
    f, (ax1, ax2,ax3) = plt.subplots(3, sharex=True, sharey=True)
    ax1tri=ax1.tripcolor(data1['trigrid'],speed1,vmin=0,vmax=2)
    ax1cb=plt.colorbar(ax1tri,ax=ax1)
    ax1cb.set_label(r'Speed (ms$^{-1}$)')
    ax1.yaxis.set_major_formatter(_formatter)
    ax1.xaxis.set_major_formatter(_formatter)
    ax1.set_ylabel(r'Latitude (N$^{\circ}$)')
    ax1.annotate("A",xy=(.025,.85),xycoords='axes fraction')

    ax2tri=ax2.tripcolor(data1['trigrid'],np.divide(speed2-speed1,speed1+.01),vmin=cmin,vmax=cmax)
    ax2cb=plt.colorbar(ax2tri,ax=ax2)
    ax2cb.set_label(r'Relative Difference')
    ax2.yaxis.set_major_formatter(_formatter)
    ax2.xaxis.set_major_formatter(_formatter)
    ax2.set_ylabel(r'Latitude (N$^{\circ}$)')
    ax2.annotate("B",xy=(.025,.85),xycoords='axes fraction')
    ax2.plot(data1['uvnodell'][cages2,0],data1['uvnodell'][cages2,1],'k.',markersize=.5)

    ax3tri=ax3.tripcolor(data1['trigrid'],np.divide(speed3-speed1,speed1+.01),vmin=cmin,vmax=cmax)
    ax3cb=plt.colorbar(ax3tri,ax=ax3)
    ax3cb.set_label(r'Relative Difference')
    ax3.yaxis.set_major_formatter(_formatter)
    ax3.xaxis.set_major_formatter(_formatter)
    ax3.axis(region['region'])
    ax3.set_xlabel(r'Longitude (W$^{\circ}$)')
    ax3.set_ylabel(r'Latitude (N$^{\circ}$)')
    ax3.annotate("C",xy=(.025,.85),xycoords='axes fraction')
    ax3.plot(data1['uvnodell'][cages3,0],data1['uvnodell'][cages3,1],'k.',markersize=.5)

    f.suptitle(r'Speed Difference')
    f.savefig(savepath + grid + '_' + regionname +'_speeddiff_rel_' + ("%04d" %(starttime+offset+i)) + '.png',dpi=300)

    plt.close(f)





























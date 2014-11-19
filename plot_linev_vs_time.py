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
import time as timem
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
from scipy import interpolate as intp
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Define names and types of data
name_orig='kit4_45days_3'
name_change='kit4_kelp_20m_0.018'
grid='kit4'
datatype='2d'
regionname='kit4_kelp_tight2'
starttime=400
endtime=520



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name_orig+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name_change+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'



savepath='figures/png/' + grid + '_' + datatype + '/linev_vs_time/' + name_orig + '_' + name_change + '/'
if not os.path.exists(savepath): os.makedirs(savepath)


region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)


spacing=1
line=[-129.48666,52.63,52.68]
ngridy = 500
eles=[77566,80168]


H1=(sw.dist([line[2], line[1]],[line[0], line[0]],'km'))[0]*1000;
linea=(sw.dist([data['uvnodell'][eles[0],1], line[1]],[line[0], line[0]],'km'))[0]*1000;
lineb=(sw.dist([data['uvnodell'][eles[1],1], line[1]],[line[0], line[0]],'km'))[0]*1000;

start = timem.clock()
time=np.arange(0,endtime-starttime,spacing)
yi = np.linspace(line[1],line[2], ngridy)
yim = np.linspace(0,H1, ngridy)
xi = (np.zeros((len(yi),1))+line[0]).flatten()
interpdataT=np.empty((ngridy,len(time)))
interpdata2T=np.empty((ngridy,len(time)))
for i in range(0,len(time)):
    interpdataT[:,i]=mpl.mlab.griddata(data['nodell'][nidx,0],data['nodell'][nidx,1], data2['zeta'][starttime+time[i],nidx], xi, yi)[:,0]
    interpdata2T[:,i]=mpl.mlab.griddata(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1], data2['va'][starttime+time[i],eidx], xi, yi)[:,0]
print ('griddata interp: %f' % (timem.clock() - start))








#interpFun1 = intp.LinearNDInterpolator((data['uvnodell'][:,0],data['uvnodell'][:,1],time),data['va'][starttime:endtime,:].T)
#interpFun1 = intp.griddata((data['uvnodell'][:,0],data['uvnodell'][:,1],time),data['va'][starttime:endtime,:].T,(xi, yi,time))
#interpFun1 = intp.LinearNDInterpolator(data['uvnodell'],data['va'][384,:])

f, ax = plt.subplots(nrows=2,ncols=1, sharex=True)




ax0cb=ax[0].pcolor(time,yim,interpdataT)
divider0 = make_axes_locatable(ax[0])
cax0 = divider0.append_axes("right", "3%", pad="2%")
cb1=plt.colorbar(ax0cb,cax=cax0)
cb1.set_label(r'Elevation (m)',fontsize=8)
ax[0].axis([time.min(), time.max(),yim.min(),yim.max()])
ax[0].set_ylabel(r'Distance (m)',fontsize=10)
ax[0].plot(time,np.zeros(shape=time.shape)+linea,'k',lw=.5,ls='--')
ax[0].plot(time,np.zeros(shape=time.shape)+lineb,'k',lw=.5,ls='--')

ax1cb=ax[1].pcolor(time,yim,interpdata2T,vmin=-.18,vmax=.18)
divider1 = make_axes_locatable(ax[1])
cax1 = divider1.append_axes("right", "3%", pad="2%")
cb2=plt.colorbar(ax1cb,cax=cax1)
cb2.set_label(r'v-velocity (m s$^{-1}$)',fontsize=8)
ax[1].axis([time.min(), time.max(),yim.min(),yim.max()])
ax[1].set_ylabel(r'Distance (m)',fontsize=10)
ax[1].set_xlabel(r'Time (h)',fontsize=10)
ax[1].plot(time,np.zeros(shape=time.shape)+linea,'k',lw=.5,ls='--')
ax[1].plot(time,np.zeros(shape=time.shape)+lineb,'k',lw=.5,ls='--')


_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
ax[0].yaxis.set_major_formatter(_formatter)
ax[0].xaxis.set_major_formatter(_formatter)
ax[1].yaxis.set_major_formatter(_formatter)
ax[1].xaxis.set_major_formatter(_formatter)


ax[0].annotate("A",xy=(.025,.9),xycoords='axes fraction')
ax[1].annotate("B",xy=(.025,.9),xycoords='axes fraction')



f.tight_layout(h_pad=.1)
f.savefig(savepath + grid + '_' + name_orig + '_' + name_change + '_linev_vs_time.png',dpi=300)
plt.close(f)







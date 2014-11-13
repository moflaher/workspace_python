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

# Define names and types of data
name_orig='kit4_45days_3'
name_change='kit4_kelp_20m_0.018'
grid='kit4'
datatype='2d'
regionname='kit4_kelp_tight2'
starttime=400
endtime=425



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


factor=2
spacing=1
line=[-129.48666,52.63,52.67]
ngridy = 500




start = timem.clock()
time=np.arange(0,endtime-starttime,spacing)
yi = np.linspace(line[1],line[2], ngridy)
xi = (np.zeros((len(yi),1))+line[0]).flatten()
interpdataT=np.empty((ngridy,len(time)))
interpdata2T=np.empty((ngridy,len(time)))
for i in range(0,len(time)):
    interpdataT[:,i]=mpl.mlab.griddata(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1], data['va'][starttime+time[i],eidx], xi, yi)[:,0]
    interpdata2T[:,i]=mpl.mlab.griddata(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1], data2['va'][starttime+time[i],eidx], xi, yi)[:,0]
print ('griddata interp: %f' % (timem.clock() - start))








#interpFun1 = intp.LinearNDInterpolator((data['uvnodell'][:,0],data['uvnodell'][:,1],time),data['va'][starttime:endtime,:].T)
#interpFun1 = intp.griddata((data['uvnodell'][:,0],data['uvnodell'][:,1],time),data['va'][starttime:endtime,:].T,(xi, yi,time))
#interpFun1 = intp.LinearNDInterpolator(data['uvnodell'],data['va'][384,:])

f, ax = plt.subplots(nrows=2,ncols=1, sharex=True, sharey=True)

for i in range(0,len(time)):
    ax[0].plot(0*factor*interpdataT[:,i]+time[i],yi,'k',lw=.25,ls='--')
    ax[0].plot(factor*interpdataT[:,i]+time[i],yi)

for i in range(0,len(time)):
    ax[1].plot(0*factor*interpdataT[:,i]+time[i],yi,'k',lw=.25,ls='--')
    ax[1].plot(factor*interpdata2T[:,i]+time[i],yi)


_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
ax[0].yaxis.set_major_formatter(_formatter)
ax[0].xaxis.set_major_formatter(_formatter)
ax[1].yaxis.set_major_formatter(_formatter)
ax[1].xaxis.set_major_formatter(_formatter)


ax[0].annotate("A",xy=(.025,.9),xycoords='axes fraction')
ax[1].annotate("B",xy=(.025,.9),xycoords='axes fraction')



f.savefig(savepath + grid + '_' + name_orig + '_' + name_change + '_linev_vs_time.png',dpi=300)
plt.close(f)







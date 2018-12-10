
# coding: utf-8



# In[57]:

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

figsize(16,12)


# Load the data in to the notebook

# In[42]:

name1='kit4_45days_3'
name2='kit4_kelp_0.1'
grid='kit4'
regionname='mostchannels'

starttime=130
endtime=160

data1 = loadnc('/media/moflaher/My Book/kit4_runs/' + name1 +'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('/media/moflaher/My Book/kit4_runs/' + name2 +'/output/',singlename=grid + '_0001.nc')
data1 = ncdatasort(data1)
data2 = ncdatasort(data2)

data1['uvzeta']=(data1['zeta'][starttime:endtime,data1['nv'][:,0]] + data1['zeta'][starttime:endtime,data1['nv'][:,1]] + data1['zeta'][starttime:endtime,data1['nv'][:,2]]) / 3.0
data2['uvzeta']=(data2['zeta'][starttime:endtime,data1['nv'][:,0]] + data2['zeta'][starttime:endtime,data1['nv'][:,1]] + data2['zeta'][starttime:endtime,data1['nv'][:,2]]) / 3.0

region=regions(regionname)
nidx=get_nodes(data1,region)


#savepath='figures/png/' + grid + '_'  + '/kelp_drag_speed/'
#if not os.path.exists(savepath): os.makedirs(savepath)


# Find the location with the largest differences over all

# In[10]:

speed1=np.sqrt(data1['ua'][starttime:endtime,:]**2+data1['va'][starttime:endtime,:]**2)
speed2=np.sqrt(data2['ua'][starttime:endtime,:]**2+data2['va'][starttime:endtime,:]**2)
diff=np.fabs(speed1-speed2)
diffsum=np.sum(np.fabs(speed1-speed2),axis=0)
idx=np.argsort(diffsum)
idx=idx[::-1]


# Plot the timeseries from both grids at the element with the biggest speed difference

# In[58]:

howmany=5
plt.close()
plt.tripcolor(data1['trigrid'],data1['h'],vmin=data1['h'][nidx].min(),vmax=data1['h'][nidx].max())
plt.plot(data1['uvnodell'][idx[0:howmany],0],data1['uvnodell'][idx[0:howmany],1],'r*',markersize=16)
cb=plt.colorbar()
cb.set_label('Depth (meters)')
plt=prettyplot_ll(plt,setregion=region,grid=True)
#plt.savefig(savepath + grid + '_' +name1+ '_'+name2+'_'+ regionname +'_current_locations.png',dpi=1200)


# In[59]:

for i in range(0,howmany):
    f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=False)
    ax1.plot(data1['time'][starttime:endtime],np.sqrt(data1['u'][starttime:endtime,0,idx[i]]**2+data1['v'][starttime:endtime,0,idx[i]]**2),'r',lw=2,label='No kelp')
    ax1.plot(data1['time'][starttime:endtime],np.sqrt(data2['u'][starttime:endtime,0,idx[i]]**2+data2['v'][starttime:endtime,0,idx[i]]**2),'b',lw=1,label='Kelp')
    ax1.grid()
    ax1.set_title('Surface currents at: %d' % (idx[i]))
    ax1.set_ylabel(r'Speed ($\frac{m}{s}$)')
    handles, labels = ax1.get_legend_handles_labels()
    ax1.legend(handles[::-1], labels[::-1])
    
    ax2.plot(data1['time'][starttime:endtime],np.sqrt(data1['u'][starttime:endtime,10,idx[i]]**2+data1['v'][starttime:endtime,10,idx[i]]**2),'r',lw=2,label='No kelp')
    ax2.plot(data1['time'][starttime:endtime],np.sqrt(data2['u'][starttime:endtime,10,idx[i]]**2+data2['v'][starttime:endtime,10,idx[i]]**2),'b',lw=1,label='Kelp')
    ax2.grid()
    ax2.set_title('Mid currents at: %d' % (idx[i]))
    ax2.set_ylabel(r'Speed ($\frac{m}{s}$)')
    handles, labels = ax2.get_legend_handles_labels()
    ax2.legend(handles[::-1], labels[::-1])
    
    ax3.plot(data1['time'][starttime:endtime],np.sqrt(data1['u'][starttime:endtime,19,idx[i]]**2+data1['v'][starttime:endtime,19,idx[i]]**2),'r',lw=2,label='No kelp')
    ax3.plot(data1['time'][starttime:endtime],np.sqrt(data2['u'][starttime:endtime,19,idx[i]]**2+data2['v'][starttime:endtime,19,idx[i]]**2),'b',lw=1,label='Kelp')
    ax3.grid()
    ax3.set_title('Bottom currents at: %d' % (idx[i]))
    ax3.set_ylabel(r'Speed ($\frac{m}{s}$)')
    handles, labels = ax3.get_legend_handles_labels()
    ax3.legend(handles[::-1], labels[::-1])
    
    #f.savefig(savepath + grid + '_' +name1+ '_'+name2+'_currents_at_' +("%d"%idx[i])+ '.png',dpi=1200)


# In[ ]:




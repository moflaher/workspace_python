from __future__ import division
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
from misctools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import scipy.signal as spsig

# Define names and types of data
name='kit4_kelp_20m_drag_0.018_2d_5min'
grid='kit4_kelp'
datatype='2d'
starttime=4608
endtime=starttime+1225#5503
regionname='douglas'



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

region=regions(regionname)

savepath='figures/png/' + grid + '_' + datatype + '/slacktide_offset/'
if not os.path.exists(savepath): os.makedirs(savepath)


refloc={}
refloc['region']=np.array([-128.69,-128.69,53.95,53.95])
refloc=expand_region(refloc,[1000])
newloc={}
newloc['region']=np.array([-128.83,-128.83,53.59,53.59])
newloc=expand_region(newloc,[1500])



refeidx=get_elements(data,refloc)
neweidx=get_elements(data,newloc)
nidx=get_nodes(data,region)



#f=plt.figure()
#ax=f.add_axes([.125,.1,.775,.8])
#ax.triplot(data['trigrid'],lw=.15)
#plot_box(ax,refloc,'r',1.5)
#plot_box(ax,newloc,'b',1.5)
#prettyplot_ll(ax,setregion=region)
#f.savefig(savepath + grid + '_' +name+ '_'+regionname +'_slacktide_offset_locations.png',dpi=600)
#plt.close(f)



refspeed=speeder(data['ua'][starttime:endtime,refeidx],data['va'][starttime:endtime,refeidx])
newspeed=speeder(data['ua'][starttime:endtime,neweidx],data['va'][starttime:endtime,neweidx])
rzeta=data['zeta'][starttime:endtime,nidx].mean(axis=1)
time=(data['time'][starttime:endtime]-data['time'][starttime])*24*60

f=plt.figure()
ax=f.add_axes([.125,.335,.775,.6])
ax.plot(time,refspeed.mean(axis=1),'r',label=r'Mean Kitimat Speed')
ax.plot(time,newspeed.mean(axis=1),'b',label=r'Mean Sill Speed')
ax.plot(time,refspeed.max(axis=1),'r--',label=r'Max Kitimat Speed')
ax.plot(time,newspeed.max(axis=1),'b--',label=r'Max Sill Speed')
ax.legend(fontsize=6)
ax.grid()
ax.set_xlabel(r'Time (minutes)')
ax.set_ylabel(r'Speed (m/s)')


ax1=f.add_axes([.125,.05,.775,.2])
ax1.plot(time,rzeta,'k',label=r'Mean Elevation')
ax1.axhline(y=0,color='k')
ax1.xaxis.set_tick_params(labelbottom='off')
ax1.grid()
ax1.legend(fontsize=6)
ax1.set_ylabel(r'Elevation (m)')

f.savefig(savepath + grid + '_' +name+ '_'+regionname +'_slacktide_offset_speeds_in_boxes.png',dpi=600)
plt.close(f)



refms=refspeed.max(axis=1)
newms=newspeed.max(axis=1)


reftide=spsig.argrelmax(-refms,order=5)[0]
newtide=spsig.argrelmax(-newms,order=5)[0]








minlen=np.min([len(reftide),len(newtide)])
print (newtide[0:minlen]-reftide[0:minlen])*(np.diff(data['time'])[0])*24*60


for idx in newtide:
    print newms[(idx-6):(idx+6)].max()























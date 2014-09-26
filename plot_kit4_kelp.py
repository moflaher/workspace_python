from __future__ import division
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import scipy.io as sio
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
from StringIO import StringIO
from gridtools import *
from datatools import *
from misctools import *
from plottools import *
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)




# Define names and types of data
name='kit4_kelp_0.05'
grid='kit4'
datatype='2d'


regionA=regions('kit4')
region1=regions('kelpchain')
region2=regions('doubleisland')
regionAf=[-.025,.1,.725,.75]
cbarf=[.1,.95,.45,.025]
region1f=[.565,.075,.375,.415]
region2f=[.39,.55,.575,.32]


### load the .nc file #####
data = loadnc('/media/moe46/My Passport/'+ grid +'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

cages=np.genfromtxt('/media/moe46/My Passport/'+ grid +'/' +name+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)








savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)

#create plot and plot whole sfm grid with contours (make it look like jasons gmt)
f=plt.figure()
ax_all=plt.axes(regionAf)
cax=f.add_axes(cbarf)
maxh=500
trip=ax_all.tripcolor(data['trigrid'],data['h'],vmax=maxh)
#CS=ax_all.tricontour(data['trigrid'],data['h'],np.array([350]),colors='k')
#CS=ax_all.tricontour(data['trigrid'],data['h'],colors='k')
cb=plt.colorbar(trip,cax=cax,orientation='horizontal')
cb.set_label(r'Depth (m)')
for label in cb.ax.get_xticklabels()[::2]:
    label.set_visible(False)
plot_box(ax_all,region1,'g',1.5)
plot_box(ax_all,region2,'g',1.5)
#ax_all.axis(regionA['region'])



#manual_locations = [(-70, 40),(-68.1,42.1),(-69.8,42.35),(-65,42)]
#ax_all.clabel(CS, fontsize=12,fmt='%d', manual=manual_locations,colors='k')
#ax_all.text(-68.5,43,'Gulf of\n Maine',fontsize=14)
#ax_all.text(-69.35,41.85,'Georges Bank',fontsize=14,rotation=35)
#ax_all.text(-69.75,39,'Atlantic Ocean',fontsize=14)
#ax_all.text(-71,45,'A',fontsize=24)
prettyplot_ll(ax_all,setregion=regionA)
#ax_all.yaxis.set_tick_params(labelright='on',labelleft='off')

ax_all.text(-129.1,54.1,'Kitimat',fontsize=8)
ax_all.text(-129.5,53.7,'D.C.',fontsize=8)
ax_all.text(-128.25,53,'British Columbia',fontsize=8)
ax_all.text(-127.9,52.88,'Canada',fontsize=8)

#add bof subplot
axsub1=f.add_axes(region1f)
axsub1.triplot(data['trigrid'],color='black',lw=.2)

axsub1.axis(region1['region'])
axsub1.set_aspect(get_aspectratio(region1))
fix_osw(axsub1)

axsub1lw=.4
for i in cages:
    tnodes=data['nv'][i,:]    
    axsub1.plot(data['nodell'][tnodes[[0,1]],0],data['nodell'][tnodes[[0,1]],1],'r',lw=axsub1lw,label='Mesh')
    axsub1.plot(data['nodell'][tnodes[[1,2]],0],data['nodell'][tnodes[[1,2]],1],'r',lw=axsub1lw,label='Cages')
    axsub1.plot(data['nodell'][tnodes[[0,2]],0],data['nodell'][tnodes[[0,2]],1],'r',lw=axsub1lw)


#axsub1.xaxis.set_tick_params(labeltop='on',labelbottom='off')
axsub1.yaxis.set_tick_params(labelright='on',labelleft='off')
for label in axsub1.get_xticklabels()[::2]:
    label.set_visible(False)
for label in axsub1.get_yticklabels()[::2]:
    label.set_visible(False)

for label in axsub1.get_xticklabels():
    label.set_fontsize(8)
for label in axsub1.get_yticklabels():
    label.set_fontsize(8)


#plot_box(axsub1,region2,'g',1.5)
#axsub1.annotate("",xy=(region2f[0],region2f[1]),xycoords='figure fraction',xytext=(region2['region'][0],region2['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
#axsub1.annotate("",xy=(region2f[0],region2f[1]+region2f[3]),xycoords='figure fraction',xytext=(region2['region'][0],region2['region'][3]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
#axsub1.text(-67,45.65,'New Brunswick',fontsize=18)
#axsub1.text(-67.25,45.25,'Passamaquoddy Bay',fontsize=10)
#axsub1.annotate("",xy=(-67,45.1),xycoords='data',xytext=(-66.75,45.225), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='k',headwidth=3))
#axsub1.text(-65.9,44.65,'Nova Scotia',fontsize=18,rotation=28)
#axsub1.text(-67.5,45.65,'B',fontsize=24)
#axsub1.annotate("",xy=(.475,.14+.415),xycoords='figure fraction',xytext=(-66.9,45), textcoords='data',arrowprops=dict(width=5,facecolor='w',shrink=0))




#add cage subplot
axsub2=f.add_axes(region2f)
axsub2.triplot(data['trigrid'],color='black',lw=.2)

axsub2.axis(region2['region'])
axsub2.set_aspect(get_aspectratio(region2))
fix_osw(axsub2)
#axsub2.xaxis.set_tick_params(labeltop='on',labelbottom='off')
axsub2.yaxis.set_tick_params(labelright='on',labelleft='off')

for label in axsub2.get_xticklabels()[::2]:
    label.set_visible(False)
for label in axsub2.get_yticklabels()[::2]:
    label.set_visible(False)
for label in axsub2.get_xticklabels():
    label.set_fontsize(8)
for label in axsub2.get_yticklabels():
    label.set_fontsize(8)
#label=axsub2.get_yticklabels()[-2]
#label.set_visible(False)

axsub2lw=.2
for i in cages:
    tnodes=data['nv'][i,:]    
    axsub2.plot(data['nodell'][tnodes[[0,1]],0],data['nodell'][tnodes[[0,1]],1],'r',lw=axsub2lw,label='Mesh')
    axsub2.plot(data['nodell'][tnodes[[1,2]],0],data['nodell'][tnodes[[1,2]],1],'r',lw=axsub2lw,label='Cages')
    axsub2.plot(data['nodell'][tnodes[[0,2]],0],data['nodell'][tnodes[[0,2]],1],'r',lw=axsub2lw)





#force draw to get accurate ax bounds
plt.draw()

axsub1bb=axsub1.get_axes().get_position().bounds

ax_all.annotate("",xy=(axsub1bb[0],axsub1bb[1]+axsub1bb[3]),xycoords='figure fraction',xytext=(region1['region'][0],region1['region'][3]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
ax_all.annotate("",xy=(axsub1bb[0],axsub1bb[1]),xycoords='figure fraction',xytext=(region1['region'][0],region1['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))

axsub2bb=axsub2.get_axes().get_position().bounds

ax_all.annotate("",xy=(axsub2bb[0],axsub2bb[1]+axsub2bb[3]),xycoords='figure fraction',xytext=(region2['region'][0],region2['region'][3]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
ax_all.annotate("",xy=(axsub2bb[0],axsub2bb[1]),xycoords='figure fraction',xytext=(region2['region'][0],region2['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))


#plt.plot(data['uvnodell'][cages,0],data['uvnodell'][cages,1],'b.',markersize=2)




plt.savefig(savepath + grid + '_' +name+ '_kit4_kelp_map.png',dpi=600)

plt.close(f)


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


bregion=regions('kit4')
sregion=regions('kelpchain')
cregion=regions('doubleisland')
bregionf=[-.025,.1,.725,.75]
cbarf=[.1,.95,.35,.025]
sregionf=[.575,.075,.375,.415]
cregionf=[.4,.575,.65,.32]


### load the .nc file #####
data = loadnc('/media/moflaher/My Book/'+ grid +'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

cages=np.genfromtxt('/media/moflaher/My Book/'+ grid +'/' +name+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)








savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)

#create plot and plot whole sfm grid with contours (make it look like jasons gmt)
f=plt.figure()
ax_all=plt.axes(bregionf)
cax=f.add_axes(cbarf)
maxh=500
trip=ax_all.tripcolor(data['trigrid'],data['h'],vmax=maxh)
#CS=ax_all.tricontour(data['trigrid'],data['h'],np.array([350]),colors='k')
#CS=ax_all.tricontour(data['trigrid'],data['h'],colors='k')
cb=plt.colorbar(trip,cax=cax,orientation='horizontal')
cb.set_label(r'Depth (m)')
for label in cb.ax.get_xticklabels()[::2]:
    label.set_visible(False)
plot_box(ax_all,sregion,'g',1.5)
#ax_all.axis(bregion['region'])



#manual_locations = [(-70, 40),(-68.1,42.1),(-69.8,42.35),(-65,42)]
#ax_all.clabel(CS, fontsize=12,fmt='%d', manual=manual_locations,colors='k')
#ax_all.text(-68.5,43,'Gulf of\n Maine',fontsize=14)
#ax_all.text(-69.35,41.85,'Georges Bank',fontsize=14,rotation=35)
#ax_all.text(-69.75,39,'Atlantic Ocean',fontsize=14)
#ax_all.text(-71,45,'A',fontsize=24)
#_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
#ax_all.yaxis.set_major_formatter(_formatter)
#ax_all.xaxis.set_major_formatter(_formatter)
prettyplot_ll(ax_all,setregion=bregion)
#ax_all.yaxis.set_tick_params(labelright='on',labelleft='off')

#add bof subplot
ax_bof=f.add_axes(sregionf)
ax_bof.triplot(data['trigrid'],color='black',lw=.2)

ax_bof.axis(sregion['region'])
ax_bof.set_aspect(get_aspectratio(sregion))
_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
ax_bof.yaxis.set_major_formatter(_formatter)
ax_bof.xaxis.set_major_formatter(_formatter)

for i in cages:
    tnodes=data['nv'][i,:]    
    ax_bof.plot(data['nodell'][tnodes[[0,1]],0],data['nodell'][tnodes[[0,1]],1],'r',lw=.6,label='Mesh')
    ax_bof.plot(data['nodell'][tnodes[[1,2]],0],data['nodell'][tnodes[[1,2]],1],'r',lw=.6,label='Cages')
    ax_bof.plot(data['nodell'][tnodes[[0,2]],0],data['nodell'][tnodes[[0,2]],1],'r',lw=.6,label='Single Cage')


#ax_bof.xaxis.set_tick_params(labeltop='on',labelbottom='off')
ax_bof.yaxis.set_tick_params(labelright='on',labelleft='off')
for label in ax_bof.get_xticklabels()[::2]:
    label.set_visible(False)
for label in ax_bof.get_yticklabels()[::2]:
    label.set_visible(False)
#plot_box(ax_bof,cregion,'g',1.5)
#ax_bof.annotate("",xy=(cregionf[0],cregionf[1]),xycoords='figure fraction',xytext=(cregion['region'][0],cregion['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
#ax_bof.annotate("",xy=(cregionf[0],cregionf[1]+cregionf[3]),xycoords='figure fraction',xytext=(cregion['region'][0],cregion['region'][3]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
#ax_bof.text(-67,45.65,'New Brunswick',fontsize=18)
#ax_bof.text(-67.25,45.25,'Passamaquoddy Bay',fontsize=10)
#ax_bof.annotate("",xy=(-67,45.1),xycoords='data',xytext=(-66.75,45.225), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='k',headwidth=3))
#ax_bof.text(-65.9,44.65,'Nova Scotia',fontsize=18,rotation=28)
#ax_bof.text(-67.5,45.65,'B',fontsize=24)
#ax_bof.annotate("",xy=(.475,.14+.415),xycoords='figure fraction',xytext=(-66.9,45), textcoords='data',arrowprops=dict(width=5,facecolor='w',shrink=0))

ax_all.annotate("",xy=(ax_bof.get_axes().get_position().bounds[0],sregionf[1]+sregionf[3]),xycoords='figure fraction',xytext=(sregion['region'][0],sregion['region'][3]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
ax_all.annotate("",xy=(ax_bof.get_axes().get_position().bounds[0],sregionf[1]),xycoords='figure fraction',xytext=(sregion['region'][0],sregion['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))



#add cage subplot
ax_cages=f.add_axes(cregionf)
ax_cages.triplot(data['trigrid'],color='black',lw=.2)

ax_cages.axis(cregion['region'])
ax_cages.set_aspect(get_aspectratio(cregion))
#ax_cages.xaxis.set_tick_params(labeltop='on',labelbottom='off')
#ax_cages.yaxis.set_tick_params(labelright='on',labelleft='off')
_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
ax_cages.yaxis.set_major_formatter(_formatter)
ax_cages.xaxis.set_major_formatter(_formatter)
for label in ax_cages.get_xticklabels()[::2]:
    label.set_visible(False)
for label in ax_cages.get_yticklabels()[::2]:
    label.set_visible(False)
#label=ax_cages.get_yticklabels()[-2]
#label.set_visible(False)

for i in cages:
    tnodes=data['nv'][i,:]    
    ax_cages.plot(data['nodell'][tnodes[[0,1]],0],data['nodell'][tnodes[[0,1]],1],'r',lw=.6,label='Mesh')
    ax_cages.plot(data['nodell'][tnodes[[1,2]],0],data['nodell'][tnodes[[1,2]],1],'r',lw=.6,label='Cages')
    ax_cages.plot(data['nodell'][tnodes[[0,2]],0],data['nodell'][tnodes[[0,2]],1],'r',lw=.6,label='Single Cage')





#cageposx=np.empty([sortedcages.shape[0],])
#cageposy=np.empty([sortedcages.shape[0],])
#for i in range(0,sortedcages.shape[0]):
#    print i
#    cageposx[i]=np.mean(data['uvnodell'][sortedcages[i,:],0])
#    cageposy[i]=np.mean(data['uvnodell'][sortedcages[i,:],1]) 

#for i in range(0,sortedcages.shape[0]):
#    if i==5:
#        cageposx[i]=cageposx[i]-.005
#    ax_cages.text(cageposx[i],cageposy[i],"%d"%(i+1),fontsize=20,color='g')

#handles, labels = ax_cages.get_legend_handles_labels()
#handles=handles[::-1]
#labels=labels[::-1]

#legend=ax_cages.legend(handles[0:3], labels[0:3],loc=2,prop={'size':8})
#t=legend.get_lines()
#t[2].set_color('black')
#t[0].set_color('b')
#for label in legend.get_lines():
#    label.set_linewidth(1.5)

ax_cages.text(-66.823,45.055,'C',fontsize=24,bbox={'facecolor':'white','edgecolor':'white'})
ax_cages.text(-66.85,45.055,'Frye Island',fontsize=14,rotation=75)





#plt.plot(data['uvnodell'][cages,0],data['uvnodell'][cages,1],'b.',markersize=2)




plt.savefig(savepath + grid + '_' +name+ '_gmt_clone_cage_outline.png',dpi=600)

plt.close(f)


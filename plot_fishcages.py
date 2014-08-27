from __future__ import division
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import scipy.io as sio
from mpl_toolkits.basemap import Basemap
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
name='sfm6_musq2_all_cages'
grid='sfm6_musq2'
datatype='2d'


bregion=regions('sfmwhole')
sregion=regions('bof')
cregion=regions('musq_cage_tight')


### load the .nc file #####
data = loadnc('/media/moflaher/My Book/cages/' + name + '/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

cages=np.genfromtxt('/media/moflaher/My Book/cages/' +name+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)
oldcages=np.genfromtxt('/media/moflaher/My Book/cages/sfm6_musq2_old_cages/input/' +grid+ '_cage.dat',skiprows=1)
oldcages=(oldcages[:,0]-1).astype(int)


savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)

#create plot and plot whole sfm grid with contours (make it look like jasons gmt)
f=plt.figure()
ax_all=plt.axes([.1,.1,.7,.75])
cax=f.add_axes([.85,.1,.025,.425])
trip=ax_all.tripcolor(data['trigrid'],data['h'],vmax=250)
CS=ax_all.tricontour(data['trigrid'],data['h'],np.array([200]),colors='k')
cb=plt.colorbar(trip,cax=cax)
cb.set_label(r'Depth (m)')
plot_box(ax_all,sregion,'g',1.5)
ax_all.annotate("",xy=(.4,.575+.325),xycoords='figure fraction',xytext=(sregion['region'][0],sregion['region'][3]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
ax_all.annotate("",xy=(.4,.575),xycoords='figure fraction',xytext=(sregion['region'][0],sregion['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))


manual_locations = [(-70, 40),(-68.1,42.1),(-69.8,42.35),(-65,42)]
ax_all.clabel(CS, fontsize=12,fmt='%d', manual=manual_locations,colors='k')
ax_all.text(-68.5,43,'Gulf of\n Maine',fontsize=14)
ax_all.text(-69.35,41.85,'Georges Bank',fontsize=14,rotation=35)
ax_all.text(-69.75,39,'Atlantic Ocean',fontsize=14)
ax_all.text(-71,45,'A',fontsize=24)

prettyplot_ll(ax_all)

#add bof subplot
ax_bof=f.add_axes([.4,.575,.5,.325])
ax_bof.tripcolor(data['trigrid'],data['h'],vmax=250)

ax_bof.axis(sregion['region'])
ax_bof.xaxis.set_tick_params(labeltop='on',labelbottom='off')
ax_bof.yaxis.set_tick_params(labelright='on',labelleft='off')
_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
ax_bof.yaxis.set_major_formatter(_formatter)
ax_bof.xaxis.set_major_formatter(_formatter)
plot_box(ax_bof,cregion,'g',1.5)
ax_bof.annotate("",xy=(.45,.14+.415),xycoords='figure fraction',xytext=(cregion['region'][0],cregion['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
ax_bof.annotate("",xy=(.45+.375,.14+.415),xycoords='figure fraction',xytext=(cregion['region'][1],cregion['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
ax_bof.text(-67,45.65,'New Brunswick',fontsize=18)
ax_bof.text(-67.25,45.25,'Passamaquoddy Bay',fontsize=10)
ax_bof.annotate("",xy=(-67,45.1),xycoords='data',xytext=(-66.75,45.225), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='k',headwidth=3))
ax_bof.text(-65.9,44.65,'Nova Scotia',fontsize=18,rotation=28)
ax_bof.text(-67.5,45.65,'B',fontsize=24)
#ax_bof.annotate("",xy=(.475,.14+.415),xycoords='figure fraction',xytext=(-66.9,45), textcoords='data',arrowprops=dict(width=5,facecolor='w',shrink=0))




#add cage subplot
ax_cages=f.add_axes([.45,.14,.375,.415])
ax_cages.triplot(data['trigrid'],color='black',lw=.2)
ax_cages.axis(cregion['region'])
_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
ax_cages.yaxis.set_major_formatter(_formatter)
ax_cages.xaxis.set_major_formatter(_formatter)
for label in ax_cages.get_xticklabels()[::2]:
    label.set_visible(False)
for label in ax_cages.get_yticklabels()[::2]:
    label.set_visible(False)
label=ax_cages.get_yticklabels()[-2]
label.set_visible(False)

for i in cages:
    tnodes=data['nv'][i,:]    
    ax_cages.plot(data['nodell'][tnodes[[0,1]],0],data['nodell'][tnodes[[0,1]],1],'r',lw=.6,label='Mesh')
    ax_cages.plot(data['nodell'][tnodes[[1,2]],0],data['nodell'][tnodes[[1,2]],1],'r',lw=.6,label='Cages')
    ax_cages.plot(data['nodell'][tnodes[[0,2]],0],data['nodell'][tnodes[[0,2]],1],'r',lw=.6,label='Single Cage')

for i in oldcages:
    tnodes=data['nv'][i,:]    
    ax_cages.plot(data['nodell'][tnodes[[0,1]],0],data['nodell'][tnodes[[0,1]],1],'b',lw=.6)
    ax_cages.plot(data['nodell'][tnodes[[1,2]],0],data['nodell'][tnodes[[1,2]],1],'b',lw=.6)
    ax_cages.plot(data['nodell'][tnodes[[0,2]],0],data['nodell'][tnodes[[0,2]],1],'b',lw=.6)

handles, labels = ax_cages.get_legend_handles_labels()
handles=handles[::-1]
labels=labels[::-1]

legend=ax_cages.legend(handles[0:3], labels[0:3],loc=2,prop={'size':8})
t=legend.get_lines()
t[2].set_color('black')
t[0].set_color('b')
for label in legend.get_lines():
    label.set_linewidth(1.5)

ax_cages.text(-66.823,45.055,'C',fontsize=24,bbox={'facecolor':'white','edgecolor':'white'})
ax_cages.text(-66.85,45.055,'Frye Island',fontsize=14,rotation=75)





#plt.plot(data['uvnodell'][cages,0],data['uvnodell'][cages,1],'b.',markersize=2)




plt.savefig(savepath + grid + '_' +name+ '_gmt_clone_cage_outline.png',dpi=1200)


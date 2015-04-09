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
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC



# Define names and types of data
name='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'
datatype='2d'


regionA=regions('kit4')
region1=regions('kelpchain')
region2=regions('doubleisland')
region3=regions('kit4_kelpfield')
regionAf=[.09,.1,.725,.75]
cbarf=[.1,.95,.45,.025]
region1f=[.405,.06,.375,.415]
region2f=[.315,.55,.575,.32]
region3f=[.6815,.0115,.275,.55]


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

cages=np.genfromtxt('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)








savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)


###############################################################################
#create plot and plot whole grid 
###############################################################################
f=plt.figure()
ax_all=plt.axes(regionAf)
cax=f.add_axes(cbarf)
maxh=500
trip=ax_all.tripcolor(data['trigrid'],data['h'],vmax=maxh)
cb=plt.colorbar(trip,cax=cax,orientation='horizontal')
cb.set_label(r'Depth (m)')
for label in cb.ax.get_xticklabels()[::2]:
    label.set_visible(False)
plot_box(ax_all,region1,'g',1.5)
plot_box(ax_all,region2,'g',1.5)
prettyplot_ll(ax_all,setregion=regionA)


#ax_all.text(-129.1,54.1,'Kitimat',fontsize=8)
ax_all.text(-129.24,53.58,'Douglas',fontsize=4,rotation=90)
ax_all.text(-129.2,53.76,'Channel',fontsize=4,rotation=39)
#ax_all.text(-128.25,53,'British Columbia',fontsize=8)
#ax_all.text(-127.9,52.88,'Canada',fontsize=8)
ax_all.text(-131.3,53.1,'Hecate Strait',fontsize=8,rotation=-55)


_formatter = mpl.ticker.FormatStrFormatter("%3.0f")
ax_all.xaxis.set_major_formatter(_formatter)


###############################################################################
#add kelp chain subplot
###############################################################################
axsub1=f.add_axes(region1f)
axsub1.triplot(data['trigrid'],color='black',lw=.075)

locations=[11974,11418]
labelstr=['1','2']
arrows=[(.8,.65),(.85,.55)]
#for j in range(0,len(locations)):
#    axsub1.annotate(labelstr[j],xy=(data['uvnodell'][locations[j],0],data['uvnodell'][locations[j],1]),xycoords='data',xytext=arrows[j], textcoords='axes fraction',arrowprops=dict(width=2,facecolor='w',shrink=0))

axsub1.axis(region1['region'])
axsub1.set_aspect(get_aspectratio(region1))
fix_osw(axsub1)

plotcoast(axsub1,filename='pacific.nc',color='0.75',fill=True)

arrow=dict(arrowstyle='|-|,widthA=.25,widthB=.25',color='k',connectionstyle="angle,rad=0")
axsub1.annotate(r'5 km',xy=(region1['region'][0]+.02,region1['region'][2]+.02),xycoords='data',xytext=(region1['region'][0]+ll_dist(region1,5000)+.02,region1['region'][2]+.02), textcoords='data',fontsize=6,arrowprops=arrow)


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

axsub1.text(-129.2725,52.775,'Aristazabal',fontsize=6,rotation=-45)
axsub1.text(-129.2725,52.755,'Island',fontsize=6,rotation=-45)
axsub1.text(-129.39,52.675,'Moore Islands',fontsize=6,rotation=0,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3})
axsub1.text(-129.53,52.78,'Rennison Island',fontsize=6,rotation=0,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3})
axsub1.text(-129.53,52.5,'Conroy Island',fontsize=6,rotation=0,bbox={'facecolor':'white','edgecolor':'None','alpha':1, 'pad':3})
axsub1.text(-129.4,52.485,'Harvey Island',fontsize=6,rotation=0,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3})





###############################################################################
#add doubleisland subplot
###############################################################################
axsub2=f.add_axes(region2f)
axsub2.triplot(data['trigrid'],color='black',lw=.1)

locations=[119754,118418]
labelstr=['1','2']
arrows=[(.45,.365),(.85,.325)]

axsub2.axis(region2['region'])
axsub2.set_aspect(get_aspectratio(region2))
fix_osw(axsub2)

plotcoast(axsub2,filename='pacific.nc',color='0.75',fill=True)

arrow=dict(arrowstyle='|-|,widthA=.25,widthB=.25',color='k',connectionstyle="angle,rad=0")
axsub2.annotate(r'5 km',xy=(region2['region'][0]+.02,region2['region'][2]+.02),xycoords='data',xytext=(region2['region'][0]+ll_dist(region2,5000)+.02,region2['region'][2]+.02), textcoords='data',fontsize=6,arrowprops=arrow)

axsub2.yaxis.set_tick_params(labelright='on',labelleft='off')

for label in axsub2.get_xticklabels()[::2]:
    label.set_visible(False)
for label in axsub2.get_yticklabels()[::2]:
    label.set_visible(False)
for label in axsub2.get_xticklabels():
    label.set_fontsize(8)
for label in axsub2.get_yticklabels():
    label.set_fontsize(8)

axsub2.text(-129.5,53.125,'Campania Island',fontsize=8,rotation=-40)
axsub2.text(-129.6,53.1175,'Estevan Sound',fontsize=8,rotation=-40)
axsub2.text(-129.715,53.11,'Estevan Group',fontsize=8,rotation=-40)
axsub2.text(-129.775,53.20,'Banks Island',fontsize=6,rotation=0,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3})
axsub2.text(-129.715,53.16,'Otter Passage',fontsize=5,rotation=0,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3})





###############################################################################
#add kelpfield subplot
###############################################################################
axsub3=f.add_axes(region3f)
axsub3.triplot(data['trigrid'],color='black',lw=.1)

#locations=[119754,118418]
#labelstr=['1','2']
#arrows=[(.45,.365),(.85,.325)]

axsub3.axis(region3['region'])
axsub3.set_aspect(get_aspectratio(region3))
fix_osw(axsub3)

plotcoast(axsub3,filename='pacific.nc',color='0.75',fill=True)

arrow=dict(arrowstyle='|-|,widthA=.25,widthB=.25',color='k',connectionstyle="angle,rad=0")
axsub3.annotate(r'200 m',xy=(region3['region'][0]+.002,region3['region'][2]+.002),xycoords='data',xytext=(region3['region'][0]+ll_dist(region3,200)+.002,region3['region'][2]+.002), textcoords='data',fontsize=6,arrowprops=arrow)

axsub3.yaxis.set_tick_params(labelright='on',labelleft='off')
axsub3.xaxis.set_tick_params(labeltop='on',labelbottom='off')

for label in axsub3.get_xticklabels()[::2]:
    label.set_visible(False)
for label in axsub3.get_yticklabels()[::2]:
    label.set_visible(False)
for label in axsub3.get_xticklabels():
    label.set_fontsize(8)
for label in axsub3.get_yticklabels():
    label.set_fontsize(8)

_formatter2 = mpl.ticker.FormatStrFormatter("%.2f")
axsub3.yaxis.set_major_formatter(_formatter2)





###############################################################################
#force draw to get accurate ax bounds
###############################################################################
plt.draw()

axsub1bb=axsub1.get_axes().get_position().bounds
ax_all.annotate("",xy=(axsub1bb[0],axsub1bb[1]+axsub1bb[3]),xycoords='figure fraction',xytext=(region1['region'][0],region1['region'][3]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
ax_all.annotate("",xy=(axsub1bb[0],axsub1bb[1]),xycoords='figure fraction',xytext=(region1['region'][0],region1['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))

axsub2bb=axsub2.get_axes().get_position().bounds
ax_all.annotate("",xy=(axsub2bb[0],axsub2bb[1]+axsub2bb[3]),xycoords='figure fraction',xytext=(region2['region'][0],region2['region'][3]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
ax_all.annotate("",xy=(axsub2bb[0],axsub2bb[1]),xycoords='figure fraction',xytext=(region2['region'][0],region2['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))

axsub3bb=axsub3.get_axes().get_position().bounds
tmp=axsub1.annotate("",xy=(axsub3bb[0],axsub3bb[1]+axsub3bb[3]),xycoords='figure fraction',xytext=(region3['region'][0],region3['region'][3]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
tmp.set_zorder(40)
tmp=axsub1.annotate("",xy=(axsub3bb[0],axsub3bb[1]),xycoords='figure fraction',xytext=(region3['region'][0],region3['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
tmp.set_zorder(40)


ax_all.annotate("A",xy=(.025,.95),xycoords='axes fraction')
axsub1.annotate("C",xy=(.025,.925),xycoords='axes fraction')
axsub2.annotate("B",xy=(.025,.9),xycoords='axes fraction')
axsub3.annotate("D",xy=(.025,.925),xycoords='axes fraction')


###############################################################################
#add region boxes
###############################################################################
rn=regions('kit4_kelp_tight5')
plot_box(axsub1,rn,'r',1.5)
aa=axsub1.text(rn['center'][0],rn['center'][1],'R1',fontsize=12,rotation=0,color='r')

rn=regions('kit4_kelp_tight2_small')
plot_box(axsub1,rn,'r',1.5)
axsub1.text(rn['center'][0],rn['center'][1],'R2',fontsize=12,rotation=0,color='r')
plot_box(axsub1,region3,'g',1.5)

#rn=regions('kit4_kelp_tight6')
#plot_box(axsub1,rn,'k',1.5)
#axsub1.text(rn['center'][0],rn['center'][1],'R3',fontsize=12,rotation=0,color='k')

#rn=regions('kit4_crossdouble')
#plot_box(axsub2,rn,'r',1.5)
#axsub2.text(rn['center'][0],rn['center'][1],'R3',fontsize=12,rotation=0,color='r')

#rn=regions('kit4_ftb')
#plot_box(axsub2,rn,'r',1.5)
#axsub2.text(rn['center'][0],rn['center'][1],'R4',fontsize=12,rotation=0,color='r')


###############################################################################
#add kelp
###############################################################################
tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2]],0],data['nodell'][data['nv'][i,[0,1,2]],1])) for i in cages ]
lsega=PC(tmparray,facecolor = 'g',edgecolor='None')
lseg1=PC(tmparray,facecolor = 'g',edgecolor='None')
lseg2=PC(tmparray,facecolor = 'g',edgecolor='None')
lseg3=PC(tmparray,facecolor = 'g',edgecolor='None')

ax_all.add_collection(lsega)
axsub1.add_collection(lseg1)
axsub2.add_collection(lseg2)
axsub3.add_collection(lseg3)


plt.savefig(savepath + grid + '_' +name+ '_kit4_kelp_map.png',dpi=600)

plt.close(f)


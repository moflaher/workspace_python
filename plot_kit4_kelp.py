from __future__ import division,print_function
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
from projtools import *
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
region2=regions('kit4_kelp_tight5')
region3=regions('kit4_kelp_tight2_kelpfield')
regionAf=[.09,.1,.725,.75]
cbarf=[.885,.1,.025,.8]
region1f=[.19,.55,.31,.415]
region2f=[.36,.035,.575,.39]
region3f=[.535,.4575,.275,.5]


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

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
cb=plt.colorbar(trip,cax=cax,orientation='vertical')
cb.set_label(r'Depth (m)')
for label in cb.ax.get_xticklabels()[::2]:
    label.set_visible(False)
plot_box(ax_all,region1,'g',1.5)
#plot_box(ax_all,region2,'g',1.5)
_formatter = mpl.ticker.FormatStrFormatter("%3.0f")
ax_all.xaxis.set_major_formatter(_formatter)
prettyplot_ll(ax_all,setregion=regionA)


a=ax_all.text(-128.5,53.905,'Kitimat',fontsize=8)
a.set_zorder(100)
#ax_all.text(-129.24,53.58,'Douglas',fontsize=4,rotation=90)
#ax_all.text(-129.2,53.76,'Channel',fontsize=4,rotation=39)
#ax_all.text(-128.25,53,'British Columbia',fontsize=8)
#ax_all.text(-127.9,52.88,'Canada',fontsize=8)
ax_all.text(-131.3,53.1,'Hecate Strait',fontsize=8,rotation=-55)





###############################################################################
#add kelp chain subplot
###############################################################################
axsub1=f.add_axes(region1f)
axsub1.triplot(data['trigrid'],color='black',lw=.075)

axsub1.axis(region1['region'])
axsub1.set_aspect(get_aspectratio(region1))
fix_osw(axsub1)

plotcoast(axsub1,filename='pacific.nc',color='0.75',fill=True)

axsub1.xaxis.set_tick_params(labeltop='on',labelbottom='off')
#axsub1.yaxis.set_tick_params(labelright='on',labelleft='off')
for label in axsub1.get_xticklabels()[::2]:
    label.set_visible(False)
for label in axsub1.get_yticklabels()[1::2]:
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

axsub2.text(-129.4275,52.5175,'1',fontsize=8,rotation=0,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3})
axsub2.plot([-129.422344,-129.415837],[52.511620,52.520465],'r',lw=3)
axsub2.text(-129.39,52.525,'2',fontsize=8,rotation=0,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3})
axsub2.plot([-129.382917,-129.403779],[52.520149,52.520465],'r',lw=3)

lons=np.array([-129.44])
lats=np.array([52.5475])

savedic={}
savedic['elements']=np.empty(shape=lats.shape)
for i in range(len(lats)):
    meter_box(axsub2,[lons[i],lats[i]],[250,150],lw=2,color='r')

axsub2.axis(region2['region'])
axsub2.set_aspect(get_aspectratio(region2))
fix_osw(axsub2)

plotcoast(axsub2,filename='pacific.nc',color='0.75',fill=True)

axsub2.yaxis.set_tick_params(labelright='on',labelleft='off')

for label in axsub2.get_xticklabels()[::2]:
    label.set_visible(False)
for label in axsub2.get_yticklabels()[::2]:
    label.set_visible(False)
for label in axsub2.get_xticklabels():
    label.set_fontsize(8)
for label in axsub2.get_yticklabels():
    label.set_fontsize(8)

#axsub2.text(-129.5,53.125,'Campania Island',fontsize=8,rotation=-40)
#axsub2.text(-129.6,53.1175,'Estevan Sound',fontsize=8,rotation=-40)
#axsub2.text(-129.715,53.11,'Estevan Group',fontsize=8,rotation=-40)
#axsub2.text(-129.775,53.20,'Banks Island',fontsize=6,rotation=0,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3})
#axsub2.text(-129.715,53.16,'Otter Passage',fontsize=5,rotation=0,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3})





###############################################################################
#add kelpfield subplot
###############################################################################
axsub3=f.add_axes(region3f)
axsub3.triplot(data['trigrid'],color='black',lw=.1)

#lons=np.array([-129.4885,-129.4875,-129.489])
#lats=np.array([52.664,52.651,52.638])
lons=np.array([-129.4875])#,-129.489])
lats=np.array([52.651])#,52.638])

for i in range(len(lats)):
    meter_box(axsub3,[lons[i],lats[i]],100,lw=2,color='r')

locx=[-129.4875,-129.49535]#,-129.475]
locy=[52.65,52.6485]#,52.65]

#axsub3.plot(locx,locy,'*r',markersize=10)


rn={}
rn['region']=np.array([-129.492, -129.479,52.6375,52.655])
rn['center']=[(rn['region'][0]+rn['region'][1])/2,(rn['region'][2]+rn['region'][3])/2]
plot_box(axsub3,rn,'b',1.5)
aa=axsub3.text(rn['center'][0],rn['center'][1],'1',fontsize=12,rotation=0,color='b')

rn={}
rn['region']=np.array([-129.499, -129.494,52.651,52.6551])
rn['center']=[(rn['region'][0]+rn['region'][1])/2,(rn['region'][2]+rn['region'][3])/2]
plot_box(axsub3,rn,'b',1.5)
aa=axsub3.text(rn['center'][0],rn['center'][1],'2',fontsize=12,rotation=0,color='b')

rn={}
rn['region']=np.array([-129.49, -129.48,52.6575,52.665])
rn['center']=[(rn['region'][0]+rn['region'][1])/2,(rn['region'][2]+rn['region'][3])/2]
plot_box(axsub3,rn,'b',1.5)
aa=axsub3.text(rn['center'][0],rn['center'][1],'3',fontsize=12,rotation=0,color='b')

rn={}
rn['region']=np.array([-129.474, -129.465,52.6475,52.655])
rn['center']=[(rn['region'][0]+rn['region'][1])/2,(rn['region'][2]+rn['region'][3])/2]
plot_box(axsub3,rn,'b',1.5)
aa=axsub3.text(rn['center'][0],rn['center'][1],'4',fontsize=12,rotation=0,color='b')


xx=np.empty((100,1))-129.471
yy=np.linspace(52.645,52.656,100)
axsub3.plot(xx,yy,color='m',lw=3)
 

axsub3.axis(region3['region'])
axsub3.set_aspect(get_aspectratio(region3))
_formatter2 = mpl.ticker.FormatStrFormatter("%.3f")
axsub3.yaxis.set_major_formatter(_formatter2)
fix_osw(axsub3)

plotcoast(axsub3,filename='pacific.nc',color='0.75',fill=True)

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







###############################################################################
#force draw to get accurate ax bounds
###############################################################################
plt.draw()

axsub1bb=axsub1.get_axes().get_position().bounds
ax_all.annotate("",xy=(axsub1bb[0]+axsub1bb[2],axsub1bb[1]),xycoords='figure fraction',xytext=(region1['region'][1],region1['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
ax_all.annotate("",xy=(axsub1bb[0],axsub1bb[1]),xycoords='figure fraction',xytext=(region1['region'][0],region1['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))

axsub2bb=axsub2.get_axes().get_position().bounds
axsub1.annotate("",xy=(axsub2bb[0]+axsub2bb[2],axsub2bb[1]+axsub2bb[3]),xycoords='figure fraction',xytext=(region2['region'][1],region2['region'][3]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
axsub1.annotate("",xy=(axsub2bb[0],axsub2bb[1]),xycoords='figure fraction',xytext=(region2['region'][0],region2['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))

axsub3bb=axsub3.get_axes().get_position().bounds
tmp=axsub1.annotate("",xy=(axsub3bb[0],axsub3bb[1]+axsub3bb[3]),xycoords='figure fraction',xytext=(region3['region'][0],region3['region'][3]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
tmp.set_zorder(40)
tmp=axsub1.annotate("",xy=(axsub3bb[0],axsub3bb[1]),xycoords='figure fraction',xytext=(region3['region'][0],region3['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
tmp.set_zorder(40)


scalebar(axsub1,region1,5000,fontsize=6,label='5 km',drawn=True)
scalebar(axsub2,region2,2000,fontsize=6,label='2 km',drawn=True)
scalebar(axsub3,region3,300,fontsize=6,label='300 m',drawn=True)
axes_label(ax_all,"A",drawn=True)
axes_label(axsub1,"B",drawn=True)
axes_label(axsub2,"C",drawn=True)
axes_label(axsub3,"D",drawn=True)


###############################################################################
#add region boxes
###############################################################################
rn=regions('kit4_kelp_tight5')
plot_box(axsub1,rn,'g',1.5)
#plot_box(ax_all,region2,'g',1.5)
aa=axsub1.text(rn['center'][0],rn['center'][1],'R1',fontsize=12,rotation=0,color='r')

rn=regions('kit4_kelp_tight2_small')
plot_box(axsub1,rn,'g',1.5)
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


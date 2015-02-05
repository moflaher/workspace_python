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
name='sfm6_musq_obc_aug122009_slrmod2'
grid='sfm6_musq'
datatype='2d'


bregion=regions('sfmwhole_l')
subregion=regions('slr_upperbof')

### load the .nc file #####
data = loadnc('runs/misc/sealevelrise/',singlename='sfm6e_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

neifile=loadnei('runs/misc/sealevelrise/sfm6e.nei')


data['nodell']=neifile['nodell']
data['lon']=neifile['nodell'][:,0]
data['lat']=neifile['nodell'][:,1]
data['trigrid'] = mplt.Triangulation(data['lon'], data['lat'],data['nv'])

savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)

#create plot and plot whole sfm grid with contours (make it look like jasons gmt)
f=plt.figure()
ax_all=plt.axes([.075,.1,.7,.75])

trip=ax_all.tripcolor(data['trigrid'],data['h'],vmax=250)
CS=ax_all.tricontour(data['trigrid'],data['h'],np.array([200]),colors='k')
manual_locations = [(-70, 40),(-68.1,42.1),(-69.8,42.35),(-65,42)]
ax_all.clabel(CS, fontsize=12,fmt='%d', manual=manual_locations,colors='k')

cbarf=[.075,.95,.7,.025]
cax=f.add_axes(cbarf)
cb=plt.colorbar(trip,cax=cax,orientation='horizontal')
cb.set_label(r'Depth (m)')

markers=np.genfromtxt('data/misc/slr_base/tide_station_ll.dat')
ax_all.plot(markers[:,0],markers[:,1],'k.')
#ax_all.grid()

prettyplot_ll(ax_all)#,cb=trip,cblabel=r'Depth (m)')
ax_all.axis(bregion['region'])


textcolor='w'

ax_all.text(-67.25,45.15,'Bay of Fundy',fontsize=10,color=textcolor,rotation=35)
ax_all.text(-61.9,44.75,'Scotian Shelf',fontsize=12,color=textcolor,rotation=15)
ax_all.text(-68.5,43,'Gulf of\n Maine',fontsize=14,color=textcolor)
ax_all.text(-69.35,41.85,'Georges Bank',fontsize=12,color=textcolor,rotation=35)
ax_all.text(-69.75,39,'Atlantic Ocean',fontsize=14,color=textcolor)


#ax_all.text(-64.25,45.,'Halifax',fontsize=10,color=textcolor,rotation=25)
#ax_all.text(-64.4,45.475,'Minas Passage',fontsize=6,color=textcolor)
#ax_all.text(-63.25,45.3,'Minas Basin',fontsize=6,color=textcolor)
ax_all.text(-67.5,45.35,'St. John',fontsize=10,color=textcolor)

_formatter = mpl.ticker.FormatStrFormatter("%3.0f")
ax_all.xaxis.set_major_formatter(_formatter)

plotcoast(ax_all,filename='mid_nwatl6b.nc',fill=True,lw=.25)




ax_upperbof=plt.axes([.53,.05,.4,.6])
ax_upperbof.tripcolor(data['trigrid'],data['h'],vmax=250)
ax_upperbof.plot(markers[:,0],markers[:,1],'k.')
prettyplot_ll(ax_upperbof,setregion=subregion)



ax_upperbof.set_xlabel('')
ax_upperbof.set_ylabel('')
ax_upperbof.yaxis.set_tick_params(labelright='on',labelleft='off')
#ax_upperbof.xaxis.set_tick_params(labeltop='on',labelbottom='off')
for label in ax_upperbof.get_xticklabels()[::2]:
    label.set_visible(False)
for label in ax_upperbof.get_yticklabels()[::2]:
    label.set_visible(False)
#ax_upperbof.axis(subregion['region'])

#ax_upperbof.text(-64,44.75,'Halifax',fontsize=10,color=textcolor)
#ax_upperbof.text(-64.4,45.475,'Minas Passage',fontsize=8,color=textcolor)
#ax_upperbof.text(-63.75,45.25,'Minas Basin',fontsize=8,color=textcolor)

ax_upperbof.annotate("Minas Passage",xy=(-64.4,45.35),xycoords='data',xytext=(-64.25,45.45), textcoords='data',arrowprops=dict(width=.5,shrink=0,color=textcolor,headwidth=3),color=textcolor,fontsize=8)
ax_upperbof.annotate("Minas Basin",xy=(-64.15,45.3),xycoords='data',xytext=(-65,44.85), textcoords='data',arrowprops=dict(width=.5,shrink=0,color=textcolor,headwidth=3),color=textcolor,fontsize=8)
ax_upperbof.annotate("Halifax",xy=(-63.6,44.7),xycoords='data',xytext=(-63.75,45.0), textcoords='data',arrowprops=dict(width=.5,shrink=0,color=textcolor,headwidth=3),color=textcolor,fontsize=8)

plotcoast(ax_upperbof,filename='mid_nwatl6b.nc',fill=True,lw=.25)




plt.draw()
region1=subregion

plot_box(ax_all,region1,'g',1.5)
axsub1bb=ax_upperbof.get_axes().get_position().bounds
ax_all.annotate("",xy=(axsub1bb[0]+axsub1bb[2],axsub1bb[1]+axsub1bb[3]),xycoords='figure fraction',xytext=(region1['region'][1],region1['region'][3]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
ax_all.annotate("",xy=(axsub1bb[0],axsub1bb[1]),xycoords='figure fraction',xytext=(region1['region'][0],region1['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))



#f.show()
f.savefig(savepath + grid + '_' +name+ '_bof_sub.png',dpi=300)

plt.close(f)



















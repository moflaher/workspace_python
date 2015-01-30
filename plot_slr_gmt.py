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


bregion=regions('sfmwhole')


### load the .nc file #####
data = loadnc('/mnt/old_home/chaffey/sealevelrise/',singlename='sfm6e_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

neifile=loadnei('/mnt/old_home/chaffey/sealevelrise/sfm6e.nei')


data['nodell']=neifile['nodell']
data['lon']=neifile['nodell'][:,0]
data['lat']=neifile['nodell'][:,1]
data['trigrid'] = mplt.Triangulation(data['lon'], data['lat'],data['nv'])

savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)

#create plot and plot whole sfm grid with contours (make it look like jasons gmt)
f=plt.figure()
ax_all=plt.axes([.125,.1,.775,.8])

trip=ax_all.tripcolor(data['trigrid'],data['h'],vmax=250)
CS=ax_all.tricontour(data['trigrid'],data['h'],np.array([200]),colors='k')
manual_locations = [(-70, 40),(-68.1,42.1),(-69.8,42.35),(-65,42)]
ax_all.clabel(CS, fontsize=12,fmt='%d', manual=manual_locations,colors='k')
#ax_all.triplot(data['trigrid'],lw=.2)
#S=ax_all.tricontour(data['trigrid'],data['h'],np.array([200]),colors='k')

#ax_all.grid()
#cb.set_label(r'Depth (m)')
#plot_box(ax_all,sregion,'g',1.5)
#ax_all.annotate("",xy=(.4,.575+.325),xycoords='figure fraction',xytext=(sregion['region'][0],sregion['region'][3]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
#ax_all.annotate("",xy=(.4,.575),xycoords='figure fraction',xytext=(sregion['region'][0],sregion['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))

prettyplot_ll(ax_all,cb=trip,cblabel=r'Depth (m)')

#plt.draw()
#ax_allbb=ax_all.get_axes().get_position().bounds
#cax=f.add_axes([ax_allbb[0]+.025+ax_allbb[2],ax_allbb[1],.025,ax_allbb[3]])
#cb=plt.colorbar(trip,cax=cax)

#manual_locations = [(-70, 40),(-68.1,42.1),(-69.8,42.35),(-65,42)]
#ax_all.clabel(CS, fontsize=12,fmt='%d', manual=manual_locations,colors='k')

textcolor='w'
#ax_all.text(-69,42.75,'Gulf of\n Maine',fontsize=10,color=textcolor)
#ax_all.text(-69.1,41.6,'Georges Bank',fontsize=10,color=textcolor,rotation=17.5)
ax_all.text(-67.25,45.15,'Bay of Fundy',fontsize=10,color=textcolor,rotation=35)
ax_all.text(-62.5,43.75,'Scotian Shelf',fontsize=10,color=textcolor,rotation=20)
#ax_all.text(-69.5,39,'Atlantic Ocean',fontsize=10,color=textcolor)

ax_all.text(-68.5,43,'Gulf of\n Maine',fontsize=14,color=textcolor)
ax_all.text(-69.35,41.85,'Georges Bank',fontsize=14,color=textcolor,rotation=35)
ax_all.text(-69.75,39,'Atlantic Ocean',fontsize=14,color=textcolor)
#ax_all.text(-71,45,'A',fontsize=24)
plotcoast(ax_all,fill=True)



markers=np.genfromtxt('data/misc/slr_base/tide_station_ll.dat')



#markers=np.append(np.array([[-70.08004231, -69.64633286, -69.24435825, -68.7577574 ,
#       -68.32404795, -67.85860367, -67.31911142, -66.97002821, -66.4622708 ],
#       [ 42.90267176,  43.0629771 ,  43.26908397,  43.53244275,
#         43.73854962,  43.96755725,  44.17366412,  44.39122137,
#         44.70038168]]),markers)


ax_all.plot(markers[:,0],markers[:,1],'k.')


plt.savefig(savepath + grid + '_' +name+ '_bof.png',dpi=1200)


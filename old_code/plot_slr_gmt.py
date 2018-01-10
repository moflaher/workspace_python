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
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)




# Define names and types of data
name='sfm6_musq_obc_aug122009_slrmod2'
grid='sfm6_musq'
datatype='2d'


bregion=regions('sfmwhole')


### load the .nc file #####
data = loadnc('runs/misc/sealevelrise/',singlename='sfm6e_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

neifile=loadnei('runs/misc/sealevelrise/sfm6e.nei')


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

markers=np.genfromtxt('data/misc/slr_base/tide_station_ll.dat')
ax_all.plot(markers[:,0],markers[:,1],'k.')
#ax_all.grid()

prettyplot_ll(ax_all,cb=trip,cblabel=r'Depth (m)')
ax_all.axis(bregion['region'])


textcolor='w'

ax_all.text(-67.25,45.15,'Bay of Fundy',fontsize=10,color=textcolor,rotation=35)
ax_all.text(-62.5,43.75,'Scotian Shelf',fontsize=10,color=textcolor,rotation=20)
ax_all.text(-68.5,43,'Gulf of\n Maine',fontsize=14,color=textcolor)
ax_all.text(-69.35,41.85,'Georges Bank',fontsize=12,color=textcolor,rotation=35)
ax_all.text(-69.75,39,'Atlantic Ocean',fontsize=14,color=textcolor)


ax_all.text(-64.25,45.,'Halifax',fontsize=10,color=textcolor,rotation=25)
ax_all.text(-64.4,45.475,'Minas Passage',fontsize=6,color=textcolor)
ax_all.text(-63.25,45.3,'Minas Basin',fontsize=6,color=textcolor)
ax_all.text(-67.5,45.35,'St. John',fontsize=10,color=textcolor)



plotcoast(ax_all,filename='mid_nwatl6b.nc',fill=True,lw=.25)




#f.show()
f.savefig(savepath + grid + '_' +name+ '_bof.png',dpi=1200)


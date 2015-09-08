from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import time
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import matplotlib.path as path


# Define names and types of data
imgfile='figures/png/misc/vh_harbour_google_nogrid.jpg'

savepath='figures/png/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)


#y - moves picture donw
#x - move right
y=-.0005
x=.0003

f=plt.figure()
ax=plt.axes([.125,.5,.775,.4])
im = plt.imread(imgfile);
implot = ax.imshow(im,extent=[-123.155+x,-123.0+x,49.27+y,49.3275+y]);
plotcoast(ax,filename='pacific.nc',lw=2,color='r')
cl=loadkml('data/misc/vh_bathymetry/vh_harbour_coast.kml')
ax.plot(cl[:,0],cl[:,1],'b')

region={}
region['region']=[-123.1375,-123.08,49.283,49.304]
plot_box(ax,region,'g',3)
ax.axis([-123.155+x,-123.0+x,49.27+y,49.3275+y])
_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
ax.yaxis.set_major_formatter(_formatter)
ax.xaxis.set_major_formatter(_formatter)


ax1=plt.axes([.125,.075,.775,.375])
implot = ax1.imshow(im,extent=[-123.155+x,-123.0+x,49.27+y,49.3275+y]);
plotcoast(ax1,filename='pacific.nc',lw=2,color='r')
ax1.plot(cl[:,0],cl[:,1],'b')
ax1.axis(region['region'])
ax1.yaxis.set_major_formatter(_formatter)
ax1.xaxis.set_major_formatter(_formatter)



plt.draw()

axsub1bb=ax1.get_axes().get_position().bounds
ax.annotate("",xy=(axsub1bb[0]+axsub1bb[2],axsub1bb[1]+axsub1bb[3]),xycoords='figure fraction',xytext=(region['region'][1],region['region'][3]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))
ax.annotate("",xy=(axsub1bb[0],axsub1bb[1]+axsub1bb[3]),xycoords='figure fraction',xytext=(region['region'][0],region['region'][3]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='g',headwidth=3))


plt.savefig(savepath + 'coastline_overgoogle.png',dpi=300)
plt.close(f)










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


grid='vh_high'
name='2012-02-01_2012-03-01_0.01_0.001'
datatype='2d'

data=load_nei2fvcom('runs/'+grid+'/'+name+'/input/vh_high.nei')

savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)



# Plot grid
f=plt.figure()
ax0=f.add_axes([.125,.1,.375,.8])
ax0.triplot(data['trigrid'],lw=.075,color='k')
region0=regions('vhfr_whole')
prettyplot_ll(ax0,setregion=region0)
plotcoast(ax0,filename='pacific_harbour.nc',fill=True,color='None')
axes_label(ax0,'A',color='g',size=12)

#plot second narrow
ax2=f.add_axes([.55,.05,.4,.8])
ax2.triplot(data['trigrid'],lw=.15,color='k')
region2=regions('secondnarrows')
prettyplot_ll(ax2,setregion=region2,axlabels=False)
plotcoast(ax2,filename='pacific_harbour.nc',fill=True,color='None')

#plot vh_whole
ax1=f.add_axes([.365,.225,.4,.8])
ax1.triplot(data['trigrid'],lw=.05,color='k')
region1=regions('vh_whole')
region1['region'][3]=region1['region'][3]-.05
prettyplot_ll(ax1,setregion=region1,axlabels=False)
plotcoast(ax1,filename='pacific_harbour.nc',fill=True,color='None')

box2ax(ax0,ax1,region1,'B',textcolor='g',color='g',lw=1.5,fontsize=14)
box2ax(ax1,ax2,region2,'C',textcolor='g',color='g',lw=.5,fontsize=8)

#f.show()
f.savefig(savepath + grid + '_' + name +'_cmos_showgrid.png',dpi=1200)
#plt.close(f)


























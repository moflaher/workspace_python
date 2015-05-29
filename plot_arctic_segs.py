from __future__ import division
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




region={}
region['region']=np.array([-135,-45,50,95])

f=plt.figure()

ax=f.add_axes([.125,.1,.775,.8])
ax.set_axis_bgcolor('dodgerblue')




prettyplot_ll(ax,setregion=region)
plotcoast(ax,filename='world_GSHHS_f_L1.nc',fill=True,fcolor='darkgreen')


#f.show()

f.savefig('figures/png/misc/arctic_segs.png',dpi=600)






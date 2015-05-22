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
import time
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import matplotlib.path as path


# Define names and types of data
filename='data/bathy_mod/vh_depth.dat'

data=np.genfromtxt(filename)

region={}
region['region']=np.array([np.min(data[:,0]),np.max(data[:,0]),np.min(data[:,1]),np.max(data[:,1])])

f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
scb=ax.scatter(data[:,0],data[:,1],c=data[:,2],s=10,edgecolor='None',vmin=0,vmax=300)
prettyplot_ll(ax,setregion=region,cb=scb,cblabel='',grid=True)


vec=f.ginput(n=-1,timeout=-1)
plt.close(f)


p=path.Path(vec)

idx=p.contains_points(np.array([data[:,0],data[:,1]]).T)

data[idx,2]=(data[idx,2]+100)/2


save_llz(data,'data/bathy_mod/vh_depth_modify1.dat')


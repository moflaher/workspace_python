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
filename='data/bathy_mod/van_low_dep.dat'
averaged=100

data=np.genfromtxt(filename)

region={}
region['region']=np.array([np.min(data[:,0]),np.max(data[:,0]),np.min(data[:,1]),np.max(data[:,1])])

f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
scb=ax.scatter(data[:,0],data[:,1],c=data[:,2],s=10,edgecolor='None',vmin=0,vmax=100)
prettyplot_ll(ax,setregion=region,cb=scb,cblabel='',grid=True)


vec=f.ginput(n=-1,timeout=-1)
plt.close(f)


#turn selected points into path
p=path.Path(vec)

#find points inside path
idx_vec=p.contains_points(np.array([data[:,0],data[:,1]]).T)
idx_d=np.argwhere(data[:,2]<averaged)
idx_vec_f=np.flatnonzero(idx_vec)
ind_b=np.in1d(idx_vec_f,idx_d)
idx=idx_vec_f[ind_b]

data[idx,2]=(data[idx,2]+averaged)/2
save_llz(data,'data/bathy_mod/van_low_dep_'+str(averaged)+'_1.dat')


idx_d=np.argwhere(data[:,2]<averaged)
ind_b=np.in1d(idx_vec_f,idx_d)
idx=idx_vec_f[ind_b]

data[idx,2]=(data[idx,2]+averaged)/2
save_llz(data,'data/bathy_mod/van_low_dep_'+str(averaged)+'_2.dat')














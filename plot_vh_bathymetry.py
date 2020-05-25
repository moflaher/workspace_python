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
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
import time
import pyproj as pyp



p=pyp.Proj('+proj=utm +zone=10')









ASB=np.genfromtxt('data/misc/vh_bathymetry/Area-A_SB.txt',delimiter=',')
BSB=np.genfromtxt('data/misc/vh_bathymetry/Area-B_SB.txt',delimiter=',')
AMB=np.genfromtxt('data/misc/vh_bathymetry/Area-A_MB-10m.txt',delimiter=',')
BMB=np.genfromtxt('data/misc/vh_bathymetry/Area-B_MB-10m.txt',delimiter=',')



ASB[:,0],ASB[:,1]=p(ASB[:,0],ASB[:,1],inverse=True)
BSB[:,0],BSB[:,1]=p(BSB[:,0],BSB[:,1],inverse=True)
AMB[:,0],AMB[:,1]=p(AMB[:,0],AMB[:,1],inverse=True)
BMB[:,0],BMB[:,1]=p(BMB[:,0],BMB[:,1],inverse=True)


f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])


ax.scatter(AMB[:,0],AMB[:,1],c=AMB[:,2],s=15,edgecolor='None',vmin=-5,vmax=10)
ax.scatter(BMB[:,0],BMB[:,1],c=BMB[:,2],s=15,edgecolor='None',vmin=-5,vmax=10)

sax=ax.scatter(ASB[:,0],ASB[:,1],c=ASB[:,2],s=5,vmin=-5,vmax=10)
ax.scatter(BSB[:,0],BSB[:,1],c=BSB[:,2],s=5,vmin=-5,vmax=10)


plt.colorbar(sax)
fix_osw(ax)


f.savefig('figures/png/misc/vh_bathymetry.png',dpi=600)




if True:
    allpts=np.vstack([ASB,BSB,AMB,BMB])

    fp=open('data/misc/vh_bathymetry/vh_fr_all.dat','w')
    for i in range(len(allpts)):
        fp.write('%f %f %f\n'% (allpts[i,0],allpts[i,1],allpts[i,2]))

    fp.close()





















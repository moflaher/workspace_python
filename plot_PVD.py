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



filename='MADCP_hud2013021_1841_3367_3600_interpolated.nc'
data=loadnc('data/misc/pvd/',singlename=filename)

spacing=4
cutoff=22

dt=(data['time2'][1]-data['time2'][0])/1000
labels=np.round(data['depth'][:cutoff:spacing]).astype(int)

u=(data['u_1205'][:,:cutoff:spacing,0,0]/100).copy()
u[u>1000]=0
u[u<-1000]=0
v=(data['v_1206'][:,:cutoff:spacing,0,0]/100).copy()
v[v>1000]=0
v[v<-1000]=0

ud=u*dt
vd=v*dt

usume=np.cumsum(ud,axis=0)
usums=usume-usume[0,:]
vsume=np.cumsum(vd,axis=0)
vsums=vsume-vsume[0,:]

f=plt.figure(figsize=(12,12))
ax=f.add_axes([.125,.1,.775,.8])

lines=ax.plot(usums/1000,vsums/1000)
#ax.quiver(usum,vsum,ud,vd,pivot='tail',headlength=0,headwidth=0,units='xy',angles='xy')
ax.grid()
ax.set_aspect('equal', 'datalim')
ax.axis([-500,4500,-500,1500])
legend=ax.legend(lines, labels,loc='best')
for label in legend.get_lines():
    label.set_linewidth(3)

ax.set_xlabel(r'km')
ax.set_ylabel(r'km')


#f.show()
f.savefig('figures/png/misc/pvd/'+ filename[:-3] +'.png',dpi=150)






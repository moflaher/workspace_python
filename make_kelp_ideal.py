from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
import pyproj as pyp

def at(xx,yy,xt,yt):
    xx=np.append(xx,xt)
    yy=np.append(yy,yt)
    
    return xx,yy

x=0.0
y=0.0

xspace=200.0
yspace=200.0
xcube=5000.0
ycube=1000.0
bayr=2000.0
rspace=.1


llx=x-xcube/2
lly=y-ycube/2

urx=x+xcube/2
ury=y+ycube/2

xx=np.array([])
yy=np.array([])

#left side
yt=np.arange(lly,ury+yspace,yspace)
xt=np.repeat(llx,len(yt))
xx,yy=at(xx,yy,xt,yt)


#top side
xt=np.arange(llx,urx+xspace,xspace)
yt=np.repeat(ury,len(xt))
xx,yy=at(xx,yy,xt,yt)


#bay top
ang2=np.arange(np.pi-np.arctan(ycube/2/bayr),0,-rspace)
ang=ang2[2:]
yt=bayr*np.sin(ang)
xxt=bayr*np.cos(ang)
xtt=bayr*np.cos(ang2)
xt=xcube+xxt-np.min(xtt+xcube/2)
xx,yy=at(xx,yy,xt,yt)

#bay bottom
ang2=np.arange(0,-np.pi+np.arctan(ycube/2/bayr),-rspace)[:-2]
ang=ang2#[:-1]
#ang=np.arange(0,-np.pi,-rspace)
yt=bayr*np.sin(ang)
xxt=bayr*np.cos(ang)
#xtt=bayr*np.cos(ang2)
xt=xcube+xxt-np.min(xtt+xcube/2)
xx,yy=at(xx,yy,xt,yt)

#bottom side
xt=np.arange(urx,llx-xspace,-xspace)
yt=np.repeat(lly,len(xt))
xx,yy=at(xx,yy,xt,yt)

#convert to fake projection close to equator
projstr='lcc +lon_0=0.0 +lat_0=1.0 +lat_1=0.5 +lat_2=1.5'
proj=pyp.Proj(proj=projstr)

lon,lat=proj(xx,yy,inverse=True)

segfile={}
segfile['1']=np.vstack([lon,lat]).T

save_nodfile(segfile,'data/kelp_ideal/kelpideal_0.nod')


plt.plot(lon,lat,'.')
plt.plot(lon,lat)
plt.savefig('test.png')











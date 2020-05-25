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
from scipy.optimize import curve_fit
import matplotlib.tri as tri

def at(xx,yy,xt,yt):
    xx=np.append(xx,xt)
    yy=np.append(yy,yt)
    
    return xx,yy


XG=np.array([])
YG=np.array([])
#gfactor has to be less than .5
gfactorx=.1
gfactory=.49

#define general grid
xlspace=200
ylspace=200
gfactorxl=0.1
gfactoryl=0.25
lll=np.array([-7000,-1000])
url=np.array([3000,1000])


#define high res
xhspace=2
yhspace=2
llh=np.array([-300,-150])
urh=np.array([300,150])
xh=np.arange(llh[0],urh[0]+xhspace,xhspace)
yh=np.arange(llh[1],urh[1]+yhspace,yhspace)
XH,YH=np.meshgrid(xh,yh)
XH=XH.flatten()
YH=YH.flatten()
#jiggle
XH=XH+(np.random.rand(len(XH))-.5)*xhspace*gfactorx
YH=YH+(np.random.rand(len(YH))-.5)*yhspace*gfactory
XG,YG=at(XG,YG,XH,YH)

#define  taper area
xlspace=50
ylspace=50
llt=np.array([-2000,-500])
urt=np.array([2000,500])


#define buffer area
num=18
xcay=np.exp(np.log(xlspace/xhspace)/num)
ycay=np.exp(np.log(ylspace/yhspace)/num)

xc=np.array([])
yc=np.array([])
for i in range(num):
    xs=xhspace*xcay**(i+1)
    ys=yhspace*ycay**(i+1)
    xc=np.append(xc,xs)
    yc=np.append(xc,ys)
    
if (xc.sum()>(llh[0]-llt[0])) or (xc.sum()>(urt[0]-urh[0])):
    print('Not enough space to decay x. Reduce num or increase x domain')
    print(xc.sum())
    print(llh[0]-llt[0])
    print(urt[0]-urh[0])
    sys.exit(0)
if (yc.sum()>(llh[1]-llt[1])) or (yc.sum()>(urt[1]-urh[1])):
    print('Not enough space to decay y. Reduce num or increase y domain')
    print(yc.sum())
    print(llh[1]-llt[1])
    print(urt[1]-urh[1])
    sys.exit(0)
    
print(xc)
print(yc)

#make a series of lower res meshes
for i in range(num-1):
    # define new bigger box
    tll=llh+(i+1)*(llt-llh)/num
    tur=urh+(i+1)*(urt-urh)/num
    #grid the box
    xt=np.arange(tll[0],tur[0],xc[i])
    yt=np.arange(tll[1],tur[1],yc[i])
    XT,YT=np.meshgrid(xt,yt)
    XT=XT.flatten()
    YT=YT.flatten()
    #jiggle
    XT=XT+(np.random.rand(len(XT))-.5)*xc[i]*gfactorx
    YT=YT+(np.random.rand(len(YT))-.5)*yc[i]*gfactory
    #delete points in the box that have points
    idx=np.argwhere((XT>XG.min()) & (XT<XG.max())&(YT>YG.min()) & (YT<YG.max()))
    XT=np.delete(XT,idx)
    YT=np.delete(YT,idx)
    # maybe delete points outside "new bigger box"
    
    
    XG,YG=at(XG,YG,XT,YT)

#add the low res area outside taper
xl=np.arange(lll[0]+xlspace*2,url[0]-xlspace,xlspace)
yl=np.arange(lll[1]+ylspace*2,url[1]-ylspace,ylspace)
XL,YL=np.meshgrid(xl,yl)
XL=XL.flatten()
YL=YL.flatten()
#jiggle
XL=XL+(np.random.rand(len(XL))-.5)*xlspace*gfactorxl
YL=YL+(np.random.rand(len(YL))-.5)*ylspace*gfactoryl
#delete points in the box that have points
idx=np.argwhere((XL>XG.min()) & (XL<XG.max())&(YL>YG.min()) & (YL<YG.max()))
XL=np.delete(XL,idx)
YL=np.delete(YL,idx)
XG,YG=at(XG,YG,XL,YL)

#add the boundary
xl=np.arange(lll[0],url[0]+xlspace,xlspace)
yl=np.arange(lll[1],url[1]+ylspace,ylspace)
XL,YL=np.meshgrid(xl,yl)
XL=XL.flatten()
YL=YL.flatten()
#delete points in the box that have points
idx=np.argwhere((XL>XG.min()) & (XL<XG.max())&(YL>YG.min()) & (YL<YG.max()))
XL=np.delete(XL,idx)
YL=np.delete(YL,idx)
XG,YG=at(XG,YG,XL,YL)


f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.scatter(XG,YG)
f.show()


triang = tri.Triangulation(XG, YG)



f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.triplot(triang)
f.show()

print(XG.shape)
print(triang.triangles.shape)


#convert to fake projection close to equator
projstr='lcc +lon_0=2 +lat_0=2.0 +lat_1=1 +lat_2=3'
proj=pyp.Proj(proj=projstr)

lon,lat=proj(XG,YG,inverse=True)

np.savetxt('data/kelp_ideal/xy.dat',np.vstack([lon,lat,lat*0]).T,fmt='%f %f %f')


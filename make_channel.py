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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pyproj as pyp
from scipy.optimize import curve_fit
import matplotlib.tri as tri


#define general grid
xlspace=100
ylspace=100
xl=np.arange(-2000,2000+xlspace,xlspace)
yl=np.arange(-500,500+ylspace,ylspace)
XL,YL=np.meshgrid(xl,yl)
XL=XL.flatten()
YL=YL.flatten()


#define high res
xhspace=2
yhspace=2
ll=np.array([-400,-200])
ur=np.array([400,200])
xh=np.arange(ll[0],ur[0]+xhspace,xhspace)
yh=np.arange(ll[1],ur[1]+yhspace,yhspace)
XH,YH=np.meshgrid(xh,yh)

#define buffer area
xb=1000
yb=200
xnum=20
ynum=10

#remove low res points
XHmax=XH.max()+xb
XHmin=XH.min()-xb
YHmax=YH.max()
YHmin=YH.min()
idx=np.argwhere((XL>=XHmin) & (XL<=XHmax)&(YL>=YHmin) & (YL<=YHmax))
XL=np.delete(XL,idx)
YL=np.delete(YL,idx)
XHmax=XH.max()
XHmin=XH.min()
YHmax=YH.max()+yb
YHmin=YH.min()-yb
idx=np.argwhere((XL>=XHmin) & (XL<=XHmax)&(YL>=YHmin) & (YL<=YHmax))
XL=np.delete(XL,idx)
YL=np.delete(YL,idx)

#merge low and high
XL=np.append(XL,XH)
YL=np.append(YL,YH)

# create buffer area x
xlbuff=np.array([ll[0]-xb])
xrbuff=np.array([ur[0]+xb])
cnt=0
decay=.08175
for i in range(xnum):
    xadd=xlspace*(1-decay)**i
    if xadd<2*(1+decay):
        xadd=2*(1+decay)
    cnt+=xadd
    print('x')
    print(cnt)
    print(xadd)
    print()
    xlbuff=np.append(xlbuff,xlbuff[-1]+xadd)
    xrbuff=np.append(xrbuff,xrbuff[-1]-xadd)
    
# create buffer area y
ybbuff=np.array([ll[1]-yb])
ytbuff=np.array([ur[1]+yb])
cnt=0
decay=.53
for i in range(ynum):
    yadd=ylspace*(1-decay)**i
    if yadd<2*(1+decay):
        yadd=2*(1+decay)
    cnt+=yadd
    print('y')
    print(cnt)
    print(yadd)
    print()
    ybbuff=np.append(ybbuff,ybbuff[-1]+yadd)
    ytbuff=np.append(ytbuff,ytbuff[-1]-yadd)
    

#mesh buffer vertical
XHmax=XH.max()
XHmin=XH.min()
YHmax=YH.max()+yb
YHmin=YH.min()-yb
idx=np.argwhere((XL>=XHmin) & (XL<=XHmax)& (YL>YHmax))
XLbuff=np.unique(XL[idx])

#merge top buff
xt,yt=np.meshgrid(XLbuff,ytbuff)
XL=np.append(XL,xt)
YL=np.append(YL,yt)
#merge bottom buff
xt,yt=np.meshgrid(XLbuff,ybbuff)
XL=np.append(XL,xt)
YL=np.append(YL,yt)


#mesh buffer horiz
XHmax=XH.max()+xb
XHmin=XH.min()-xb
YHmax=YH.max()
YHmin=YH.min()
idx=np.argwhere((YL>=YHmin) & (YL<=YHmax)& (XL>XHmax))
YLbuff=np.unique(YL[idx])
#YLbuff=np.linspace(YL.min(),YL.max(),2*len(YLbuff))

#merge left buff
xt,yt=np.meshgrid(xlbuff,YLbuff)
XL=np.append(XL,xt)
YL=np.append(YL,yt)
#merge right buff
xt,yt=np.meshgrid(xrbuff,YLbuff)
XL=np.append(XL,xt)
YL=np.append(YL,yt)


f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.scatter(XL,YL)
f.show()


triang = tri.Triangulation(XL, YL)



f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.triplot(triang)
f.show()


#convert to fake projection close to equator
projstr='lcc +lon_0=2 +lat_0=2.0 +lat_1=1 +lat_2=3'
proj=pyp.Proj(proj=projstr)

lon,lat=proj(XL,YL,inverse=True)

np.savetxt('data/kelp_ideal/xy.dat',np.vstack([lon,lat,lat*0]).T,fmt='%f %f %f')


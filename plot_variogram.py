from __future__ import division,print_function
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
from mytools import *
import os, sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name='test_river_utc'
grid='sjh_lr_v1_sub'


### load the .nc file #####
data = loadnc('/media/moflaher/runs/sjh_lr_v1_sub/test_river_utc/output/',singlename=grid + '_0001.nc')
print('done load')

savepath='{}/png/{}/variogram/{}/'.format(figpath,grid,name)
if not os.path.exists(savepath): os.makedirs(savepath)

region=regions('rattling_beach')

speed=np.sqrt(data['ua']**2+data['va']**2)
mspeed=np.max(speed,axis=0)
pspeed=np.percentile(speed,95,axis=0)
bspeed=.1
bpspeed=copy.deepcopy(pspeed)
bpspeed[bpspeed<=bspeed]=np.nan

eidx=get_elements(data,region)

rmspd=bpspeed[eidx[:,0]]
xc=data['xc'][eidx[:,0]]
yc=data['yc'][eidx[:,0]]

ratio=np.zeros((len(rmspd),len(rmspd)))
dist=np.zeros((len(rmspd),len(rmspd)))

for i in range(len(xc)):
    print(i)
    ratio[i,:]=rmspd/rmspd[i]
    dist[i,:]=np.sqrt((xc-xc[i])**2 +(yc-yc[i])**2)


# f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8]);
# ax.plot(np.ravel(dist),np.ravel(ratio),'k.')
# f.show()


def plot_fun(Zm,xg,yg,cr):    
    f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8]);
    ax.set_facecolor('.9')
    cax=ax.contourf(xg,yg,100*np.divide(Zm.T,Zm.max()),cr,extend='max',vmin=0,vmax=cr[-1],cmap=mpl.cm.Blues)
    plt.colorbar(cax)
    CS=ax.contour(xg,yg,100*np.divide(Zm.T,Zm.max()),cr,linestyles='solid',colors='k',zorder=30)
    ax.clabel(CS,labels=cr, fontsize=8, inline=1,zorder=31,fmt='%d')
    ax.axhline(1,color='k')
    ax.axhline(1*1.5,color='r',linestyle='--')
    ax.axhline(1/1.5,color='r',linestyle='--')
    ax.axhline(1/2.0,color='m',linestyle='--')
    ax.axhline(1*2.0,color='m',linestyle='--')
    #ax.clabel(CS,labels=v, fontsize=8, inline=1,zorder=31,fmt='%d')
    f.show()    

xg=np.arange(0,10000,100)

yg=np.arange(0,5,.1)
cmin=0; cmax=110
cr=np.arange(cmin,cmax,20)

grid, _, _ = np.histogram2d(np.ravel(dist), np.ravel(ratio), bins=[xg,yg])
    
# gt=grid[:-1,:]+grid[1:,:]
# ht=gt[:,:-1]+gt[:,1:]
# ft=np.zeros((ht.shape[0]+2,ht.shape[1]+2))
# ft[1:-1,1:-1]=ht/4.0
# Zm = np.ma.masked_where(ft==0,ft)
    
#plot_fun(Zm,xg,yg,cr)

ccnts=grid.sum(axis=1)

xl=len(xg)-1
yl=len(yg)-1

a=grid/np.repeat(ccnts,yl).reshape(xl,yl)


f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8]);
ax.set_facecolor('.9')
cax=ax.contourf(xg[:-1],yg[:-1],a.T,extend='max',cmap=mpl.cm.Blues)
plt.colorbar(cax)
# CS=ax.contour(xg,yg,100*np.divide(Zm.T,Zm.max()),cr,linestyles='solid',colors='k',zorder=30)
# ax.clabel(CS,labels=cr, fontsize=8, inline=1,zorder=31,fmt='%d')
#ax.axhline(1,color='k')
# ax.axhline(1*1.5,color='r',linestyle='--')
# ax.axhline(1/1.5,color='r',linestyle='--')
# ax.axhline(1/2.0,color='m',linestyle='--')
# ax.axhline(1*2.0,color='m',linestyle='--')
#ax.clabel(CS,labels=v, fontsize=8, inline=1,zorder=31,fmt='%d')
f.show()    











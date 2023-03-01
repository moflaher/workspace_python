from __future__ import division,print_function
import numpy as np
import scipy as sp
import matplotlib as mpl
mpl.use('agg')
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
from mytools import *
import os, sys
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
import matplotlib.colors as colors
import argparse



parser = argparse.ArgumentParser()
#required arguments
parser.add_argument("grid", help="name of the grid", type=str)
parser.add_argument("name", help="name of the run", type=str)
parser.add_argument("max", help="specify colorbar upper limit",type=float,nargs=1)
parser.add_argument("ncfile", help="specify ncfile", type=str)
parser.add_argument("loc", help="Specify Location to use for comparsion",type=float,nargs=2)


#optional arguments
parser.add_argument("-zoomdist", help="specify zoom distances as a string (ie "") (default is 5km from loc)",type=str,nargs=1,default="5000")



args= parser.parse_args()
print(args)

grid=args.grid
name=args.name
loc=args.loc
zoomdist=np.array([float(f) for f in args.zoomdist[0].split(' ')])


### load the .nc file #####
data = loadnc('',args.ncfile)
print('done load')


savepath='{}/png/{}/variogram4loc/{}/'.format(figpath,grid,name)

print(savepath)
if not os.path.exists(savepath): os.makedirs(savepath)


speed=np.sqrt(data['ua']**2+data['va']**2)
mspeed=np.max(speed,axis=0)
pspeed=np.percentile(speed,95,axis=0)
bspeed=-1.0
bpspeed=copy.deepcopy(pspeed)
bpspeed[bpspeed<=bspeed]=np.nan

eidx=closest_element(data,loc)
#print(eidx,loc)
#print(data['lonc'][eidx],data['latc'][eidx])

x,y=data['proj'](loc[0],loc[1])
ratio=bpspeed/bpspeed[eidx]


f=plt.figure(); ax=f.add_axes([.15,.125,.775,.8])    
plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc', filepath=coastpath, color='k', fill=True,zorder=50)   
triax=ax.tripcolor(data['trigrid'],ratio,cmap=mpl.cm.seismic,norm=colors.TwoSlopeNorm(vcenter=1.0,vmin=0.,vmax=float(args.max[0])))    
cb=plt.colorbar(triax)
ax.plot(loc[0],loc[1],'r*',zorder=70)
ax.plot(data['lon'][data['nv'][eidx,[0,1,2,0]]],data['lat'][data['nv'][eidx,[0,1,2,0]]],'k',lw=2,zorder=60)
ax.set_xlabel(r'Longitude ($^{\circ}$)')
ax.set_ylabel(r'Latitude ($^{\circ}$)')

for kk in range(len(zoomdist)):
    lon,lat=data['proj']([x-zoomdist[kk],x+zoomdist[kk]],[y-zoomdist[kk],y+zoomdist[kk]],inverse=True)
    ax.axis([lon[0],lon[1],lat[0],lat[1]])

    f.savefig('{}{}_{}_variogram4loc_at_{}_{}_zoomdist_{}_cbmax_{}.png'.format(savepath,grid,name,loc[0],loc[1],zoomdist[kk],args.max[0]),dpi=300)


plt.close(f)













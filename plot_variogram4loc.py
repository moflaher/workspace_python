from __future__ import division,print_function
import numpy as np
import scipy as sp
import matplotlib as mpl
#mpl.use('agg')
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
parser.add_argument("-zoomdist", help="specify zoom distance (default is 5km from loc)",type=float,nargs=1,default=5000)



args= parser.parse_args()
print(args)

grid=args.grid
name=args.name
loc=args.loc



# Define names and types of data
#name='passbay_v4_2018.20211008'
#grid='passbay_v4'
#loc=np.array([-66.723517, 44.718500])
#loc=np.array([-66.978755,45.014255])
#loc=np.array([-65.75375,44.64903])
#loc=np.array([-66.8314,45.0599])
#loc=np.array([-66.8171,45.0601])
#loc=np.array([-66.8675,45.031])
#loc=np.array([-66.04, 45.235])
#loc=np.array([-66.72253333, 45.06113333])
#barnaby head
#loc=np.array([-66.538866667, 45.108366667])
#stmarys bay dg009
#loc=np.array([-66.15, 44.41])
#stmarys bay dg010
#loc=np.array([-66.23, 44.35])

#site=np.array([[1, 66, 32, 24.960, 45, 6, 41.760],
#[2, 66, 32, 3.787, 45, 6, 35.634],
#[3, 66, 32, 32.088, 45, 6, 5.649],
#[4, 66, 32, 42.258, 45, 6, 11.774]])
#tsite=np.array([[-1*(row[1]+row[2]/60.+row[3]/3600.), row[4]+row[5]/60.+row[6]/3600. ] for row in site])



### load the .nc file #####
data = loadnc('',args.ncfile)
#data = loadnc('/home/suh001/scratch/passbay_v4/runs/{}/output/'.format(name),singlename=grid + '_0001.nc')
#data = loadnc('/gpfs/fs1/dfo/dfo_odis/mif001/run_save/{}/runs/{}/output/'.format(grid,name),singlename=grid + '_0001.nc')
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

#print(bpspeed)
eidx=closest_element(data,loc)


x,y=data['proj'](loc[0],loc[1])
lon,lat=data['proj']([x-args.zoomdist[0],x+args.zoomdist[0]],[y-args.zoomdist[0],y+args.zoomdist[0]],inverse=True)

ratio=bpspeed/bpspeed[eidx]
#dist=np.sqrt((data['xc']-data['xc'][i])**2 +(data['yc']-data['yc'][i])**2)


f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8])    
plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc', filepath=coastpath, color='k', fill=True,zorder=50)   
#triax=ax.tripcolor(data['trigrid'],ratio,cmap=mpl.cm.seismic,norm=colors.TwoSlopeNorm(vcenter=1.0,vmin=0.,vmax=float(args.max[0])))    
triax=ax.tripcolor(data['trigrid'],ratio,cmap=mpl.cm.seismic)    

#cb=plt.colorbar(triax)
ax.plot(loc[0],loc[1],'r*',zorder=70)
ax.plot(data['lon'][data['nv'][eidx,[0,1,2,0]]],data['lat'][data['nv'][eidx,[0,1,2,0]]],'k',lw=2)
#ax.set_xlabel(r'Longitude ($^{\circ}$)')
#ax.set_ylabel(r'Latitude ($^{\circ}$)')
ax.axis([lon[0],lon[1],lat[0],lat[1]])



#ax.plot(np.append(tsite[:,0],tsite[0,0]),np.append(tsite[:,1],tsite[0,1]),'k')

#ax.annotate('{} {}'.format(data['Time'][i][:10],data['Time'][i][11:19]),xy=region['textloc'],xycoords='axes fraction')


#for label in ax.get_xticklabels()[::2]:
#    label.set_visible(False)


f.savefig('{}{}_{}_variogram4loc_at_{}_{}_zoomdist_{}_cbmax_{}.png'.format(savepath,grid,name,loc[0],loc[1],args.zoomdist[0],args.max[0]),dpi=300)
#plt.close(f)
#f.show()


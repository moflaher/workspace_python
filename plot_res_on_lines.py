from __future__ import division,print_function
import matplotlib as mpl
mpl.use('Agg')
import scipy as sp
from folderpath import *
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
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import multiprocessing
import pymp
import seawater as sw



# Define names and types of data
name='sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1_15mins'
grid='sjh_lr_v1'

starttime=0
endtime=-1
#name='sjh_hr_v3_year_wet_15mins'
#grid='sjh_hr_v3'


### load the .nc file #####
data = loadnc('/mnt/drive_1/runs/{}/{}/output/'.format(grid,name),singlename=grid + '_0001.nc')
print('done load')
trifinder=data['trigrid'].get_trifinder()
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
data['nodexy']=np.vstack([data['x'],data['y']]).T

savepath='{}png/{}_{}/phase1b/{}/'.format(figpath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)


time=data['Time']


##spec lines
line1=np.genfromtxt('data/nemofvcom/line1.ll')
#line2=np.genfromtxt('data/nemofvcom/line2.ll')
lines=np.vstack([line1])#,line2])

slmean=np.array([])
slmin=np.array([])
slmax=np.array([])
hosts=np.array([])
for i in range(len(lines)):
    print(i/(len(lines)*1.))
    host=trifinder(lines[i,0],lines[i,1])
    hosts=np.append(host,hosts)
    slmint=100000
    slmaxt=0
    slmeant=0
    for j in range(3):
        slt=np.sqrt((data['nodexy'][data['nv'][host,j-1],0]-data['nodexy'][data['nv'][host,j],0])**2+(data['nodexy'][data['nv'][host,j-1],1]-data['nodexy'][data['nv'][host,j],1])**2)

        slmeant=slmeant+slt
        slmint=np.min([slt,slmint])
        slmaxt=np.max([slt,slmaxt])
    
    slmean=np.append(slmean,slmeant/3.0)
    slmin=np.append(slmin,slmint)
    slmax=np.append(slmax,slmaxt)

locs=np.array([0])
hc=hosts[0]
for i,h in enumerate(hosts):
    if h!=hc:
        locs=np.append(locs,i)
    hc=h
        
        

 
 
#f=plt.figure()
#ax=f.add_axes([.125,.1,.775,.8])
#ax.plot(slmean,'k')
#ax.plot(slmin,'b')
#ax.plot(slmax,'b')
#f.show()
 
 
#f=plt.figure()
#ax=f.add_axes([.125,.1,.775,.8])
#ax.plot(hosts,'.k')
#for line in locs:
    #ax.axvline(line)
#f.show()

f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.hist(np.diff(locs),bins=20)
ax.xaxis.set_ticks(range(0,100,5))
ax.set_xlabel('Interpolation length scale ?  (m)')
ax.set_ylabel('Freq')
f.savefig('{}{}_line1_interpolation_length.png'.format(savepath,grid),dpi=300)




usurf=np.genfromtxt('/mnt/drive_0/misc/gpscrsync/dataout/{}_2d/phase1b/{}/{}_usurf_line1.dat'.format(grid,name,name))
#time=np.genfromtxt('/mnt/drive_0/misc/gpscrsync/dataout/{}_2d/phase1b/{}/{}_time.dat'.format(grid,name,name),dtype=str)

#times=dates.datestr2num(time)

u=usurf[:,1056:(1056+96)]

xx,yy=np.meshgrid(line1[:,0],np.arange(0,24,.25))

f=plt.figure(figsize=(15,5))
ax=f.add_axes([.125,.1,.775,.8])
cax=ax.pcolormesh(xx.T,yy.T,u,vmin=-1,vmax=1,cmap=mpl.cm.jet)
for lon in line1[locs,0]:
    ax.axvline(lon,color='k',lw=.5)
plt.colorbar(cax)
f.savefig('{}{}_specline_map_lines_on_elements.png'.format(savepath,grid))











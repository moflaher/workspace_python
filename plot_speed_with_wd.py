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
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import multiprocessing


global name
global grid
global regionname
global region
global tmparray
global savepath
global data
global cmin
global cmax
global vectorflag
global uniformvectorflag
global coastflag
global vidx
global vector_scale



# Define names and types of data
name='sfm5m_sjr_baroclinic_20150615-20150905'
grid='sfm5m_sjr'

regionname='stjohn_harbour'
starttime=120
endtime=1200
spacing=1
cmin=0
cmax=1


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data,trifinder=False,uvhset=False)
print('done sort')

vectorflag=False
coastflag=True
uniformvectorflag=False
vector_spacing=300
vector_scale=300

#vector_spacing=600
#vector_scale=150

#vector_spacing=75
#vector_scale=1250

#vector_spacing=125
#vector_scale=750

cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
if np.shape(cages)!=():
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.2
    ls='solid'


region=regions(regionname)
#region={}
#region['regionname']='kelpfield_rightisland'
#region['region']=np.array([-129.46,-129.48,52.640,52.665])
vidx=equal_vectors(data,region,vector_spacing)


savepath='figures/timeseries/' + grid + '_'  + '/speed_with_wd/' + name + '_' + region['regionname'] + '_' +("%f" %cmin) + '_' + ("%f" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)


def speed_plot(i):
    print(i)
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    if coastflag==True:
        plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc',color='k', fcolor='0.75', fill=True,zorder=100)
        
    triax=ax.tripcolor(data['trigrid'],np.sqrt(data['ua'][i,:]**2+data['va'][i,:]**2),vmin=cmin,vmax=cmax)
    
    if np.shape(cages)!=():   
        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        ax.add_collection(lseg_t) 
    if vectorflag==True:
        Q1=ax.quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],data['ua'][i,vidx],data['va'][i,vidx],angles='xy',scale_units='xy',scale=vector_scale,zorder=100,width=.0025)    
    if uniformvectorflag==True:
        norm=np.sqrt(data['ua'][i,vidx]**2+data['va'][i,vidx]**2)
        Q1=ax.quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],np.divide(data['ua'][i,vidx],norm),np.divide(data['va'][i,vidx],norm),angles='xy',scale_units='xy',scale=vector_scale,zorder=100,width=.002,color='k')  
            
    sand=np.argwhere(data['wet_cells'][i,:]==0)
    tmparray=[list(zip(data['nodell'][data['nv'][j,[0,1,2]],0],data['nodell'][data['nv'][j,[0,1,2]],1])) for j in sand ]
    lseg_sand=PC(tmparray,facecolor = '0.75',edgecolor='0.75')
    ax.add_collection(lseg_sand) 
        
    prettyplot_ll(ax,setregion=region,cblabel=r'Speed (ms$^{-1}$)',cb=triax)
    f.savefig(savepath + grid + '_' + region['regionname'] +'_speed_' + ("%04d" %(i)) + '.png',dpi=150)
    plt.close(f)



pool = multiprocessing.Pool()
pool.map(speed_plot,range(starttime,endtime,spacing))































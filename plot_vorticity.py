from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'
datatype='2d'
regionname='kit4_kelp_tight5'
starttime=400
endtime=450
cmin=-.025
cmax=.025


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
if cages!=None:
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.2
    ls='solid'


savepath='figures/timeseries/' + grid + '_' + datatype + '/curl/' + name + '_' + regionname + '_' +("%f" %cmin) + '_' + ("%f" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)


region=regions(regionname)



# Plot mesh
for i in range(starttime,endtime):
    print i
    ua=np.hstack([data['ua'][i,:],0])
    va=np.hstack([data['va'][i,:],0])
    dudy= data['a2u'][0,:]*ua[0:-1]+data['a2u'][1,:]*ua[data['nbe'][:,0]]+data['a2u'][2,:]*ua[data['nbe'][:,1]]+data['a2u'][3,:]*ua[data['nbe'][:,2]];
    dvdx= data['a1u'][0,:]*va[0:-1]+data['a1u'][1,:]*va[data['nbe'][:,0]]+data['a1u'][2,:]*va[data['nbe'][:,1]]+data['a1u'][3,:]*va[data['nbe'][:,2]];
    
    #print np.mean(dvdx-dudy)
    #print np.min(dvdx-dudy)
    #print np.max(dvdx-dudy)
    #print np.std(dvdx-dudy)
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],dvdx-dudy,vmin=cmin,vmax=cmax)
    if cages!=None:   
        ax.plot(data['uvnodell'][cages,0],data['uvnodell'][cages,1],'w.',markersize=1) 
    prettyplot_ll(ax,setregion=region,cblabel='Curl',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_curl_' + ("%04d" %(i)) + '.png',dpi=600)
    plt.close(f)
































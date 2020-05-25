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
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)


# Define names and types of data
name='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'

regionlist=['kit4_ftb','kit4_crossdouble','kit4_kelp_tight2_small','kit4_kelp_tight5','kit4_kelp_tight2_kelpfield']
starttime=621
endtime=1081


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

savepath='figures/png/' + grid + '_'  + '/curl/'
if not os.path.exists(savepath): os.makedirs(savepath)
plt.close()



curl=np.zeros((endtime-starttime,len(data['nv'])))


# Calculate vorticity for specified time
for idx,i in enumerate(range(starttime,endtime)):
    print i
    ua=np.hstack([data['ua'][i,:],0])
    va=np.hstack([data['va'][i,:],0])
    dudy= data['a2u'][0,:]*ua[0:-1]+data['a2u'][1,:]*ua[data['nbe'][:,0]]+data['a2u'][2,:]*ua[data['nbe'][:,1]]+data['a2u'][3,:]*ua[data['nbe'][:,2]]
    dvdx= data['a1u'][0,:]*va[0:-1]+data['a1u'][1,:]*va[data['nbe'][:,0]]+data['a1u'][2,:]*va[data['nbe'][:,1]]+data['a1u'][3,:]*va[data['nbe'][:,2]]
    curl[idx,:]=dvdx-dudy

# Find the mean vorticity
mcurl=curl.mean(axis=0)


for regionname in regionlist:
    print 'Plotting region:' + regionname
    region=regions(regionname)
    eidx=get_elements(data,region)

    #Plot the mean vorticity
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],mcurl,vmin=mcurl[eidx].min(),vmax=mcurl[eidx].max())
    prettyplot_ll(ax,setregion=region,cblabel='Mean Curl',cb=triax)
    plotcoast(ax,filename='pacific.nc',color='k',fill=True)
    if cages!=None:   
        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        ax.add_collection(lseg_t)
    f.savefig(savepath + grid + '_' +name + '_'+ regionname +'_curl_mean.png',dpi=600)
    plt.close(f)
































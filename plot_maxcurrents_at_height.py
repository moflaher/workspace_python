from __future__ import division,print_function
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import scipy.io as sio
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
from StringIO import StringIO
from gridtools import *
from datatools import *
from misctools import *
from plottools import *
from projtools import *
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)


# Define names and types of data
name='kit4_baroclinic_new_322'
grid='kit4'
#regionname='douglaslarge'
regionlist=['douglaslarge','gilisland_tight','kit4_area5']

starttime=384
interpheight=1

### load the .nc file #####
data = loadnc('runs/'+grid+'/' + name + '/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')


savepath='figures/png/' + grid + '_'  + '/maxcurrents_' + ("%d" %interpheight)+ 'm/'
if not os.path.exists(savepath): os.makedirs(savepath)

print('Loading interpolated currents')
currents=np.load('data/interp_currents/'+ grid + '_' +name+ '_' + ("%d" %interpheight) + 'm.npy')
currents=currents[()]
print('Loaded interpolated currents')

maxspeed=np.sqrt(currents['u']**2+currents['v']**2).max(axis=0)
for regionname in regionlist:
    
    region=regions(regionname)    
    eidx=get_elements(data,region)
    clim=np.percentile(maxspeed[eidx],[5,98])
    #arrows=20    
    #width=ll2m([region['region'][0],region['center'][1]],[region['region'][1],region['center'][1]])[0]
    #height=ll2m([region['center'][0],region['region'][2]],[region['center'][0],region['region'][3]])[1]    
    #vectorspacing=np.min([width/arrows,height/arrows]).astype(int)
    #print(vectorspacing)
    #vidx=equal_vectors(data,region,vectorspacing)

    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],maxspeed,vmin=clim[0],vmax=clim[1])
    plotcoast(ax,color='k',fill=True)
    #if np.shape(cages)!=():   
        #lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        #ax.add_collection(lseg_t) 
    #Q1=ax.quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],1,1,angles='xy',scale_units='xy',scale=arrows,zorder=100,width=.0025)           
    prettyplot_ll(ax,setregion=region,cblabel=r'Max Speed (ms$^{-1}$)',cb=triax)
    f.savefig(savepath + grid + '_' + region['regionname'] +'_maxspeed.png',dpi=300)
    plt.close(f)

























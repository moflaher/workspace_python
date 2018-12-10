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
name1='kit4_kelp_nodrag'
name2='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'
regionname='kit4_kelp_tight2_kelpfield'

starttime=400
endtime=450
cmin=-0.01
cmax=0.01




### load the .nc file #####
data1 = loadnc('runs/'+grid+'/'+name1+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')
print('done load')
data1 = ncdatasort(data1)
data2 = ncdatasort(data2)
print('done sort')

cages=None
with open('runs/'+grid+'/' +name2+ '/input/' +grid+ '_cage.dat') as f_in:
    cages=np.genfromtxt(f_in,skiprows=1)
    if len(cages)>0:
        cages=(cages[:,0]-1).astype(int)
    else:
        cages=None

region=regions(regionname)

savepath='figures/timeseries/' + grid + '_'  + '/curl_diff/' + name1+ '_'+ name2 + '_' + regionname + '_' +("%f" %cmin) + '_' + ("%f" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)
plt.close()




# Plot mesh
for i in range(starttime,endtime):
    print i
    ua=np.hstack([data1['ua'][i,:],0])
    va=np.hstack([data1['va'][i,:],0])
    dudy1= data1['a2u'][0,:]*ua[0:-1]+data1['a2u'][1,:]*ua[data1['nbe'][:,0]]+data1['a2u'][2,:]*ua[data1['nbe'][:,1]]+data1['a2u'][3,:]*ua[data1['nbe'][:,2]];
    dvdx1= data1['a1u'][0,:]*va[0:-1]+data1['a1u'][1,:]*va[data1['nbe'][:,0]]+data1['a1u'][2,:]*va[data1['nbe'][:,1]]+data1['a1u'][3,:]*va[data1['nbe'][:,2]];
    ua=np.hstack([data2['ua'][i,:],0])
    va=np.hstack([data2['va'][i,:],0])
    dudy2= data1['a2u'][0,:]*ua[0:-1]+data1['a2u'][1,:]*ua[data1['nbe'][:,0]]+data1['a2u'][2,:]*ua[data1['nbe'][:,1]]+data1['a2u'][3,:]*ua[data1['nbe'][:,2]];
    dvdx2= data1['a1u'][0,:]*va[0:-1]+data1['a1u'][1,:]*va[data1['nbe'][:,0]]+data1['a1u'][2,:]*va[data1['nbe'][:,1]]+data1['a1u'][3,:]*va[data1['nbe'][:,2]];
    
    #print np.mean(dvdx-dudy)
    #print np.min(dvdx-dudy)
    #print np.max(dvdx-dudy)
    #print np.std(dvdx-dudy)
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data1['trigrid'],(dvdx1-dudy1)-(dvdx2-dudy2),vmin=cmin,vmax=cmax)
    if cages!=None:   
        ax.plot(data2['uvnodell'][cages,0],data2['uvnodell'][cages,1],'w.',markersize=1) 
    prettyplot_ll(ax,setregion=region,cblabel='Curl',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_curl_diff_' + ("%04d" %(i)) + '.png',dpi=600)
    plt.close(f)
































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
import time
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
mpl.rcParams['contour.negative_linestyle'] = 'solid'

# Define names and types of data
name_orig='kit4_kelp_nodrag'
name_change='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'

#regionname='kit4_kelp_tight6'
regionlist=['kit4_ftb','kit4_crossdouble','kit4_kelp_tight2_small','kit4_kelp_tight2','kit4_kelp_tight4','kit4_kelp_tight5','kit4_kelp_tight6']
regionlist=['kit4_kelp_tight5','kit4_kelp_tight2_kelpfield']
starttime=384




### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name_orig+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name_change+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

cages=loadcage('runs/'+grid+'/' +name_change+ '/input/' +grid+ '_cage.dat')
if cages!=None:
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.1
    ls='solid'

savepath='figures/png/' + grid + '_'  + '/current_var_mag_ratio/' + name_orig + '_' + name_change + '/'
if not os.path.exists(savepath): os.makedirs(savepath)




for regionname in regionlist:
    print 'plotting region: ' +regionname

    region=regions(regionname)
    nidx=get_nodes(data,region)
    eidx=get_elements(data,region)


    start = time.clock()
    uvar_o=data['ua'][starttime:,:].var(axis=0)
    vvar_o=data['va'][starttime:,:].var(axis=0)
    uvar_c=data2['ua'][starttime:,:].var(axis=0)
    vvar_c=data2['va'][starttime:,:].var(axis=0)

    cvarm_o=np.sqrt(uvar_o+vvar_o)
    cvarm_c=np.sqrt(uvar_c+vvar_c)
    cvarm_rel=np.divide(cvarm_c,cvarm_o)*100

    print ('calc current mag: %f' % (time.clock() - start))

    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])
    clims=np.percentile(cvarm_rel[eidx],[1,99])
    trip=ax.tripcolor(data['trigrid'],cvarm_rel,vmin=clims[0],vmax=clims[1])
    prettyplot_ll(ax,setregion=region,cb=trip,cblabel='Ratio Current Var. Mag.',grid=True)

    f.savefig(savepath + grid + '_' + regionname+'_current_variance_magnitude_ratio.png',dpi=600)
    plt.close(f)












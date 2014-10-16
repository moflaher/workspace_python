from __future__ import division
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
name='kit4_kelp_20m_0.018'
grid='kit4'
regionlist=['kelparea2','kit4_crossdouble','kit4_ftb','kit4_kelp_tight','kit4_kelp_tight2_small','kit4_kelp_tight3','kit4_kelp_tight4','kit4_kelp_tight5','kit4_kelp_tight6']
datatype='2d'
starttime=384
cmin=-1
cmax=1


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'







savepath='figures/png/' + grid + '_' + datatype + '/ebbfld_instant_symmetry/'+name+'/'
if not os.path.exists(savepath): os.makedirs(savepath)
plt.close()

# Plot mesh
for i in range(0,len(regionlist)):
    print ("%d"%i)+"              "+("%f"%((i+1)/len(regionlist)*100)) 
    regionname=regionlist[i]
    region=regions(regionname)
    nidx=get_nodes(data,region)
    eidx=get_elements(data,region)

    zeta_grad=np.gradient(data['zeta'][starttime:,nidx])[0]
    fld=np.argmax(np.sum(zeta_grad,axis=1))
    ebb=np.argmin(np.sum(zeta_grad,axis=1))

    uf=data['ua'][starttime+fld,:]
    ue=data['ua'][starttime+ebb,:]
    vf=data['va'][starttime+fld,:]
    ve=data['va'][starttime+ebb,:]
    efs=np.divide(np.sqrt(uf**2+vf**2)-np.sqrt(ue**2+ve**2),np.sqrt(uf**2+vf**2)+np.sqrt(ue**2+ve**2))

    f=plt.figure()
    ax=plt.axes([.125,.1,.8,.8])  
    triax=ax.tripcolor(data['trigrid'],efs,vmin=cmin,vmax=cmax)
    prettyplot_ll(ax,setregion=region,cblabel=r'EbbFld Symmetry',cb=triax)
    #f.savefig(savepath + grid + '_'+name+'_' + regionname +'_ebbfld_symmetry.png',dpi=150)
    f.savefig(savepath + grid + '_'+name+'_' + regionname +'_ebbfld_symmetry.png',dpi=600)
    plt.close(f)































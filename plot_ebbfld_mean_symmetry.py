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
name='kit4_45days_3'
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

data['uvzeta']=(data['zeta'][starttime:,data['nv'][:,0]] + data['zeta'][starttime:,data['nv'][:,1]] + data['zeta'][starttime:,data['nv'][:,2]]) / 3.0
zeta_grad=np.gradient(data['uvzeta'])[0]

zeta_boolf=zeta_grad<0
zeta_boole=zeta_grad>0

uatmp=data['ua'][starttime:,:].copy()
uatmp[zeta_boolf]=np.nan
vatmp=data['va'][starttime:,:].copy()
vatmp[zeta_boolf]=np.nan
uf=np.nanmean(uatmp,axis=0)
vf=np.nanmean(vatmp,axis=0)
uatmp=data['ua'][starttime:,:].copy()
uatmp[zeta_boole]=np.nan
vatmp=data['va'][starttime:,:].copy()
vatmp[zeta_boole]=np.nan
ue=np.nanmean(uatmp,axis=0)
ve=np.nanmean(vatmp,axis=0)

efs=np.divide(np.sqrt(uf**2+vf**2)-np.sqrt(ue**2+ve**2),np.sqrt(uf**2+vf**2)+np.sqrt(ue**2+ve**2))

savepath='figures/png/' + grid + '_' + datatype + '/ebbfld_symmetry/'+name+'/'
if not os.path.exists(savepath): os.makedirs(savepath)
plt.close()

# Plot mesh
for i in range(0,len(regionlist)):
    print ("%d"%i)+"              "+("%f"%((i+1)/len(regionlist)*100)) 
    regionname=regionlist[i]
    region=regions(regionname)
    eidx=get_elements(data,region)

    f=plt.figure()
    ax=plt.axes([.125,.1,.8,.8])  
    triax=ax.tripcolor(data['trigrid'],efs,vmin=cmin,vmax=cmax)
    prettyplot_ll(ax,setregion=region,cblabel=r'EbbFld Symmetry',cb=triax)
    #f.savefig(savepath + grid + '_'+name+'_' + regionname +'_ebbfld_symmetry.png',dpi=150)
    f.savefig(savepath + grid + '_'+name+'_' + regionname +'_ebbfld_symmetry.png',dpi=600)
    plt.close(f)































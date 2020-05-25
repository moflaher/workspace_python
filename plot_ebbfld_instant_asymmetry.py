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
from matplotlib.collections import LineCollection as LC


# Define names and types of data
name='try16'
grid='beaufort3'
#regionlist=['kelparea2','kit4_crossdouble','kit4_ftb','kit4_kelp_tight','kit4_kelp_tight2_small','kit4_kelp_tight3','kit4_kelp_tight4','kit4_kelp_tight5','kit4_kelp_tight6']
regionlist=['beaufort3_southcoast']

starttime=0
cmin=-1
cmax=1


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')


#cages=np.genfromtxt('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat',skiprows=1)
#cages=(cages[:,0]-1).astype(int)



#tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
#color='g'
#lw=.5
#ls='solid'






savepath='figures/png/' + grid + '_'  + '/ebbfld_instant_asymmetry/'+name+'/'
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
    prettyplot_ll(ax,setregion=region,cblabel=r'Asymmetry',cb=triax)
    plotcoast(ax,filename='pacific.nc',color='k')

    #lseg1=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    #ax.add_collection(lseg1)

    for label in ax.get_yticklabels():
        label.set_fontsize(8)
    for label in ax.get_xticklabels():
        label.set_fontsize(8)

    #f.savefig(savepath + grid + '_'+name+'_' + regionname +'_ebbfld_symmetry.png',dpi=150)
    f.savefig(savepath + grid + '_'+name+'_' + regionname +'_ebbfld_asymmetry.png',dpi=600)
    plt.close(f)































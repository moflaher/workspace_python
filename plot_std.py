from __future__ import division
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import seawater as sw

# Define names and types of data
namelist=['kit4_kelp_20m_drag_0.018','kit4_kelp_20m_drag_0.007','kit4_kelp_20m_drag_0.011','kit4_kelp_nodrag']


for name in namelist:
    grid='kit4_kelp'
    datatype='2d'
    regionname='kit4_kelp_tight5'
    starttime=0


    ### load the .nc file #####
    data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
    print 'done load'
    data = ncdatasort(data,trifinder=True)
    print 'done sort'

    savepath='figures/png/' + grid + '_' + datatype + '/spatial_std/'
    if not os.path.exists(savepath): os.makedirs(savepath)

    cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
    if cages!=None:
        tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
        color='g'
        lw=.2
        ls='solid'

 
    region=regions(regionname)
    nidx=get_nodes(data,region)
    eidx=get_elements(data,region)
    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])
    ustd=np.std(data['ua'][starttime:],axis=0)
    triax=ax.tripcolor(data['trigrid'],ustd,vmin=ustd[eidx].min(),vmax=ustd[eidx].max())
    #if cages!=None:   
    #    lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    #    coast=ax.add_collection(lseg_t)
    #    coast.set_zorder(30)
    prettyplot_ll(ax,setregion=region,cb=triax,cblabel=r'Std (m/s)') 
    f.savefig(savepath + name+'_'+regionname+'_spatial_std_ua.png',dpi=600)
    plt.close(f)

    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])
    vstd=np.std(data['va'][starttime:],axis=0)
    triax=ax.tripcolor(data['trigrid'],vstd,vmin=vstd[eidx].min(),vmax=vstd[eidx].max())
    #if cages!=None:   
    #    lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    #    coast=ax.add_collection(lseg_t)
    #    coast.set_zorder(30)
    prettyplot_ll(ax,setregion=region,cb=triax,cblabel=r'Std (m/s)') 
    f.savefig(savepath + name+'_'+regionname+'_spatial_std_va.png',dpi=600)
    plt.close(f)




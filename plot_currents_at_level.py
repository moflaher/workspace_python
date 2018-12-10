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
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from matplotlib.collections import LineCollection as LC


# Define names and types of data
name='sfm6_musq2_old_cages'
grid='sfm6_musq2'
regionname='musq_cage_tight2'

starttime=0
spacing=125
scaleset=50
#remember 0 is surface and 19/9 is bottom
level=0

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')


region=regions(regionname)
sidx=equal_vectors(data,region,spacing)
nidx=get_nodes(data,region)

for level in range(0,19):

    if datatype=='2d':
        savepath='figures/png/' + grid + '_'  + '/currents_at_level/DA/'
        newu=data['ua']
        newv=data['va']
    else:
        savepath='figures/png/' + grid + '_'  + '/currents_at_level/'
        newu=data['u'][starttime:,level,:]
        newv=data['v'][starttime:,level,:]
    if not os.path.exists(savepath): os.makedirs(savepath)


    cages=np.genfromtxt('runs/'+grid+'/sfm6_musq2_all_cages/input/' +grid+ '_cage.dat',skiprows=1)
    cages=(cages[:,0]-1).astype(int)



    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=1
    ls='solid'




    zeta_grad=np.gradient(data['zeta'][starttime:,nidx])[0]


    #find biggest ebb and fld
    fld=np.argmax(np.sum(zeta_grad,axis=1))
    ebb=np.argmin(np.sum(zeta_grad,axis=1))


    #plot ebb vectors
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    uplot=newu[ebb,sidx].copy()
    vplot=newv[ebb,sidx].copy()
    tspeed=np.sqrt(uplot**2+vplot**2)
    uplot[tspeed<=.01]=np.nan
    vplot[tspeed<=.01]=np.nan
    triax=plt.tripcolor(data['trigrid'],data['h'],vmin=data['h'][nidx].min(),vmax=data['h'][nidx].max())
    lseg1=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    ax.add_collection(lseg1)
    prettyplot_ll(ax,setregion=region,cblabel=r'Depth (m)',cb=triax)
    ax_label_spacer(ax)
    Q=ax.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],uplot,vplot,angles='xy',scale_units='xy',scale=scaleset,zorder=10)
    qk = ax.quiverkey(Q,  .2,1.05,0.5, r'0.5 ms$^{-1}$', labelpos='W')
    if datatype=='2d':
        plt.savefig(savepath + name + '_' + regionname +'_vector_ebb_levelDA_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(ebb+starttime)) + '_with_bathy.png',dpi=600)
    else:
        plt.savefig(savepath + name + '_' + regionname +'_vector_ebb_level' +("%d" %level)+ '_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(ebb+starttime)) + '_with_bathy.png',dpi=600)

    plt.close(f)



    #plot fld vectors
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    uplot=newu[fld,sidx].copy()
    vplot=newv[fld,sidx].copy()
    tspeed=np.sqrt(uplot**2+vplot**2)
    uplot[tspeed<=.01]=np.nan
    vplot[tspeed<=.01]=np.nan
    triax=plt.tripcolor(data['trigrid'],data['h'],vmin=data['h'][nidx].min(),vmax=data['h'][nidx].max())
    lseg2=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    ax.add_collection(lseg2)
    prettyplot_ll(ax,setregion=region,cblabel=r'Depth (m)',cb=triax)
    Q=ax.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],uplot,vplot,angles='xy',scale_units='xy',scale=scaleset,zorder=10)
    qk = ax.quiverkey(Q,  .2,1.05,0.5, r'0.5 ms$^{-1}$', labelpos='W')
    if datatype=='2d':
        plt.savefig(savepath + name + '_' + regionname +'_vector_fld_levelDA_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(fld+starttime)) + '_with_bathy.png',dpi=600)
    else:
        plt.savefig(savepath + name + '_' + regionname +'_vector_fld_level' +("%d" %level)+ '_spacing_' + ("%d" %spacing) + 'm_at_time_' +("%d" %(fld+starttime)) + '_with_bathy.png',dpi=600)
    plt.close(f)


    #plot max speed
    #plt.close()
    #maxs=np.max(np.sqrt(newu**2+newv**2),axis=0)
    #plt.tripcolor(data['trigrid'],np.max(np.sqrt(newu**2+newv**2),axis=0),vmin=1.15*np.min(maxs[sidx]),vmax=.85*np.max(maxs[sidx]))
    #prettyplot_ll(plt.gca(),setregion=region,grid=True,cblabel=r'Max Speed (ms$^{-1}$)')
    #if datatype=='2d':
    #    plt.savefig(savepath + name + '_' + regionname +'_maxspeed_at_levelDA.png',dpi=1200)
    #else:
    #    plt.savefig(savepath + name + '_' + regionname +'_maxspeed_at_level_' + ("%d" %level)+ '.png',dpi=1200)




from __future__ import division
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name_orig='kit4_kelp_nodrag'
name_change='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'
datatype='2d'
#regionname='kit4_kelp_tight6'
regionlist=['kit4_ftb','kit4_crossdouble','kit4_kelp_tight2_small','kit4_kelp_tight2','kit4_kelp_tight4','kit4_kelp_tight5','kit4_kelp_tight6']
regionlist=['kit4_kelp_tight2_kelpfield','kit4_kelp_tight5']



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name_orig+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'








savepath='figures/png/' + grid + '_' + datatype + '/ttide_reldiff/' + name_orig + '_' + name_change + '/'
if not os.path.exists(savepath): os.makedirs(savepath)





#uv_orig=np.load('data/ttide/'+grid+'_'+name_orig+'_'+datatype+'_uv.npy')
#uv_orig=uv_orig[()]
#uv_change=np.load('data/ttide/'+grid+'_'+name_change+'_'+datatype+'_uv.npy')
#uv_change=uv_change[()]

el_orig=np.load('data/ttide/'+grid+'_'+name_orig+'_'+datatype+'_el_all.npy')
el_orig=el_orig[()]
el_change=np.load('data/ttide/'+grid+'_'+name_change+'_'+datatype+'_el_all.npy')
el_change=el_change[()]

for regionname in regionlist:
    print 'plotting region: ' +regionname

    region=regions(regionname)
    nidx=get_nodes(data,region)
    eidx=get_elements(data,region)

    
    con=np.argwhere(el_orig['nameu']=='M2  ').flatten()[0]


    f,ax=place_axes(region,3,cb=True) 
 
    clim=np.percentile(el_orig['tidecon'][nidx,con,0],[2,98])
    ax0cb=ax[0].tripcolor(data['trigrid'],el_orig['tidecon'][:,con,0],vmin=clim[0],vmax=clim[1])

    clim=np.percentile(el_change['tidecon'][nidx,con,0],[2,98])
    ax1cb=ax[1].tripcolor(data['trigrid'],el_change['tidecon'][:,con,0],vmin=clim[0],vmax=clim[1])

    clim=np.percentile((100*(el_change['tidecon'][:,con,0]-el_orig['tidecon'][:,con,0]))/(el_orig['tidecon'][:,con,0]+.01),[2,98])
    ax2cb=ax[2].tripcolor(data['trigrid'],(100*(el_change['tidecon'][:,con,0]-el_orig['tidecon'][:,con,0]))/(el_orig['tidecon'][:,con,0]+.01),vmin=clim[0],vmax=clim[1])
    
    ppll_sub(ax,setregion=region,cb=[ax0cb,ax1cb,ax2cb],cblabel=[r'M2 Amp. No Drag (m)',r'M2 Amp. Drag (m)',r'Relative difference (%)'],llfontsize=10,fontsize=8,cblabelsize=6,cbticksize=6,cbtickrotation=-45)
    ABC=['A','B','C']
    figW, figH = f.get_size_inches()
    plt.draw()
    for i,axi in enumerate(ax):
        plotcoast(ax[i],filename='pacific.nc',color='None',fill=True)
        axbb=ax[i].get_axes().get_position().bounds
        ax[i].annotate(ABC[i],xy=(axbb[0]+.0075,axbb[1]+axbb[3]-.03),xycoords='figure fraction')


    f.savefig(savepath + grid + '_' + regionname +'_el_m2_amp_reldiff.png',dpi=600)
    plt.close(f)



    f,ax=place_axes(region,3,cb=True) 
 
    clim=np.percentile(el_orig['tidecon'][nidx,con,2],[2,98])
    ax0cb=ax[0].tripcolor(data['trigrid'],el_orig['tidecon'][:,con,2],vmin=clim[0],vmax=clim[1])

    clim=np.percentile(el_change['tidecon'][nidx,con,2],[2,98])
    ax1cb=ax[1].tripcolor(data['trigrid'],el_change['tidecon'][:,con,2],vmin=clim[0],vmax=clim[1])

    clim=np.percentile((el_change['tidecon'][:,con,0]-el_orig['tidecon'][:,con,0]),[2,98])
    ax2cb=ax[2].tripcolor(data['trigrid'],el_change['tidecon'][:,con,0]-el_orig['tidecon'][:,con,0],vmin=clim[0],vmax=clim[1])
    
    ppll_sub(ax,setregion=region,cb=[ax0cb,ax1cb,ax2cb],cblabel=[r'M2 Phase No Drag ($\deg$)',r'M2 Phase Drag ($\deg$)',r'Relative difference ($\deg$)'],llfontsize=10,fontsize=8,cblabelsize=6,cbticksize=6,cbtickrotation=-45)
    ABC=['A','B','C']
    figW, figH = f.get_size_inches()
    plt.draw()
    for i,axi in enumerate(ax):
        plotcoast(ax[i],filename='pacific.nc',color='None',fill=True)
        axbb=ax[i].get_axes().get_position().bounds
        ax[i].annotate(ABC[i],xy=(axbb[0]+.0075,axbb[1]+axbb[3]-.03),xycoords='figure fraction')


    f.savefig(savepath + grid + '_' + regionname +'_el_m2_phase_diff.png',dpi=600)
    plt.close(f)












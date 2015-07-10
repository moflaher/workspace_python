from __future__ import division
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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name0='van_low_pre_redep_final'
name1='merged_7'
regionlist=['vhfr_whole','vhfr_tight','fr_whole','fr_mouth','pitt_lake','fr_area1','fr_area2','fr_area3']
datatype='2d'



### load the mesh files #####
data0=loadnei('/home/moe46/Desktop/school/grids/van_low/van_low_pre/'+name0+'.nei')
data0=get_nv(data0)
data0['x'],data0['y'],data0['proj']=lcc(data0['lon'],data0['lat'])
data0=ncdatasort(data0)
data0=get_sidelength(data0)

data1=loadnei('/home/moe46/Desktop/school/grids/fr_high/fr_50m_tight2/add_to_mesh/'+name1+'.nei')
data1['x'],data1['y'],data1['proj']=lcc(data1['lon'],data1['lat'])
data1=get_nv(data1)
data1=ncdatasort(data1)
data1=get_sidelength(data1)


savepath='figures/png/misc/mesh_compare/' + name0+'_'+name1 +'/'
if not os.path.exists(savepath): os.makedirs(savepath)



for regionname in regionlist:
    
    region=regions(regionname)
    nidx0=get_nodes(data0,region)
    eidx0=get_elements(data0,region)
    nidx1=get_nodes(data1,region)
    eidx1=get_elements(data1,region)

    if ((len(nidx1)==0) or (len(eidx1)==0)):
        continue
    
    print 'plotting region: ' +regionname


    # Plot mesh    
    f,ax=place_axes(region,2)  
    ax[0].triplot(data0['trigrid'],lw=.1)
    ax[1].triplot(data1['trigrid'],lw=.1)
    ppll_sub(ax,setregion=region,llfontsize=10,fontsize=8,cblabelsize=6,cbticksize=6,cbtickrotation=-45)
    ABC=['A','B']
    figW, figH = f.get_size_inches()
    plt.draw()
    for i,axi in enumerate(ax):
        plotcoast(ax[i],filename='pacific.nc',color='None',fill=True)
        axbb=ax[i].get_axes().get_position().bounds
        ax[i].annotate(ABC[i],xy=(axbb[0]+.0075,axbb[1]+axbb[3]-.03),xycoords='figure fraction')
    f.savefig(savepath + name0+'_'+name1 +'_'+regionname+'_mesh.png',dpi=600)
    plt.close(f)




    # Plot sidelength
    clims0=np.percentile(data0['sl'][eidx0],[1,99])
    clims1=np.percentile(data1['sl'][eidx1],[1,99])

    f,ax=place_axes(region,2,cb=True)  
    triax0=ax[0].tripcolor(data0['trigrid'],data0['sl'],vmin=clims0[0],vmax=clims0[1])
    triax1=ax[1].tripcolor(data1['trigrid'],data1['sl'],vmin=clims1[0],vmax=clims1[1])
    ppll_sub(ax,setregion=region,cb=[triax0,triax1],cblabel=['Sidelength (m)','Sidelength (m)'],llfontsize=10,fontsize=8,cblabelsize=6,cbticksize=6,cbtickrotation=-45)
    ABC=['A','B']
    figW, figH = f.get_size_inches()
    plt.draw()
    for i,axi in enumerate(ax):
        plotcoast(ax[i],filename='pacific.nc',color='None',fill=True)
        axbb=ax[i].get_axes().get_position().bounds
        ax[i].annotate(ABC[i],xy=(axbb[0]+.0075,axbb[1]+axbb[3]-.03),xycoords='figure fraction')
    f.savefig(savepath + name0+'_'+name1 +'_'+regionname+'_sidelength.png',dpi=600)
    plt.close(f)



















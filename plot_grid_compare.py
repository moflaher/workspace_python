from __future__ import division,print_function
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import scipy.io as sio
#from mpl_toolkits.basemap import Basemap
import os, sys
from mytools import *
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)



# Define names and types of data
name1='passbay_v4'
grid1='passbay_v4'
name2='uscoast_11'
grid2='passbay_v5'
regionlist=regions()
#regionlist=['fr_whole','fr_mouth','pitt_lake','fr_area1','fr_area2','vh_whole','firstnarrows','secondnarrows','vhfr_whole']
#regionlist=['kelp_channel']
regionlist=['gp','pp','gp_tight','dg','dg_upper','sfmwhole','bof','mp','pp','blackrock','blackrock_ebb','blackrock_fld','capedor','northgrid','northgrid_cape']
regionlist=['stjohn_nemo','bof_nemo','sfmwhole','musq_large','musq_cage','musq_cage_tight','musq_cage_tight2','musq','musq_4cage','passbay_all','lubec_passage','cobsbay','standrews','passbay_tight','grandmanan']
#regionlist=['standrews']
#regionlist=['passbay_tight','grandmanan']


### load the mesh files #####
data1=load_nei2fvcom('/home/moflaher/Desktop/work/compare_grid/passbay_v4.nei')
data1=get_sidelength(data1)

data2=load_nei2fvcom('/home/moflaher/Desktop/work/compare_grid/uscoast_11.nei')
data2=get_sidelength(data2)


savepath='figures/png/grid_compare_nocoast/' +grid1 + '_' +grid2 + '/'
if not os.path.exists(savepath): os.makedirs(savepath)



for regionname in regionlist:
    
    region=regions(regionname)
    nidx1=get_nodes(data1,region)
    eidx1=get_elements(data1,region)
    nidx2=get_nodes(data2,region)
    eidx2=get_elements(data2,region)

    if ((len(nidx1)==0) or (len(eidx1)==0)):
        continue
    
    print('plotting region: ' +regionname)


    # Plot mesh    
    f=plt.figure(figsize=(20,10))  
    ax0=f.add_axes([.125,.1,.375,.8])
    ax1=f.add_axes([.125+.375+.1,.1,.375,.8])
    ax0.triplot(data1['trigrid'],lw=.1,color='k')
    ax1.triplot(data2['trigrid'],lw=.1,color='k')
    ax0.axis(region['region'])
    ax1.axis(region['region'])
    #ppll_sub(ax,setregion=region,llfontsize=10,fontsize=8,cblabelsize=6,cbticksize=6,cbtickrotation=-45)
    #ABC=['A','B']
    #figW, figH = f.get_size_inches()
    #plt.draw()
    #for i,axi in enumerate(ax):
    #plotcoast(ax0,filename='mid_nwatl6c_sjh_lr.nc',color='k',fill=True,lw=.5)
    #plotcoast(ax1,filename='mid_nwatl6c_sjh_lr.nc',color='k',fill=True,lw=.5)
        #axbb=ax[i].get_axes().get_position().bounds
        #ax[i].annotate(ABC[i],xy=(axbb[0]+.0075,axbb[1]+axbb[3]-.03),xycoords='figure fraction')
    f.savefig(savepath + name1+'_'+name2 +'_'+regionname+'_mesh.png',dpi=300)
    plt.close(f)


    # # Plot mesh    
    # f,ax=plt.subplots(1,2,figsize=(20,10))  
    # ax[0].triplot(data1['trigrid'],lw=.1,color='k')
    # ax[1].triplot(data2['trigrid'],lw=.1,color='k')
    # ppll_sub(ax,setregion=region,llfontsize=10,fontsize=8,cblabelsize=6,cbticksize=6,cbtickrotation=-45)
    # ABC=['A','B']
    # figW, figH = f.get_size_inches()
    # plt.draw()
    # for i,axi in enumerate(ax):
        # plotcoast(ax[i],filename='mid_nwatl6c_sjh_lr.nc',color='k',fill=True,lw=.5)
        # #axbb=ax[i].get_axes().get_position().bounds
        # #ax[i].annotate(ABC[i],xy=(axbb[0]+.0075,axbb[1]+axbb[3]-.03),xycoords='figure fraction')
    # f.savefig(savepath + name1+'_'+name2 +'_'+regionname+'_mesh.png',dpi=300)
    # plt.close(f)



    ## Plot sidelength
    #clims0=np.percentile(np.vstack([data1['sl'][eidx1],data2['sl'][eidx2]]),[1,99])

    #f,ax=place_axes(region,2)  
    #triax0=ax[0].tripcolor(data1['trigrid'],data1['sl'],vmin=clims0[0],vmax=clims0[1])
    #triax1=ax[1].tripcolor(data2['trigrid'],data2['sl'],vmin=clims0[0],vmax=clims0[1])
    #ppll_sub(ax,setregion=region,cb=triax0,cblabel='Sidelength (m)',llfontsize=10,fontsize=8,cblabelsize=6,cbticksize=6,cbtickrotation=-45)
    #ABC=['A','B']
    #figW, figH = f.get_size_inches()
    #plt.draw()
    #for i,axi in enumerate(ax):
        #plotcoast(ax[i],filename='mid_nwatl6c_sjh_lr.nc',color='k',fill=True,lw=.5)
        #axbb=ax[i].get_axes().get_position().bounds
        #ax[i].annotate(ABC[i],xy=(axbb[0]+.0075,axbb[1]+axbb[3]-.03),xycoords='figure fraction')
    #f.savefig(savepath + name1+'_'+name2 +'_'+regionname+'_sidelength.png',dpi=300)
    #plt.close(f)

    ## Plot depth
    #clims0=np.percentile(np.vstack([data1['h'][nidx1],data2['h'][nidx2]]),[1,99])

    #f,ax=place_axes(region,2)  
    #triax0=ax[0].tripcolor(data1['trigrid'],data1['h'],vmin=clims0[0],vmax=clims0[1])
    #triax1=ax[1].tripcolor(data2['trigrid'],data2['h'],vmin=clims0[0],vmax=clims0[1])
    #ppll_sub(ax,setregion=region,cb=triax0,cblabel='Depth (m)',llfontsize=10,fontsize=8,cblabelsize=6,cbticksize=6,cbtickrotation=-45)
    #ABC=['A','B']
    #figW, figH = f.get_size_inches()
    #plt.draw()
    #for i,axi in enumerate(ax):
        #plotcoast(ax[i],filename='mid_nwatl6c_sjh_lr.nc',color='k',fill=True,lw=.5)
        #axbb=ax[i].get_axes().get_position().bounds
        #ax[i].annotate(ABC[i],xy=(axbb[0]+.0075,axbb[1]+axbb[3]-.03),xycoords='figure fraction')
    #f.savefig(savepath + name1+'_'+name2 +'_'+regionname+'_depth_percentile.png',dpi=300)
    #plt.close(f)


















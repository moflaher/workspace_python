from __future__ import division,print_function
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
import time
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
mpl.rcParams['contour.negative_linestyle'] = 'solid'

# Define names and types of data
name_orig='kit4_kelp_nodrag'
name_change1='kit4_kelp_20m_drag_0.007'
name_change2='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'
datatype='2d'
#regionname='kit4_kelp_tight6'
regionlist=['kit4_ftb','kit4_crossdouble','kit4_kelp_tight2_small','kit4_kelp_tight2','kit4_kelp_tight4','kit4_kelp_tight5','kit4_kelp_tight6']
regionlist=['kit4_kelp_tight5']#,'kit4_kelp_tight2_kelpfield']
starttime=621
endtime=1081

cbfix=True


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name_orig+'/output/',singlename=grid + '_0001.nc')
data1 = loadnc('runs/'+grid+'/'+name_change1+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name_change2+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')





cages=loadcage('runs/'+grid+'/' +name_change2+ '/input/' +grid+ '_cage.dat')
if np.shape(cages)!=():
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.1
    ls='solid'


for regionname in regionlist:
    print 'plotting region: ' +regionname

    region=regions(regionname)
    nidx=get_nodes(data,region)
    eidx=get_elements(data,region)


    savepath='figures/png/' + grid + '_' + datatype + '/zeta_std_subplot_interp/' + name_orig + '_' + name_change1 + '_' + name_change2 + '/'
    if not os.path.exists(savepath): os.makedirs(savepath)

    start = time.clock()


    cvarm_o=data['zeta'][starttime:endtime,:].std(axis=0)
    cvarm_c1=data1['zeta'][starttime:endtime,:].std(axis=0)
    cvarm_c2=data2['zeta'][starttime:endtime,:].std(axis=0)

    cvarm_diff1=cvarm_c1-cvarm_o
    cvarm_diff2=cvarm_c2-cvarm_o
    cvarm_diff_rel1=np.divide(cvarm_diff1,cvarm_o)*100
    cvarm_diff_rel2=np.divide(cvarm_diff2,cvarm_o)*100

    print ('calc zeta std: %f' % (time.clock() - start))


    ngridx = 2000
    ngridy = 2000


    start = time.clock()
    xi = np.linspace(region['region'][0],region['region'][1], ngridx)
    yi = np.linspace(region['region'][2],region['region'][3], ngridy)
    cvarm_o_interp=mpl.mlab.griddata(data['nodell'][:,0],data['nodell'][:,1], cvarm_o, xi, yi)
    cvarm_diff_rel_interp1=mpl.mlab.griddata(data['nodell'][:,0],data['nodell'][:,1], cvarm_diff_rel1, xi, yi)
    cvarm_diff_rel_interp2=mpl.mlab.griddata(data['nodell'][:,0],data['nodell'][:,1], cvarm_diff_rel2, xi, yi)

    tmpxy=np.meshgrid(xi,yi)
    xii=tmpxy[0]
    yii=tmpxy[1]
    host=data['trigrid'].get_trifinder().__call__(xii,yii)

    cvarm_o_interp_mask = np.ma.masked_where(host==-1,cvarm_o_interp)
    cvarm_diff_rel_interp_mask1 = np.ma.masked_where(host==-1,cvarm_diff_rel_interp1)
    cvarm_diff_rel_interp_mask2 = np.ma.masked_where(host==-1,cvarm_diff_rel_interp2)

    print ('griddata interp: %f' % (time.clock() - start))


    f,ax=place_axes(region,3,cb=True)  

    fmt=r'%d'

    if cbfix==True:
        V=np.array([-80,-70,-60,-50,-40,-30,-20,-10,0,2,4,6,8,10,12,14,16,18,20])
        Vpos=np.array([0,2,4,6,8,10,12,14,16,18,20])
        Vneg=np.array([-80,-70,-60,-50,-40,-30,-20,-10])
        Vpos=np.array([0,4,8,12,16,20])
        Vneg=np.array([-60,-30,0])
        #V=np.array([-80,-60,-40,-20,0,5,10,15,20])
        clims0=np.percentile(cvarm_o_interp_mask,[1,99])
        ax0cb=ax[0].pcolormesh(xi,yi,cvarm_o_interp_mask,vmin=clims0[0],vmax=clims0[1])
        ax1cb=ax[1].pcolormesh(xi,yi,cvarm_diff_rel_interp_mask1,vmin=-.25,vmax=.25,cmap=mpl.cm.seismic)
        ax2cb=ax[2].pcolormesh(xi,yi,cvarm_diff_rel_interp_mask2,vmin=-.25,vmax=.25,cmap=mpl.cm.seismic)
        #CS2=ax[2].contour(xi,yi,cvarm_diff_rel_interp_mask,Vpos,colors='k',zorder=30,linestyles='solid',linewidths=.5)
        #ax[2].clabel(CS2, fontsize=4, inline=1,zorder=30,fmt=fmt)
        #CS3=ax[2].contour(xi,yi,cvarm_diff_rel_interp_mask,Vneg,colors='w',zorder=30,linestyles='solid',linewidths=.5)
        #ax[2].clabel(CS3, fontsize=4, inline=1,zorder=30,fmt=fmt)
    else:
        clims0=np.percentile(cvarm_o_interp_mask,[1,99])
        clims1=np.percentile(cvarm_diff_rel_interp_mask1,[1,99])
        clims2=np.percentile(cvarm_diff_rel_interp_mask2,[1,99])
        ax0cb=ax[0].pcolormesh(xi,yi,cvarm_o_interp_mask,vmin=clims0[0],vmax=clims0[1])
        ax1cb=ax[1].pcolormesh(xi,yi,cvarm_diff_rel_interp_mask1,vmin=clims1[0],vmax=clims1[1],cmap=mpl.cm.seismic)
        ax2cb=ax[2].pcolormesh(xi,yi,cvarm_diff_rel_interp_mask2,vmin=clims2[0],vmax=clims2[1],cmap=mpl.cm.seismic)
        #CS2=ax[2].contour(xi,yi,cvarm_diff_rel_interp_mask,colors='w',zorder=30,linestyles='dashed')
        #ax[2].clabel(CS2, fontsize=6, inline=1,zorder=30,fmt=fmt)



    ppll_sub(ax,setregion=region,cb=[ax0cb,ax1cb,ax2cb],cblabel=[r'Elevation STD (m)',r'Relative difference (%)',r'Relative difference (%)'],llfontsize=10,fontsize=8,cblabelsize=6,cbticksize=6,cbtickrotation=-45)

    ABC=['A','B','C']
    figW, figH = f.get_size_inches()
    plt.draw()
    for i,axi in enumerate(ax):
        plotcoast(ax[i],filename='pacific.nc',color='None',fill=True)
        axbb=ax[i].get_axes().get_position().bounds
        ax[i].annotate(ABC[i],xy=(axbb[0]+.0075,axbb[1]+axbb[3]-.03),xycoords='figure fraction')
#    lseg_t1=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
#    ax[1].add_collection(lseg_t1)
#    lseg_t2=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
#    ax[2].add_collection(lseg_t2)


    f.savefig(savepath + grid + '_' + regionname+'_zeta_std_subplot.png',dpi=600)
    plt.close(f)












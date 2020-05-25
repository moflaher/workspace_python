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
name_orig='kit4_45days_3'
name_change='kit4_kelp_20m_0.018'
name_change2='kit4_kelp_20m_0.007'
grid='kit4'

#regionname='kit4_kelp_tight6'
regionlist=['kit4_ftb','kit4_crossdouble','kit4_kelp_tight2_small','kit4_kelp_tight2','kit4_kelp_tight4','kit4_kelp_tight5','kit4_kelp_tight6']
regionlist=['kit4_kelp_tight2_small']
starttime=384

cbfix=True


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name_orig+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name_change+'/output/',singlename=grid + '_0001.nc')
data3 = loadnc('runs/'+grid+'/'+name_change2+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')





cages=np.genfromtxt('runs/'+grid+'/' +name_change+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)


for regionname in regionlist:
    print 'plotting region: ' +regionname

    region=regions(regionname)
    nidx=get_nodes(data,region)
    eidx=get_elements(data,region)

    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.5
    ls='solid'



    savepath='figures/png/' + grid + '_'  + '/current_var_mag_subplot3runs_interp/' + name_orig + '_' + name_change + '/'
    if not os.path.exists(savepath): os.makedirs(savepath)

    start = time.clock()
    uvar_o=data['ua'][starttime:,:].var(axis=0)
    vvar_o=data['va'][starttime:,:].var(axis=0)
    uvar_c=data2['ua'][starttime:,:].var(axis=0)
    vvar_c=data2['va'][starttime:,:].var(axis=0)
    uvar_c2=data3['ua'][starttime:,:].var(axis=0)
    vvar_c2=data3['va'][starttime:,:].var(axis=0)

    cvarm_o=np.sqrt(uvar_o+vvar_o)
    cvarm_c=np.sqrt(uvar_c+vvar_c)
    cvarm_c2=np.sqrt(uvar_c2+vvar_c2)

    cvarm_diff=cvarm_c-cvarm_o
    cvarm_diff2=cvarm_c2-cvarm_o
    cvarm_diff_rel=np.divide(cvarm_diff,cvarm_o)*100
    cvarm_diff2_rel=np.divide(cvarm_diff2,cvarm_o)*100

    print ('calc current mag: %f' % (time.clock() - start))


    ngridx = 500
    ngridy = 500


    start = time.clock()
    xi = np.linspace(region['region'][0],region['region'][1], ngridx)
    yi = np.linspace(region['region'][2],region['region'][3], ngridy)
    cvarm_o_interp=mpl.mlab.griddata(data['uvnodell'][:,0],data['uvnodell'][:,1], cvarm_o, xi, yi)
    cvarm_diff_rel_interp=mpl.mlab.griddata(data['uvnodell'][:,0],data['uvnodell'][:,1], cvarm_diff_rel, xi, yi)
    cvarm_diff2_rel_interp=mpl.mlab.griddata(data['uvnodell'][:,0],data['uvnodell'][:,1], cvarm_diff2_rel, xi, yi)

    tmpxy=np.meshgrid(xi,yi)
    xii=tmpxy[0]
    yii=tmpxy[1]
    host=data['trigrid'].get_trifinder().__call__(xii,yii)

    cvarm_o_interp_mask = np.ma.masked_where(host==-1,cvarm_o_interp)
    cvarm_diff_rel_interp_mask = np.ma.masked_where(host==-1,cvarm_diff_rel_interp)
    cvarm_diff2_rel_interp_mask = np.ma.masked_where(host==-1,cvarm_diff2_rel_interp)

    print ('griddata interp: %f' % (time.clock() - start))



    f=plt.figure()

    xtarget=.25
    ytarget=.675

    aspect=get_aspectratio(region)
    dr=get_data_ratio(region)
    figW, figH = f.get_size_inches()
    fa = figH / figW

    if aspect>=1.1:    
        finalspace=((ytarget*fa)/aspect/dr)
        if finalspace>.265:
            finalspace[0]=.265
            ax0f=[.125,.275,finalspace[0],ytarget]
            ax1f=[ax0f[0]+finalspace[0]+.025,.275,finalspace[0],ytarget]
            ax2f=[ax1f[0]+finalspace[0]+.025,.275,finalspace[0],ytarget]
        else:
            ax0f=[.125,.275,1,ytarget]
            ax1f=[ax0f[0]+finalspace[0]+.025,.275,1,ytarget]
            ax2f=[ax1f[0]+finalspace[0]+.025,.275,1,ytarget]
    else:    
        finalspace=((((xtarget*fa)/aspect/dr)*aspect*dr)/fa)
        #ax1f=[.125,.1,.75,xtarget]
        #ax0f=[.125,ax1f[1]+finalspace[0]+.05,.75,xtarget]
        #finalspace=((ytarget*fa)/aspect/dr)
        ax2f=[.125,.1,1,xtarget]
        ax1f=[.125,ax2f[1]+finalspace[0]+.025,1,xtarget]
        ax0f=[.125,ax1f[1]+finalspace[0]+.025,1,xtarget]




    ax0=f.add_axes(ax0f)
    ax1=f.add_axes(ax1f)
    ax2=f.add_axes(ax2f)

    fmt=r'%d'

    if cbfix==True:
        V=np.array([-80,-70,-60,-50,-40,-30,-20,-10,0,2,4,6,8,10,12,14,16,18,20])
        Vpos=np.array([0,2,4,6,8,10,12,14,16,18,20])
        Vneg=np.array([-80,-60,-40,-20])
        #V=np.array([-80,-60,-40,-20,0,5,10,15,20])
        ax0cb=ax0.pcolor(xi,yi,cvarm_o_interp_mask)
        ax1cb=ax1.pcolor(xi,yi,cvarm_diff_rel_interp_mask,vmin=-80,vmax=40)
        ax2cb=ax2.pcolor(xi,yi,cvarm_diff2_rel_interp_mask,vmin=-80,vmax=40)
        CS2=ax1.contour(xi,yi,cvarm_diff_rel_interp_mask,Vpos,colors='w',zorder=30,linestyles='dashed')
        ax1.clabel(CS2, fontsize=6, inline=1,zorder=30,fmt=fmt)
        CS3=ax1.contour(xi,yi,cvarm_diff_rel_interp_mask,Vneg,colors='w',zorder=30,linestyles='solid')
        ax1.clabel(CS3, fontsize=6, inline=1,zorder=30,fmt=fmt)

        CS4=ax2.contour(xi,yi,cvarm_diff2_rel_interp_mask,Vpos,colors='w',zorder=30,linestyles='dashed')
        ax2.clabel(CS4, fontsize=6, inline=1,zorder=30,fmt=fmt)
        CS5=ax2.contour(xi,yi,cvarm_diff2_rel_interp_mask,Vneg,colors='w',zorder=30,linestyles='solid')
        ax2.clabel(CS5, fontsize=6, inline=1,zorder=30,fmt=fmt)
        #line=[-129.48666,52.62,52.68]
        line=[-129.48833,52.62,52.68]
        ax0.plot([line[0],line[0]],[line[1],line[2]],'k',lw=2)
        ax1.plot([line[0],line[0]],[line[1],line[2]],'k',lw=2)
        ax2.plot([line[0],line[0]],[line[1],line[2]],'k',lw=2)
    else:
        ax0cb=ax0.pcolor(xi,yi,cvarm_o_interp_mask)
        ax1cb=ax1.pcolor(xi,yi,cvarm_diff_rel_interp_mask)
        ax2cb=ax2.pcolor(xi,yi,cvarm_diff2_rel_interp_mask)
        CS2=ax1.contour(xi,yi,cvarm_diff_rel_interp_mask,colors='w',zorder=30,linestyles='dashed')
        ax1.clabel(CS2, fontsize=6, inline=1,zorder=30,fmt=fmt)
        CS3=ax2.contour(xi,yi,cvarm_diff2_rel_interp_mask,colors='w',zorder=30,linestyles='dashed')
        ax2.clabel(CS3, fontsize=6, inline=1,zorder=30,fmt=fmt)


    prettyplot_ll(ax0,setregion=region)
    prettyplot_ll(ax1,setregion=region)
    prettyplot_ll(ax2,setregion=region)
    ax_label_spacer(ax0)
    ax_label_spacer(ax1)
    ax_label_spacer(ax2)


    if aspect>=1.1:
        ax1.yaxis.set_tick_params(labelleft='off')
        ax2.yaxis.set_tick_params(labelleft='off')
    else:
        ax0.xaxis.set_tick_params(labelleft='off')
        ax0.set_xlabel('')
        ax1.xaxis.set_tick_params(labelleft='off')
        ax1.set_xlabel('')

    plt.draw()
    ax0bb=ax0.get_axes().get_position().bounds
    ax1bb=ax1.get_axes().get_position().bounds
    ax2bb=ax2.get_axes().get_position().bounds

    if aspect>=1.1:
        ax0ca=f.add_axes([ax0bb[0],ax0bb[1]-.125,ax0bb[2],0.025])
        ax1ca=f.add_axes([ax1bb[0],ax1bb[1]-.125,ax1bb[2],0.025])
        ax2ca=f.add_axes([ax2bb[0],ax2bb[1]-.125,ax2bb[2],0.025])
        cb=plt.colorbar(ax0cb,cax=ax0ca,orientation='horizontal')
        cb.set_label(r'Current variance magnitude (m s$^{-1}$)',fontsize=6)
        for label in cb.ax.get_xticklabels():
            label.set_rotation(90)

        cb2=plt.colorbar(ax1cb,cax=ax1ca,orientation='horizontal')
        cb2.set_label(r'Relative difference (%)',fontsize=6)
        ax1.set_ylabel('')
        for label in cb2.ax.get_xticklabels():
            label.set_rotation(90)

        cb3=plt.colorbar(ax2cb,cax=ax2ca,orientation='horizontal')
        cb3.set_label(r'Relative difference (%)',fontsize=6)
        ax2.set_ylabel('')
        for label in cb3.ax.get_xticklabels():
            label.set_rotation(90)


    else:
        ax0ca=f.add_axes([ax0bb[0]+ax0bb[2]+.025,ax0bb[1],.025,ax0bb[3]])
        ax1ca=f.add_axes([ax1bb[0]+ax1bb[2]+.025,ax1bb[1],.025,ax1bb[3]])
        ax2ca=f.add_axes([ax2bb[0]+ax2bb[2]+.025,ax2bb[1],.025,ax2bb[3]])
        cb=plt.colorbar(ax0cb,cax=ax0ca)
        cb.set_label(r'Current variance magnitude (m s$^{-1}$)',fontsize=8)
        cb2=plt.colorbar(ax1cb,cax=ax1ca)
        cb2.set_label(r'Relative difference (%)',fontsize=8)
        cb3=plt.colorbar(ax2cb,cax=ax2ca)
        cb3.set_label(r'Relative difference (%)',fontsize=8)

    plotcoast(ax0,filename='pacific.nc',color='k')
    plotcoast(ax1,filename='pacific.nc',color='k')
    plotcoast(ax2,filename='pacific.nc',color='k')


    lseg0=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    ax0.add_collection(lseg0)
    lseg1=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    ax1.add_collection(lseg1)
    lseg2=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    ax2.add_collection(lseg2)

    ax0.annotate("A",xy=(.025,1-(.05/dr)),xycoords='axes fraction')
    ax1.annotate("B",xy=(.025,1-(.05/dr)),xycoords='axes fraction')
    ax2.annotate("C",xy=(.025,1-(.05/dr)),xycoords='axes fraction')

    #add_num_label(ax1,data,1000,74845,'e')

    #plotcoast(ax0,filename='pacific.nc',color='k')
    #plotcoast(ax1,filename='pacific.nc',color='k')

    f.savefig(savepath + grid + '_' + regionname+'_current_variance_magnitude_diff_relative_subplot3runs_contour.png',dpi=600)
    plt.close('all')












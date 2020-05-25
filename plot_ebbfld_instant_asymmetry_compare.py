from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from misctools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
from matplotlib.collections import LineCollection as LC


# Define names and types of data
name='kit4_45days_3'
name2='kit4_kelp_20m_0.018'
grid='kit4'
#regionname='kit4_kelp_tight2'
regionlist=['kit4_ftb','kit4_crossdouble','kit4_kelp_tight2_small','kit4_kelp_tight2','kit4_kelp_tight4','kit4_kelp_tight5','kit4_kelp_tight6']

starttime=384
cmin=-0.8
cmax=0.8


data_f=[.125,.515,.825,.425]
data2_f=[.125,.075,.825,.425]
ABC=[.025,.9]


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

cages=np.genfromtxt('runs/'+grid+'/' +name2+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)

tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
color='g'
lw=.5
ls='solid'

savepath='figures/png/' + grid + '_'  + '/ebbfld_instant_asymmetry_subplots/'+name+'_'+name2+'/'
if not os.path.exists(savepath): os.makedirs(savepath)




for regionname in regionlist:
    print 'plotting ' + regionname
    region=regions(regionname)
    nidx=get_nodes(data,region)
    eidx=get_elements(data,region)

    zeta_grad=np.gradient(data2['zeta'][starttime:,nidx])[0]
    fld=np.argmax(np.sum(zeta_grad,axis=1))
    ebb=np.argmin(np.sum(zeta_grad,axis=1))

        
    f=plt.figure()

    xtarget=.4
    ytarget=.675
    aspect=get_aspectratio(region)
    dr=get_data_ratio(region)
    figW, figH = f.get_size_inches()
    fa = figH / figW

    if aspect>=1.1:    
        finalspace=((ytarget*fa)/aspect/dr)
        if finalspace>.4:
            finalspace[0]=.4
            ax0f=[.125,.275,finalspace[0],ytarget]
            ax1f=[ax0f[0]+finalspace[0]+.025,.275,finalspace[0],ytarget]
        else:
            ax0f=[.125,.275,1,ytarget]
            ax1f=[ax0f[0]+finalspace[0]+.025,.275,1,ytarget]
    else:    
        finalspace=((((xtarget*fa)/aspect/dr)*aspect*dr)/fa)
        #ax1f=[.125,.1,.75,xtarget]
        #ax0f=[.125,ax1f[1]+finalspace[0]+.05,.75,xtarget]
        #finalspace=((ytarget*fa)/aspect/dr)
        ax1f=[.125,.1,1,xtarget]
        ax0f=[.125,ax1f[1]+finalspace[0]+.025,1,xtarget]


    uf=data['ua'][starttime+fld,:]
    ue=data['ua'][starttime+ebb,:]
    vf=data['va'][starttime+fld,:]
    ve=data['va'][starttime+ebb,:]
    efs=np.divide(np.sqrt(uf**2+vf**2)-np.sqrt(ue**2+ve**2),np.sqrt(uf**2+vf**2)+np.sqrt(ue**2+ve**2))
    #print runstats(efs[eidx])
    ax0=f.add_axes(ax0f)  
    axtri0=ax0.tripcolor(data['trigrid'],efs,vmin=cmin,vmax=cmax)

    uf=data2['ua'][starttime+fld,:]
    ue=data2['ua'][starttime+ebb,:]
    vf=data2['va'][starttime+fld,:]
    ve=data2['va'][starttime+ebb,:]
    efs=np.divide(np.sqrt(uf**2+vf**2)-np.sqrt(ue**2+ve**2),np.sqrt(uf**2+vf**2)+np.sqrt(ue**2+ve**2))
    #print runstats(efs[eidx])
    ax1=f.add_axes(ax1f)  
    axtri1=ax1.tripcolor(data['trigrid'],efs,vmin=cmin,vmax=cmax)

    prettyplot_ll(ax0,setregion=region)
    prettyplot_ll(ax1,setregion=region)
    ax_label_spacer(ax0)
    ax_label_spacer(ax1)

    if aspect>=1.1:
        ax1.yaxis.set_tick_params(labelleft='off')
    else:
        ax0.xaxis.set_tick_params(labelleft='off')
        ax0.set_xlabel('')

    plt.draw()
    ax0bb=ax0.get_axes().get_position().bounds
    ax1bb=ax1.get_axes().get_position().bounds

    if aspect>=1.1:
        ax0ca=f.add_axes([ax0bb[0],ax0bb[1]-.125,ax0bb[2],0.025])
        ax1ca=f.add_axes([ax1bb[0],ax1bb[1]-.125,ax1bb[2],0.025])
        cb=plt.colorbar(axtri0,cax=ax0ca,orientation='horizontal')
        cb.set_label(r'Asymmetry',fontsize=6)
        for label in cb.ax.get_xticklabels():
            label.set_rotation(90)

        cb2=plt.colorbar(axtri1,cax=ax1ca,orientation='horizontal')
        cb2.set_label(r'Asymmetry',fontsize=6)
        ax1.set_ylabel('')
        for label in cb2.ax.get_xticklabels():
            label.set_rotation(90)

    else:
        ax0ca=f.add_axes([ax0bb[0]+ax0bb[2]+.025,ax0bb[1],.025,ax0bb[3]])
        ax1ca=f.add_axes([ax1bb[0]+ax1bb[2]+.025,ax1bb[1],.025,ax1bb[3]])
        cb=plt.colorbar(axtri0,cax=ax0ca)
        cb.set_label(r'Asymmetry',fontsize=8)
        cb2=plt.colorbar(axtri1,cax=ax1ca)
        cb2.set_label(r'Asymmetry',fontsize=8)

    plotcoast(ax0,filename='pacific.nc',color='k')
    lseg0=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    ax0.add_collection(lseg0)

    plotcoast(ax1,filename='pacific.nc',color='k')
    lseg1=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    ax1.add_collection(lseg1)

    ax0.text(ABC[0],ABC[1],"A",transform=ax0.transAxes)#,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3},zorder=31)
    ax1.text(ABC[0],ABC[1],"B",transform=ax1.transAxes)#,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3},zorder=31)

    f.savefig(savepath + grid + '_'+name+'_'+name2+'_' + regionname +'_ebbfld_asymmetry.png',dpi=600)
    plt.close(f)































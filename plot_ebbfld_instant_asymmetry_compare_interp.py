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
import time

# Define names and types of data
name='kit4_kelp_nodrag'
name_change='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'
#regionname='kit4_kelp_tight2'
regionlist=['kit4_ftb','kit4_kelp_tight2_small','kit4_kelp_tight5','kit4_kelp_tight2_kelpfield']
#regionlist=['kit4_kelp_tight2_kelpfield']

starttime=384
cmin=-1
cmax=1
fmt=r'%1.1f'


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name_change+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

cages=np.genfromtxt('runs/'+grid+'/' +name_change+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)

tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
color='g'
lw=.1
ls='solid'

savepath='figures/png/' + grid + '_'  + '/ebbfld_instant_asymmetry_subplots_interp/'+name+'_'+name_change+'/'
if not os.path.exists(savepath): os.makedirs(savepath)




for regionname in regionlist:
    print 'plotting ' + regionname

    region=regions(regionname)
    nidx=get_nodes(data,region)
    eidx=get_elements(data,region)

    zeta_grad=np.gradient(data2['zeta'][starttime:,nidx])[0]
    fld=np.argmax(np.sum(zeta_grad,axis=1))
    ebb=np.argmin(np.sum(zeta_grad,axis=1))

        
    f,ax=place_axes(region,2,cb=True)  

    uf=data['ua'][starttime+fld,:]
    ue=data['ua'][starttime+ebb,:]
    vf=data['va'][starttime+fld,:]
    ve=data['va'][starttime+ebb,:]
    efs=np.divide(np.sqrt(uf**2+vf**2)-np.sqrt(ue**2+ve**2),np.sqrt(uf**2+vf**2)+np.sqrt(ue**2+ve**2))
    #print runstats(efs[eidx])
    ngridx = 2000
    ngridy = 2000
    start = time.clock()
    xi = np.linspace(region['region'][0],region['region'][1], ngridx)
    yi = np.linspace(region['region'][2],region['region'][3], ngridy)
    efs_interp=mpl.mlab.griddata(data['uvnodell'][:,0],data['uvnodell'][:,1], efs, xi, yi)
    tmpxy=np.meshgrid(xi,yi)
    xii=tmpxy[0]
    yii=tmpxy[1]
    host=data['trigrid'].get_trifinder().__call__(xii,yii)
    efs_interp_mask = np.ma.masked_where(host==-1,efs_interp)
    print ('griddata interp: %f' % (time.clock() - start))
 
    axtri=ax[0].pcolormesh(xi,yi,efs_interp_mask,vmin=cmin,vmax=cmax)
    Vpos=np.array([0,.4,.8])
    Vneg=np.array([-.8,-.4])
    CS2=ax[0].contour(xi,yi,efs_interp_mask,Vpos,colors='k',zorder=30,linestyles='solid',linewidths=.5)
    ax[0].clabel(CS2, fontsize=4, inline=1,zorder=30,fmt=fmt)
    CS3=ax[0].contour(xi,yi,efs_interp_mask,Vneg,colors='w',zorder=30,linestyles='solid',linewidths=.5)
    ax[0].clabel(CS3, fontsize=4, inline=1,zorder=30,fmt=fmt)




    uf=data2['ua'][starttime+fld,:]
    ue=data2['ua'][starttime+ebb,:]
    vf=data2['va'][starttime+fld,:]
    ve=data2['va'][starttime+ebb,:]
    efs=np.divide(np.sqrt(uf**2+vf**2)-np.sqrt(ue**2+ve**2),np.sqrt(uf**2+vf**2)+np.sqrt(ue**2+ve**2))
    start = time.clock()    
    efs_interp=mpl.mlab.griddata(data['uvnodell'][:,0],data['uvnodell'][:,1], efs, xi, yi)
    efs_interp_mask = np.ma.masked_where(host==-1,efs_interp)
    print ('griddata interp: %f' % (time.clock() - start))
 
    axtri=ax[1].pcolormesh(xi,yi,efs_interp_mask,vmin=cmin,vmax=cmax)
    Vpos=np.array([0,.4,.8])
    Vneg=np.array([-.8,-.4])
    CS2=ax[1].contour(xi,yi,efs_interp_mask,Vpos,colors='k',zorder=30,linestyles='solid',linewidths=.5)
    ax[1].clabel(CS2, fontsize=4, inline=1,zorder=30,fmt=fmt)
    CS3=ax[1].contour(xi,yi,efs_interp_mask,Vneg,colors='w',zorder=30,linestyles='solid',linewidths=.5)
    ax[1].clabel(CS3, fontsize=4, inline=1,zorder=30,fmt=fmt)


    ppll_sub(ax,setregion=region,cb=axtri,cblabel='Asymmetry')    
    ABC=['A','B','C']
    figW, figH = f.get_size_inches()
    for i,axi in enumerate(ax):
        plotcoast(ax[i],filename='pacific.nc',color='None',fill=True)
        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        ax[i].add_collection(lseg_t)
        ax[i].annotate(ABC[i],xy=(.025,1-.05/get_data_ratio(region)/(figH/figW)),xycoords='axes fraction')


    f.savefig(savepath + grid + '_'+name+'_'+name_change+'_' + regionname +'_ebbfld_asymmetry.png',dpi=600)
    plt.close('all')































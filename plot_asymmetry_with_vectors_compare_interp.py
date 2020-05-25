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
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
sys.path.append('/home/moe46/Desktop/school/workspace_python/ttide_py/ttide/')
sys.path.append('/home/moflaher/Desktop/workspace_python/ttide_py/ttide/')
from t_tide import t_tide
from t_predic import t_predic
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import time


# Define names and types of data
name_orig='kit4_kelp_nodrag'
name_change='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'
regionlist=['kit4_kelp_tight2_kelpfield']#,'kit4_kelp_tight2_kelpfield']#,'kit4_kelp_tight2_small']

starttime=384
offset=0
fontsize=6
cmin=-1
cmax=1


usemean=True

kl=[.815,.815]
kl=[.8,.025]

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name_orig+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name_change+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

cages=loadcage('runs/'+grid+'/' +name_change+ '/input/' +grid+ '_cage.dat')
if np.shape(cages)!=():
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.4
    ls='solid'

savepath='figures/png/' + grid + '_'  + '/asymmetry_compare_interp_with_vectors/'
if not os.path.exists(savepath): os.makedirs(savepath)



for regionname in regionlist:


    vectorspacing=400#2000*np.diff(region['region'][0:2])
    ebbfld=.2#np.ceil(10*np.linalg.norm(np.vstack([q2u1,q2v1]),axis=0).mean())/10
    scale1=60#np.sqrt(ebbfld*(vectorspacing*2)**2)


    vectorspacing=100#2000*np.diff(region['region'][0:2])
    ebbfld=.2#np.ceil(10*np.linalg.norm(np.vstack([q2u1,q2v1]),axis=0).mean())/10
    scale1=200#np.sqrt(ebbfld*(vectorspacing*2)**2)

    ebbfldscale=('%.1f'%ebbfld)

    region=regions(regionname)
    nidx=get_nodes(data,region)    
    eidx=get_elements(data,    expand_region(region.copy(),1000))
    vidx=equal_vectors(data,region,vectorspacing)
    evidx=np.in1d(eidx,vidx)


    if usemean==True:
        data['uvzeta']=(data['zeta'][starttime:,data['nv'][eidx,0]] + data['zeta'][starttime:,data['nv'][eidx,1]] + data['zeta'][starttime:,data['nv'][eidx,2]]) / 3.0
        data2['uvzeta']=(data2['zeta'][starttime:,data2['nv'][eidx,0]] + data2['zeta'][starttime:,data2['nv'][eidx,1]] + data2['zeta'][starttime:,data2['nv'][eidx,2]]) / 3.0
        zeta_grad1=np.gradient(data['uvzeta'])[0]
        zeta_grad2=np.gradient(data2['uvzeta'])[0]
        zeta_bool1=zeta_grad1>0
        zeta_bool2=zeta_grad2>0
    else:
        zeta_grad=np.gradient(data['zeta'][starttime:,nidx])[0]
        fld=np.argmax(np.sum(zeta_grad,axis=1))
        ebb=np.argmin(np.sum(zeta_grad,axis=1))




    f,ax=place_axes(region,2)
    r=f.canvas.get_renderer()


    if usemean==True:
        tmp=data['ua'][starttime:,eidx].copy()
        tmp[~zeta_bool1]=np.nan
        uf1=np.nanmean(tmp,axis=0)

        tmp=data['va'][starttime:,eidx].copy()
        tmp[~zeta_bool1]=np.nan
        vf1=np.nanmean(tmp,axis=0)

        tmp=data2['ua'][starttime:,eidx].copy()
        tmp[~zeta_bool2]=np.nan
        uf2=np.nanmean(tmp,axis=0)

        tmp=data2['va'][starttime:,eidx].copy()
        tmp[~zeta_bool2]=np.nan
        vf2=np.nanmean(tmp,axis=0)

        tmp=data['ua'][starttime:,eidx].copy()
        tmp[zeta_bool1]=np.nan
        ue1=np.nanmean(tmp,axis=0)

        tmp=data['va'][starttime:,eidx].copy()
        tmp[zeta_bool1]=np.nan
        ve1=np.nanmean(tmp,axis=0)

        tmp=data2['ua'][starttime:,eidx].copy()
        tmp[zeta_bool2]=np.nan
        ue2=np.nanmean(tmp,axis=0)

        tmp=data2['va'][starttime:,eidx].copy()
        tmp[zeta_bool2]=np.nan
        ve2=np.nanmean(tmp,axis=0)
    else:
        uf1=data['ua'][starttime+offset+fld,eidx]
        vf1=data['va'][starttime+offset+fld,eidx]
        uf2=data2['ua'][starttime+offset+fld,eidx]
        vf2=data2['va'][starttime+offset+fld,eidx]
        ue1=data['ua'][starttime+offset+ebb,eidx]
        ve1=data['va'][starttime+offset+ebb,eidx]
        ue2=data2['ua'][starttime+offset+ebb,eidx]
        ve2=data2['va'][starttime+offset+ebb,eidx]








#plot no change case
    efs=np.divide(np.sqrt(uf1**2+vf1**2)-np.sqrt(ue1**2+ve1**2),np.sqrt(uf1**2+vf1**2)+np.sqrt(ue1**2+ve1**2))
    ngridx = 2000
    ngridy = 2000
    start = time.clock()
    xi = np.linspace(region['region'][0],region['region'][1], ngridx)
    yi = np.linspace(region['region'][2],region['region'][3], ngridy)
    efs_interp=mpl.mlab.griddata(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1], efs, xi, yi)
    tmpxy=np.meshgrid(xi,yi)
    xii=tmpxy[0]
    yii=tmpxy[1]
    host=data['trigrid'].get_trifinder().__call__(xii,yii)
    efs_interp_mask = np.ma.masked_where(host==-1,efs_interp)
    print ('griddata interp: %f' % (time.clock() - start))
 
    colorax=ax[0].pcolormesh(xi,yi,efs_interp_mask,vmin=cmin,vmax=cmax)

    Q1=ax[0].quiver(data['uvnodell'][eidx[evidx],0],data['uvnodell'][eidx[evidx],1],uf1[evidx],vf1[evidx],angles='xy',scale_units='xy',scale=scale1,zorder=10)
    Q2=ax[0].quiver(data['uvnodell'][eidx[evidx],0],data['uvnodell'][eidx[evidx],1],ue1[evidx],ve1[evidx],angles='xy',scale_units='xy',scale=scale1,color='r',zorder=10)

    t_textf=ax[0].annotate(r''+ebbfldscale+' m s$^{-1}$',xy=(kl[0],kl[1]+.105),xycoords='axes fraction',zorder=30,fontsize=fontsize,label=r''+ebbfldscale+' m s$^{-1}$')
    aqk1f=ax[0].quiverkey(Q1,kl[0],kl[1]+.075,float(ebbfldscale), r'Flood', labelpos='E',fontproperties={'size': fontsize})
    aqk2f=ax[0].quiverkey(Q2,kl[0],kl[1]+.03,float(ebbfldscale), r'Ebb', labelpos='E',fontproperties={'size': fontsize})
    aqk1f.set_zorder(30)
    aqk2f.set_zorder(30)






#plot change case
    efs=np.divide(np.sqrt(uf2**2+vf2**2)-np.sqrt(ue2**2+ve2**2),np.sqrt(uf2**2+vf2**2)+np.sqrt(ue2**2+ve2**2))
    ngridx = 2000
    ngridy = 2000
    start = time.clock()
    xi = np.linspace(region['region'][0],region['region'][1], ngridx)
    yi = np.linspace(region['region'][2],region['region'][3], ngridy)
    efs_interp=mpl.mlab.griddata(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1], efs, xi, yi)
    tmpxy=np.meshgrid(xi,yi)
    xii=tmpxy[0]
    yii=tmpxy[1]
    host=data['trigrid'].get_trifinder().__call__(xii,yii)
    efs_interp_mask = np.ma.masked_where(host==-1,efs_interp)
    print ('griddata interp: %f' % (time.clock() - start))
 #,cmap=mpl.cm.seismic
    colorax=ax[1].pcolormesh(xi,yi,efs_interp_mask,vmin=cmin,vmax=cmax)

    Q1=ax[1].quiver(data['uvnodell'][eidx[evidx],0],data['uvnodell'][eidx[evidx],1],uf2[evidx],vf2[evidx],angles='xy',scale_units='xy',scale=scale1,zorder=10)
    Q2=ax[1].quiver(data['uvnodell'][eidx[evidx],0],data['uvnodell'][eidx[evidx],1],ue2[evidx],ve2[evidx],angles='xy',scale_units='xy',scale=scale1,color='r',zorder=10)

    t_texte=ax[1].annotate(r''+ebbfldscale+' m s$^{-1}$',xy=(kl[0],kl[1]+.105),xycoords='axes fraction',zorder=30,fontsize=fontsize,label=r''+ebbfldscale+' m s$^{-1}$')
    aqk1e=ax[1].quiverkey(Q1,kl[0],kl[1]+.075,float(ebbfldscale), r'Flood', labelpos='E',fontproperties={'size': fontsize})
    aqk2e=ax[1].quiverkey(Q2,kl[0],kl[1]+.03,float(ebbfldscale), r'Ebb', labelpos='E',fontproperties={'size': fontsize})
    aqk1e.set_zorder(30)
    aqk2e.set_zorder(30)



    ppll_sub(ax,setregion=region,cb=colorax,cblabel='Asymmetry',llfontsize=10,fontsize=8)


    f.canvas.draw()
    bb=bboxer(aqk1f.vector.get_window_extent(r).transformed(ax[0].transAxes.inverted()).bounds,aqk1f.text.get_window_extent(r).transformed(ax[0].transAxes.inverted()).bounds)
    bb=bboxer(bb,aqk2f.vector.get_window_extent(r).transformed(ax[0].transAxes.inverted()).bounds)
    bb=bboxer(bb,aqk2f.text.get_window_extent(r).transformed(ax[0].transAxes.inverted()).bounds)
    bb=bboxer(bb,t_textf.get_window_extent(r).transformed(ax[0].transAxes.inverted()).bounds)
    bb1=[bb[0]-bb[2]*.05,bb[1]-bb[3]*.05,bb[2]*1.1,bb[3]*1.1]
    rec=mpl.patches.Rectangle((bb1[0],bb1[1]),bb1[2],bb1[3],transform=ax[0].transAxes,fc='w',zorder=20)
    ax[0].add_patch(rec)


    f.canvas.draw()
    bb=bboxer(aqk1e.vector.get_window_extent(r).transformed(ax[1].transAxes.inverted()).bounds,aqk1e.text.get_window_extent(r).transformed(ax[1].transAxes.inverted()).bounds)
    bb=bboxer(bb,aqk2e.vector.get_window_extent(r).transformed(ax[1].transAxes.inverted()).bounds)
    bb=bboxer(bb,aqk2e.text.get_window_extent(r).transformed(ax[1].transAxes.inverted()).bounds)
    bb=bboxer(bb,t_texte.get_window_extent(r).transformed(ax[1].transAxes.inverted()).bounds)
    bb2=[bb[0]-bb[2]*.05,bb[1]-bb[3]*.05,bb[2]*1.1,bb[3]*1.1]
    rec=mpl.patches.Rectangle((bb2[0],bb2[1]),bb2[2],bb2[3],transform=ax[1].transAxes,fc='w',zorder=20)
    ax[1].add_patch(rec)


    #lseg=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    #ax[1].add_collection(lseg)

    ABC=['A','B','C']
    plt.draw()
    for i,axi in enumerate(ax):
        plotcoast(ax[i],filename='pacific.nc',color='None',fill=True)
        axbb=ax[i].get_axes().get_position().bounds
        t=ax[i].annotate(ABC[i],xy=(axbb[0]+.0075,axbb[1]+axbb[3]-.03),xycoords='figure fraction')
        t.set_zorder(100)

        #ax[i].text(-129.4225,52.686,r'Moore Islands',fontsize=5,rotation=80)

    if usemean==True:
        f.savefig(savepath + grid + '_'+ name_orig+'_'+ name_change+'_'+regionname+'_meanasymmetry_meanvector.png',dpi=600)
    else:
        f.savefig(savepath + grid + '_'+ name_orig+'_'+ name_change+'_'+regionname+'_instantasymmetry_instantvector.png',dpi=600)
    plt.close(f)




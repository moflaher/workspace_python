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
sys.path.append('/home/moe46/Desktop/school/workspace_python/ttide_py/ttide/')
sys.path.append('/home/moflaher/Desktop/workspace_python/ttide_py/ttide/')
from t_tide import t_tide
from t_predic import t_predic
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC


# Define names and types of data
name_orig='kit4_kelp_nodrag'
name_change='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'
regionlist=['kit4_kelp_tight2_kelpfield']#,'kit4_kelp_tight2_small']#,'kit4_kelp_tight5']
datatype='2d'
starttime=384
offset=0
fontsize=6

testing=False
usemean=True

kl=[.675,.79]
kl=[.725,.025]

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name_orig+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name_change+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

cages=loadcage('runs/'+grid+'/' +name_change+ '/input/' +grid+ '_cage.dat')
if np.shape(cages)!=():
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2]],0],data['nodell'][data['nv'][i,[0,1,2]],1])) for i in cages ]
    color='g'

savepath='figures/png/' + grid + '_' + datatype + '/ebbfldres_dragnodrag_subplot/'
if not os.path.exists(savepath): os.makedirs(savepath)


uv1=np.load('data/ttide/'+grid+'_'+name_orig+'_'+datatype+'_uv_all.npy')
uv1=uv1[()]
uv2=np.load('data/ttide/'+grid+'_'+name_change+'_'+datatype+'_uv_all.npy')
uv2=uv2[()]


for regionname in regionlist:

    region=regions(regionname)
    vectorspacing=400#2000*np.diff(region['region'][0:2])
    vectorspacing=125#2000*np.diff(region['region'][0:2])
    nidx=get_nodes(data,region)
    eidx=equal_vectors(data,region,vectorspacing)


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




    f,ax=place_axes(region,3)
    r=f.canvas.get_renderer()
    ppll_sub(ax,setregion=region,llfontsize=10,fontsize=8)

    if usemean==True:
        uatmp=data['ua'][starttime:,eidx].copy()
        uatmp[~zeta_bool1]=np.nan
        vatmp=data['va'][starttime:,eidx].copy()
        vatmp[~zeta_bool1]=np.nan
        uatmp2=data2['ua'][starttime:,eidx].copy()
        uatmp2[~zeta_bool1]=np.nan
        vatmp2=data2['va'][starttime:,eidx].copy()
        vatmp2[~zeta_bool1]=np.nan
        q2u1=np.nanmean(uatmp,axis=0)
        q2v1=np.nanmean(vatmp,axis=0)
        q2u2=np.nanmean(uatmp2,axis=0)
        q2v2=np.nanmean(vatmp2,axis=0)
    else:
        q2u1=data['ua'][starttime+offset+fld,eidx]
        q2v1=data['va'][starttime+offset+fld,eidx]
        q2u2=data2['ua'][starttime+offset+fld,eidx]
        q2v2=data2['va'][starttime+offset+fld,eidx]

    ebbfld=.3#np.ceil(10*np.linalg.norm(np.vstack([q2u1,q2v1]),axis=0).mean())/10
    ebbfld=.2#np.ceil(10*np.linalg.norm(np.vstack([q2u1,q2v1]),axis=0).mean())/10
    ebbfldscale=('%.1f'%ebbfld)
    scale1=35#np.sqrt(ebbfld*(vectorspacing*2)**2)
    scale1=75#np.sqrt(ebbfld*(vectorspacing*2)**2)

    Q1=ax[0].quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],q2u1,q2v1,angles='xy',scale_units='xy',scale=scale1,zorder=10)
    Q2=ax[0].quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],q2u2,q2v2,angles='xy',scale_units='xy',scale=scale1,color='r',zorder=10)

    t_text=ax[0].annotate(r''+ebbfldscale+' m s$^{-1}$',xy=(kl[0],kl[1]+.105),xycoords='axes fraction',zorder=30,fontsize=fontsize,label=r''+ebbfldscale+' m s$^{-1}$')
    aqk1=ax[0].quiverkey(Q1,kl[0],kl[1]+.075,float(ebbfldscale), r'No drag', labelpos='E',fontproperties={'size': fontsize})
    aqk2=ax[0].quiverkey(Q2,kl[0],kl[1]+.03,float(ebbfldscale), r'Drag', labelpos='E',fontproperties={'size': fontsize})
    aqk1.set_zorder(30)
    aqk2.set_zorder(30)


    f.canvas.draw()
    bb=bboxer(aqk1.vector.get_window_extent(r).transformed(ax[0].transAxes.inverted()).bounds,aqk1.text.get_window_extent(r).transformed(ax[0].transAxes.inverted()).bounds)
    bb=bboxer(bb,aqk2.vector.get_window_extent(r).transformed(ax[0].transAxes.inverted()).bounds)
    bb=bboxer(bb,aqk2.text.get_window_extent(r).transformed(ax[0].transAxes.inverted()).bounds)
    bb=bboxer(bb,t_text.get_window_extent(r).transformed(ax[0].transAxes.inverted()).bounds)
    bb=[bb[0]-bb[2]*.05,bb[1]-bb[3]*.05,bb[2]*1.1,bb[3]*1.1]
    rec=mpl.patches.Rectangle((bb[0],bb[1]),bb[2],bb[3],transform=ax[0].transAxes,fc='w',zorder=20)
    ax[0].add_patch(rec)


    if usemean==True:
        uatmp=data['ua'][starttime:,eidx].copy()
        uatmp[zeta_bool1]=np.nan
        vatmp=data['va'][starttime:,eidx].copy()
        vatmp[zeta_bool1]=np.nan
        uatmp2=data2['ua'][starttime:,eidx].copy()
        uatmp2[zeta_bool1]=np.nan
        vatmp2=data2['va'][starttime:,eidx].copy()
        vatmp2[zeta_bool1]=np.nan
        q2u1=np.nanmean(uatmp,axis=0)
        q2v1=np.nanmean(vatmp,axis=0)
        q2u2=np.nanmean(uatmp2,axis=0)
        q2v2=np.nanmean(vatmp2,axis=0)

    else:
        q2u1=data['ua'][starttime+offset+ebb,eidx]
        q2v1=data['va'][starttime+offset+ebb,eidx]
        q2u2=data2['ua'][starttime+offset+ebb,eidx]
        q2v2=data2['va'][starttime+offset+ebb,eidx]


    Q1=ax[1].quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],q2u1,q2v1,angles='xy',scale_units='xy',scale=scale1,zorder=10)
    Q2=ax[1].quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],q2u2,q2v2,angles='xy',scale_units='xy',scale=scale1,color='r',zorder=10)

    t_text=ax[1].annotate(r''+ebbfldscale+' m s$^{-1}$',xy=(kl[0],kl[1]+.105),xycoords='axes fraction',zorder=30,fontsize=fontsize,label=r''+ebbfldscale+' m s$^{-1}$')
    aqk1=ax[1].quiverkey(Q1,kl[0],kl[1]+.075,float(ebbfldscale), r'No drag', labelpos='E',fontproperties={'size': fontsize})
    aqk2=ax[1].quiverkey(Q2,kl[0],kl[1]+.03,float(ebbfldscale), r'Drag', labelpos='E',fontproperties={'size': fontsize})
    aqk1.set_zorder(30)
    aqk2.set_zorder(30)

    f.canvas.draw()
    bb=bboxer(aqk1.vector.get_window_extent(r).transformed(ax[1].transAxes.inverted()).bounds,aqk1.text.get_window_extent(r).transformed(ax[1].transAxes.inverted()).bounds)
    bb=bboxer(bb,aqk2.vector.get_window_extent(r).transformed(ax[1].transAxes.inverted()).bounds)
    bb=bboxer(bb,aqk2.text.get_window_extent(r).transformed(ax[1].transAxes.inverted()).bounds)
    bb=bboxer(bb,t_text.get_window_extent(r).transformed(ax[1].transAxes.inverted()).bounds)
    bb=[bb[0]-bb[2]*.05,bb[1]-bb[3]*.05,bb[2]*1.1,bb[3]*1.1]
    rec=mpl.patches.Rectangle((bb[0],bb[1]),bb[2],bb[3],transform=ax[1].transAxes,fc='w',zorder=20)
    ax[1].add_patch(rec)



    resu=np.empty((len(eidx),len(data['time'][starttime:])))
    resv=np.empty((len(eidx),len(data['time'][starttime:])))
    resu2=np.empty((len(eidx),len(data['time'][starttime:])))
    resv2=np.empty((len(eidx),len(data['time'][starttime:])))
    if testing==False:
        for j in range(0,len(eidx)):
            #print ("%d"%j)+"              "+("%f"%(j/len(eidx)*100)) 
            i=eidx[j]    
            resu[j,:]=data['ua'][starttime:,i]-np.real(t_predic(data['time'][starttime:],uv1['nameu'],uv1['freq'],uv1['tidecon'][i,:,:])).flatten()
            resv[j,:]=data['va'][starttime:,i]-np.imag(t_predic(data['time'][starttime:],uv1['nameu'],uv1['freq'],uv1['tidecon'][i,:,:])).flatten()
            resu2[j,:]=data2['ua'][(starttime+offset):,i]-np.real(t_predic(data2['time'][(starttime+offset):],uv2['nameu'],uv2['freq'],uv2['tidecon'][i,:,:])).flatten()
            resv2[j,:]=data2['va'][(starttime+offset):,i]-np.imag(t_predic(data2['time'][(starttime+offset):],uv2['nameu'],uv2['freq'],uv2['tidecon'][i,:,:])).flatten()

    res=.05#np.linalg.norm(np.vstack([resu,resv]),axis=0).mean()
    resscale=('%.2f'%res)
    scale2=15#res*vectorspacing*2
    scale2=25#res*vectorspacing*2

    Q1=ax[2].quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],np.mean(resu2,axis=1),np.mean(resv2,axis=1),angles='xy',scale_units='xy',scale=scale2,zorder=10)
    Q2=ax[2].quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],np.mean(resu,axis=1),np.mean(resv,axis=1),angles='xy',scale_units='xy',scale=scale2,color='r',zorder=10)

    t_text=ax[2].annotate(r''+resscale+' m s$^{-1}$',xy=(kl[0],kl[1]+.105),xycoords='axes fraction',zorder=30,fontsize=fontsize,label=r''+resscale+' m s$^{-1}$')
    aqk1=ax[2].quiverkey(Q1,kl[0],kl[1]+.075,float(resscale), r'No drag', labelpos='E',fontproperties={'size': fontsize})
    aqk2=ax[2].quiverkey(Q2,kl[0],kl[1]+.03,float(resscale), r'Drag', labelpos='E',fontproperties={'size': fontsize})
    aqk1.set_zorder(30)
    aqk2.set_zorder(30)

    f.canvas.draw()
    bb=bboxer(aqk1.vector.get_window_extent(r).transformed(ax[2].transAxes.inverted()).bounds,aqk1.text.get_window_extent(r).transformed(ax[2].transAxes.inverted()).bounds)
    bb=bboxer(bb,aqk2.vector.get_window_extent(r).transformed(ax[2].transAxes.inverted()).bounds)
    bb=bboxer(bb,aqk2.text.get_window_extent(r).transformed(ax[2].transAxes.inverted()).bounds)
    bb=bboxer(bb,t_text.get_window_extent(r).transformed(ax[2].transAxes.inverted()).bounds)
    bb=[bb[0]-bb[2]*.05,bb[1]-bb[3]*.05,bb[2]*1.1,bb[3]*1.1]
    rec=mpl.patches.Rectangle((bb[0],bb[1]),bb[2],bb[3],transform=ax[2].transAxes,fc='w',zorder=20)
    ax[2].add_patch(rec)


    rn={}
    rn['region']=np.array([-129.492, -129.479,52.6375,52.655])
    rn['center']=[(rn['region'][0]+rn['region'][1])/2,(rn['region'][2]+rn['region'][3])/2]
    plot_box(ax[0],rn,'k',1.5)
    aa=ax[0].text(rn['center'][0]-.011,rn['center'][1]-.005,'F1',fontsize=12,rotation=0,color='k')
    
    rn={}
    rn['region']=np.array([-129.499, -129.494,52.651,52.6551])
    rn['center']=[(rn['region'][0]+rn['region'][1])/2,(rn['region'][2]+rn['region'][3])/2]
    plot_box(ax[0],rn,'k',1.5)
    aa=ax[0].text(rn['center'][0]-.007,rn['center'][1],'F2',fontsize=12,rotation=0,color='k')
    
    rn={}
    rn['region']=np.array([-129.49, -129.48,52.6575,52.665])
    rn['center']=[(rn['region'][0]+rn['region'][1])/2,(rn['region'][2]+rn['region'][3])/2]
    plot_box(ax[0],rn,'k',1.5)
    aa=ax[0].text(rn['center'][0]-.01,rn['center'][1]+.0025,'F3',fontsize=12,rotation=0,color='k')
    
    rn={}
    rn['region']=np.array([-129.474, -129.465,52.6475,52.655])
    rn['center']=[(rn['region'][0]+rn['region'][1])/2,(rn['region'][2]+rn['region'][3])/2]
    plot_box(ax[0],rn,'k',1.5)
    aa=ax[0].text(rn['center'][0]+.0025,rn['center'][1]+.005,'F4',fontsize=12,rotation=0,color='k')



    lseg=np.empty((3,),dtype=object)
    ABC=['A','B','C']
    #ABC=['D','E','F']
    plt.draw()        
    for i,axi in enumerate(ax):
        plotcoast(ax[i],filename='pacific.nc',color='None',fill=True)
        axbb=ax[i].get_axes().get_position().bounds
        t=ax[i].annotate(ABC[i],xy=(axbb[0]+.0075,axbb[1]+axbb[3]-.03),xycoords='figure fraction')
        t.set_zorder(100)
        lseg[i]=PC(tmparray,facecolor = 'g',edgecolor='None')
        ax[i].add_collection(lseg[i])
        #ax[i].text(-129.4225,52.686,r'Moore Islands',fontsize=5,rotation=80)            

    if usemean==True:
        f.savefig(savepath + grid + '_'+ name_orig+'_'+ name_change+'_'+regionname+'_meanebb_meanfld_meanres.png',dpi=600)
    else:
        f.savefig(savepath + grid + '_'+ name_orig+'_'+ name_change+'_'+regionname+'_ebb_fld_meanres.png',dpi=600)
    plt.close(f)




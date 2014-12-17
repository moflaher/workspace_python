from __future__ import division
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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
sys.path.append('/home/moe46/Desktop/school/workspace_python/ttide_py/ttide/')
sys.path.append('/home/moflaher/Desktop/workspace_python/ttide_py/ttide/')
from t_tide import t_tide
from t_predic import t_predic
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC


# Define names and types of data
name='sfm6_musq2_all_cages'
name2='sfm6_musq2_no_cages'
grid='sfm6_musq2'
regionname='musq_large'
datatype='3d'
starttime=0
offset=1008


testing=False
usemean=False

kl=[.775,.025,.2,.14]
scale1=35
scale2=10
vectorspacing=2000
fldax_r=[.125,.1,.775,.8]
ebbax_r=[.125,.1,.775,.8]
resax_r=[.125,.1,.775,.8]
ebbfldscale='1.0'
resscale='0.25'
ABC=[.05,.925]
fcolor='b'
arrowshift1=.1




region=regions(regionname)

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

cages=np.genfromtxt('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)

savepath='figures/png/' + grid + '_' + datatype + '/ebbfldres_dragnodrag/'
if not os.path.exists(savepath): os.makedirs(savepath)

tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2]],0],data['nodell'][data['nv'][i,[0,1,2]],1])) for i in cages ]




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

for level in range(0,19):

    lsegf=PC(tmparray,facecolor = fcolor,edgecolor='None')
    lsege=PC(tmparray,facecolor = fcolor,edgecolor='None')
    lsegr=PC(tmparray,facecolor = fcolor,edgecolor='None')

    f=plt.figure()

    ax_fld=f.add_axes(fldax_r)
    ax_fld.add_collection(lsegf)

    if usemean==True:
        uatmp=data['u'][starttime:,level,eidx].copy()
        uatmp[~zeta_bool1]=np.nan
        vatmp=data['v'][starttime:,level,eidx].copy()
        vatmp[~zeta_bool1]=np.nan
        uatmp2=data2['u'][starttime:,level,eidx].copy()
        uatmp2[~zeta_bool1]=np.nan
        vatmp2=data2['v'][starttime:,level,eidx].copy()
        vatmp2[~zeta_bool1]=np.nan
        q2u2=np.nanmean(uatmp2,axis=0)
        q2v2=np.nanmean(vatmp2,axis=0)
        q2u1=np.nanmean(uatmp,axis=0)
        q2v1=np.nanmean(vatmp,axis=0)
    else:
        q2u2=data2['u'][starttime+offset+fld,level,eidx]
        q2v2=data2['v'][starttime+offset+fld,level,eidx]
        q2u1=data['u'][starttime+fld,level,eidx]
        q2v1=data['v'][starttime+fld,level,eidx]

    Q1=ax_fld.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],q2u2,q2v2,angles='xy',scale_units='xy',scale=scale1,zorder=10)
    Q2=ax_fld.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],q2u1,q2v1,angles='xy',scale_units='xy',scale=scale1,color='r',zorder=10)
    prettyplot_ll(ax_fld,setregion=region)
    plt.draw()
    rec=mpl.patches.Rectangle((kl[0],kl[1]),kl[2],kl[3],transform=ax_fld.transAxes,fc='w',zorder=20)
    ax_fld.add_patch(rec)
    ax_fld.annotate(r''+ebbfldscale+' m s$^{-1}$',xy=(kl[0]+arrowshift1-.025,kl[1]+.09),xycoords='axes fraction',zorder=30,fontsize=8)
    aqk1=ax_fld.quiverkey(Q1,kl[0]+arrowshift1,kl[1]+.065,float(ebbfldscale), r'No cage', labelpos='W',fontproperties={'size': 8})
    aqk2=ax_fld.quiverkey(Q2,kl[0]+arrowshift1,kl[1]+.03,float(ebbfldscale), r'Cage', labelpos='W',fontproperties={'size': 8})
    aqk1.set_zorder(30)
    aqk2.set_zorder(30)


    plotcoast(ax_fld,color='k',fill=True)
    if usemean==True:
        f.savefig(savepath + grid + '_'+ name+'_'+ name2+'_'+regionname+'_meanfld_level' +("%d"%level)+ '.png',dpi=600)
    else:
        f.savefig(savepath + grid + '_'+ name+'_'+ name2+'_'+regionname+'_fld_level' +("%d"%level)+ '.png',dpi=600)
    plt.close(f)


    f=plt.figure()
    ax_ebb=f.add_axes(ebbax_r)
    ax_ebb.add_collection(lsege)
    if usemean==True:
        uatmp=data['u'][starttime:,level,eidx].copy()
        uatmp[zeta_bool1]=np.nan
        vatmp=data['v'][starttime:,level,eidx].copy()
        vatmp[zeta_bool1]=np.nan
        uatmp2=data2['u'][starttime:,level,eidx].copy()
        uatmp2[zeta_bool1]=np.nan
        vatmp2=data2['v'][starttime:,level,eidx].copy()
        vatmp2[zeta_bool1]=np.nan
        q2u2=np.nanmean(uatmp2,axis=0)
        q2v2=np.nanmean(vatmp2,axis=0)
        q2u1=np.nanmean(uatmp,axis=0)
        q2v1=np.nanmean(vatmp,axis=0)
    else:
        q2u2=data2['u'][starttime+offset+ebb,level,eidx]
        q2v2=data2['v'][starttime+offset+ebb,level,eidx]
        q2u1=data['u'][starttime+ebb,level,eidx]
        q2v1=data['v'][starttime+ebb,level,eidx]

    Q1=ax_ebb.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],q2u2,q2v2,angles='xy',scale_units='xy',scale=scale1,zorder=10)
    Q2=ax_ebb.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],q2u1,q2v1,angles='xy',scale_units='xy',scale=scale1,color='r',zorder=10)
    prettyplot_ll(ax_ebb,setregion=region)
    plt.draw()
    rec=mpl.patches.Rectangle((kl[0],kl[1]),kl[2],kl[3],transform=ax_ebb.transAxes,fc='w',zorder=20)
    ax_ebb.add_patch(rec)
    ax_ebb.annotate(r''+ebbfldscale+' m s$^{-1}$',xy=(kl[0]+arrowshift1-.025,kl[1]+.09),xycoords='axes fraction',zorder=30,fontsize=8)
    aqk1=ax_ebb.quiverkey(Q1,kl[0]+arrowshift1,kl[1]+.065,float(ebbfldscale), r'No cage', labelpos='W',fontproperties={'size': 8})
    aqk2=ax_ebb.quiverkey(Q2,kl[0]+arrowshift1,kl[1]+.03,float(ebbfldscale), r'Cage', labelpos='W',fontproperties={'size': 8})
    aqk1.set_zorder(30)
    aqk2.set_zorder(30)
    plotcoast(ax_ebb,color='k',fill=True)
    if usemean==True:
        f.savefig(savepath + grid + '_'+ name+'_'+ name2+'_'+regionname+'_meanebb_level' +("%d"%level)+ '.png',dpi=600)
    else:
        f.savefig(savepath + grid + '_'+ name+'_'+ name2+'_'+regionname+'_ebb_level' +("%d"%level)+ '.png',dpi=600)

    plt.close(f)


    f=plt.figure()
    resu=np.empty((len(eidx),len(data['time'][starttime:])))
    resv=np.empty((len(eidx),len(data['time'][starttime:])))
    resu2=np.empty((len(eidx),len(data['time'][starttime:])))
    resv2=np.empty((len(eidx),len(data['time'][starttime:])))
    if testing==False:
        for j in range(0,len(eidx)):
            print ("%d"%j)+"              "+("%f"%(j/len(eidx)*100)) 
            i=eidx[j]    
            [nameu, freq, tidecon_uv, xout]=t_tide(data['u'][starttime:,level,i]+1j*data['v'][starttime:,level,i],stime=data['time'][starttime],lat=data['uvnodell'][i,1],output=False,constitnames=np.array([['M2  '],['N2  '],['S2  '],['K1  '],['O1  ']]))
            resu[j,:]=data['u'][starttime:,level,i]-np.real(t_predic(data['time'][starttime:],nameu,freq,tidecon_uv)).flatten()
            resv[j,:]=data['v'][starttime:,level,i]-np.imag(t_predic(data['time'][starttime:],nameu,freq,tidecon_uv)).flatten()
            [nameu, freq, tidecon_uv, xout]=t_tide(data2['u'][starttime:,level,i]+1j*data2['v'][starttime:,level,i],stime=data['time'][starttime],lat=data['uvnodell'][i,1],output=False,constitnames=np.array([['M2  '],['N2  '],['S2  '],['K1  '],['O1  ']]))
            resu2[j,:]=data2['u'][(starttime+offset):,level,i]-np.real(t_predic(data2['time'][(starttime+offset):],nameu,freq,tidecon_uv)).flatten()
            resv2[j,:]=data2['v'][(starttime+offset):,level,i]-np.imag(t_predic(data2['time'][(starttime+offset):],nameu,freq,tidecon_uv)).flatten()

    ax_res=f.add_axes(resax_r)
    ax_res.add_collection(lsegr)
    Q1=ax_res.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],np.mean(resu2,axis=1),np.mean(resv2,axis=1),angles='xy',scale_units='xy',scale=scale2,zorder=10)
    Q2=ax_res.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],np.mean(resu,axis=1),np.mean(resv,axis=1),angles='xy',scale_units='xy',scale=scale2,color='r',zorder=10)
    prettyplot_ll(ax_res,setregion=region)
    plt.draw()
    rec=mpl.patches.Rectangle((kl[0],kl[1]),kl[2],kl[3],transform=ax_res.transAxes,fc='w',zorder=20)
    ax_res.add_patch(rec)
    ax_res.annotate(r''+resscale+' m s$^{-1}$',xy=(kl[0]+arrowshift1-.025,kl[1]+.09),xycoords='axes fraction',zorder=30,fontsize=8)
    aqk1=ax_res.quiverkey(Q1,kl[0]+arrowshift1,kl[1]+.065,float(resscale), r'No cage', labelpos='W',fontproperties={'size': 8})
    aqk2=ax_res.quiverkey(Q2,kl[0]+arrowshift1,kl[1]+.03,float(resscale), r'Cage', labelpos='W',fontproperties={'size': 8})
    aqk1.set_zorder(30)
    aqk2.set_zorder(30)
    plotcoast(ax_res,color='k',fill=True)

    f.savefig(savepath + grid + '_'+ name+'_'+ name2+'_'+regionname+'_meanres_level' +("%d"%level)+ '.png',dpi=600)
    plt.close(f)




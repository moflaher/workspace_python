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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
sys.path.append('/home/moe46/Desktop/school/workspace_python/ttide_py/ttide/')
sys.path.append('/home/moflaher/Desktop/workspace_python/ttide_py/ttide/')
from t_tide import t_tide
from t_predic import t_predic
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC


# Define names and types of data
name='kit4_kelp_20m_0.018'
name2='kit4_45days_3'
grid='kit4'
regionname='kit4_kelp_tight6'
datatype='2d'
starttime=384
endtime=400
offset=0


testing=False
usemean=True

kl=[.625,.02,.345,.1]
scale1=50
scale2=15
vectorspacing=50
fldax_r=[.1,.1,.275,.8]
ebbax_r=[.385,.1,.275,.8]
resax_r=[.67,.1,.275,.8]
ebbfldscale='0.3'
resscale='0.05'
ABC=[.05,.95]



region=regions(regionname)

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

cages=np.genfromtxt('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)

savepath='figures/png/' + grid + '_' + datatype + '/ebbfldres_dragnodrag_subplot/'
if not os.path.exists(savepath): os.makedirs(savepath)

tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2]],0],data['nodell'][data['nv'][i,[0,1,2]],1])) for i in cages ]
lsegf=PC(tmparray,facecolor = 'g',edgecolor='None')
lsege=PC(tmparray,facecolor = 'g',edgecolor='None')
lsegr=PC(tmparray,facecolor = 'g',edgecolor='None')

uv1=np.load('/home/moflaher/Desktop/workspace_python/data/ttide/'+grid+'_'+name+'_'+datatype+'_uv.npy')
uv1=uv1[()]
uv2=np.load('/home/moflaher/Desktop/workspace_python/data/ttide/'+grid+'_'+name2+'_'+datatype+'_uv.npy')
uv2=uv2[()]

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



f=plt.figure()

ax_fld=f.add_axes(fldax_r)
ax_fld.add_collection(lsegf)

if usemean==True:
    uatmp=data['ua'][starttime:,eidx].copy()
    uatmp[~zeta_bool1]=np.nan
    vatmp=data['va'][starttime:,eidx].copy()
    vatmp[~zeta_bool1]=np.nan
    uatmp2=data2['ua'][starttime:,eidx].copy()
    uatmp2[~zeta_bool1]=np.nan
    vatmp2=data2['va'][starttime:,eidx].copy()
    vatmp2[~zeta_bool1]=np.nan
    q2u2=np.nanmean(uatmp2,axis=0)
    q2v2=np.nanmean(vatmp2,axis=0)
    q2u1=np.nanmean(uatmp,axis=0)
    q2v1=np.nanmean(vatmp,axis=0)
else:
    q2u2=data2['ua'][starttime+offset+fld,eidx]
    q2v2=data2['va'][starttime+offset+fld,eidx]
    q2u1=data['ua'][starttime+offset+fld,eidx]
    q2v1=data['va'][starttime+offset+fld,eidx]

Q1=ax_fld.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],q2u2,q2v2,angles='xy',scale_units='xy',scale=scale1,zorder=10)
Q2=ax_fld.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],q2u1,q2v1,angles='xy',scale_units='xy',scale=scale1,color='r',zorder=10)
ax_fld.axis(region['region'])
fix_osw(ax_fld)
ax_fld.set_aspect(get_aspectratio(region))
plt.draw()
rec=mpl.patches.Rectangle((kl[0],kl[1]),kl[2],kl[3],transform=ax_fld.transAxes,fc='w',zorder=20)
ax_fld.add_patch(rec)
ax_fld.annotate(r''+ebbfldscale+' m s$^{-1}$',xy=(kl[0]+.035,kl[1]+.07),xycoords='axes fraction',zorder=30,fontsize=8)
aqk1=ax_fld.quiverkey(Q1,kl[0]+.075,kl[1]+.045,float(ebbfldscale), r'No drag', labelpos='E',fontproperties={'size': 8})
aqk2=ax_fld.quiverkey(Q2,kl[0]+.075,kl[1]+.015,float(ebbfldscale), r'Drag', labelpos='E',fontproperties={'size': 8})
aqk1.set_zorder(30)
aqk2.set_zorder(30)
for label in ax_fld.get_xticklabels()[::2]:
    label.set_visible(False)
plotcoast(ax_fld,filename='pacific.nc',color='k')
#ax_fld.text(-129.4225,52.686,r'Moore Islands',fontsize=5,rotation=80)


ax_ebb=f.add_axes(ebbax_r)
ax_ebb.add_collection(lsege)
if usemean==True:
    uatmp=data['ua'][starttime:,eidx].copy()
    uatmp[zeta_bool1]=np.nan
    vatmp=data['va'][starttime:,eidx].copy()
    vatmp[zeta_bool1]=np.nan
    uatmp2=data2['ua'][starttime:,eidx].copy()
    uatmp2[zeta_bool1]=np.nan
    vatmp2=data2['va'][starttime:,eidx].copy()
    vatmp2[zeta_bool1]=np.nan
    q2u2=np.nanmean(uatmp2,axis=0)
    q2v2=np.nanmean(vatmp2,axis=0)
    q2u1=np.nanmean(uatmp,axis=0)
    q2v1=np.nanmean(vatmp,axis=0)
else:
    q2u2=data2['ua'][starttime+offset+ebb,eidx]
    q2v2=data2['va'][starttime+offset+ebb,eidx]
    q2u1=data['ua'][starttime+offset+ebb,eidx]
    q2v1=data['va'][starttime+offset+ebb,eidx]

Q1=ax_ebb.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],q2u2,q2v2,angles='xy',scale_units='xy',scale=scale1,zorder=10)
Q2=ax_ebb.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],q2u1,q2v1,angles='xy',scale_units='xy',scale=scale1,color='r',zorder=10)
ax_ebb.axis(region['region'])
#for label in ax_ebb.get_xticklabels():
#    label.set_visible(False)
fix_osw(ax_ebb)
ax_ebb.set_aspect(get_aspectratio(region))
ax_ebb.yaxis.set_tick_params(labelleft='off')
plt.draw()
rec=mpl.patches.Rectangle((kl[0],kl[1]),kl[2],kl[3],transform=ax_ebb.transAxes,fc='w',zorder=20)
ax_ebb.add_patch(rec)
ax_ebb.annotate(r''+ebbfldscale+' m s$^{-1}$',xy=(kl[0]+.035,kl[1]+.07),xycoords='axes fraction',zorder=30,fontsize=8)
aqk1=ax_ebb.quiverkey(Q1,kl[0]+.075,kl[1]+.045,float(ebbfldscale), r'No drag', labelpos='E',fontproperties={'size': 8})
aqk2=ax_ebb.quiverkey(Q2,kl[0]+.075,kl[1]+.015,float(ebbfldscale), r'Drag', labelpos='E',fontproperties={'size': 8})
aqk1.set_zorder(30)
aqk2.set_zorder(30)
for label in ax_ebb.get_xticklabels()[::2]:
    label.set_visible(False)
plotcoast(ax_ebb,filename='pacific.nc',color='k')
#ax_ebb.text(-129.4225,52.686,r'Moore Islands',fontsize=5,rotation=80)


resu=np.empty((len(eidx),len(data['time'][starttime:])))
resv=np.empty((len(eidx),len(data['time'][starttime:])))
resu2=np.empty((len(eidx),len(data['time'][starttime:])))
resv2=np.empty((len(eidx),len(data['time'][starttime:])))
if testing==False:
    for j in range(0,len(eidx)):
        print ("%d"%j)+"              "+("%f"%(j/len(eidx)*100)) 
        i=eidx[j]    
        resu[j,:]=data['ua'][starttime:,i]-np.real(t_predic(data['time'][starttime:],uv1['nameu'],uv1['freq'],uv1['tidecon'][i,:,:])).flatten()
        resv[j,:]=data['va'][starttime:,i]-np.imag(t_predic(data['time'][starttime:],uv1['nameu'],uv1['freq'],uv1['tidecon'][i,:,:])).flatten()
        resu2[j,:]=data2['ua'][(starttime+offset):,i]-np.real(t_predic(data2['time'][(starttime+offset):],uv2['nameu'],uv2['freq'],uv2['tidecon'][i,:,:])).flatten()
        resv2[j,:]=data2['va'][(starttime+offset):,i]-np.imag(t_predic(data2['time'][(starttime+offset):],uv2['nameu'],uv2['freq'],uv2['tidecon'][i,:,:])).flatten()

ax_res=f.add_axes(resax_r)
ax_res.add_collection(lsegr)
Q1=ax_res.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],np.mean(resu2,axis=1),np.mean(resv2,axis=1),angles='xy',scale_units='xy',scale=scale2,zorder=10)
Q2=ax_res.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],np.mean(resu,axis=1),np.mean(resv,axis=1),angles='xy',scale_units='xy',scale=scale2,color='r',zorder=10)
ax_res.axis(region['region'])
fix_osw(ax_res)
ax_res.set_aspect(get_aspectratio(region))
ax_res.yaxis.set_tick_params(labelleft='off')
plt.draw()
rec=mpl.patches.Rectangle((kl[0],kl[1]),kl[2],kl[3],transform=ax_res.transAxes,fc='w',zorder=20)
ax_res.add_patch(rec)
ax_res.annotate(r''+resscale+' m s$^{-1}$',xy=(kl[0]+.035,kl[1]+.07),xycoords='axes fraction',zorder=30,fontsize=8)
aqk1=ax_res.quiverkey(Q1,kl[0]+.075,kl[1]+.045,float(resscale), r'No drag', labelpos='E',fontproperties={'size': 8})
aqk2=ax_res.quiverkey(Q2,kl[0]+.075,kl[1]+.015,float(resscale), r'Drag', labelpos='E',fontproperties={'size': 8})
aqk1.set_zorder(30)
aqk2.set_zorder(30)
for label in ax_res.get_yticklabels()[::2]:
    label.set_visible(False)
for label in ax_res.get_xticklabels()[::2]:
    label.set_visible(False)
plotcoast(ax_res,filename='pacific.nc',color='k')
#ax_res.text(-129.4225,52.686,r'Moore Islands',fontsize=5,rotation=80)


ax_fld.text(ABC[0],ABC[1],"A",transform=ax_fld.transAxes,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3},zorder=31)
ax_ebb.text(ABC[0],ABC[1],"B",transform=ax_ebb.transAxes,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3},zorder=31)
ax_res.text(ABC[0],ABC[1],"C",transform=ax_res.transAxes,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3},zorder=31)

ax_fld.set_ylabel(r'Latitude ($^{\circ}$N)',fontsize=8)
ax_fld.set_xlabel(r'Longitude ($^{\circ}$W)',fontsize=8)
ax_ebb.set_xlabel(r'Longitude ($^{\circ}$W)',fontsize=8)
ax_res.set_xlabel(r'Longitude ($^{\circ}$W)',fontsize=8)

for label in ax_fld.get_xticklabels():
    label.set_fontsize(8)
for label in ax_fld.get_yticklabels():
    label.set_fontsize(8)
for label in ax_ebb.get_xticklabels():
    label.set_fontsize(8)
for label in ax_ebb.get_yticklabels():
    label.set_fontsize(8)
for label in ax_res.get_xticklabels():
    label.set_fontsize(8)
for label in ax_res.get_yticklabels():
    label.set_fontsize(8)


if usemean==True:
    f.savefig(savepath + grid + '_'+ name+'_'+ name2+'_'+regionname+'_meanebb_meanfld_meanres.png',dpi=600)
else:
    f.savefig(savepath + grid + '_'+ name+'_'+ name2+'_'+regionname+'_ebb_fld_meanres.png',dpi=600)
plt.close(f)




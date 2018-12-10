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
name='try16'
grid='beaufort3'
regionname='beaufort3_southcoast'

starttime=0
endtime=400
offset=0


testing=False
usemean=False

kl=[.8,.1,.175,.125]
scale1=.35
scale2=.05
vectorspacing=10000
fldax_r=[.125,.1,.8,.8]
ebbax_r=[.125,.1,.8,.8]
resax_r=[.125,.1,.8,.8]
ebbfldscale='0.2'
resscale='0.025'
ABC=[.025,.875]



region=regions(regionname)

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')


savepath='figures/png/' + grid + '_'  + '/ebbfldres/'
if not os.path.exists(savepath): os.makedirs(savepath)




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

if usemean==True:
    uatmp=data['ua'][starttime:,eidx].copy()
    uatmp[~zeta_bool1]=np.nan
    vatmp=data['va'][starttime:,eidx].copy()
    vatmp[~zeta_bool1]=np.nan
    q2u1=np.nanmean(uatmp,axis=0)
    q2v1=np.nanmean(vatmp,axis=0)
else:
    q2u1=data['ua'][starttime+offset+fld,eidx]
    q2v1=data['va'][starttime+offset+fld,eidx]

Q=ax_fld.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],q2u1,q2v1,angles='xy',scale_units='xy',scale=scale1,color='r',zorder=10)
#ax_fld.axis(region['region'])
prettyplot_ll(ax_fld,setregion=region)
#ax_fld.set_aspect(get_aspectratio(region))
#ax_fld.xaxis.set_tick_params(labelbottom='off')
plt.draw()
rec=mpl.patches.Rectangle((kl[0],kl[1]),kl[2],kl[3],transform=ax_fld.transAxes,fc='w',zorder=20)
ax_fld.add_patch(rec)
#ax_fld.annotate(r''+ebbfldscale+' m s$^{-1}$',xy=(kl[0]+.035,kl[1]+.15),xycoords='axes fraction',zorder=30,fontsize=8)
aqk=ax_fld.quiverkey(Q,kl[0]+.065,kl[1]+.05,float(ebbfldscale), r''+ebbfldscale+' m s$^{-1}$', labelpos='E',fontproperties={'size': 8})
aqk.set_zorder(30)
for label in ax_fld.get_yticklabels()[::2]:
    label.set_visible(False)
plotcoast(ax_fld,filename='world_GSHHS_f_L1.nc',color='k')


if usemean==True:
    f.savefig(savepath + grid + '_'+ name+'_'+regionname+'_meanfld.png',dpi=600)
else:
    f.savefig(savepath + grid + '_'+ name+'_'+regionname+'_fld.png',dpi=600)
plt.close(f)




f=plt.figure()
ax_ebb=f.add_axes(ebbax_r)

if usemean==True:
    uatmp=data['ua'][starttime:,eidx].copy()
    uatmp[zeta_bool1]=np.nan
    vatmp=data['va'][starttime:,eidx].copy()
    vatmp[zeta_bool1]=np.nan
    q2u1=np.nanmean(uatmp,axis=0)
    q2v1=np.nanmean(vatmp,axis=0)
else:
    q2u1=data['ua'][starttime+offset+ebb,eidx]
    q2v1=data['va'][starttime+offset+ebb,eidx]

Q=ax_ebb.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],q2u1,q2v1,angles='xy',scale_units='xy',scale=scale1,color='r',zorder=10)

#for label in ax_ebb.get_xticklabels():
#    label.set_visible(False)

#ax_ebb.axis(region['region'])
prettyplot_ll(ax_ebb,setregion=region)
#ax_ebb.set_aspect(get_aspectratio(region))
#ax_ebb.xaxis.set_tick_params(labelbottom='off')
plt.draw()
rec=mpl.patches.Rectangle((kl[0],kl[1]),kl[2],kl[3],transform=ax_ebb.transAxes,fc='w',zorder=20)
ax_ebb.add_patch(rec)
#ax_ebb.annotate(r''+ebbfldscale+' m s$^{-1}$',xy=(kl[0]+.035,kl[1]+.15),xycoords='axes fraction',zorder=30,fontsize=8)
aqk=ax_ebb.quiverkey(Q,kl[0]+.065,kl[1]+.05,float(ebbfldscale), r''+ebbfldscale+' m s$^{-1}$', labelpos='E',fontproperties={'size': 8})
aqk.set_zorder(30)
for label in ax_ebb.get_yticklabels()[::2]:
    label.set_visible(False)
plotcoast(ax_ebb,filename='world_GSHHS_f_L1.nc',color='k')


if usemean==True:
    f.savefig(savepath + grid + '_'+ name+'_'+regionname+'_meanebb.png',dpi=600)
else:
    f.savefig(savepath + grid + '_'+ name+'_'+regionname+'_ebb.png',dpi=600)
plt.close(f)



f=plt.figure()
resu=np.empty((len(eidx),len(data['time'][starttime:])))
resv=np.empty((len(eidx),len(data['time'][starttime:])))
if testing==False:
    for j in range(0,len(eidx)):
        print ("%d"%j)+"              "+("%f"%(j/len(eidx)*100)) 
        i=eidx[j]    
        [nameu, freq, tidecon_uv, xout]=t_tide(data['ua'][starttime:,i]+1j*data['va'][starttime:,i],stime=data['time'][starttime],lat=data['uvnodell'][i,1],output=False,constitnames=np.array([['M2  '],['N2  '],['S2  '],['K1  '],['O1  ']]))
        tpre=t_predic(data['time'][starttime:],nameu,freq,tidecon_uv)
        resu[j,:]=data['ua'][starttime:,i]-np.real(tpre).flatten()
        resv[j,:]=data['va'][starttime:,i]-np.imag(tpre).flatten()


ax_res=f.add_axes(resax_r)

Q=ax_res.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],np.mean(resu,axis=1),np.mean(resv,axis=1),angles='xy',scale_units='xy',color='r',scale=scale2,zorder=10)
#ax_res.axis(region['region'])
prettyplot_ll(ax_res,setregion=region)
#ax_res.set_aspect(get_aspectratio(region))
plt.draw()
rec=mpl.patches.Rectangle((kl[0],kl[1]),kl[2],kl[3],transform=ax_res.transAxes,fc='w',zorder=20)
ax_res.add_patch(rec)
#ax_res.annotate(r''+resscale+' m s$^{-1}$',xy=(kl[0]+.035,kl[1]+.15),xycoords='axes fraction',zorder=30,fontsize=8)
aqk=ax_res.quiverkey(Q,kl[0]+.04,kl[1]+.05,float(resscale), r''+resscale+' m s$^{-1}$', labelpos='E',fontproperties={'size': 8})
aqk.set_zorder(30)
for label in ax_res.get_yticklabels()[::2]:
    label.set_visible(False)
for label in ax_res.get_xticklabels()[::2]:
    label.set_visible(False)
plotcoast(ax_res,filename='world_GSHHS_f_L1.nc',color='k')



f.savefig(savepath + grid + '_'+ name+'_'+regionname+'_meanres.png',dpi=600)
plt.close(f)




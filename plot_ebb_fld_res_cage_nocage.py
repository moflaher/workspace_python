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


# Define names and types of data
name='sfm6_musq2_all_cages'
name2='sfm6_musq2_no_cages'
grid='sfm6_musq2'
regionname='musq_cage_tight2'
datatype='2d'
starttime=384
endtime=400
offset=1008
cagecolor='g'


#kelp_tight2
#kl=[.85,.875,.175,.06]
#crossdouble
kl=[.93,.825,.1,.08]
#should be able to set the rectangle using the plt.draw() bbox of the legend. do it next time.

region=regions(regionname)

### load the .nc file #####
#data = loadnc('/media/moflaher/MB_3TB/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
#data2 = loadnc('/media/moflaher/My Book/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')


savepath='figures/png/' + grid + '_' + datatype + '/ebb_fld_res_cage_no_cage/' + name + '_' + name2 + '/'
if not os.path.exists(savepath): os.makedirs(savepath)

#cages=np.genfromtxt('/media/moflaher/MB_3TB/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=np.genfromtxt('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)


nidx=get_nodes(data,region)
eidx=get_elements(data,region)

zeta_grad=np.gradient(data['zeta'][starttime:,nidx])[0]
fld=np.argmax(np.sum(zeta_grad>0,axis=1))
ebb=np.argmax(np.sum(zeta_grad<0,axis=1))


f=plt.figure()

ax_fld=f.add_axes([.125,.1,.8,.775])
ax_fld.triplot(data['trigrid'],lw=.5)
axsub1lw=1
for i in cages:
    tnodes=data['nv'][i,:]    
    ax_fld.plot(data['nodell'][tnodes[[0,1]],0],data['nodell'][tnodes[[0,1]],1],cagecolor,lw=axsub1lw,label='Drag')
    ax_fld.plot(data['nodell'][tnodes[[1,2]],0],data['nodell'][tnodes[[1,2]],1],cagecolor,lw=axsub1lw,label='No Drag')
    ax_fld.plot(data['nodell'][tnodes[[0,2]],0],data['nodell'][tnodes[[0,2]],1],cagecolor,lw=axsub1lw)
Q=ax_fld.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],data2['ua'][starttime+offset+fld,eidx],data2['va'][starttime+offset+fld,eidx],angles='xy',scale_units='xy',scale=200,zorder=10)
ax_fld.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],data['ua'][starttime+fld,eidx],data['va'][starttime+fld,eidx],angles='xy',scale_units='xy',scale=200,color='r',zorder=10)
ax_fld.axis(region['region'])
#for label in ax_fld.get_xticklabels():
#    label.set_visible(False)
prettyplot_ll(ax_fld,setregion=region)

rec=mpl.patches.Rectangle((kl[0]-kl[2]/2,kl[1]-kl[3]/1.25),kl[2],kl[3],transform=ax_fld.transAxes,fc='w',zorder=20)
ax_fld.add_patch(rec)
aqk=ax_fld.quiverkey(Q,kl[0],kl[1],0.5, r'0.5 m s$^{-1}$', labelpos='S',fontproperties={'size': 8})
aqk.set_zorder(30)

handles, labels = ax_fld.get_legend_handles_labels()
legend=ax_fld.legend(handles[0:2], labels[0:2],loc=1,prop={'size':8})
legend.set_zorder(100000)
t=legend.get_lines()
t[1].set_color('black')
#for label in legend.get_lines():
#    label.set_linewidth(1.5)

f.savefig(savepath + grid + '_'+regionname+'_fld_vectors_at_' + ("%04d" %(starttime+fld)) + '.png',dpi=600)
plt.close(f)




f=plt.figure()
ax_ebb=f.add_axes([.125,.1,.8,.775])
ax_ebb.triplot(data['trigrid'],lw=.5)
axsub1lw=1
for i in cages:
    tnodes=data['nv'][i,:]    
    ax_ebb.plot(data['nodell'][tnodes[[0,1]],0],data['nodell'][tnodes[[0,1]],1],cagecolor,lw=axsub1lw,label='Drag')
    ax_ebb.plot(data['nodell'][tnodes[[1,2]],0],data['nodell'][tnodes[[1,2]],1],cagecolor,lw=axsub1lw,label='No Drag')
    ax_ebb.plot(data['nodell'][tnodes[[0,2]],0],data['nodell'][tnodes[[0,2]],1],cagecolor,lw=axsub1lw)
Q2=ax_ebb.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],data2['ua'][starttime+offset+ebb,eidx],data2['va'][starttime+offset+ebb,eidx],angles='xy',scale_units='xy',scale=200,zorder=10)
ax_ebb.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],data['ua'][starttime+ebb,eidx],data['va'][starttime+ebb,eidx],angles='xy',scale_units='xy',scale=200,color='r',zorder=10)
ax_ebb.axis(region['region'])
#for label in ax_ebb.get_xticklabels():
#    label.set_visible(False)
prettyplot_ll(ax_ebb,setregion=region)

rec=mpl.patches.Rectangle((kl[0]-kl[2]/2,kl[1]-kl[3]/1.25),kl[2],kl[3],transform=ax_ebb.transAxes,fc='w',zorder=20)
ax_ebb.add_patch(rec)
aqk2=ax_ebb.quiverkey(Q2,kl[0],kl[1],0.5, r'0.5 m s$^{-1}$', labelpos='S',fontproperties={'size': 8})
aqk2.set_zorder(30)

handles, labels = ax_ebb.get_legend_handles_labels()
legend=ax_ebb.legend(handles[0:2], labels[0:2],loc=1,prop={'size':8})
legend.set_zorder(100000)
t=legend.get_lines()
t[1].set_color('black')
#for label in legend.get_lines():
#    label.set_linewidth(1.5)

f.savefig(savepath + grid +'_'+regionname+ '_ebb_vectors_at_' + ("%04d" %(starttime+offset+ebb)) + '.png',dpi=600)
plt.close(f)





resu=np.empty((len(eidx),len(data['time'][starttime:])))
resv=np.empty((len(eidx),len(data['time'][starttime:])))
resu2=np.empty((len(eidx),len(data['time'][starttime:])))
resv2=np.empty((len(eidx),len(data['time'][starttime:])))
for j in range(0,len(eidx)):
    print j
    i=eidx[j]
    [nameu, freq, tidecon_uv, xout]=t_tide(data['ua'][starttime:,i]+1j*data['va'][starttime:,i],stime=data['time'][starttime],lat=data['uvnodell'][i,1],output=False,constitnames=np.array([['M2  '],['N2  '],['S2  '],['K1  '],['O1  ']]))
    resu[j,:]=data['ua'][starttime:,i]-np.real(t_predic(data['time'][starttime:],nameu,freq,tidecon_uv)).flatten()
    resv[j,:]=data['va'][starttime:,i]-np.imag(t_predic(data['time'][starttime:],nameu,freq,tidecon_uv)).flatten()
    [nameu, freq, tidecon_uv, xout]=t_tide(data2['ua'][starttime:,i]+1j*data2['va'][starttime:,i],stime=data['time'][starttime],lat=data['uvnodell'][i,1],output=False,constitnames=np.array([['M2  '],['N2  '],['S2  '],['K1  '],['O1  ']]))
    resu2[j,:]=data2['ua'][(starttime+offset):,i]-np.real(t_predic(data2['time'][(starttime+offset):],nameu,freq,tidecon_uv)).flatten()
    resv2[j,:]=data2['va'][(starttime+offset):,i]-np.imag(t_predic(data2['time'][(starttime+offset):],nameu,freq,tidecon_uv)).flatten()



f=plt.figure()
ax_res=f.add_axes([.125,.1,.8,.775])
ax_res.triplot(data['trigrid'],lw=.5)
axsub1lw=1
for i in cages:
    tnodes=data['nv'][i,:]    
    ax_res.plot(data['nodell'][tnodes[[0,1]],0],data['nodell'][tnodes[[0,1]],1],cagecolor,lw=axsub1lw,label='Drag')
    ax_res.plot(data['nodell'][tnodes[[1,2]],0],data['nodell'][tnodes[[1,2]],1],cagecolor,lw=axsub1lw,label='No Drag')
    ax_res.plot(data['nodell'][tnodes[[0,2]],0],data['nodell'][tnodes[[0,2]],1],cagecolor,lw=axsub1lw)
Q3=ax_res.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],np.mean(resu2,axis=1),np.mean(resv2,axis=1),angles='xy',scale_units='xy',scale=50,color='r',zorder=10)
ax_res.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],np.mean(resu,axis=1),np.mean(resv,axis=1),angles='xy',scale_units='xy',scale=50,zorder=10)

ax_res.axis(region['region'])
#for label in ax_ebb.get_xticklabels():
#    label.set_visible(False)
prettyplot_ll(ax_res,setregion=region)

rec=mpl.patches.Rectangle((kl[0]-kl[2]/2,kl[1]-kl[3]/1.25),kl[2],kl[3],transform=ax_res.transAxes,fc='w',zorder=20)
ax_res.add_patch(rec)
aqk3=ax_res.quiverkey(Q3,kl[0],kl[1],0.1, r'0.1 m s$^{-1}$', labelpos='S',fontproperties={'size': 8})
aqk3.set_zorder(30)

handles, labels = ax_res.get_legend_handles_labels()
legend=ax_res.legend(handles[0:2], labels[0:2],loc=1,prop={'size':8})
legend.set_zorder(100000)
t=legend.get_lines()
t[1].set_color('black')
#for label in legend.get_lines():
#    label.set_linewidth(1.5)

f.savefig(savepath + grid +'_'+regionname+ '_res_mean_vectors.png',dpi=600)
plt.close(f)





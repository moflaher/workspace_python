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
regionname='musq_cage_tight2'
datatype='2d'
starttime=0
offset=1008


testing=False


resax_r=[.125,.1,.775,.8]
fcolor='g'





region=regions(regionname)

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

cages=np.genfromtxt('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)

savepath='figures/png/' + grid + '_' + datatype + '/res_dragnodrag_spatial/'
if not os.path.exists(savepath): os.makedirs(savepath)

tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2]],0],data['nodell'][data['nv'][i,[0,1,2]],1])) for i in cages ]
lsegr=PC(tmparray,facecolor = fcolor,edgecolor='None')

uv1=np.load('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv.npy')
uv1=uv1[()]
uv2=np.load('data/ttide/'+grid+'_'+name2+'_'+datatype+'_uv.npy')
uv2=uv2[()]

nidx=get_nodes(data,region)
eidx=get_elements(data,region)




resu=np.empty((len(eidx),len(data['time'][starttime:])))
resv=np.empty((len(eidx),len(data['time'][starttime:])))
resu2=np.empty((len(eidx),len(data['time'][starttime:])))
resv2=np.empty((len(eidx),len(data['time'][starttime:])))
if testing==False:
    for j in range(0,len(eidx)):
        print ("%d"%j)+"              "+("%f"%(j/len(eidx)*100)) 
        i=eidx[j]    
        tp1=t_predic(data['time'][starttime:],uv1['nameu'],uv1['freq'],uv1['tidecon'][i,:,:])
        resu[j,:]=data['ua'][starttime:,i]-np.real(tp1).flatten()
        resv[j,:]=data['va'][starttime:,i]-np.imag(tp1).flatten()
        tp2=t_predic(data2['time'][(starttime+offset):],uv2['nameu'],uv2['freq'],uv2['tidecon'][i,:,:])
        resu2[j,:]=data2['ua'][(starttime+offset):,i]-np.real(tp2).flatten()
        resv2[j,:]=data2['va'][(starttime+offset):,i]-np.imag(tp2).flatten()




resu_m=resu.mean(axis=1)
resv_m=resv.mean(axis=1)
resu2_m=resu2.mean(axis=1)
resv2_m=resv2.mean(axis=1)

rspeed=np.sqrt(resu_m**2+resv_m**2)
rspeed2=np.sqrt(resu2_m**2+resv2_m**2)



f=plt.figure()
ax_res=f.add_axes(resax_r)
ax_res.add_collection(lsegr)

pspeed=np.zeros(shape=data['ua'][0,:].shape)
pspeed[eidx]=rspeed2-rspeed

triax=ax_res.tripcolor(data['trigrid'],pspeed)

prettyplot_ll(ax_res,setregion=region,cb=triax,cblabel=r'Residual Speed Difference (m s$^{-1}$)')
plotcoast(ax_res,color='k',fill=True)

f.savefig(savepath + grid + '_'+ name+'_'+ name2+'_'+regionname+'_meanres.png',dpi=600)
plt.close(f)




f=plt.figure()

ax_res=f.add_axes(resax_r)
lsegr=PC(tmparray,facecolor = fcolor,edgecolor='None')
ax_res.add_collection(lsegr)

pspeed=np.zeros(shape=data['ua'][0,:].shape)
pspeed[eidx]=rspeed
triax=ax_res.tripcolor(data['trigrid'],pspeed)

prettyplot_ll(ax_res,setregion=region,cb=triax,cblabel=r'Residual Speed (m s$^{-1}$)')
plotcoast(ax_res,color='k',fill=True)

f.savefig(savepath + grid + '_'+ name+'_'+regionname+'_meanres.png',dpi=600)
plt.close(f)



f=plt.figure()

ax_res=f.add_axes(resax_r)
lsegr=PC(tmparray,facecolor = fcolor,edgecolor='None')
ax_res.add_collection(lsegr)

pspeed=np.zeros(shape=data['ua'][0,:].shape)
pspeed[eidx]=rspeed2
triax=ax_res.tripcolor(data['trigrid'],pspeed)

prettyplot_ll(ax_res,setregion=region,cb=triax,cblabel=r'Residual Speed (m s$^{-1}$)')
plotcoast(ax_res,color='k',fill=True)

f.savefig(savepath + grid + '_'+ name2+'_'+regionname+'_meanres.png',dpi=600)
plt.close(f)


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


# Define names and types of data
name='kit4_kelp_0.05'
grid='kit4'
regionname='cross_shore_1'
datatype='2d'
starttime=384
endtime=400



### load the .nc file #####
data = loadnc('/media/moe46/My Passport/kit4_runs/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

trigridxy = mplt.Triangulation(data['x'], data['y'],data['nv'])

vectorstart=np.array([-129.617,53.1032])
vectorend=np.array([-129.532,53.0352])
snv=(vectorend-vectorstart)/np.linalg.norm(vectorend-vectorstart)
spv=np.array([-snv[1],snv[0]])


vectorstart=np.array([-127396,-9801.19])
vectorend=np.array([-119650,-20630.2])
vectorx=np.array([vectorstart[0],vectorend[0]])
vectory=np.array([vectorstart[1],vectorend[1]])
snv=(vectorend-vectorstart)/np.linalg.norm(vectorend-vectorstart)



#angle between vectors but dont need, save for another day
#np.arccos(np.dot(snv,spv)

#a1=np.dot(A,B)*B
#a2=A-a1


savepath='figures/timeseries/' + grid + '_' + datatype + '/shore_current/' + name + '/'
if not os.path.exists(savepath): os.makedirs(savepath)




region={}
region['region']=[-130000,-118000,-25000,-5000]
eidx=get_elements_xy(data,region)


for i in range(starttime,endtime):
    print i
    inner=np.inner(np.vstack([data['ua'][i,:],data['va'][i,:]]).T,snv)
    ashore=np.vstack([inner*snv[0],inner*snv[1]]).T
    cshore=np.vstack([data['ua'][i,:],data['va'][i,:]]).T-ashore

    f,ax=plt.subplots(nrows=1,ncols=2)
    ashores=np.linalg.norm(ashore,axis=1)
    triax0=ax[0].tripcolor(trigridxy,ashores,vmin=ashores[eidx].min(),vmax=ashores[eidx].max())
    plt.colorbar(triax0,ax=ax[0])
    ax[0].plot(vectorx,vectory,'k')
    ax[0].set_title('Along shore')
    ax[0].axis([-130000,-118000,-25000,-5000])
    ax[0].set_xticklabels((ax[0].get_xticks())/1000,rotation=90)
    ax[0].set_yticklabels((ax[0].get_yticks())/1000)


    cshores=np.linalg.norm(cshore,axis=1)
    triax1=ax[1].tripcolor(trigridxy,cshores,vmin=cshores[eidx].min(),vmax=cshores[eidx].max())
    plt.colorbar(triax1,ax=ax[1])
    #plt.triplot(trigridxy,lw=.3)
    ax[1].plot(vectorx,vectory,'k')
    ax[1].set_title('Cross shore')
    ax[1].axis([-130000,-118000,-25000,-5000])
    ax[1].set_xticklabels((ax[1].get_xticks())/1000,rotation=90)
    ax[1].set_yticklabels((ax[1].get_yticks())/1000)


    f.tight_layout(pad=0.6)

    f.savefig(savepath + grid + '_shore_current_' + ("%04d" %(i)) + '.png',dpi=600)
    plt.close(f)





















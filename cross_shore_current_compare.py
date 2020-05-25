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
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)


# Define names and types of data
name1='kit4_45days_3'
name2='kit4_kelp_0.05'
grid='kit4'
regionname='cross_shore_1'

starttime=384
endtime=400



### load the .nc file #####
data1 = loadnc('/media/moe46/My Passport/kit4_runs/'+name1+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('/media/moe46/My Passport/kit4_runs/'+name2+'/output/',singlename=grid + '_0001.nc')
print('done load')
data1 = ncdatasort(data1)
print('done sort')

trigridxy = mplt.Triangulation(data1['x'], data1['y'],data1['nv'])

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


savepath='figures/timeseries/' + grid + '_'  + '/shore_current_compare/' + name1 + '_' +name2+ '/'
if not os.path.exists(savepath): os.makedirs(savepath)




region={}
region['region']=[-130000,-118000,-25000,-5000]
eidx=get_elements_xy(data1,region)


for i in range(starttime,endtime):
    print i


    f,ax=plt.subplots(nrows=2,ncols=2)



    inner=np.inner(np.vstack([data1['ua'][i,:],data1['va'][i,:]]).T,snv)
    ashore=np.vstack([inner*snv[0],inner*snv[1]]).T
    cshore=np.vstack([data1['ua'][i,:],data1['va'][i,:]]).T-ashore

    ashores=np.linalg.norm(ashore,axis=1)
    asmin=ashores[eidx].min()
    asmax=ashores[eidx].max()
    triax0=ax[0,0].tripcolor(trigridxy,ashores,vmin=asmin,vmax=asmax)
    plt.colorbar(triax0,ax=ax[0,0])
    ax[0,0].plot(vectorx,vectory,'k')
    ax[0,0].set_title('Along shore - No Kelp')
    ax[0,0].axis([-130000,-118000,-25000,-5000])
    ax[0,0].set_xticklabels((ax[0,0].get_xticks())/1000,rotation=90)
    ax[0,0].set_yticklabels((ax[0,0].get_yticks())/1000)

    cshores=np.linalg.norm(cshore,axis=1)
    csmin=cshores[eidx].min()
    csmax=cshores[eidx].max()
    triax1=ax[0,1].tripcolor(trigridxy,cshores,vmin=csmin,vmax=csmax)
    plt.colorbar(triax1,ax=ax[0,1])
    #plt.triplot(trigridxy,lw=.3)
    ax[0,1].plot(vectorx,vectory,'k')
    ax[0,1].set_title('Cross shore - No Kelp')
    ax[0,1].axis([-130000,-118000,-25000,-5000])
    ax[0,1].set_xticklabels((ax[0,1].get_xticks())/1000,rotation=90)
    ax[0,1].set_yticklabels((ax[0,1].get_yticks())/1000)





    inner=np.inner(np.vstack([data2['ua'][i,:],data2['va'][i,:]]).T,snv)
    ashore=np.vstack([inner*snv[0],inner*snv[1]]).T
    cshore=np.vstack([data2['ua'][i,:],data2['va'][i,:]]).T-ashore

    ashores=np.linalg.norm(ashore,axis=1)
    triax0=ax[1,0].tripcolor(trigridxy,ashores,vmin=asmin,vmax=asmax)
    plt.colorbar(triax0,ax=ax[1,0])
    ax[1,0].plot(vectorx,vectory,'k')
    ax[1,0].set_title('Along shore - Kelp (0.05)')
    ax[1,0].axis([-130000,-118000,-25000,-5000])
    ax[1,0].set_xticklabels((ax[1,0].get_xticks())/1000,rotation=90)
    ax[1,0].set_yticklabels((ax[1,0].get_yticks())/1000)

    cshores=np.linalg.norm(cshore,axis=1)
    triax1=ax[1,1].tripcolor(trigridxy,cshores,vmin=csmin,vmax=csmax)
    plt.colorbar(triax1,ax=ax[1,1])
    #plt.triplot(trigridxy,lw=.3)
    ax[1,1].plot(vectorx,vectory,'k')
    ax[1,1].set_title('Cross shore - Kelp (0.05)')
    ax[1,1].axis([-130000,-118000,-25000,-5000])
    ax[1,1].set_xticklabels((ax[1,1].get_xticks())/1000,rotation=90)
    ax[1,1].set_yticklabels((ax[1,1].get_yticks())/1000)



    f.tight_layout(pad=0.6)

    f.savefig(savepath + grid + '_shore_current_' + ("%04d" %(i)) + '.png',dpi=600)
    plt.close(f)





















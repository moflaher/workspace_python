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
name='kit4_kelp_0.05'
grid='kit4'
regionname='cross_shore_1'

starttime=384
endtime=0



### load the .nc file #####
data = loadnc('/media/moe46/My Passport/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

trigridxy = mplt.Triangulation(data['x'], data['y'],data['nv'])

data['time']=data['time']-678570


vectorstart=np.array([-127396,-9801.19])
vectorend=np.array([-119650,-20630.2])
vectorx=np.array([vectorstart[0],vectorend[0]])
vectory=np.array([vectorstart[1],vectorend[1]])
snv=(vectorend-vectorstart)/np.linalg.norm(vectorend-vectorstart)



#angle between vectors but dont need, save for another day
#np.arccos(np.dot(snv,spv)

#a1=np.dot(A,B)*B
#a2=A-a1


savepath='figures/png/' + grid + '_'  + '/shore_current_at_locations/'
if not os.path.exists(savepath): os.makedirs(savepath)




region={}
region['region']=[-130000,-118000,-25000,-5000]
eidx=get_elements_xy(data,region)

locations=[119754,118418,119991,118339]

f,ax=plt.subplots(nrows=4,ncols=1,sharex=True)
axtwin=ax.copy()
for a in range(0,4):
    axtwin[a]=ax[a].twinx()

for j in range(0,len(locations)):
    i=locations[j]
    inner=np.inner(np.vstack([data['ua'][starttime:,i],data['va'][starttime:,i]]).T,snv)
    ashore=np.vstack([inner*snv[0],inner*snv[1]]).T
    cshore=np.vstack([data['ua'][starttime:,i],data['va'][starttime:,i]]).T-ashore



    ashores=np.linalg.norm(ashore,axis=1)
    cshores=np.linalg.norm(cshore,axis=1)

  


    ax[j].plot(data['time'][starttime:],ashores,'r')
    axtwin[j].plot(data['time'][starttime:],cshores,'b',lw=.5)

    #ax[j].set_ylabel(r'Along Shore (ms$^{-1}$)', color='r')
    #axtwin[j].set_ylabel(r'Cross Shore (ms$^{-1}$)', color='b')
    #ax[j].set_title('Along shore')
    #ax[j].axis([-130000,-118000,-25000,-5000])
    #ax[j].set_xticklabels((ax[0].get_xticks())/1000,rotation=90)
    #ax[j].set_yticklabels((ax[0].get_yticks())/1000)


ax[j].set_xlabel(r'Time')
ax[j].annotate(r'Along Shore (ms$^{-1}$)',xy=(.025,.625),xycoords='figure fraction',rotation=90,color='r')
ax[j].annotate(r'Cross Shore (ms$^{-1}$)',xy=(.95,.625),xycoords='figure fraction',rotation=90,color='b')

f.tight_layout(rect=[.05, 0, .95, 1])
f.savefig(savepath + grid + '_shore_current_at_location.png',dpi=600)
plt.close(f)





















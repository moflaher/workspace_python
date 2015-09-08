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


# Define names and types of data
name='kit4_45days_3'
name2='kit4_kelp_20m_0.018'
grid='kit4'
datatype='2d'
starttime=384
endtime=624
offset=0

labelstr=['A','B']#,'C','D']
labelstr2=['C','D']#,'G','H']

ylim1=[0,.5]
ylim2=[0,0.4]

### load the .nc file #####
data = loadnc('/media/moflaher/My Book/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('/media/moflaher/MB_3TB/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')
#data = loadnc('/media/moe46/My Passport/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
#data2 = loadnc('/media/moe46/Hardy/spet_18_work/'+name2+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')


trigridxy = mplt.Triangulation(data['x'], data['y'],data['nv'])

data['time']=data['time']-678570

#leftshore
vectorstart=np.array([-127396,-9801.19])
vectorend=np.array([-119650,-20630.2])
vectorx=np.array([vectorstart[0],vectorend[0]])
vectory=np.array([vectorstart[1],vectorend[1]])
snv=(vectorend-vectorstart)/np.linalg.norm(vectorend-vectorstart)

#south shore
vectorstart=np.array([-115000,-55000])
vectorend=np.array([-115000,-65000])
vectorx=np.array([vectorstart[0],vectorend[0]])
vectory=np.array([vectorstart[1],vectorend[1]])
snv=(vectorend-vectorstart)/np.linalg.norm(vectorend-vectorstart)
locations=[89579,88053]

#right shore
vectorstart=np.array([-105000,-15000])
vectorend=np.array([-103000,-17000])
vectorx=np.array([vectorstart[0],vectorend[0]])
vectory=np.array([vectorstart[1],vectorend[1]])
snv=(vectorend-vectorstart)/np.linalg.norm(vectorend-vectorstart)
locations=[71718,66651]#,119991,118339]

#right shore2
vectorstart=np.array([-105000,-15000])
vectorend=np.array([-103000,-17000])
vectorx=np.array([vectorstart[0],vectorend[0]])
vectory=np.array([vectorstart[1],vectorend[1]])
snv=(vectorend-vectorstart)/np.linalg.norm(vectorend-vectorstart)
locations=[126991,115472]#,119991,118339]

#south shore2
vectorstart=np.array([-115000,-55000])
vectorend=np.array([-115000,-65000])
vectorx=np.array([vectorstart[0],vectorend[0]])
vectory=np.array([vectorstart[1],vectorend[1]])
snv=(vectorend-vectorstart)/np.linalg.norm(vectorend-vectorstart)
locations=[85049,77563]

#angle between vectors but dont need, save for another day
#np.arccos(np.dot(snv,spv)

#a1=np.dot(A,B)*B
#a2=A-a1


savepath='figures/png/' + grid + '_' + datatype + '/shore_current_at_locations/'
if not os.path.exists(savepath): os.makedirs(savepath)




region={}
region['region']=[-130000,-118000,-25000,-5000]
eidx=get_elements_xy(data,region)



f,ax=plt.subplots(nrows=2,ncols=2,sharex=True)
axtwin=ax.copy()
for a in range(0,2):
    axtwin[a,0]=ax[a,0].twinx()
    axtwin[a,1]=ax[a,1].twinx() 

for j in range(0,len(locations)):
    i=locations[j]
    inner=np.inner(np.vstack([data['ua'][starttime:endtime,i],data['va'][starttime:endtime,i]]).T,snv)
    ashore=np.vstack([inner*snv[0],inner*snv[1]]).T
    cshore=np.vstack([data['ua'][starttime:endtime,i],data['va'][starttime:endtime,i]]).T-ashore



    ashores=np.linalg.norm(ashore,axis=1)
    cshores=np.linalg.norm(cshore,axis=1)

  

    
    ax[j,0].plot(data['time'][starttime:endtime],ashores,'r')
    axtwin[j,0].plot(data['time'][starttime:endtime],cshores,'b',lw=.5)
    ax[j,0].annotate(labelstr[j],xy=(.025,.925),xycoords='axes fraction')
    ax[j,0].set_ylim(ylim1)
    axtwin[j,0].set_ylim(ylim2)

    for label in ax[j,0].get_xticklabels():
        label.set_fontsize(8)
    for label in ax[j,0].get_yticklabels():
        label.set_fontsize(8)
    for label in ax[j,0].get_yticklabels():
        label.set_color('r')
    #for label in ax[j,0].get_yticklabels()[::2]:
    #    label.set_visible(False)

    for label in axtwin[j,0].get_xticklabels():
        label.set_fontsize(8)
    for label in axtwin[j,0].get_yticklabels():
        label.set_fontsize(8)
    for label in axtwin[j,0].get_yticklabels():
        label.set_color('b')
    #for label in axtwin[j,0].get_yticklabels()[::2]:
    #    label.set_visible(False)

    #ax[j].set_ylabel(r'Along Shore (ms$^{-1}$)', color='r')
    #axtwin[j].set_ylabel(r'Cross Shore (ms$^{-1}$)', color='b')
    #ax[j].set_title('Along shore')
    #ax[j].axis([-130000,-118000,-25000,-5000])
    #ax[j].set_xticklabels((ax[0].get_xticks())/1000,rotation=90)
    #ax[j].set_yticklabels((ax[0].get_yticks())/1000)


ax[j,0].set_xlabel(r'Time (day)')
ax[j,0].annotate(r'Along Shore (m s$^{-1}$)',xy=(.025,.625),xycoords='figure fraction',rotation=90,color='r')
ax[j,0].annotate(r'Cross Shore (m s$^{-1}$)',xy=(.95,.625),xycoords='figure fraction',rotation=90,color='b')



for j in range(0,len(locations)):
    i=locations[j]
    inner=np.inner(np.vstack([data2['ua'][starttime:endtime,i],data2['va'][starttime:endtime,i]]).T,snv)
    ashore=np.vstack([inner*snv[0],inner*snv[1]]).T
    cshore=np.vstack([data2['ua'][starttime:endtime,i],data2['va'][starttime:endtime,i]]).T-ashore



    ashores=np.linalg.norm(ashore,axis=1)
    cshores=np.linalg.norm(cshore,axis=1)

  


    ax[j,1].plot(data['time'][starttime:endtime],ashores,'r')
    axtwin[j,1].plot(data['time'][starttime:endtime],cshores,'b',lw=.5)
    ax[j,1].annotate(labelstr2[j],xy=(.025,.925),xycoords='axes fraction')
    ax[j,1].set_ylim(ylim1)
    axtwin[j,1].set_ylim(ylim2)

    #ax[j].set_ylabel(r'Along Shore (ms$^{-1}$)', color='r')
    #axtwin[j].set_ylabel(r'Cross Shore (ms$^{-1}$)', color='b')
    #ax[j].set_title('Along shore')
    #ax[j].axis([-130000,-118000,-25000,-5000])
    #ax[j].set_xticklabels((ax[0].get_xticks())/1000,rotation=90)
    #ax[j].set_yticklabels((ax[0].get_yticks())/1000)


    for label in ax[j,1].get_xticklabels():
        label.set_fontsize(8)
    for label in ax[j,1].get_yticklabels():
        label.set_fontsize(8)
    for label in ax[j,1].get_yticklabels():
        label.set_color('r')
    #for label in ax[j,1].get_yticklabels()[::2]:
     #   label.set_visible(False)

    for label in axtwin[j,1].get_xticklabels():
        label.set_fontsize(8)
    for label in axtwin[j,1].get_yticklabels():
        label.set_fontsize(8)
    for label in axtwin[j,1].get_yticklabels():
        label.set_color('b')
    #for label in axtwin[j,1].get_yticklabels()[::2]:
    #    label.set_visible(False)



ax[j,1].set_xlabel(r'Time (day)')
#ax[j,1].annotate(r'Along Shore (m s$^{-1}$)',xy=(.52,.625),xycoords='figure fraction',rotation=90,color='r')
#ax[j,1].annotate(r'Cross Shore (m s$^{-1}$)',xy=(.455,.625),xycoords='figure fraction',rotation=90,color='b')


#ax[j,1].annotate(r'No kelp',xy=(.2,.95),xycoords='figure fraction',color='k')
#ax[j,1].annotate(r'Kelp (0.018)',xy=(.7,.95),xycoords='figure fraction',color='k')

f.tight_layout(rect=[.05, 0, .95, .95])
#f.subplots_adjust(wspace=.75)
f.savefig(savepath + grid + '_'+name+'_'+name2+'_shore_current_at_location_compare_'+("%d"%locations[0])+'_'+("%d"%locations[1])+'.png',dpi=600)
plt.close(f)





















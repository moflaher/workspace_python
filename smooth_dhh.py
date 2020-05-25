from __future__ import division,print_function
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import scipy.io as sio
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
from StringIO import StringIO
from gridtools import *
from datatools import *
from misctools import *
from plottools import *
from projtools import *
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
import copy


# Define names and types of data
name='dormerge_36_16_chigbay.nei'
grid='acadia_bof_v2_2d'

cutoff=0.5
smoothing=50


### load the mesh files #####
path='/mnt/old_main/home/moe46/Desktop/school/bathymetry_data/redepth_folder/voucher_after_jiggle/'
data=load_nei2fvcom(path+name)
data=get_nv(data)
data=ncdatasort(data)
data=get_dhh(data)

savepath='figures/png/' + grid + '/smooth_dhh/'
if not os.path.exists(savepath): os.makedirs(savepath)


region={}
region['region']=np.array([np.min(data['lon']),np.max(data['lon']),np.min(data['lat']),np.max(data['lat'])])
region=expand_region(region,dist=10000)
region=regions('capeenrage')
eidx=get_elements(data,region)
nidx=get_nodes(data,region)



# Plot depth
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
clims=np.percentile(data['h'][nidx],[5,95])
triax=ax.tripcolor(data['trigrid'],data['h'],vmin=clims[0],vmax=clims[1])
prettyplot_ll(ax,setregion=region,grid=True,cblabel='Depth (m)',cb=triax)
f.savefig(savepath + grid +'_depth.png',dpi=600)
plt.close(f)

# Plot dh/h
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
clims=np.percentile(data['dhh'][eidx],[5,95])
triax=ax.tripcolor(data['trigrid'],data['dhh'],vmin=clims[0],vmax=clims[1])
prettyplot_ll(ax,setregion=region,grid=True,cblabel=r'$\frac{\delta H}{H}$',cb=triax)
f.savefig(savepath + grid +'_dhh.png',dpi=600)
plt.close(f)

modified=np.arange(data['nnodes'])

for loop in range(smoothing):
    data=get_dhh(data)
    datasave=copy.deepcopy(data)  

    print(np.sum(data['dhh'][eidx]>cutoff))
    for i in eidx:#range(len(data['dhh'])):
        if data['dhh'][i]>cutoff:
            h=data['h'][data['nv'][i,:]]
            hm=np.min(h)
            
            if hm==0:
                print('There is a zero value at '+("%d"%i))
            
            for j in range(-1,2):
                #print(j)
                #if (np.fabs(h[j]-h[j+1])/hm)>cutoff:
                n=data['neighbours'][data['nv'][i,j]]
                n=n[n!=0]
                print('newpoint --------------------------------')
                print(data['h'][n-1])
                if True:
                    #get neighbours of neighbours
                    n=data['neighbours'][n-1,:]
                    n=n[n!=0]
                    n=np.unique(n)
                    print(data['h'][n-1])
                    ##only smooth a point once
                    #if np.sum(modified==data['nv'][i,j])==1:
                        #modified[data['nv'][i,j]]=999999999
                        #datasave['h'][data['nv'][i,j]]=data['h'][n-1].mean()
                datasave['h'][data['nv'][i,j]]=data['h'][n-1].mean()
                    
                    
       
    save_neifile('data/grid_stuff/'+grid+ '_smoothed_dhh_'+("%.2f"%cutoff)+'_loop_'+("%d"%loop)+'.nei',datasave)
      
    datasave=get_dhh(datasave)               
                    
    # Plot depth
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    clims=np.percentile(datasave['h'][nidx],[5,95])
    triax=ax.tripcolor(data['trigrid'],datasave['h'],vmin=clims[0],vmax=clims[1])
    prettyplot_ll(ax,setregion=region,grid=True,cblabel='Depth (m)',cb=triax)
    f.savefig(savepath + grid +'_depth_smoothed_dhh_'+("%.2f"%cutoff)+'_loop_'+("%d"%loop)+'.png',dpi=600)
    plt.close(f)

    # Plot dh/h
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    clims=np.percentile(datasave['dhh'][eidx],[5,95])
    triax=ax.tripcolor(data['trigrid'],datasave['dhh'],vmin=clims[0],vmax=clims[1])
    prettyplot_ll(ax,setregion=region,grid=True,cblabel=r'$\frac{\delta H}{H}$',cb=triax)
    f.savefig(savepath + grid +'_dhh_smoothed_dhh_'+("%.2f"%cutoff)+'_loop_'+("%d"%loop)+'.png',dpi=1200)
    plt.close(f)
    
    data=copy.deepcopy(datasave)
                
















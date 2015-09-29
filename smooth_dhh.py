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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import copy


# Define names and types of data
name='vh_high_clean_hpc'
grid='vh_high'
datatype='2d'
cutoff=1
smoothing=10


### load the mesh files #####
data=load_fvcom_files('runs/'+grid+'/'+name+'/input',grid)
data.update(loadnei('runs/'+grid+'/'+name+'/input/' +grid+ '.nei'))
data=get_nv(data)
data=ncdatasort(data)
data=get_dhh(data)

savepath='figures/png/' + grid + '_' + datatype + '/smoooth_dhh/'
if not os.path.exists(savepath): os.makedirs(savepath)


region={}
region['region']=np.array([np.min(data['lon']),np.max(data['lon']),np.min(data['lat']),np.max(data['lat'])])
region=expand_region(region,dist=10000)



# Plot depth
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigrid'],data['h'])
prettyplot_ll(ax,setregion=region,grid=True,cblabel='Depth (m)',cb=triax)
f.savefig(savepath + grid +'_depth.png',dpi=600)
plt.close(f)

# Plot dh/h
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigrid'],data['dhh'])
prettyplot_ll(ax,setregion=region,grid=True,cblabel=r'$\frac{\delta H}{H}$',cb=triax)
f.savefig(savepath + grid +'_dhh.png',dpi=600)
plt.close(f)


for loop in range(smoothing):
    data=get_dhh(data)
    datasave=copy.deepcopy(data)  

    print(np.sum(data['dhh']>cutoff))
    for i in range(len(data['dhh'])):
        if data['dhh'][i]>cutoff:
            h=data['h'][data['nv'][i,:]]
            hm=np.min(h)
            
            if hm==0:
                print('There is a zero value at '+("%d"%i))
            
            for j in range(-1,2):
                #print(j)
                if (np.fabs(h[j]-h[j+1])/hm)>cutoff:
                    n=data['neighbours'][data['nv'][i,j]]
                    n=n[n!=0]
                    datasave['h'][data['nv'][i,j]]=data['h'][n-1].mean()
                    
                    
       
    savenei('data/grid_stuff/'+grid+ '_smoothed_dhh_'+("%.2f"%cutoff)+'_loop_'+("%d"%loop)+'.nei',datasave)
      
    datasave=get_dhh(datasave)               
                    
    # Plot depth
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],datasave['h'])
    prettyplot_ll(ax,setregion=region,grid=True,cblabel='Depth (m)',cb=triax)
    f.savefig(savepath + grid +'_depth_smoothed_dhh_'+("%.2f"%cutoff)+'_loop_'+("%d"%loop)+'.png',dpi=600)
    plt.close(f)

    # Plot dh/h
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],datasave['dhh'])
    prettyplot_ll(ax,setregion=region,grid=True,cblabel=r'$\frac{\delta H}{H}$',cb=triax)
    f.savefig(savepath + grid +'_dhh_smoothed_dhh_'+("%.2f"%cutoff)+'_loop_'+("%d"%loop)+'.png',dpi=1200)
    plt.close(f)
    
    data=copy.deepcopy(datasave)
                
















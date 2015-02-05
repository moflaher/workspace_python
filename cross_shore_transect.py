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
name='kit4_45days_3'
grid='kit4'




### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data,trifinder=True)
print 'done sort'



vectorstart=np.array([-128.865,53.565])
vectorend=np.array([-128.84,53.61])
vectorx=np.array([vectorstart[0],vectorend[0]])
vectory=np.array([vectorstart[1],vectorend[1]])
snv=(vectorend-vectorstart)/np.linalg.norm(vectorend-vectorstart)
spv=np.array([-snv[1],snv[0]])


#idxs=closest_element(data,vectorstart)
#idxe=closest_element(data,vectorend)

#vectorstart=data['uvnodell'][idxs,:]
#vectorend=data['uvnodell'][idxe,:]
#vectorx=np.array([vectorstart[0],vectorend[0]])
#vectory=np.array([vectorstart[1],vectorend[1]])
#snv2=(vectorend-vectorstart)/np.linalg.norm(vectorend-vectorstart)



#angle between vectors but dont need, save for another day
#np.arccos(np.dot(snv,spv)

#a1=np.dot(A,B)*B
#a2=A-a1


savepath='data/cross_shore_transect/'
if not os.path.exists(savepath): os.makedirs(savepath)


xi=np.linspace(vectorstart[0],vectorend[0],50)
yi=np.linspace(vectorstart[1],vectorend[1],50)

us=data['u'].shape
numlay=us[1]
fillarray_u=np.empty((us[0],numlay,len(xi)))
fillarray_v=np.empty((us[0],numlay,len(xi)))
fillarray_w=np.empty((us[0],numlay,len(xi)))
fillalong=np.empty((us[0],numlay,len(xi)))

print 'interp uvw on path'

for i in range(0,len(xi)):
    print i
    for j in range(0,numlay):
        print j
        fillarray_u[:,j,i],fillarray_v[:,j,i],fillarray_w[:,j,i]=interp_vel(data,[xi[i],yi[i]],layer=j)


print 'Calc along path current'

for i in range(0,len(xi)):
    print i
    for j in range(0,numlay):
        print j
        inner=np.inner(np.vstack([fillarray_u[:,j,i],fillarray_v[:,j,i]]).T,snv)
        along=np.vstack([inner*snv[0],inner*snv[1]]).T
        tmp=np.multiply(np.sign(np.arctan2(along[:,1],along[:,0])),np.linalg.norm(along,axis=1))
        fillalong[:,j,i]=tmp







savedic={}

savedic['u']=fillarray_u
savedic['v']=fillarray_v
savedic['w']=fillarray_w
savedic['along']=fillalong


np.save(savepath+grid+'_'+name+'_'+('%f'%vectorx[0])+'_'+('%f'%vectorx[1])+'_'+('%f'%vectory[0])+'_'+('%f'%vectory[1])+'_'+('%d'%numlay)+'_'+('%d'%len(xi))+'.npy',savedic)




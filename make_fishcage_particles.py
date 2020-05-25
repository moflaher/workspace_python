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
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)




# Define names and types of data
name='sfm6_musq2_half_cages'
grid='sfm6_musq2'



### load the .nc file #####
data = loadnc('runs/sfm6_musq2/' + name + '/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data,trifinder=True)
print('done sort')

cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
if np.shape(cages)!=():
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2]],0],data['nodell'][data['nv'][i,[0,1,2]],1])) for i in cages ]
    color='g'



sortedcages=np.zeros([100,data['nv'].shape[0]],dtype=bool)
cagesleft=cages
cagecnt=0
while (len(cagesleft)>0):    
    cage1=np.array([cagesleft[0]])
    clen=1
    cnt=0
    while (cnt<clen):
        #print cage1
        v=data['nbe'][cage1[cnt],:]
        cage1=np.append(cage1,cagesleft[np.vectorize(lambda x: x in v)(cagesleft)])
        idx=np.unique(cage1,return_index=True)[1]
        #print idx
        cage1=cage1[np.sort(idx)]
        cnt+=1
        clen=cage1.shape[0]    
        #print 'cnt:'+ ("%d"%cnt)
        #print clen

    print('cagecnt:' +("%d"%cagecnt))
    #print cage1  
    sortedcages[cagecnt,cage1]=True
    cagecnt+=1
    #print np.vectorize(lambda x: x in cage1)(cagesleft)
    cagesleft=np.delete(cagesleft,np.flatnonzero(np.vectorize(lambda x: x in cage1)(cagesleft)))
    
sortedcages=sortedcages[0:cagecnt,:]


savepath='figures/png/' + grid + '_'  + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)


host={}
for i in range(len(sortedcages)):
    host[str(i)]=np.flatnonzero(sortedcages[i,:])

savex=np.array([])
savey=np.array([])
numpar=1000
for key in host:
    lonmax=data['uvnodell'][host[key],0].max()
    lonmin=data['uvnodell'][host[key],0].min()
    latmax=data['uvnodell'][host[key],1].max()
    latmin=data['uvnodell'][host[key],1].min()
    dist=np.linalg.norm(np.array([lonmax,latmax])-np.array([lonmin,latmin]))
    cenx=data['uvnodell'][host[key],0].mean()
    ceny=data['uvnodell'][host[key],1].mean()

    ranx=((np.random.rand(numpar*10000)-.5)*dist*10)+cenx
    rany=((np.random.rand(numpar*10000)-.5)*dist*10)+ceny

    parhost=data['trigrid_finder'].__call__(ranx,rany)

    ranxnew=ranx[np.in1d(parhost,host[key])]
    ranynew=rany[np.in1d(parhost,host[key])]
    
    savex=np.append(savex,ranxnew[:numpar])
    savey=np.append(savey,ranynew[:numpar])
    
    
    
savedic={}
#proj=gridproj(grid)
x,y,proj=lcc(data['lon'],data['lat'])
x,y=proj(savex,savey)
savedic['x']=x
savedic['y']=y
sio.savemat('data/pt_starts/sfm6_musq2_half_cages_1.mat',mdict=savedic)  







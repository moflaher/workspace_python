from __future__ import division
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
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pandas as pd


# Define names and types of data
tmpn='no'
name='sfm6_musq2_'+tmpn+'_cages'
grid='sfm6_musq2'
regionname='musq_cage_tight'
datatype='2d'
lfolder='25_part_'+tmpn+'_cage_in60min_time1min_out10min'
lname=''+tmpn+'_cages_25_part_sfm6_musq2_0'


### load the .nc file #####
data = loadnc('/media/moflaher/My Book/cages/' + name +'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

savepath='figures/png/' + grid + '_' + datatype + '/lagtracker/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)

trigridxy = mplt.Triangulation(data['x'], data['y'],data['nv'])
region=regions(regionname)


savelag=(sio.loadmat('/home/moflaher/workspace_matlab/lagtracker/savedir/'+lfolder+'/'+lname+'.mat',squeeze_me=True,struct_as_record=False))['savelag']
cages=np.genfromtxt('/media/moflaher/My Book/cages/sfm6_musq2_all_cages/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)

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

    print 'cagecnt:' +("%d"%cagecnt)
    #print cage1  
    sortedcages[cagecnt,cage1]=True
    cagecnt+=1
    #print np.vectorize(lambda x: x in cage1)(cagesleft)
    cagesleft=np.delete(cagesleft,np.flatnonzero(np.vectorize(lambda x: x in cage1)(cagesleft)))
    
sortedcages=sortedcages[0:cagecnt,:]



distance=np.empty([savelag.x.shape[0]])
for i in range(0,savelag.x.shape[0]):
    distance[i]=np.nansum(np.sqrt(np.diff(savelag.x[i,:])**2+np.diff(savelag.y[i,:])**2))

host=trigridxy.get_trifinder().__call__(savelag.x[:,0],savelag.y[:,0])
pltarray=np.zeros([data['nv'].shape[0],])
hostcnt=np.zeros([data['nv'].shape[0],])
for i in range(0,len(host)):
    if ~np.isnan(distance[i]):
        hostcnt[host[i]]+=1
        pltarray[host[i]]=distance[i]+pltarray[host[i]]

final=np.zeros([data['nv'].shape[0],])
for i in np.unique(host):
    if hostcnt[i]!=0:
        final[i]=(pltarray[i]/1000)/hostcnt[i]

rows = ['%d' % x for x in range(1,sortedcages.shape[0]+1)]

cageposx=np.empty([sortedcages.shape[0],])
cageposy=np.empty([sortedcages.shape[0],])
cagemean=np.empty([sortedcages.shape[0],])
cagestd=np.empty([sortedcages.shape[0],])
for i in range(0,sortedcages.shape[0]):
    print i
    cageposx[i]=np.mean(data['uvnodell'][sortedcages[i,:],0])
    cageposy[i]=np.mean(data['uvnodell'][sortedcages[i,:],1]) 
    cagemean[i]=np.mean(final[sortedcages[i,:]])
    cagestd[i]=np.std(final[sortedcages[i,:]])


plt.close()
ax1=plt.axes([.15,0,.8,1])
#ax1 = plt.subplot2grid((1,3), (0,0), colspan=2)
#ax2 = plt.subplot2grid((1,3), (0,2), colspan=1)
ax1.triplot(data['trigrid'],lw=.3)
ax1.plot(data['uvnodell'][cages,0],data['uvnodell'][cages,1],'r.')
for i in range(0,sortedcages.shape[0]):
    ax1.text(cageposx[i],cageposy[i],"%d"%(i+1),fontsize=20,color='b')

ax1.text(-66.89,45.0525,'No Farms',fontsize=18,color='k')
prettyplot_ll(ax1,setregion=region,grid=True)
mytable=ax1.table(cellText=np.vstack([cagemean.round(1),cagestd.round(1)]),colLabels=rows,rowLabels=['Mean (km)','Std (km)'],loc='right',fontsize=20, bbox=[.175, 1.15, .85, .4])

tcel=mytable.get_celld()[0, 1]
mytable.add_cell(0,-1,tcel.get_width(),tcel.get_height(),text='    Farm Number')



plt.savefig(savepath +lname+'_path_distance.png',dpi=600)





maxdistance=np.zeros([savelag.x.shape[0],1])
for j in range(0,savelag.x.shape[1]):        
    maxdistance=np.nanmax(np.hstack([maxdistance.reshape(-1,1),np.sqrt((savelag.x[:,0]-savelag.x[:,j])**2+(savelag.y[:,0]-savelag.y[:,j])**2).reshape(-1,1)   ]),axis=1)
        
pltarray=np.zeros([data['nv'].shape[0],])
hostcnt=np.zeros([data['nv'].shape[0],])
for i in range(0,len(host)):
    if ~np.isnan(maxdistance[i]):
        hostcnt[host[i]]+=1
        pltarray[host[i]]=maxdistance[i]+pltarray[host[i]]

final=np.zeros([data['nv'].shape[0],])
for i in np.unique(host):
    if hostcnt[i]!=0:
        final[i]=(pltarray[i]/1000)/hostcnt[i]

cageposx=np.empty([sortedcages.shape[0],])
cageposy=np.empty([sortedcages.shape[0],])
cagemean=np.empty([sortedcages.shape[0],])
cagestd=np.empty([sortedcages.shape[0],])
for i in range(0,sortedcages.shape[0]):
    print i
    cageposx[i]=np.mean(data['uvnodell'][sortedcages[i,:],0])
    cageposy[i]=np.mean(data['uvnodell'][sortedcages[i,:],1]) 
    cagemean[i]=np.mean(final[sortedcages[i,:]])
    cagestd[i]=np.std(final[sortedcages[i,:]])

plt.close()
ax1=plt.axes([.15,0,.8,1])
#ax1 = plt.subplot2grid((1,3), (0,0), colspan=2)
#ax2 = plt.subplot2grid((1,3), (0,2), colspan=1)
ax1.triplot(data['trigrid'],lw=.3)
ax1.plot(data['uvnodell'][cages,0],data['uvnodell'][cages,1],'r.')
for i in range(0,sortedcages.shape[0]):
    ax1.text(cageposx[i],cageposy[i],"%d"%(i+1),fontsize=20,color='b')

ax1.text(-66.89,45.0525,'No Farms',fontsize=18,color='k')
prettyplot_ll(ax1,setregion=region,grid=True)
mytable=ax1.table(cellText=np.vstack([cagemean.round(1),cagestd.round(1)]),colLabels=rows,rowLabels=['Mean (km)','Std (km)'],loc='right',fontsize=20, bbox=[.175, 1.15, .85, .4])

tcel=mytable.get_celld()[0, 1]
mytable.add_cell(0,-1,tcel.get_width(),tcel.get_height(),text='    Farm Number')

plt.savefig(savepath +lname+'_max_distance.png',dpi=600)




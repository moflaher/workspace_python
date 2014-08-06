from __future__ import division
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
from numba import jit
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name='kit4_45days_3'
grid='kit4'
regionname='kit4_area3'
datatype='2d'
starttime=384
spacing=500


### load the .nc file #####
data = loadnc('/media/moflaher/My Book/kit4_runs/' + name + '/output/',singlename=grid + '_0001.nc')

print 'done load'
data = ncdatasort(data)
print 'done sort'


region=regions(regionname)

def interzeta(rlhzero,interpheight,i):
        tidx=(np.where(rlhzero[i,:]<interpheight)[0]).min()
        weightdiff=rlhzero[i,tidx-1]-rlhzero[i,tidx]
        uweight=1-((rlhzero[i,tidx-1]-interpheight)/weightdiff)
        lweight=1-((interpheight-rlhzero[i,tidx])/weightdiff)    
        if (tidx==20):  
            tu=(data['u'][starttime:,tidx-1,i]*uweight)
            tv=(data['v'][starttime:,tidx-1,i]*uweight)
        else:
            tu=((data['u'][starttime:,tidx-1,i]*uweight)+(data['u'][starttime:,tidx,i]*lweight))
            tv=((data['v'][starttime:,tidx-1,i]*uweight)+(data['v'][starttime:,tidx,i]*lweight))
        
        
        return tu,tv








interpheight=1

levelheight=data['uvh']*data['siglay'][:,0]
levelheight=-1*levelheight
rlh=data['uvh']-levelheight
rlhzero=np.hstack((rlh,np.zeros((data['nele'],1))))

starttime=384
#newu=np.zeros((len(data['time'][starttime:]),data['nele']))
#newv=np.zeros((len(data['time'][starttime:]),data['nele']))




#for i in range(0,data['nele']):
#    print i
#    newu[:,i],newv[:,i]=interzeta(rlhzero,interpheight,i)



#np.save('newu.npy',newu)
#np.save('newv.npy',newv)
newu=np.load('newu.npy')
newv=np.load('newv.npy')


sidx=equal_vectors(data,region,spacing)


savepath='figures/png/' + grid + '_' + datatype + '/maxs_1m/'
if not os.path.exists(savepath): os.makedirs(savepath)



zeta_grad=np.gradient(data['zeta'][starttime:,:])[0]



ebbu=newu.copy()
ebbv=newv.copy()
ebbu[zeta_grad>0]=np.nan
ebbv[zeta_grad>0]=np.nan
ebbspeed=np.nanargmax(np.sqrt(ebbu**2+ebbv**2),axis=0)
del ebbu
del ebbv


fldu=newu.copy()
fldv=newv.copy()
fldu[zeta_grad<0]=np.nan
fldv[zeta_grad<0]=np.nan
fldspeed=np.nanargmax(np.sqrt(fldu**2+fldv**2),axis=0)
del fldu
del fldv



plt.close()

ebbuplot=newu[ebbspeed,range(0,data['nele'])].copy()
ebbvplot=newv[ebbspeed,range(0,data['nele'])].copy()
ebbspeedplot=np.sqrt(ebbuplot**2+ebbvplot**2)
ebbuplot[ebbspeedplot<=.01]=np.nan
ebbvplot[ebbspeedplot<=.01]=np.nan
#Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],ebbuplot[sidx],ebbvplot[sidx],width=.002,pivot='tail',headwidth=3.,headlength=4)

Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],ebbuplot[sidx],ebbvplot[sidx],angles='xy',scale_units='xy',scale=10)
qk = plt.quiverkey(Q,  .2,1.05,0.25, '0.25 ms^-1', labelpos='W')
plt.grid()
plt.axis(region['region'])
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
#plt.show()
plt.savefig(savepath + name + '_' + regionname +'_vector_maxebb_s_' + ("%d" %spacing) + '.png',dpi=1200)





plt.close()
flduplot=newu[fldspeed,range(0,data['nele'])].copy()
fldvplot=newv[fldspeed,range(0,data['nele'])].copy()
fldspeedplot=np.sqrt(flduplot**2+fldvplot**2)
flduplot[fldspeedplot<=.01]=np.nan
fldvplot[fldspeedplot<=.01]=np.nan
#Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],flduplot[sidx],fldvplot[sidx],width=.002,pivot='tail',headwidth=3.,headlength=4)
Q=plt.quiver(data['uvnodell'][sidx,0],data['uvnodell'][sidx,1],flduplot[sidx],fldvplot[sidx],angles='xy',scale_units='xy',scale=10)
qk = plt.quiverkey(Q, .2,1.05,0.25, '0.25 ms^-1', labelpos='W')
plt.grid()
plt.axis(region['region'])
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
#plt.show()
plt.savefig(savepath + name + '_' + regionname +'_vector_maxfld_s_' + ("%d" %spacing) + '.png',dpi=1200)

plt.close()
plt.tripcolor(data['trigrid'],np.max(np.sqrt(newu**2+newv**2),axis=0),vmin=1.15*np.min(np.max(np.sqrt(newu[:,sidx]**2+newv[:,sidx]**2),axis=0)),vmax=.85*np.max(np.max(np.sqrt(newu[:,sidx]**2+newv[:,sidx]**2),axis=0)))
plt.colorbar()
plt.grid()
plt.axis(region['region'])
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
#plt.show()
plt.savefig(savepath + name + '_' + regionname +'_maxspeed.png',dpi=1200)

from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from folderpath import *
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pandas as pd
import ttide

# Define names and types of data
name='tg_yar'
grid='obs'

starttime=0
intv=29
window=intv*24*60

    
    
savepath='{}/{}_{}/TG_ttide_window/{}_{}m/'.format(datapath,grid,datatype,name,window)
if not os.path.exists(savepath): os.makedirs(savepath)


tg65=np.load('/home/mif001/scratch/obs/tg/tg_yar_clean.npy')
tg65[tg65[:,1]>100,1]=np.nan

tgtime=tg65[:,0]
tgzeta=tg65[:,1]
tgzeta1=tg65[:,1]
tgtime=tgtime[~np.isnan(tgzeta)]
tgzeta=tgzeta[~np.isnan(tgzeta)]
time=np.arange(tgtime.min(),tgtime.max(),60/(24.0*3600))
mtgzeta=ipt.interp1d(tgtime.flatten(),tgzeta.flatten(),time)

num=len(range(0,len(time)-window,np.round(intv/3).astype(int)*24*60))


m2amp=np.empty((num,))
m2phs=np.empty((num,))
m2nans=np.empty((num,))


for j,i in enumerate(range(0,len(time)-window,np.round(intv/3).astype(int)*24*60)):
    out=ttide.t_tide(mtgzeta[starttime+i:window+i],stime=time[starttime+i],dt=np.diff(time)[0]*24,synth=-1,out_style=None)
    idx=np.argwhere(out['nameu']=='M2  ')
    m2amp[j]=out['tidecon'][idx,0]
    m2phs[j]=out['tidecon'][idx,2]
    m2nans[j]=np.isnan(tgzeta1[starttime+i:window+i]).sum()




f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.plot(m2amp,'r',lw=2,label='M2 Amp.')
#ax.set_xlabel('Time (hours)')
ax.set_ylabel('M2 Amp. (m)')
f.suptitle('Min: {}    Max: {}    Range: {}\n Mean: {} STD: {} '.format(m2amp.min(),m2amp.max(),m2amp.max()-m2amp.min(),m2amp.mean(),np.sqrt(np.var(m2amp))))
f.savefig('{}m2amp_{}.png'.format(savepath,intv),dpi=300)


f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.plot(m2phs,'r',lw=2,label='M2 Phase')
#ax.set_xlabel('Time (hours)')
ax.set_ylabel('M2 Phase (degree)')
f.suptitle('Min: {}    Max: {}    Range: {}\n Mean: {}  STD: {}'.format(m2phs.min(),m2phs.max(),m2phs.max()-m2phs.min(),m2phs.mean(),np.sqrt(np.var(m2phs))))
f.savefig('{}m2phs_{}.png'.format(savepath,intv),dpi=300)


df=pd.DataFrame(np.vstack([m2amp,m2phs,m2nans]).T,columns=['Amp','Phase','NaNCount'])
df.to_csv('{}{}_data.csv'.format(savepath,name))

    

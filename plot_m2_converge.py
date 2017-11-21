from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import ttide


# Define names and types of data
name='sjh_lr_v1_year_origbc_wet_hfx100'
grid='sjh_lr_v1'
datatype='2d'
starttime=0
endtime=25


### load the .nc file #####
data = loadnc('/fs/vnas_Hdfo/odis/suh001/scratch/sjh_lr_v1/runs/{}/output/'.format(name),singlename=grid + '_0001.nc')
print('done load')


tg65=np.load('/home/mif001/scratch/obs/tg/tg65_clean.npy')


savepath='figures/png/' + grid + '_' + datatype + '/m2_converge/' + name + '/'
if not os.path.exists(savepath): os.makedirs(savepath)

time=data['time']-4/24.0
idx=np.argwhere((tg65[:,0]>=(time[0]-1/24.0)) & (tg65[:,0]<=(time[-1]+1/24.0)))
tgtime=tg65[idx,0]
tgzeta=tg65[idx,1]-np.nanmean(tg65[idx,1])
tgtime=tgtime[~np.isnan(tgzeta)]
tgzeta=tgzeta[~np.isnan(tgzeta)]	

mtgzeta=ipt.interp1d(tgtime.flatten(),tgzeta.flatten(),time)


n=55468

m2amp=np.empty((5000,))
m2amp_tg=np.empty((5000,))
m2amp_cur=np.empty((5000,))

for i in range(5000):
    print(i)
    out=ttide.t_tide(data['zeta'][starttime+i:endtime+i,n],stime=time[starttime+i],dt=np.diff(data['time'])[0]*24,synth=-1,out_style=None,lat=data['lat'][n])#,constitnames=np.array(['M2  ']))
    idx=np.argwhere(out['nameu']=='M2  ')
    amp=out['tidecon'][idx,0]
    m2amp[i]=amp

    out=ttide.t_tide(mtgzeta[starttime+i:endtime+i],stime=time[starttime+i],dt=np.diff(data['time'])[0]*24,synth=-1,out_style=None,lat=data['lat'][n])#,constitnames=np.array(['M2  ']))
    idx=np.argwhere(out['nameu']=='M2  ')
    amp=out['tidecon'][idx,0]
    m2amp_tg[i]=amp

    out=ttide.t_tide(data['ua'][starttime+i:endtime+i,n]+1j*data['va'][starttime+1:endtime+1,n],stime=time[starttime+i],dt=np.diff(data['time'])[0]*24,synth=-1,out_style=None,lat=data['lat'][n])#,constitnames=np.array(['M2  ']))
    idx=np.argwhere(out['nameu']=='M2  ')
    amp=out['tidecon'][idx,0]
    m2amp_cur[i]=amp



f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.plot(m2amp,'r',lw=2,label='Model M2 Amp.')
ax.plot(m2amp_tg,'b',lw=1,label='Real M2 Amp.')
ax.set_xlabel('Time (hours)')
ax.set_ylabel('M2 Amp. (m)')
ax.legend()
f.savefig('{}m2_converge_all.png'.format(savepath),dpi=300)
ax.axis([-5,200,0,3.5])

f.savefig('{}m2_converge_100.png'.format(savepath),dpi=300)

f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.plot(m2amp_cur,'r',lw=2,label='Model M2 Amp.')
ax.set_xlabel('Time (hours)')
ax.set_ylabel('M2 Amp. (m)')
ax.legend()
f.savefig('{}m2_converge_cur_all.png'.format(savepath),dpi=300)
ax.axis([-5,200,0,3.5])

f.savefig('{}m2_converge_cur_100.png'.format(savepath),dpi=300)


















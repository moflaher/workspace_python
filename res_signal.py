from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from folderpath import *
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
from stattools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pandas as pd
import netCDF4 as n4
import copy
import matplotlib.dates as dates
import argparse
import ttide
import scipy.fftpack as fftp


tgname='tg_00365'
name1='sjh_lr_v1_sub_fit_N4_test_nest_bfric02_taup'
name2='test_1_redo'
name4='sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1_jcool0'
name5='sjh_lr_v1_year_coare3_wu_mixing'
data1=loadnc('/home/moflaher/Desktop/workspace_python/dataout/sjh_lr_v1_sub/tg/'+name1,tgname+'_fvcom.nc',False)
data2=loadnc('/home/moflaher/Desktop/workspace_python/dataout/sjh_lr_v1_sub/tg/'+name2,tgname+'_fvcom.nc',False)
data4=loadnc('/home/moflaher/Desktop/workspace_python/dataout/sjh_lr_v1/tg/'+name4,tgname+'_fvcom.nc',False)
data5=loadnc('/home/moflaher/Desktop/workspace_python/dataout/sjh_lr_v1/tg/'+name5,tgname+'_fvcom.nc',False)
obs=loadnc('/mnt/drive_1/obs/east/all',tgname+'.nc',False)



tt1=ttide.t_tide(data1['zeta'],lat=data1['lat'],dt=1)
tt2=ttide.t_tide(data2['zeta'],lat=data2['lat'],dt=1)
tt4=ttide.t_tide(data4['zeta'],lat=data4['lat'],dt=1)
tt5=ttide.t_tide(data5['zeta'],lat=data5['lat'],dt=1)

t1,d1,d2=interp_clean_common(data2['time'],data2['zeta'],obs['time'],obs['zeta'],500,-500)
time=np.arange(t1[0],t1[-1]+1/24.0,1/24.0)
testz=ipt.interp1d(t1,d2,time)

tt3=ttide.t_tide(testz,lat=obs['lat'],dt=1)


FFT1=sp.fft(tt1['xres'])
FFT2=sp.fft(tt2['xres'])
FFT3=sp.fft(tt3['xres'])
FFT4=sp.fft(tt4['xres'])
FFT5=sp.fft(tt5['xres'])
freqs1=fftp.fftfreq(tt1['xres'].size,3600)
freqs2=fftp.fftfreq(tt2['xres'].size,3600)
freqs3=fftp.fftfreq(tt3['xres'].size,3600)
freqs4=fftp.fftfreq(tt4['xres'].size,3600)
freqs5=fftp.fftfreq(tt5['xres'].size,3600)


f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8]);
ax.plot((1/freqs3)/3600,(np.abs(FFT3)),'k',lw=2,label=tgname)
ax.plot((1/freqs2)/3600,(np.abs(FFT2)),'r',lw=1,label=''+name2)
ax.plot((1/freqs1)/3600,(np.abs(FFT1)),'b',lw=.5,label=''+name1)
ax.plot((1/freqs4)/3600,(np.abs(FFT4)),'g',lw=.5,label=''+name4)
ax.plot((1/freqs5)/3600,(np.abs(FFT5)),'y',lw=.5,label=''+name5)
ax.set_xlim([0,500])
ax.legend()
#f.show()
f.savefig('figures/png/misc/{}_residual_freq_withold.png'.format(tgname),dpi=300)



NS=[3,6,12,24]
for N in NS:
    rFFT3=np.convolve(np.abs(FFT3), np.ones((N,))/N, mode='same')
    rFFT2=np.convolve(np.abs(FFT2), np.ones((N,))/N, mode='same')
    rFFT1=np.convolve(np.abs(FFT1), np.ones((N,))/N, mode='same')
    rFFT4=np.convolve(np.abs(FFT4), np.ones((N,))/N, mode='same')
    rFFT5=np.convolve(np.abs(FFT5), np.ones((N,))/N, mode='same')

    f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8]);
    ax.plot((1/freqs3)/3600,(np.abs(rFFT3)),'k',lw=2,label=tgname)
    ax.plot((1/freqs2)/3600,(np.abs(rFFT2)),'r',lw=1,label=''+name2)
    ax.plot((1/freqs1)/3600,(np.abs(rFFT1)),'b',lw=.5,label=''+name1)
    ax.plot((1/freqs4)/3600,(np.abs(rFFT4)),'g',lw=.5,label=''+name4)
    ax.plot((1/freqs5)/3600,(np.abs(rFFT5)),'y',lw=.5,label=''+name5)
    ax.set_xlim([0,500])
    ax.set_ylim([0,100])
    ax.legend()
    #f.show()
    f.savefig('figures/png/misc/{}_residual_freq_running_mean_n{}_withold.png'.format(tgname,N),dpi=300)



f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8]);
ax.plot((1/freqs3)/3600,np.abs(rFFT3)-np.abs(rFFT3),'k',lw=2,label=tgname)
ax.plot((1/freqs2)/3600,np.abs(rFFT3)-np.abs(rFFT2),'r',lw=1,label=''+name2)
ax.plot((1/freqs1)/3600,np.abs(rFFT3)-np.abs(rFFT1),'b',lw=.5,label=''+name1)
ax.plot((1/freqs4)/3600,np.abs(rFFT3)-np.abs(rFFT4),'g',lw=.5,label=''+name4)
ax.plot((1/freqs5)/3600,np.abs(rFFT3)-np.abs(rFFT5),'y',lw=.5,label=''+name5)
ax.set_xlim([0,500])
ax.set_ylim([-30,30])
ax.legend()
#f.show()
f.savefig('figures/png/misc/{}_residual_freq_running_mean_n{}_obs-model.png'.format(tgname,NS[-1]),dpi=300)

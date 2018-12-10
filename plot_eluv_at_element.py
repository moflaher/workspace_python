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
import scipy.io as sio
import scipy.fftpack as fftp


# Define names and types of data
name='kit4_kelp_20m_0.018'
name2='kit4_45days_3'
grid='kit4'

starttime=384
endtime=432
endtime=456
elements=[77566,80184,80168,74835]
elements=[83637,85846]

single=False

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')
data['time']=data['time']-678576

savepath='figures/png/' + grid + '_'  + '/eluv_at_element/'
if not os.path.exists(savepath): os.makedirs(savepath)
base_dir = os.path.dirname(__file__)


data['uvzeta']=(data['zeta'][starttime:endtime,data['nv'][:,0]] + data['zeta'][starttime:endtime,data['nv'][:,1]] + data['zeta'][starttime:endtime,data['nv'][:,2]]) / 3.0
data2['uvzeta']=(data2['zeta'][starttime:endtime,data2['nv'][:,0]] + data2['zeta'][starttime:endtime,data2['nv'][:,1]] + data2['zeta'][starttime:endtime,data2['nv'][:,2]]) / 3.0



for i in range(0,len(elements)):

    f,ax=plt.subplots(nrows=3,ncols=1,sharex=True)

    ax[0].plot(data['time'][starttime:endtime],np.zeros(shape=data['time'][starttime:endtime].shape),'k')
    ax[0].plot(data['time'][starttime:endtime],data['uvzeta'][:,elements[i]],'r',lw=1,label='Kelp')
    ax[0].plot(data2['time'][starttime:endtime],data2['uvzeta'][:,elements[i]],'k',label='No kelp')

    ax[1].plot(data['time'][starttime:endtime],np.zeros(shape=data['time'][starttime:endtime].shape),'k')
    ax[1].plot(data['time'][starttime:endtime],data['ua'][starttime:endtime,elements[i]],'r',lw=1,label='Kelp')
    ax[1].plot(data2['time'][starttime:endtime],data2['ua'][starttime:endtime,elements[i]],'k',label='No kelp')
    ax[1].plot(data['time'][starttime:endtime],np.zeros(shape=data['ua'][starttime:endtime,elements[i]].shape)+data['ua'][starttime:endtime,elements[i]].mean(),'r-.',lw=1,label='Kelp mean')
    ax[1].plot(data2['time'][starttime:endtime],np.zeros(shape=data2['ua'][starttime:endtime,elements[i]].shape)+data2['ua'][starttime:endtime,elements[i]].mean(),'k-.',label='No kelp mean')


    ax[2].plot(data['time'][starttime:endtime],np.zeros(shape=data['time'][starttime:endtime].shape),'k')
    ax[2].plot(data['time'][starttime:endtime],data['va'][starttime:endtime,elements[i]],'r',lw=1,label='Kelp')
    ax[2].plot(data2['time'][starttime:endtime],data2['va'][starttime:endtime,elements[i]],'k',label='No kelp')
    ax[2].plot(data['time'][starttime:endtime],np.zeros(shape=data['va'][starttime:endtime,elements[i]].shape)+data['va'][starttime:endtime,elements[i]].mean(),'r-.',lw=1,label='Kelp mean')
    ax[2].plot(data2['time'][starttime:endtime],np.zeros(shape=data2['va'][starttime:endtime,elements[i]].shape)+data2['va'][starttime:endtime,elements[i]].mean(),'k-.',label='No kelp mean')



    ax[0].set_ylabel(r'Elevation (m)',fontsize=8)
    ax[1].set_ylabel(r'u-velocity (m s$^{-1}$)',fontsize=8)
    ax[2].set_ylabel(r'v-velocity (m s$^{-1}$)',fontsize=8)
    ax[2].set_xlabel(r'Time (day)',fontsize=8)

    for label in ax[0].get_yticklabels()[::2]:
        label.set_visible(False)
    for label in ax[1].get_yticklabels()[::2]:
        label.set_visible(False)
    for label in ax[2].get_yticklabels()[::2]:
        label.set_visible(False)

    for label in ax[0].get_yticklabels():
        label.set_fontsize(8)
    for label in ax[1].get_yticklabels():
        label.set_fontsize(8)
    for label in ax[2].get_yticklabels():
        label.set_fontsize(8)
    for label in ax[2].get_xticklabels():
        label.set_fontsize(8)

    handles, labels = ax[0].get_legend_handles_labels()
    legend=ax[0].legend(handles, labels,prop={'size':6},loc=4)
    for label in legend.get_lines():
        label.set_linewidth(1.5)

    handles, labels = ax[1].get_legend_handles_labels()
    legend=ax[1].legend(handles, labels,prop={'size':6},loc=4)
    for label in legend.get_lines():
        label.set_linewidth(1.5)
    handles, labels = ax[2].get_legend_handles_labels()
    legend=ax[2].legend(handles, labels,prop={'size':6},loc=4)
    for label in legend.get_lines():
        label.set_linewidth(1.5)

    ABC=[.02,.87]
    ax[0].text(ABC[0],ABC[1],"A",transform=ax[0].transAxes,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3},zorder=31)
    ax[1].text(ABC[0],ABC[1],"B",transform=ax[1].transAxes,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3},zorder=31)
    ax[2].text(ABC[0],ABC[1],"C",transform=ax[2].transAxes,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3},zorder=31)

    if single==True:
        ax[1].set_ylim([-.4,.1])
        ax[2].set_ylim([-.2,.4])

    f.subplots_adjust(hspace=.075)

    f.savefig(savepath + grid + '_'+name+'_'+name2+'_eluv_at_element_'+("%d"%elements[i])+'.png',dpi=300)
    plt.close(f)


    #tempdic={}
    #tempdic['uvzeta_drag']=data['uvzeta'][:,elements[i]]
    #tempdic['uvzeta_nodrag']=data2['uvzeta'][:,elements[i]]

    #tempdic['ua_drag']=data['ua'][starttime:endtime,elements[i]]
    #tempdic['ua_nodrag']=data2['ua'][starttime:endtime,elements[i]]

    #tempdic['va_drag']=data['va'][starttime:endtime,elements[i]]
    #tempdic['va_nodrag']=data2['va'][starttime:endtime,elements[i]]

    #sio.savemat(os.path.join(base_dir,'data',grid+'_'+name+'_'+name2+'_eluv_at_element_'+("%d"%elements[i])+'.mat'),mdict=tempdic)




    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])


    FFT=sp.fft(data['ua'][starttime:,elements[i]]+1j*data['va'][starttime:,elements[i]])
    FFT2=sp.fft(data2['ua'][starttime:,elements[i]]+1j*data2['va'][starttime:,elements[i]])
    freqs=fftp.fftfreq(data['ua'][starttime:,elements[i]].size,3600)

    ax.plot((1/freqs)/3600,(np.abs(FFT)),'r',lw=1,label='Kelp')
    ax.plot((1/freqs)/3600,(np.abs(FFT2)),'k',lw=1,label='No kelp')
    ax.grid()
    ax.set_xlim([0,30])
    ax.set_xlabel(r'Time (h)')
    ax.legend()    


    f.savefig(savepath + grid + '_'+name+'_'+name2+'_fft_at_element_'+("%d"%elements[i])+'.png',dpi=300)



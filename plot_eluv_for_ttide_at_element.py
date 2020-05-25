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
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
import scipy.io as sio
sys.path.append('/home/moe46/Desktop/school/workspace_python/ttide_py/ttide/')
sys.path.append('/home/moflaher/Desktop/workspace_python/ttide_py/ttide/')
from t_tide import t_tide
from t_predic import t_predic

# Define names and types of data
name='kit4_kelp_20m_0.018'
name2='kit4_45days_3'
grid='kit4'

starttime=384
plotlength=72
elements=[77566,80184,80168]
#elements=[80184]

single=False

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')
data['time']=data['time']-678576

savepath='figures/png/' + grid + '_'  + '/eluv_for_ttide_at_element/'
if not os.path.exists(savepath): os.makedirs(savepath)
base_dir = os.path.dirname(__file__)

cons=np.array([['M2  '],['M4  ']])




for i in range(0,len(elements)):
    j=elements[i]
    print 'Element: ' +("%d"%j)

    f,ax=plt.subplots(nrows=3,ncols=1,sharex=True)

    [nameu, freq, tidecon_uv, xout]=t_tide(data['ua'][starttime:,j]+1j*data['va'][starttime:,j],stime=data['time'][starttime],lat=data['uvnodell'][j,1],output=False,constitnames=cons)
    tpre=t_predic(data['time'][starttime:(starttime+plotlength)],nameu,freq,tidecon_uv)

    [nameu, freq, tidecon_uv2, xout]=t_tide(data2['ua'][starttime:,j]+1j*data2['va'][starttime:,j],stime=data['time'][starttime],lat=data['uvnodell'][j,1],output=False,constitnames=cons)
    tpre2=t_predic(data['time'][starttime:(starttime+plotlength)],nameu,freq,tidecon_uv2)


    uvel1=(data['zeta'][starttime:,data['nv'][j,0]] + data['zeta'][starttime:,data['nv'][j,1]] + data['zeta'][starttime:,data['nv'][j,2]]) / 3.0
    [nameu, freq, tidecon_el, xout]=t_tide(uvel1,stime=data['time'][starttime],lat=data['uvnodell'][j,1],output=False,constitnames=cons)
    tpre_el=t_predic(data['time'][starttime:(starttime+plotlength)],nameu,freq,tidecon_el)

    uvel2=(data['zeta'][starttime:,data['nv'][j,0]] + data['zeta'][starttime:,data['nv'][j,1]] + data['zeta'][starttime:,data['nv'][j,2]]) / 3.0
    [nameu, freq, tidecon_el2, xout]=t_tide(uvel2,stime=data['time'][starttime],lat=data['uvnodell'][j,1],output=False,constitnames=cons)
    tpre_el2=t_predic(data['time'][starttime:(starttime+plotlength)],nameu,freq,tidecon_el2)




    ax[0].plot(data['time'][starttime:(starttime+plotlength)],np.zeros(shape=data['time'][starttime:(starttime+plotlength)].shape),'k')
    ax[0].plot(data['time'][starttime:(starttime+plotlength)], tpre_el,'r',lw=1,label='Kelp')
    ax[0].plot(data2['time'][starttime:(starttime+plotlength)], tpre_el2,'k',label='No kelp')

    ax[1].plot(data['time'][starttime:(starttime+plotlength)],np.zeros(shape=data['time'][starttime:(starttime+plotlength)].shape),'k')
    ax[1].plot(data['time'][starttime:(starttime+plotlength)],np.real(tpre),'r',lw=1,label='Kelp')
    ax[1].plot(data2['time'][starttime:(starttime+plotlength)],np.real(tpre2),'k',label='No kelp')
    ax[1].plot(data['time'][starttime:(starttime+plotlength)],np.zeros(shape=np.real(tpre).shape)+np.real(tpre).mean(),'r-.',lw=1,label='Kelp mean')
    ax[1].plot(data2['time'][starttime:(starttime+plotlength)],np.zeros(shape=np.real(tpre2).shape)+np.real(tpre2).mean(),'k-.',label='No kelp mean')


    ax[2].plot(data['time'][starttime:(starttime+plotlength)],np.zeros(shape=data['time'][starttime:(starttime+plotlength)].shape),'k')
    ax[2].plot(data['time'][starttime:(starttime+plotlength)],np.imag(tpre),'r',lw=1,label='Kelp')
    ax[2].plot(data2['time'][starttime:(starttime+plotlength)],np.imag(tpre2),'k',label='No kelp')
    ax[2].plot(data['time'][starttime:(starttime+plotlength)],np.zeros(shape=np.imag(tpre).shape)+np.imag(tpre).mean(),'r-.',lw=1,label='Kelp mean')
    ax[2].plot(data2['time'][starttime:(starttime+plotlength)],np.zeros(shape=np.imag(tpre2).shape)+np.imag(tpre2).mean(),'k-.',label='No kelp mean')



    ax[0].set_ylabel(r'Elevation for M2 M4 (m)',fontsize=8)
    ax[1].set_ylabel(r'u-velocity for M2 M4 (m s$^{-1}$)',fontsize=8)
    ax[2].set_ylabel(r'v-velocity for M2 M4 (m s$^{-1}$)',fontsize=8)
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

    f.savefig(savepath + grid + '_'+name+'_'+name2+'_eluv_for_M2_M4_at_element_'+("%d"%j)+'.png',dpi=300)

    #tempdic={}
    #tempdic['uvzeta_drag']=data['uvzeta'][:,j]
    #tempdic['uvzeta_nodrag']=data2['uvzeta'][:,j]

    #tempdic['ua_drag']=data['ua'][starttime:,j]
    #tempdic['ua_nodrag']=data2['ua'][starttime:,j]

    #tempdic['va_drag']=data['va'][starttime:,j]
    #tempdic['va_nodrag']=data2['va'][starttime:,j]

    #sio.savemat(os.path.join(base_dir,'data',grid+'_'+name+'_'+name2+'_eluv_for_'+cons[0][0]+'at_element_'+("%d"%j)+'.mat'),mdict=tempdic)













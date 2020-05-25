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
import scipy.fftpack as fftp


# Define names and types of data
name_orig='kit4_kelp_nodrag'
name_change='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'

starttime=384
endtime=432
endtime=456
locx=[-129.4875,-129.4875,-129.4875]
locy=[52.664,52.65,52.6375]
ABC=[.02,.87]
ABC_text=['N','M','S']

single=False

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name_orig+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name_change+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')
data['time']=data['time']-678576


cages=loadcage('runs/'+grid+'/' +name_change+ '/input/' +grid+ '_cage.dat')
if np.shape(cages)!=():
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2]],0],data['nodell'][data['nv'][i,[0,1,2]],1])) for i in cages ]
    color='g'

savepath='figures/png/' + grid + '_'  + '/vvv_for_kelp/'
if not os.path.exists(savepath): os.makedirs(savepath)








f,ax=plt.subplots(nrows=3,ncols=1,sharex=True,sharey=True)

for i in range(0,3):
    element=closest_element(data,[locx[i],locy[i]])

    ax[i].plot(data['time'][starttime:endtime],data['va'][starttime:endtime,element],'r',lw=1,label='Kelp')
    ax[i].plot(data2['time'][starttime:endtime],data2['va'][starttime:endtime,element],'k',label='No kelp')
    #ax[i].axhline(data['va'][starttime:endtime,element].mean(),color='r',lw=1,label='Kelp mean')
    #ax[i].axhline(data2['va'][starttime:endtime,element].mean(),color='k',label='No kelp mean')
    ax[i].axhline(0,color='k')
    ax[i].set_ylabel(r'v-velocity (m s$^{-1}$)',fontsize=8)

    handles, labels = ax[i].get_legend_handles_labels()
    legend=ax[i].legend(handles, labels,prop={'size':6},loc=4)
    for label in legend.get_lines():
        label.set_linewidth(1.5)
#    for label in ax[i].get_yticklabels()[::2]:
#        label.set_visible(False)
    for label in ax[i].get_yticklabels():
        label.set_fontsize(8)
    ax[i].text(ABC[0],ABC[1],ABC_text[i],transform=ax[i].transAxes,bbox={'facecolor':'white','edgecolor':'None', 'alpha':1, 'pad':3},zorder=31)


ax[2].set_xlabel(r'Time (day)',fontsize=8)
for label in ax[2].get_xticklabels():
    label.set_fontsize(8)




if single==True:
    ax[1].set_ylim([-.4,.1])
    ax[2].set_ylim([-.2,.4])

f.subplots_adjust(hspace=.075)

f.savefig(savepath + grid + '_'+name_orig+'_'+name_change+'_vvv_for_kelp_'+("%f"%locx[0])+'_'+("%f"%locy[0])+'_'+("%f"%locx[1])+'_'+("%f"%locy[1])+'_'+("%f"%locx[2])+'_'+("%f"%locy[2])+'.png',dpi=300)
plt.close(f)




f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.triplot(data['trigrid'],lw=.5)
prettyplot_ll(ax,setregion=regions('kit4_kelp_tight2_kelpfield'))
plotcoast(ax,filename='pacific.nc',color='None',fill=True)
lseg=PC(tmparray,facecolor = 'g',edgecolor='None')
ax.add_collection(lseg)
for i in range(0,3):
    ax.plot(locx[i],locy[i],'b*')
f.savefig(savepath + grid + '_'+name_orig+'_'+name_change+'_vvv_for_kelp_'+("%f"%locx[0])+'_'+("%f"%locy[0])+'_'+("%f"%locx[1])+'_'+("%f"%locy[1])+'_'+("%f"%locx[2])+'_'+("%f"%locy[2])+'_locations.png',dpi=600)
plt.close(f)


    #tempdic={}
    #tempdic['uvzeta_drag']=data['uvzeta'][:,elements[i]]
    #tempdic['uvzeta_nodrag']=data2['uvzeta'][:,elements[i]]

    #tempdic['ua_drag']=data['ua'][starttime:endtime,elements[i]]
    #tempdic['ua_nodrag']=data2['ua'][starttime:endtime,elements[i]]

    #tempdic['va_drag']=data['va'][starttime:endtime,elements[i]]
    #tempdic['va_nodrag']=data2['va'][starttime:endtime,elements[i]]

    #sio.savemat(os.path.join(base_dir,'data',grid+'_'+name+'_'+name2+'_eluv_at_element_'+("%d"%elements[i])+'.mat'),mdict=tempdic)




#    f=plt.figure()
#    ax=f.add_axes([.125,.1,.775,.8])


#    FFT=sp.fft(data['ua'][starttime:,elements[i]]+1j*data['va'][starttime:,elements[i]])
#    FFT2=sp.fft(data2['ua'][starttime:,elements[i]]+1j*data2['va'][starttime:,elements[i]])
#    freqs=fftp.fftfreq(data['ua'][starttime:,elements[i]].size,3600)

#    ax.plot((1/freqs)/3600,(np.abs(FFT)),'r',lw=1,label='Kelp')
#    ax.plot((1/freqs)/3600,(np.abs(FFT2)),'k',lw=1,label='No kelp')
#    ax.grid()
#    ax.set_xlim([0,30])
#    ax.set_xlabel(r'Time (h)')
#    ax.legend()    


#    f.savefig(savepath + grid + '_'+name+'_'+name2+'_fft_at_element_'+("%d"%elements[i])+'.png',dpi=300)



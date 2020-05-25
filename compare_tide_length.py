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
import scipy.signal as spsig


# Define names and types of data
name_change='kit4_kelp_20m_0.018'
name_orig='kit4_45days_3'
grid='kit4'
regionname='kit4_kelp_tight2_small'

starttime=384


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name_orig+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name_change+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')
data['time']=data['time']-678576

savepath='figures/png/' + grid + '_'  + '/tide_length/' + name_orig + '_' + name_change + '/' +regionname +'/'
if not os.path.exists(savepath): os.makedirs(savepath)

region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)

peakarray=np.empty((len(nidx),3))
peakarray2=np.empty((len(nidx),3))
peakarray_neg=np.empty((len(nidx),3))
peakarray2_neg=np.empty((len(nidx),3))


for i in range(0,len(nidx)):
    j=nidx[i]
    print ("%d"%i)+"              "+("%f"%((i)/(len(nidx))*100)) 

    peakinddiff=np.diff(spsig.argrelmax(data['zeta'][starttime:,j],order=5)[0])
    peakarray[i,0]=np.mean(peakinddiff)
    peakarray[i,1]=np.min(peakinddiff)
    peakarray[i,2]=np.max(peakinddiff)
    peakinddiff=np.diff(spsig.argrelmax(data2['zeta'][starttime:,j],order=5)[0])
    peakarray2[i,0]=np.mean(peakinddiff)
    peakarray2[i,1]=np.min(peakinddiff)
    peakarray2[i,2]=np.max(peakinddiff)

    peakinddiff=np.diff(spsig.argrelmax(-data['zeta'][starttime:,j],order=5)[0])
    peakarray_neg[i,0]=np.mean(peakinddiff)
    peakarray_neg[i,1]=np.min(peakinddiff)
    peakarray_neg[i,2]=np.max(peakinddiff)
    peakinddiff=np.diff(spsig.argrelmax(-data2['zeta'][starttime:,j],order=5)[0])
    peakarray2_neg[i,0]=np.mean(peakinddiff)
    peakarray2_neg[i,1]=np.min(peakinddiff)
    peakarray2_neg[i,2]=np.max(peakinddiff)


fldidx=nidx[np.where((peakarray-peakarray2)>0)[0]]
ebbidx=nidx[np.where((peakarray_neg-peakarray2_neg)>0)[0]]


plotidx=fldidx[np.in1d(fldidx,ebbidx)]

print 'Both'
for i in range(0,len(plotidx)):
    j=plotidx[i]
    print ("%d"%i)+"              "+("%f"%((i)/(len(plotidx))*100)) 
    
    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])

    ax.plot(data['time'][starttime:],data['zeta'][starttime:,j]-data2['zeta'][starttime:,j],'k',lw=1,label='No kelp - Kelp')
    peakind=spsig.argrelmax(data['zeta'][:,j],order=5)[0]
    ax.plot(data['time'][peakind],data['zeta'][peakind,j]-data2['zeta'][peakind,j],'r*')

    #ax.plot(data['time'][starttime:],data2['zeta'][starttime:,j],'r',lw=1,label='Kelp')
    ax.grid()
    ax.set_xlim([data['time'][starttime:].min(),data['time'][starttime:].max()])
    ax.set_xlabel(r'Time (day)')
    ax.set_ylabel(r'Elevation Difference (m)')
    ax.legend()    
    f.savefig(savepath + grid + '_'+name_orig+'_'+name_change+'_zetadiff_both_at_node_'+("%d"%j)+'.png',dpi=300)
    plt.close(f)


print 'Ebb'
for i in range(0,len(ebbidx)):
    j=ebbidx[i]
    print ("%d"%i)+"              "+("%f"%((i)/(len(ebbidx))*100)) 
    
    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])

    ax.plot(data['time'][starttime:],data['zeta'][starttime:,j]-data2['zeta'][starttime:,j],'k',lw=1,label='No kelp - Kelp')
    peakind=spsig.argrelmax(data['zeta'][:,j],order=5)[0]
    ax.plot(data['time'][peakind],data['zeta'][peakind,j]-data2['zeta'][peakind,j],'r*')

    #ax.plot(data['time'][starttime:],data2['zeta'][starttime:,j],'r',lw=1,label='Kelp')
    ax.grid()
    ax.set_xlim([data['time'][starttime:].min(),data['time'][starttime:].max()])
    ax.set_xlabel(r'Time (day)')
    ax.set_ylabel(r'Elevation Difference (m)')
    ax.legend()    
    f.savefig(savepath + grid + '_'+name_orig+'_'+name_change+'_zetadiff_ebb_at_node_'+("%d"%j)+'.png',dpi=300)
    plt.close(f)


print 'Fld'
for i in range(0,len(fldidx)):
    j=fldidx[i]
    print ("%d"%i)+"              "+("%f"%((i)/(len(fldidx))*100)) 
    
    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])

    ax.plot(data['time'][starttime:],data['zeta'][starttime:,j]-data2['zeta'][starttime:,j],'k',lw=1,label='No kelp - Kelp')
    peakind=spsig.argrelmax(data['zeta'][:,j],order=5)[0]
    ax.plot(data['time'][peakind],data['zeta'][peakind,j]-data2['zeta'][peakind,j],'r*')

    #ax.plot(data['time'][starttime:],data2['zeta'][starttime:,j],'r',lw=1,label='Kelp')
    ax.grid()
    ax.set_xlim([data['time'][starttime:].min(),data['time'][starttime:].max()])
    ax.set_xlabel(r'Time (day)')
    ax.set_ylabel(r'Elevation Difference (m)')
    ax.legend()    
    f.savefig(savepath + grid + '_'+name_orig+'_'+name_change+'_zetadiff_fld_at_node_'+("%d"%j)+'.png',dpi=300)
    plt.close(f)






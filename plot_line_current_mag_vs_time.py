from __future__ import division
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
import time as timem
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
from scipy import interpolate as intp
from mpl_toolkits.axes_grid1 import make_axes_locatable
import scipy.io as sio

# Define names and types of data
name_orig='kit4_45days_3'
name_change='kit4_kelp_20m_0.018'
name_change2='kit4_kelp_20m_0.011'
name_change3='kit4_kelp_20m_0.011'
grid='kit4'
datatype='2d'
regionname='kit4_kelp_tight5'
starttime=400
endtime=520



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name_orig+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name_change+'/output/',singlename=grid + '_0001.nc')
data3 = loadnc('runs/'+grid+'/'+name_change2+'/output/',singlename=grid + '_0001.nc')
data4 = loadnc('runs/'+grid+'/'+name_change3+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'



savepath='figures/png/' + grid + '_' + datatype + '/line_current_mag_vs_time/'
if not os.path.exists(savepath): os.makedirs(savepath)


region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)

kelp=False
spacing=1
#line=[-129.48666,52.62,52.68]
#define line as line=[bottomx,topx,bottomy,topy]

#kit4_kelp_tight2
#line=[-129.48833,-129.48833,52.62,52.68]
#kit4_kelp_tight5 a
line=[-129.44,-129.40,52.56,52.60]
line=[-129.35,-129.3,52.52,52.54]
ngridy = 2000
eles=[77566,80168]


H1=(sw.dist([line[2], line[3]],[line[0], line[1]],'km'))[0]*1000;
if kelp==True:
    linea=(sw.dist([data['uvnodell'][eles[0],1], line[2]],[line[0], line[0]],'km'))[0]*1000;
    lineb=(sw.dist([data['uvnodell'][eles[1],1], line[2]],[line[0], line[0]],'km'))[0]*1000;



start = timem.clock()
uvar_o=data['ua'][starttime:,:].var(axis=0)
vvar_o=data['va'][starttime:,:].var(axis=0)
uvar_c=data2['ua'][starttime:,:].var(axis=0)
vvar_c=data2['va'][starttime:,:].var(axis=0)
uvar_c2=data3['ua'][starttime:,:].var(axis=0)
vvar_c2=data3['va'][starttime:,:].var(axis=0)
uvar_c3=data4['ua'][starttime:,:].var(axis=0)
vvar_c3=data4['va'][starttime:,:].var(axis=0)


cvarm_o=np.sqrt(uvar_o+vvar_o)
cvarm_c=np.sqrt(uvar_c+vvar_c)
cvarm_c2=np.sqrt(uvar_c2+vvar_c2)
cvarm_c3=np.sqrt(uvar_c3+vvar_c3)

#cvarm_diff=cvarm_c-cvarm_o
#cvarm_diff2=cvarm_c2-cvarm_o
#cvarm_diff_rel=np.divide(cvarm_diff,cvarm_o)*100
#cvarm_diff2_rel=np.divide(cvarm_diff2,cvarm_o)*100

print ('calc current mag: %f' % (timem.clock() - start))

start = timem.clock()

yi = np.linspace(line[2],line[3], ngridy)
yim = np.linspace(0,H1, ngridy)
xi = np.linspace(line[0],line[1], ngridy)
points=np.flipud(np.eye(2000,dtype=bool))

interpdata1=np.empty((ngridy,))
interpdata2=np.empty((ngridy,))
interpdata3=np.empty((ngridy,))
interpdata4=np.empty((ngridy,))

interpdata1=mpl.mlab.griddata(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1], cvarm_o[eidx], xi, yi)[points]
interpdata2=mpl.mlab.griddata(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1], cvarm_c[eidx], xi, yi)[points]
interpdata3=mpl.mlab.griddata(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1], cvarm_c2[eidx], xi, yi)[points]
interpdata4=mpl.mlab.griddata(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1], cvarm_c3[eidx], xi, yi)[points]
print ('griddata interp: %f' % (timem.clock() - start))









f = plt.figure()

ax=f.add_axes([.125,.1,.775,.8])

ax.plot(yim,interpdata1,'k',label='No drag')
ax.plot(yim,interpdata2,'r',label='Drag: 0.018')
ax.plot(yim,interpdata3,'b',label='Drag: 0.011')
ax.plot(yim,interpdata4,'g',label='Drag: 0.007')
if kelp==True:
    ax.axvline(lineb,color='k',linestyle='dashed')
    ax.axvline(linea,color='k',linestyle='dashed')

ax.set_ylabel(r'Current variance magnitude (m s$^{-1}$)',fontsize=10)
ax.set_xlabel(r'Distance (m)',fontsize=10)
ax.legend()



f.savefig(savepath + grid + '_4runs_line_current_mag_vs_time_'+("%f"%line[0])+'_'+("%f"%line[1])+'_'+("%f"%line[2])+'_'+("%f"%line[3])+'.png',dpi=300)
plt.close(f)


f = plt.figure()

ax=f.add_axes([.125,.1,.775,.8])

ax.triplot(data['trigrid'],lw=.5)
ax.plot(xi,yi,'b.')
prettyplot_ll(ax,setregion=region,grid=True)
plotcoast(ax,filename='pacific.nc',color='r')



f.savefig(savepath + grid + '_4runs_line_current_mag_vs_time_'+("%f"%line[0])+'_'+("%f"%line[1])+'_'+("%f"%line[2])+'_'+("%f"%line[3])+'_location.png',dpi=300)
plt.close(f)

tempdic={}
tempdic['interp_orig']=interpdata1
tempdic['interp_018']=interpdata2
tempdic['interp_011']=interpdata3
tempdic['interp_007']=interpdata4
tempdic['line']=line
tempdic['yi']=yi
tempdic['yi_meters']=yim
if kelp==True:
    tempdic['kelpedge_south']=lineb
    tempdic['kelpedge_north']=linea

base_dir = os.path.dirname(__file__)
sio.savemat(os.path.join(base_dir,'data', '4runs_current_mag_interp_'+("%f"%line[0])+'_'+("%f"%line[1])+'_'+("%f"%line[2])+'_'+("%f"%line[3])+'.mat'),mdict=tempdic)


















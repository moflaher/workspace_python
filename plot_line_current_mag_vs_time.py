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
name_change3='kit4_kelp_20m_0.007'
grid='kit4'
datatype='2d'
regionname='kit4_kelp_tight2'
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

cages=np.genfromtxt('runs/'+grid+'/' +name_change+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)




savepath='figures/png/' + grid + '_' + datatype + '/line_current_mag_vs_time/'
if not os.path.exists(savepath): os.makedirs(savepath)


region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)


spacing=1
#line=[-129.48666,52.62,52.68]
#define line as line=[bottomx,topx,bottomy,topy]

#kit4_kelp_tight2 verical
line=[-129.48833,-129.48833,52.62,52.68]
#kit4_kelp_tight2 horiz1
#line=[-129.53,-129.46,52.65,52.65]
#kit4_kelp_tight2 horiz2
#line=[-129.53,-129.46,52.655,52.655]

#kit4_kelp_tight5 north
#line=[-129.44,-129.40,52.56,52.60]
#kit4_kelp_tight5 south
#line=[-129.35,-129.3,52.52,52.54]
#kit4_kelp_tight5 left horiz top
#line=[-129.45,-129.375,52.575,52.575]
#kit4_kelp_tight5 left horiz bottom
#line=[-129.45,-129.375,52.54,52.54]
#kit4_kelp_tight5 right horiz bottom
#line=[-129.375,-129.3,52.5325,52.5325]
print line
ngridy = 2000



tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages[np.in1d(cages,eidx)] ]
tmparray=np.array(tmparray)

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(a1, b1, a2, b2):
    """Returns True if line segments a1b1 and a2b2 intersect."""
    return ccw(a1, b1, a2) != ccw(a1, b1, b2) and ccw(a2, b2, a1) != ccw(a2, b2, b1)


lineints=np.zeros((tmparray.shape[0],3))

for i in range(0,tmparray.shape[0]):
    lineints[i,0]=intersect((line[0],line[2]),(line[1],line[3]),(tmparray[i,-1,0],tmparray[i,-1,1]),(tmparray[i,0,0],tmparray[i,0,1]))
    lineints[i,1]=intersect((line[0],line[2]),(line[1],line[3]),(tmparray[i,0,0],tmparray[i,0,1]),(tmparray[i,1,0],tmparray[i,1,1]))
    lineints[i,2]=intersect((line[0],line[2]),(line[1],line[3]),(tmparray[i,1,0],tmparray[i,1,1]),(tmparray[i,2,0],tmparray[i,2,1]))

idx=np.where(lineints==1)
idxr=idx[0]
idxc=idx[1]

highest=0
lowest=1000000
for i in range(0,len(idxr)):
    j=idxr[i]
    k=idxc[i]
    dist=np.sqrt((line[0]-(tmparray[j,-1+k,0]+tmparray[j,k,0])/2)**2+(line[2]-(tmparray[j,-1+k,1]+tmparray[j,k,1])/2)**2)
    highest=np.max([highest,dist])
    lowest=np.min([lowest,dist])

H1=(sw.dist([line[2], line[3]],[line[0], line[1]],'km'))[0]*1000;
H2=np.sqrt((line[0]-line[1])**2+(line[2]-line[3])**2)

linea=(lowest/H2)*H1
lineb=(highest/H2)*H1




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

tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2]],0],data['nodell'][data['nv'][i,[0,1,2]],1])) for i in cages ]
lseg0=PC(tmparray,facecolor = 'g',edgecolor='None')
ax.add_collection(lseg0)

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
tempdic['kelpedge_south']=lineb
tempdic['kelpedge_north']=linea

base_dir = os.path.dirname(__file__)
sio.savemat(os.path.join(base_dir,'data', grid + '_4runs_line_current_mag_vs_time_'+("%f"%line[0])+'_'+("%f"%line[1])+'_'+("%f"%line[2])+'_'+("%f"%line[3])+'.mat'),mdict=tempdic)


















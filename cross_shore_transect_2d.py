from __future__ import division
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import seawater as sw

# Define names and types of data
name='kit4_kelp_20m_drag_0.007'
grid='kit4_kelp'
datatype='2d'


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data,trifinder=True)
print 'done sort'


cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
if cages!=None:
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.2
    ls='solid'

vectorstart=np.array([-129.496,52.644])
vectorend=np.array([-129.5,52.649])
vectorx=np.array([vectorstart[0],vectorend[0]])
vectory=np.array([vectorstart[1],vectorend[1]])
snv=(vectorend-vectorstart)/np.linalg.norm(vectorend-vectorstart)
spv=np.array([-snv[1],snv[0]])

npt=50
xi=np.linspace(vectorstart[0],vectorend[0],npt)
yi=np.linspace(vectorstart[1],vectorend[1],npt)
us=data['u'].shape


savepath='data/cross_shore_transect/'
if not os.path.exists(savepath): os.makedirs(savepath)

plotpath='figures/png/'+grid+'_'+datatype+'/cross_shore_transect/'
if not os.path.exists(plotpath): os.makedirs(plotpath)



host=data['trigrid_finder'].__call__(vectorx,vectory)

def regionarea(region):
    return (region['region'][1]-region['region'][0])*(region['region'][3]-region['region'][2])

minarea=1000000000
for regionname in regions():
    region=regions(regionname)
    eidx=get_elements(data,region)
    if ((np.sum(np.in1d(host,eidx))==2) and (regionarea(region)<minarea)):
        minarea=regionarea(region)
        bestregion=regionname


region=regions(bestregion)
nidx=get_nodes(data,region)
f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigrid'],data['h'],vmin=data['h'][nidx].min(),vmax=data['h'][nidx].max())
ax.plot(xi,yi,'k',lw=3)  
if cages!=None:   
    lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    coast=ax.add_collection(lseg_t)
    coast.set_zorder(30)
prettyplot_ll(ax,setregion=region,cb=triax,cblabel=r'Depth (m)') 
f.savefig(plotpath + name+'_'+('%f'%vectorx[0])+'_'+('%f'%vectorx[1])+'_'+('%f'%vectory[0])+'_'+('%f'%vectory[1])+'_'+('%d'%len(xi))+'_line_location.png',dpi=600)
plt.close(f)




fillarray_u=np.empty((us[0],len(xi)))
fillarray_v=np.empty((us[0],len(xi)))
fillalong=np.empty((us[0],len(xi)))
fillcross=np.empty((us[0],len(xi)))
dist=np.empty((len(xi),))
h=np.empty((len(xi),))





print 'interp uvw on path'

for i in range(0,len(xi)):
    print i
    fillarray_u[:,i],fillarray_v[:,i]=interp_vel(data,[xi[i],yi[i]])
    h[i]=ipt.interpN_at_loc(data,'h',[xi[i],yi[i]])


print 'Calc along path current'

for i in range(0,len(xi)):
    print i
    inner=np.inner(np.vstack([fillarray_u[:,i],fillarray_v[:,i]]).T,snv)
    along=np.vstack([inner*snv[0],inner*snv[1]]).T
    tmpa=np.multiply(np.sign(np.arctan2(along[:,1],along[:,0])),np.linalg.norm(along,axis=1))
    fillalong[:,i]=tmpa
    cross=np.vstack([fillarray_u[:,i],fillarray_v[:,i]]).T-along
    tmpc=np.multiply(np.sign(np.arctan2(cross[:,1],cross[:,0])),np.linalg.norm(cross,axis=1))
    fillcross[:,i]=tmpc

    dist[i]=(sw.dist([vectorstart[1], yi[i]],[vectorstart[0], xi[i]],'km'))[0]*1000;
    

if cages!=None:
    incage=np.zeros((len(xi),))
    host=data['trigrid'].get_trifinder().__call__(xi,yi)
    incage[np.in1d(host,cages)]=1




savedic={}

savedic['u']=fillarray_u
savedic['v']=fillarray_v
savedic['along']=fillalong
savedic['cross']=fillcross
savedic['distance']=dist
savedic['h']=h
savedic['lon']=xi
savedic['lat']=yi
if cages!=None:
    savedic['incage']=incage

np.save(savepath+grid+'_'+name+'_'+('%f'%vectorx[0])+'_'+('%f'%vectorx[1])+'_'+('%f'%vectory[0])+'_'+('%f'%vectory[1])+'_'+('%d'%len(xi))+'_2d.npy',savedic)




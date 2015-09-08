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


# Define names and types of data
name='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'
datatype='2d'
starttime=384


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data,trifinder=True)
print('done sort')

cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
if cages!=None:
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.2
    ls='solid'


#kit4_kelp_tight2_kelpfield 1
vectorstart=np.array([-129.496,52.644])
vectorend=np.array([-129.5,52.649])
#kit4_kelp_tight2_kelpfield 2
vectorstart=np.array([-129.5,52.645])
vectorend=np.array([-129.495,52.6475])
#kit4_kelp_tight5 1
vectorstart=np.array([-129.37,52.545])
vectorend=np.array([-129.355,52.545])
#kit4_kelp_tight5 2
vectorstart=np.array([-129.385,52.5325])
vectorend=np.array([-129.37,52.5325])


vectorx=np.array([vectorstart[0],vectorend[0]])
vectory=np.array([vectorstart[1],vectorend[1]])
snv=(vectorend-vectorstart)/np.linalg.norm(vectorend-vectorstart)
spv=np.array([-snv[1],snv[0]])


xi=np.linspace(vectorstart[0],vectorend[0],50)
yi=np.linspace(vectorstart[1],vectorend[1],50)
us=data['u'].shape
numlay=us[1]

def regionarea(region):
    return (region['region'][1]-region['region'][0])*(region['region'][3]-region['region'][2])

host=data['trigrid_finder'].__call__(vectorx,vectory)

minarea=1000000000
for regionname in regions():
    region=regions(regionname)
    eidx=get_elements(data,region)
    if ((np.sum(np.in1d(host,eidx))==2) and (regionarea(region)<minarea)):
        minarea=regionarea(region)
        bestregion=regionname

region=regions(bestregion)
nidx=get_nodes(data,region)



savepath='figures/png/'+grid+'_'+datatype+'/uv_std_ratio/'
if not os.path.exists(savepath): os.makedirs(savepath)

obs_jackson=np.load('data/misc/kelp_edge_reduction_jackson.npy')
obs_jackson=obs_jackson[()]

datapath='data/cross_shore_transect/'
namelist=['kit4_kelp_nodrag','kit4_kelp_20m_drag_0.007','kit4_kelp_20m_drag_0.011','kit4_kelp_20m_drag_0.018']
dataload={}
for name in namelist:
    dataload[name]=np.load(datapath+grid+'_'+name+'_'+('%f'%vectorx[0])+'_'+('%f'%vectorx[1])+'_'+('%f'%vectory[0])+'_'+('%f'%vectory[1])+'_'+('%d'%len(xi))+'_2d.npy')
    dataload[name]=dataload[name][()]
    dataload[name]['along_var']=dataload[name]['along'][starttime:].std(axis=0)
    dataload[name]['cross_var']=dataload[name]['cross'][starttime:].std(axis=0)


f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigrid'],data['h'],vmin=data['h'][nidx].min(),vmax=data['h'][nidx].max())
ax.plot(dataload[name]['lon'],dataload[name]['lat'],'k',lw=3)  
if cages!=None:   
    lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    coast=ax.add_collection(lseg_t)
    coast.set_zorder(30)
    ax.plot(dataload[name]['lon'][np.flatnonzero(dataload[name]['incage'])],dataload[name]['lat'][np.flatnonzero(dataload[name]['incage'])],'.w',zorder=40,markersize=.5)  
prettyplot_ll(ax,setregion=region,cb=triax,cblabel=r'Depth (m)') 
f.savefig(savepath + ('%f'%vectorx[0])+'_'+('%f'%vectorx[1])+'_'+('%f'%vectory[0])+'_'+('%f'%vectory[1])+'_'+('%d'%len(xi))+'_line_location.png',dpi=300)
plt.close(f)


#findkelp edge
dgrad=np.gradient(np.gradient(np.divide(dataload['kit4_kelp_20m_drag_0.018']['along_var'],dataload['kit4_kelp_nodrag']['along_var'])))
shiftvalue=dataload['kit4_kelp_20m_drag_0.018']['distance'][np.argmin(dgrad)]



f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
for name in namelist:
    ax.plot(dataload[name]['distance']-shiftvalue,np.divide(dataload[name]['along_var'],dataload[name]['along_var'][np.argmin(dgrad)]),label=name)

plt.legend()

#plot obs_jackson
plt.plot(obs_jackson['jx80'],obs_jackson['ju80']/obs_jackson['ju80'][0],'k.',markersize=5)
plt.plot(obs_jackson['jx81'],obs_jackson['ju81']/obs_jackson['ju81'][0],'k.',markersize=5)
plt.plot(obs_jackson['jx82'],obs_jackson['ju82']/obs_jackson['ju82'][0],'k.',markersize=5)

f.savefig(savepath + name+'_'+('%f'%vectorx[0])+'_'+('%f'%vectorx[1])+'_'+('%f'%vectory[0])+'_'+('%f'%vectory[1])+'_'+('%d'%len(xi))+'_along_std_ratio.png',dpi=150)
plt.close(f)


f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
for name in namelist:
    ax.plot(dataload[name]['distance']-shiftvalue,np.divide(dataload[name]['cross_var'],dataload[name]['cross_var'][np.argmin(dgrad)]),label=name)

plt.legend()

#plot obs_jackson
plt.plot(obs_jackson['jx80'],obs_jackson['jv80']/obs_jackson['jv80'][0],'k.',markersize=5)
plt.plot(obs_jackson['jx81'],obs_jackson['jv81']/obs_jackson['jv81'][0],'k.',markersize=5)
plt.plot(obs_jackson['jx82'],obs_jackson['jv82']/obs_jackson['jv82'][0],'k.',markersize=5)

f.savefig(savepath + name+'_'+('%f'%vectorx[0])+'_'+('%f'%vectorx[1])+'_'+('%f'%vectory[0])+'_'+('%f'%vectory[1])+'_'+('%d'%len(xi))+'_cross_std_ratio.png',dpi=150)
plt.close(f)









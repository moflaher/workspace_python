from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from misctools import *
from plottools import *
from projtools import *
from interptools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from scipy.interpolate import interp1d
from matplotlib import patches as pp

# Define names and types of data
name='2012-02-01_2012-03-01_0.01_0.001'
grid='vh_high'
datatype='2d'
region={}
region['region']=np.array([-123.19,-123.09,49.27,49.34])
stime=100

savepath='figures/timeseries/' + grid + '_' + datatype + '/shippath/'
if not os.path.exists(savepath): os.makedirs(savepath)

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

#find spacing
dist=mdist([region['region'][0],region['region'][2]],[region['region'][1],region['region'][2]])
spacing=dist/20.0
vidx=equal_vectors(data,region,spacing)

srange=np.array([.1,.5,1,2,3,5,7,10,13,99])*0.514
crange=np.array(['#7652e2','#4898d3','#61cbe5','#6dbc45','#b4dc00','#cdc100','#f8a718','#f7a29d','#ff1e1e'])

seg=load_segfile('data/misc/shippath_fake_vh_2.seg')
locs=np.array([])
for key in seg.keys():
    locs=np.append(locs,np.array([seg[key][:,0],seg[key][:,1]]).T)
locs=locs.reshape(-1,2)

proj=gridproj(grid)
x,y=proj(locs[:,0],locs[:,1])
dx=np.diff(x)
dy=np.diff(y)
d=np.sqrt(dx**2+dy**2)

np.random.seed(10)
sspeed=np.round(np.random.rand(len(locs)-1)*2)
sspeed[sspeed==0]=0.1  
times=np.append(data['time'][stime],np.cumsum(np.divide(d,sspeed)/(24*60*60))+data['time'][stime])
idx=np.argwhere(((data['time']<=times.max()) & (data['time']>=times.min()))).ravel()
if idx.min()!=0:
    idx=np.append(idx[0]-1,idx)
idx=np.append(idx,idx[-1]+1)

mtimes=data['time'][idx]
sua=np.empty((len(locs),))
sva=np.empty((len(locs),))
for i,time in enumerate(times):
    
    lidx=np.argwhere(mtimes<=time).max()
    lua=interpEfield_locs(data,'ua',locs[i,:],lidx,ll=True)    
    lva=interpEfield_locs(data,'va',locs[i,:],lidx,ll=True)  
     
    uidx=np.argwhere(mtimes>time).min()
    uua=interpEfield_locs(data,'ua',locs[i,:],uidx,ll=True)    
    uva=interpEfield_locs(data,'va',locs[i,:],uidx,ll=True)   
    
    u1 = interp1d(mtimes[[lidx,uidx]], np.array([lua,uua]).flatten())
    sua[i] = u1(time)
    v1 = interp1d(mtimes[[lidx,uidx]], np.array([lva,uva]).flatten())
    sva[i] = v1(time)


u_vec=np.empty((len(vidx),))
v_vec=np.empty((len(vidx),))

def plot_ship(i):
    f=plt.figure()
    ax=f.add_axes([.125,.1,.75,.8])
    prettyplot_ll(ax,setregion=region)
    plotcoast(ax,filename='pacific_harbour.nc',color='None',fcolor='darkgreen',fill=True)
    
    ax.plot(locs[:,0],locs[:,1],'r',lw=2)
    qax=ax.quiver(locs[:,0],locs[:,1],sua,sva,angles='xy',scale_units='xy',scale=100,width=0.003)
    qax.set_zorder(20)
    qaxk=ax.quiverkey(qax,.8,.85,0.5, r'0.5 ms')

    ax.plot(locs[i,0],locs[i,1],'m*',markersize=15)
    
    time=times[i]
    lidx=np.argwhere(mtimes<=time).max()
    uidx=np.argwhere(mtimes>time).min()
    for j,idx in enumerate(vidx):
        lua=interpEfield_locs(data,'ua',data['uvnodell'][idx,:],lidx,ll=True)    
        lva=interpEfield_locs(data,'va',data['uvnodell'][idx,:],lidx,ll=True)           

        uua=interpEfield_locs(data,'ua',data['uvnodell'][idx,:],uidx,ll=True)    
        uva=interpEfield_locs(data,'va',data['uvnodell'][idx,:],uidx,ll=True)  
        
        u1 = interp1d(mtimes[[lidx,uidx]], np.array([lua,uua]).flatten())
        u_vec[j] = u1(time)
        v1 = interp1d(mtimes[[lidx,uidx]], np.array([lva,uva]).flatten())
        v_vec[j] = v1(time)
        
    s_vec=speeder(u_vec,v_vec)
    scale=((region['region'][1]-region['region'][0])*.0475)/s_vec.max()

    for idx,u,v in zip(vidx,u_vec,v_vec):
        x,y=data['uvnodell'][idx,:]
        dx=scale*u
        dy=scale*v
        al=np.sqrt(u**2+v**2)
        sl=np.sqrt(dx**2+dy**2)
        cidx=np.argwhere(al>=srange)
        if len(cidx) > 0:
            cidx=np.max(cidx)
            fcolor=crange[cidx]
        
        if al>=srange[0]:
            a=pp.FancyArrow(x,y,dx,dy,width_base=sl*.1,width_top=sl*.2,
                            head_length=sl*.35,head_width=sl*.4,
                            length_includes_head=True, edgecolor='None',
                            facecolor=fcolor)
            ax.add_artist(a)
            
    f.savefig(savepath + grid + '_shippath_'+"{}".format(i+stime)+'.png',dpi=300)
    plt.close(f)


for p in range(37):
    print(p)
    plot_ship(p)


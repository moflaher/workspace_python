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
name='kit4_45days_3'
grid='kit4'

starttime=384
endtime=432
regionname='kit4_area5'


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data,trifinder=True)
print('done sort')


region=regions(regionname)
nidx=get_nodes(data,region)


#kit4 line1
#vectorstart=np.array([-128.865,53.565])
#vectorend=np.array([-128.84,53.61])
#kit4 line2
vectorstart=np.array([-128.84,53.61])
vectorend=np.array([-128.79,53.565])
vectorx=np.array([vectorstart[0],vectorend[0]])
vectory=np.array([vectorstart[1],vectorend[1]])
snv=(vectorend-vectorstart)/np.linalg.norm(vectorend-vectorstart)
spv=np.array([-snv[1],snv[0]])


#idxs=closest_element(data,vectorstart)
#idxe=closest_element(data,vectorend)

#vectorstart=data['uvnodell'][idxs,:]
#vectorend=data['uvnodell'][idxe,:]
#vectorx=np.array([vectorstart[0],vectorend[0]])
#vectory=np.array([vectorstart[1],vectorend[1]])
#snv2=(vectorend-vectorstart)/np.linalg.norm(vectorend-vectorstart)



#angle between vectors but dont need, save for another day
#np.arccos(np.dot(snv,spv)

#a1=np.dot(A,B)*B
#a2=A-a1


xi=np.linspace(vectorstart[0],vectorend[0],50)
yi=np.linspace(vectorstart[1],vectorend[1],50)
us=data['u'].shape
numlay=us[1]


savepath='figures/timeseries/'+grid+'_'+'/cross_shore_transect/'+name+'_'+('%f'%vectorx[0])+'_'+('%f'%vectorx[1])+'_'+('%f'%vectory[0])+'_'+('%f'%vectory[1])+'_'+('%d'%numlay)+'_'+('%d'%len(xi))+'/'
if not os.path.exists(savepath): os.makedirs(savepath)



datapath='data/cross_shore_transect/'
dataload=np.load(datapath+grid+'_'+name+'_'+('%f'%vectorx[0])+'_'+('%f'%vectorx[1])+'_'+('%f'%vectory[0])+'_'+('%f'%vectory[1])+'_'+('%d'%numlay)+'_'+('%d'%len(xi))+'.npy')
dataload=dataload[()]


f=plt.figure()

ax=f.add_axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigrid'],data['h'],vmin=data['h'][nidx].min(),vmax=data['h'][nidx].max())
ax.plot(xi,yi,'k',lw=3)   
prettyplot_ll(ax,setregion=region,cb=triax,cblabel=r'Depth (m)') 
f.savefig(savepath + 'line_location.png',dpi=600)
plt.close(f)


interp_h=mpl.tri.LinearTriInterpolator(data['trigrid'], data['h'])
new_h=interp_h(xi,yi)
dist=(sw.dist([vectorstart[1], vectorend[1]],[vectorstart[0], vectorend[0]],'km'))[0]*1000;
xi=np.linspace(0,dist,50)
xxi,yyi=np.meshgrid(xi,range(0,20))
yyi=new_h.reshape(-1,1)*data['siglay'][:,0].reshape(1,-1)
yyi=yyi.T


for i in range(starttime,endtime-1):
    for j in range(0,12):
            f=plt.figure(figsize=(25,5))
            ax=f.add_axes([.125,.1,.775,.8])
            ax.plot(xi,new_h*-1,'k',lw=3)
            interpfield_a=dataload['along'][i,:,:]*(1-(j/12))+dataload['along'][i+1,:,:]*(j/12)
            interpfield_w=dataload['w'][i,:,:]*(1-(j/12))+dataload['w'][i,:,:]*(j/12)
            
            Q=ax.quiver(xxi,yyi,interpfield_a,interpfield_w,angles='xy',scale_units='xy',scale=.0015,color='b',width=0.001)
            ax.quiverkey(Q,.48,.3,.2, r'0.2 m s$^{-1}$', labelpos='S',fontproperties={'size': 12})
            ax.grid()
            ax.set_ylabel(r'Depth (m)')
            ax.set_xlabel(r'Distance (m)')
            ax.axis([-250,5500,-200, 25])
            
            f.savefig(savepath + 'quiver_'+("%05f"%(i+(j/12)))+'.png',dpi=150)
            plt.close(f)










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
from matplotlib.patches import Ellipse
sys.path.append('/home/moe46/Desktop/school/workspace_python/ttide_py/ttide/')
from t_tide import t_tide


# Define names and types of data
name='kit4_45days_3'
name2='kit4_kelp_20m_0.018'
grid='kit4'
regionname='kit4_ftb'

starttime=384
spacing=750
divider=50


### load the .nc file #####
#data = loadnc('/media/moflaher/MB_3TB/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
#data2 = loadnc('/media/moflaher/My Book/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')

data = loadnc('/media/moe46/My Passport/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('/media/moe46/My Passport/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

region=regions(regionname)

savepath='figures/png/' + grid + '_'  + '/ellipses_compare/' + name + '_'+ name2 + '/'
if not os.path.exists(savepath): os.makedirs(savepath)




idx=equal_vectors(data,region,spacing)


tidecon_uv=np.empty([len(idx),5,8])
tidecon_uv2=np.empty([len(idx),5,8])
print len(idx)
for i in range(0,len(idx)):
    j=idx[i]
    [nameu, freq, tidecon_uv[i,], xout]=t_tide(data['ua'][starttime:,j]+1j*data['va'][starttime:,j],stime=data['time'][starttime],lat=data['uvnodell'][j,1],output=False,constitnames=np.array([['M2  '],['N2  '],['S2  '],['K1  '],['O1  ']]))
    [nameu, freq, tidecon_uv2[i,], xout]=t_tide(data2['ua'][starttime:,j]+1j*data2['va'][starttime:,j],stime=data['time'][starttime],lat=data['uvnodell'][j,1],output=False,constitnames=np.array([['M2  '],['N2  '],['S2  '],['K1  '],['O1  ']]))

print 'T_tide Finished'

idxl=np.where(tidecon_uv[:,3,2]>=0)[0]
idxr=np.where(tidecon_uv[:,3,2]<0)[0]

ellsleft = [Ellipse(xy=(data['uvnodell'][idx[idxl[i]],0],data['uvnodell'][idx[idxl[i]],1]), width=np.fabs(tidecon_uv[idxl[i],3,2])/divider, height=tidecon_uv[idxl[i],3,0]/divider, angle=tidecon_uv[idxl[i],3,4]+90,fc='None',edgecolor='b',lw=2) for i in range(0,len(idxl))]
ellsright= [Ellipse(xy=(data['uvnodell'][idx[idxr[i]],0],data['uvnodell'][idx[idxr[i]],1]), width=np.fabs(tidecon_uv[idxr[i],3,2])/divider, height=tidecon_uv[idxr[i],3,0]/divider, angle=tidecon_uv[idxr[i],3,4]+90,fc='None',edgecolor='b',linestyle='dashed',lw=2) for i in range(0,len(idxr))]

idxl2=np.where(tidecon_uv2[:,3,2]>=0)[0]
idxr2=np.where(tidecon_uv2[:,3,2]<0)[0]

ellsleft2 = [Ellipse(xy=(data['uvnodell'][idx[idxl2[i]],0],data['uvnodell'][idx[idxl2[i]],1]), width=np.fabs(tidecon_uv2[idxl2[i],3,2])/divider, height=tidecon_uv2[idxl2[i],3,0]/divider, angle=tidecon_uv2[idxl2[i],3,4]+90,fc='None',edgecolor='r') for i in range(0,len(idxl2))]
ellsright2= [Ellipse(xy=(data['uvnodell'][idx[idxr2[i]],0],data['uvnodell'][idx[idxr2[i]],1]), width=np.fabs(tidecon_uv2[idxr2[i],3,2])/divider, height=tidecon_uv2[idxr2[i],3,0]/divider, angle=tidecon_uv2[idxr2[i],3,4]+90,fc='None',edgecolor='r',linestyle='dashed') for i in range(0,len(idxr2))]

f=plt.figure()
ax=f.add_axes([.125,.1,.8,.85])
prettyplot_ll(ax,setregion=region)
plotcoast(ax,filename='pacific.nc',color='k')

for e in ellsleft:
    ax.add_artist(e)
for e in ellsright:
    ax.add_artist(e)  
for e in ellsleft2:
    ax.add_artist(e)
for e in ellsright2:
    ax.add_artist(e)  

f.savefig(savepath + grid + '_'+ regionname +'_spacing_'+("%d"%spacing)+'_noe_'+("%d"%len(idx))+'.png',dpi=600)
plt.close(f)






















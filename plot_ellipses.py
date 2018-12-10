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
from matplotlib.patches import Ellipse
from t_tide import t_tide


# Define names and types of data
name='sfm5m_sjr_basicrun'
grid='sfm5m_sjr'

regionname='stjohn_harbour_tight'
starttime=0
spacing=1500
divider=15


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

region=regions(regionname)

savepath='figures/png/' + grid + '_'  + '/ellipses/' + name + '_' + regionname + '/'
if not os.path.exists(savepath): os.makedirs(savepath)




idx=equal_vectors(data,region,spacing)


tidecon_uv=np.empty([len(idx),5,8])
print len(idx)
for i in range(0,len(idx)):
    j=idx[i]
    [nameu, freq, tidecon_uv[i,], xout]=t_tide(data['ua'][starttime:,j]+1j*data['va'][starttime:,j],stime=data['time'][starttime],lat=data['uvnodell'][j,1],output=False,constitnames=np.array([['M2  '],['N2  '],['S2  '],['K1  '],['O1  ']]))


print('T_tide Finished')

idxl=np.where(tidecon_uv[:,3,2]>=0)[0]
idxr=np.where(tidecon_uv[:,3,2]<0)[0]

ellsleft = [Ellipse(xy=(data['uvnodell'][idx[idxl[i]],0],data['uvnodell'][idx[idxl[i]],1]), width=np.fabs(tidecon_uv[idxl[i],3,2])/divider, height=tidecon_uv[idxl[i],3,0]/divider, angle=tidecon_uv[idxl[i],3,4]+90,fc='None',edgecolor='r') for i in range(0,len(idxl))]
ellsright= [Ellipse(xy=(data['uvnodell'][idx[idxr[i]],0],data['uvnodell'][idx[idxr[i]],1]), width=np.fabs(tidecon_uv[idxr[i],3,2])/divider, height=tidecon_uv[idxr[i],3,0]/divider, angle=tidecon_uv[idxr[i],3,4]+90,fc='None',edgecolor='b') for i in range(0,len(idxr))]


f=plt.figure()
ax=f.add_axes([.125,.1,.85,.85])
prettyplot_ll(ax,setregion=region)
#plotcoast(ax,filename='pacific.nc',color='k')

for e in ellsleft:
    ax.add_artist(e)
for e in ellsright:
    ax.add_artist(e)  


f.savefig(savepath + grid + '_spacing_'+("%d"%spacing)+'_noe_'+("%d"%len(idx))+'.png',dpi=600)
plt.close(f)






















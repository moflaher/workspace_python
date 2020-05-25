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
import scipy.signal as spsig


# Define names and types of data
name='kit4_kelp_20m_drag_0.018_2d_5min'
grid='kit4_kelp'
regionname='kit4_kelp_tight2_kelpfield'

starttime=4608
endtime=12961



### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

region=regions(regionname)
eidx=get_elements(data,region)
nidx=get_nodes(data,region)
region=regionll2xy(data,region)

savepath='figures/png/' + grid + '_'  + '/excursion/'
if not os.path.exists(savepath): os.makedirs(savepath)



uvel=np.empty((len(data['nv']),endtime-starttime))
maxspeed=np.zeros((len(data['nv']),))
maxpeak=np.zeros((len(data['nv']),))

for i in range(0,len(eidx)):
    print ("%d"%i)+"              "+("%f"%(i/len(eidx)*100)) 
    j=eidx[i]
    uvel[j,:]=(data['zeta'][starttime:endtime,data['nv'][j,0]] + data['zeta'][starttime:endtime,data['nv'][j,1]] + data['zeta'][starttime:endtime,data['nv'][j,2]]) / 3.0
    maxspeed[j]=np.sqrt(data['ua'][starttime:endtime,j]**2+data['va'][starttime:endtime,j]**2).max()

    peakinddiff=np.diff(spsig.argrelmax(uvel[j,:],order=5)[0])
    maxpeak[j]=np.max(peakinddiff)




te=np.zeros((len(data['nv']),))
te=np.multiply(maxspeed,maxpeak*300)/np.pi/1000
clims=np.percentile(te[eidx],[1,99])


# Plot te
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigrid'],te,vmin=clims[0],vmax=clims[1])
prettyplot_ll(ax,setregion=region,grid=True,cblabel='Tidal Excursion (km)',cb=triax)
f.savefig(savepath + grid + '_'+ name+'_' + regionname +'_tidal_excursion_ll.png',dpi=600)
plt.close(f)



# Plot te xy
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigridxy'],te,vmin=clims[0],vmax=clims[1])
ax.grid()
ax.axis(region['regionxy'])
ax.set_aspect('equal',anchor='SW')

scaler=1000
ticks = mpl.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scaler))
ax.xaxis.set_major_formatter(ticks)
ax.yaxis.set_major_formatter(ticks)

plt.draw()
box=ax.get_position()
cax=f.add_axes([box.xmax + .025, box.ymin, .025, box.height])
cb=plt.colorbar(triax,cax=cax)
cb.set_label('Tidal Excursion (km)',fontsize=10)

ax.set_xlabel('x (km)')
ax.set_ylabel('y (km)')

#prettyplot_ll(ax,setregion=region,grid=True,cblabel='Tidal Excursion (km)',cb=triax)
f.savefig(savepath + grid + '_'+ name+'_' + regionname +'_tidal_excursion_xy.png',dpi=600)
plt.close(f)


















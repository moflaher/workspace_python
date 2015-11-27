from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from ttide.t_tide import t_tide
from ttide.t_predic import t_predic

from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC


# Define names and types of data
name='2012-02-01_2012-03-01_0.01_0.001'
grid='vh_high'
regionname='secondnarrows'
datatype='2d'
starttime=0



testing=False







region=regions(regionname)

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')


savepath='figures/png/' + grid + '_' + datatype + '/residual_mean_spatial/'
if not os.path.exists(savepath): os.makedirs(savepath)



uv1=np.load('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv_all.npy')
uv1=uv1[()]


nidx=get_nodes(data,region)
eidx=get_elements(data,region)




resu=np.empty((len(eidx),len(data['time'][starttime:])))
resv=np.empty((len(eidx),len(data['time'][starttime:])))

if testing==False:
    for j in range(0,len(eidx)):
        print( ("%d"%j)+" "*14+("%f"%(j/len(eidx)*100)))
        i=eidx[j]    
        tp1=t_predic(data['time'][starttime:],uv1['nameu'],uv1['freq'],uv1['tidecon'][i,:,:])
        resu[j,:]=data['ua'][starttime:,i]-np.real(tp1).flatten()
        resv[j,:]=data['va'][starttime:,i]-np.imag(tp1).flatten()


res_speed=np.sqrt(resu**2+resv**2)
res_speed_mean=res_speed.mean(axis=0)

f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigrid'],res_speed_mean)
prettyplot_ll(ax,setregion=region,cb=triax,cblabel=r'Residual Speed (m s$^{-1}$)')
plotcoast(ax,color='None',fcolor='darkgreen',fill=True)
f.savefig(savepath + grid + '_'+ name +'_'+regionname+'_meanres.png',dpi=600)
plt.close(f)



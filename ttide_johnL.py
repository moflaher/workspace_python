from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import interptools as ipt
from misctools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
sys.path.append('/home/moflaher/Desktop/workspace_python/ttide_py/ttide/')
sys.path.append('/home/moe46/Desktop/school/workspace_python/ttide_py/ttide/')
from t_tide import t_tide

# Define names and types of data
name='voucher_2d_repmonth'
grid='voucher'
datatype='2d'
starttime=49
endtime=5041

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data,trifinder=True)
print('done sort')


savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)


loc=[-58.9161,44.1942]

ua=ipt.interpE_at_loc(data,'ua',loc)
va=ipt.interpE_at_loc(data,'va',loc)


[nameu, freq, tidecon_uv, xout]=t_tide(ua[starttime:endtime]+1j*va[starttime:endtime],stime=data['time'][starttime],lat=loc[1],output=True,constitnames=['M2','S2','N2','K1','O1'],dt=np.diff(data['time'])[0]*24)



dist=np.sqrt(ua**2+va**2)

f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
scb=ax.scatter(ua,va,s=25,c=dist,edgecolors='None')
cb=plt.colorbar(scb)
ax.set_xlabel(r'depth averaged u-velocity (m/s)')
ax.set_ylabel(r'depth averaged v-velocity (m/s)')
cb.set_label(r'depth averaged speed (m/s)')

f.savefig(savepath + grid + '_' +name+ '_john_scatter.png',dpi=600)
plt.close(f)



f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.plot(data['time']*24-data['time'][0]*24,speeder(ua,va))
ax.set_xlabel(r'time (h) ')
ax.set_ylabel(r'speed (m/s)')
f.savefig(savepath + grid + '_' +name+ '_john_speed.png',dpi=600)
plt.close(f)



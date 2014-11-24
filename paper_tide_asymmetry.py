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
sys.path.append('/home/moe46/Desktop/school/workspace_python/ttide_py/ttide/')
sys.path.append('/home/moflaher/Desktop/workspace_python/ttide_py/ttide/')
from t_tide import t_tide
from t_predic import t_predic

# Define names and types of data
name='kit4_45days_3'
grid='kit4'
regionname='kit4_kelp_tight2_small'
datatype='2d'
starttime=384
cmin=-1
cmax=1


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'


region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)

savepath='figures/png/' + grid + '_' + datatype + '/paper_asymmetry/'+name+'/'
if not os.path.exists(savepath): os.makedirs(savepath)






ttidein=np.load('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv_all.npy')
ttidein=ttidein[()]

tidecon=ttidein['tidecon']
nameu=ttidein['nameu']
freq=ttidein['freq']

resmean=np.load('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv_all_mean.npy')
resmean=resmean[()]


m2i=np.where(nameu=='M2  ')
m4i=np.where(nameu=='M4  ')

SEMAZ0 = np.sqrt(resmean['resumean']**2+resmean['resvmean']**2);
delta = np.divide(SEMAZ0,tidecon[:,m2i,0].flatten());
theta0 = np.arctan2(resmean['resvmean'],resmean['resumean']);
dtheta0 = theta0-tidecon[:,m2i,4].flatten()/180*np.pi;
epslon  = tidecon[:,m2i,2].flatten()/tidecon[:,m2i,0].flatten();
dtheta4 = (tidecon[:,m4i,4].flatten()-tidecon[:,m2i,4].flatten())/180*np.pi;
pusi = (2*tidecon[:,m2i,6].flatten()-tidecon[:,m4i,6].flatten())/180*np.pi;
ECCM4=np.sqrt(1-(tidecon[:,m4i,2].flatten()/tidecon[:,m4i,0].flatten())**2)
p = delta*np.cos(dtheta0)+epslon*(np.cos(dtheta4)*np.cos(pusi)-ECCM4*np.sin(dtheta4)*np.sin(pusi));

clims=np.percentile(p[eidx],[1,99])


f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigrid'],p,vmin=-.8,vmax=.8)
prettyplot_ll(ax,setregion=region,cblabel=r'Asymmetry',cb=triax,grid=True)
f.savefig(savepath + grid + '_' + regionname +'_paper_asymmetry.png',dpi=300)
plt.close(f)















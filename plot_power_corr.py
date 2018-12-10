from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
from misctools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from scipy.stats.stats import pearsonr 


# Define names and types of data
name='voucher_2d_repmonth'
grid='voucher'

regionname='mp'


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

region=regions(regionname)
eidx=get_elements(data,region)

savepath='figures/png/' + grid + '_'  + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)

speed=speeder(data['ua'],data['va'])**3

elecor=np.empty((data['nele'],))

for i in range(data['nele']):
    print i
    tcor=np.array([pearsonr(speed[:,i],speed[:,x])[0] for x in data['nbe'][i,:]])
    elecor[i]=np.nanmean(tcor[data['nbe'][i,:]!=-1])
    
    
elecor[np.isnan(elecor)]=0    

clim=np.percentile(elecor[eidx],[10,90])

f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
triax=ax.tripcolor(data['trigrid'],elecor,vmin=clim[0],vmax=clim[1])
prettyplot_ll(ax,setregion=region,cb=triax,cblabel='Power Corr')
f.savefig(savepath + grid + '_' +name+ '_'+regionname +'_power_corr.png',dpi=600)

plt.close(f)

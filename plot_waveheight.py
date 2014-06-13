from __future__ import division
import numpy as np
import matplotlib as mpl
import scipy as sp
from datatools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os


### load a timeslice from an .nc file #####
data = loadnc('/media/moflaher/My Book/kitimat3_runs/kitimat_wavetest_default_3sec/output/',singlename='kitimat3_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'



region=regions('gilisland')


savepath='figures/timeseries/kitimat3/waveheight/swh_3sec_default_' + region['passage'] + '/'
if not os.path.exists(savepath): os.makedirs(savepath)

#### Spatial plots
for i in xrange(len(data['time'])):
    print i
    plt.close()
    plt.tripcolor(data['trigrid'],data['hs'][i,:],vmin=0,vmax=2)
    plt.colorbar()
    plt.grid()
    plt.axis(region['region'])
    plt.title('Significant Wave Height at ' + mpl.dates.num2date(data['time'][i]).strftime('%Y-%m-%d %H:%M:%S'))
    plt.savefig(savepath + 'sigwaveheight_' + '%05.f'%i + '.png',dpi=300)
    plt.close()




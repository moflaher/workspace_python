from __future__ import division,print_function
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import scipy.io as sio
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
from StringIO import StringIO
from gridtools import *
from datatools import *
from misctools import *
from plottools import *
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import h5py as h5


# Define names and types of data
name='kit4_45days_3'
#name='kit4_45days_3'
grid='kit4'
datatype='2d'
regionname='kit4_kelp_tight2_small'
lname='element_80185_s3'


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

region=regions(regionname)

savepath='figures/png/' + grid + '_' + datatype + '/lagtracker/movement/'
if not os.path.exists(savepath): os.makedirs(savepath)

if 'savelag' not in globals():
    print "Loading savelag"
    fileload=h5.File('savedir/'+name+'/'+lname+'.mat')
    savelag={}
    for i in fileload['savelag'].keys():
            if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
                continue
            savelag[i]=fileload['savelag'][i].value.T


cols=3
rows=3

nos=rows*cols
subtimes=np.linspace(0,len(savelag['time'])-1,nos)

region={}
tmp=[np.nanmin(savelag['x']),np.nanmax(savelag['x']),np.nanmin(savelag['y']),np.nanmax(savelag['y'])]
regionscale=0
region['regiontmp']=[tmp[0]-(tmp[1]-tmp[0])*regionscale,tmp[1]+(tmp[1]-tmp[0])*regionscale,tmp[2]-(tmp[3]-tmp[2])*regionscale,tmp[3]+(tmp[3]-tmp[2])*regionscale]

f, ax = plt.subplots(nrows=rows,ncols=cols, sharex=True, sharey=True)
ax=ax.flatten()

for i in range(0,len(ax)):
    print i
    ax[i].triplot(data['trigridxy'],lw=.25)
    #plotidx=np.where(np.isnan(savelag['x'][:,subtimes[i].astype(int)]) & ((savelag['x'][:,subtimes[i].astype(int)]-savelag['x'][:,subtimes[i].astype(int)])!=0))
    #plotidxb=np.zeros(shape=(savelag['x'].shape[0],), dtype=bool)
    #plotidxb[plotidx]=1
    #ax[i].plot(savelag['x'][plotidxb,daysi*i*lph],savelag['y'][plotidxb,daysi*i*lph],'g.')
    ax[i].plot(savelag['x'][:,subtimes[i].astype(int)],savelag['y'][:,subtimes[i].astype(int)],'r.',markersize=2)
    #ax[i].plot(savelag['x'][:,daysi*i*lph],savelag['y'][:,daysi*i*lph],'g.')
    
    #plotidx2=np.where(np.fabs(savelag.z[:,daysi*i*lph]-data['uvh'][trigridxy.get_trifinder().__call__(savelag['x'][:,daysi*i*lph],savelag['y'][:,daysi*i*lph])])<=1 )
    #ax[i].plot(savelag['x'][plotidx2,daysi*i*lph],savelag['y'][plotidx2,daysi*i*lph],'y.')

    ax[i].axis(region['regiontmp'])
    ax[i].set_title('Day '+ ("%.0f"% ( ( ((savelag['time'][1]-savelag['time'][0])*subtimes[i].astype(int) )/3600)/24  ) ))
    scaler=1000
    ticks = mpl.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scaler))
    ax[i].xaxis.set_major_formatter(ticks)
    ax[i].yaxis.set_major_formatter(ticks)
    if (i>=((rows-1)*cols)):
        ax[i].set_xlabel(r'x (km)')
    if (np.mod(i,cols)==0):
        ax[i].set_ylabel(r'y (km)')
    #ax[i]=prettyplot_ll(ax[i],setregion=region,grid=True,title='Day '+ ("%d"% (48*daysi*i/48)))

    for label in (ax[i].get_xticklabels() + ax[i].get_yticklabels()):
        #label.set_fontname('Arial')
        label.set_fontsize(8)
    for label in (ax[i].get_xticklabels()):
        label.set_rotation('vertical')

  
f.tight_layout(pad=1)
#f.show()  
days=( ( ( ((savelag['time'][1]-savelag['time'][0])*subtimes[1].astype(int) )/3600)/24  ) )-(( ( ((savelag['time'][1]-savelag['time'][0])*subtimes[0].astype(int) )/3600)/24  ) )
f.savefig(savepath +name+'_'+ lname+'_every_'+("%d"%days)+'days_rows_'+("%d"%rows)+'_cols_'+("%d"%cols)+'.png',dpi=600)













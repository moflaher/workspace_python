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



# Define names and types of data
name='kit4_45days_3'
grid='kit4'
regionname='mostchannels'
datatype='2d'
lfolder='kit4_kelp_0.0'
lname='kit4_kelp_0.0_0_all_in_a_box'


### load the .nc file #####
data = loadnc('/media/moe46/My Passport/kit4_runs/' + name +'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

savepath='figures/png/' + grid + '_' + datatype + '/lagtracker/' + lfolder + '/'
if not os.path.exists(savepath): os.makedirs(savepath)

trigridxy = mplt.Triangulation(data['x'], data['y'],data['nv'])
region=regions(regionname)


savelag=(sio.loadmat('/home/moe46/workspace_matlab/lagtracker/savedir/'+lfolder+'/kit4_kelp_0.0_0.mat',squeeze_me=True,struct_as_record=False))['savelag']

if True:
    import h5py as h5
    fileload=h5.File('/home/moe46/workspace_matlab/lagtracker/savedir/'+lfolder+'/'+lname+'.mat')
    fileload=fileload['savelag']
    savelag.x=fileload['x'].value.T
    savelag.y=fileload['y'].value.T


daysi=9
lph=24*6
testi=12
rows=2
cols=2
testi=np.min([(rows*cols)-1,testi])
region['region']=[np.nanmin(savelag.x[:,daysi*testi*lph]),np.nanmax(savelag.x[:,daysi*testi*lph]),np.nanmin(savelag.y[:,daysi*testi*lph]),np.nanmax(savelag.y[:,daysi*testi*lph])]

scale=1000                                                                                                                                                                                                                                                                   
ticks = mpl.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale))


f, ax = plt.subplots(nrows=rows,ncols=cols, sharex=True, sharey=True)
ax=ax.flatten()

for i in range(0,len(ax)):
    print i
    ax[i].triplot(trigridxy,lw=.05)
    plotidx=np.where(np.isnan(savelag.x[:,daysi*i*lph]) & ((savelag.x[:,daysi*i*lph]-savelag.x[:,daysi*(i-1)*lph])!=0))
    plotidxb=np.zeros(shape=(savelag.x.shape[0],), dtype=bool)
    plotidxb[plotidx]=1
    #ax[i].plot(savelag.x[plotidxb,daysi*i*lph],savelag.y[plotidxb,daysi*i*lph],'g.')
    ax[i].plot(savelag.x[~plotidxb,daysi*i*lph],savelag.y[~plotidxb,daysi*i*lph],'r.',markersize=.5)
    #ax[i].plot(savelag.x[:,daysi*i*lph],savelag.y[:,daysi*i*lph],'g.')
    
    #plotidx2=np.where(np.fabs(savelag.z[:,daysi*i*lph]-data['uvh'][trigridxy.get_trifinder().__call__(savelag.x[:,daysi*i*lph],savelag.y[:,daysi*i*lph])])<=1 )
    #ax[i].plot(savelag.x[plotidx2,daysi*i*lph],savelag.y[plotidx2,daysi*i*lph],'y.')

    ax[i].axis(region['region'])
    ax[i].set_title('Day '+ ("%.1f"% (48*daysi*i/48)))
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

    
f.savefig(savepath + lname+'_every_'+("%.1f"%daysi)+'days_at_' +("%d"%testi)+ '_rows_'+("%d"%rows)+'_cols_'+("%d"%cols)+'.png',dpi=1200)

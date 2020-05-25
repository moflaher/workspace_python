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
from projtools import *
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)


# Define names and types of data
name='sfm5m_sjr_basicrun'
grid='sfm5m_sjr'

regionlist=['sfmwhole']
starttime=0
plotgrid=False


### load the .nc file #####
data = loadnc('runs/' +grid+'/' + name + '/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')






savepath='figures/png/' + grid + '_'  + '/modelbasic/'
if not os.path.exists(savepath): os.makedirs(savepath)


for regionname in regionlist:

    region=regions(regionname)
    nidx=get_nodes(data,region)
    eidx=get_elements(data,region)
    
    if ((len(nidx)==0) or (len(eidx)==0)):
        continue
    
    print('plotting region: ' +regionname)

    # Plot mean speed
    meanspeed=(np.sqrt(data['ua'][starttime:,]**2 +data['va'][starttime:,]**2)).mean(axis=0)
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],meanspeed,vmin=meanspeed[eidx].min(),vmax=meanspeed[eidx].max())
    prettyplot_ll(ax,setregion=region,grid=plotgrid,cblabel=r'Mean Speed (ms$^{-1}$)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_DA_meanspeed.png',dpi=600)
    plt.close(f)

    # Plot mean speed percentile
    clims=np.percentile(meanspeed[eidx],[5,95])
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],meanspeed,vmin=clims[0],vmax=clims[1])
    prettyplot_ll(ax,setregion=region,grid=plotgrid,cblabel=r'Mean Speed (ms$^{-1}$)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_DA_meanspeed_percentile.png',dpi=600)
    plt.close(f)


    # Plot max speed
    maxspeed=(np.sqrt(data['ua'][starttime:,]**2 +data['va'][starttime:,]**2)).max(axis=0)
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],maxspeed,vmin=maxspeed[eidx].min(),vmax=maxspeed[eidx].max())
    prettyplot_ll(ax,setregion=region,grid=plotgrid,cblabel=r'Max Speed (ms$^{-1}$)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_DA_maxspeed.png',dpi=600)
    plt.close(f)

    # Plot max speed percentile
    clims=np.percentile(maxspeed[eidx],[5,95])
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],maxspeed,vmin=clims[0],vmax=clims[1])
    prettyplot_ll(ax,setregion=region,grid=plotgrid,cblabel=r'Max Speed (ms$^{-1}$)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_DA_maxspeed_percentile.png',dpi=600)
    plt.close(f)


    # Plot mean zeta
    meanzeta=(data['zeta'][starttime:,:]).mean(axis=0)
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],meanzeta,vmin=meanzeta[nidx].min(),vmax=meanzeta[nidx].max())
    prettyplot_ll(ax,setregion=region,grid=plotgrid,cblabel=r'Mean Zeta (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_meanzeta.png',dpi=600)
    plt.close(f)

    # Plot mean zeta percentile
    clims=np.percentile(meanzeta[nidx],[5,95])
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],meanzeta,vmin=clims[0],vmax=clims[1])
    prettyplot_ll(ax,setregion=region,grid=plotgrid,cblabel=r'Mean Zeta (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_meanzeta_percentile.png',dpi=600)
    plt.close(f)


    # Plot tidal range
    zetarange=(data['zeta'][starttime:,:]).max(axis=0)-(data['zeta'][starttime:,:]).min(axis=0)
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],zetarange,vmin=zetarange[nidx].min(),vmax=zetarange[nidx].max())
    prettyplot_ll(ax,setregion=region,grid=plotgrid,cblabel=r'Tidal Range (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_tidalrange.png',dpi=600)
    plt.close(f)

    # Plot mean zeta percentile
    clims=np.percentile(zetarange[nidx],[5,95])
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],zetarange,vmin=clims[0],vmax=clims[1])
    prettyplot_ll(ax,setregion=region,grid=plotgrid,cblabel=r'Tidal Range (m)',cb=triax)
    f.savefig(savepath + grid + '_' + regionname +'_tidalrange_percentile.png',dpi=600)
    plt.close(f)




























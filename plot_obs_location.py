from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from misctools import *
from plottools import *
from projtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import scipy.io as sio
import scipy.fftpack as fftp
import pandas as pd
from pyseidon import TideGauge
mpl.rcParams.update(mpl.rcParamsDefault)

# Define names and types of data
name='2012-02-01_2012-03-01_0.01_0.001'
grid='vhfr_low'
datatype='2d'
regionname='fr_whole'
region=regions(regionname)

region=expand_region(region,dist=[-32000,-18000], shift=[-28000,6000])
obspath='data/misc/vhfr_obs/VancouverBC_Harbour_Currents/'
obsname='04100_20110621'
obs=loadcur(obspath+obsname+'*.cur')

path2obs = "data/misc/vhfr_obs/slev/"
obsnamelist = [s for s in os.listdir(path2obs) if ".mat" in s]
# eobs
eobs = []
for tname in obsnamelist:
    filename = path2obs + tname
    print("Stacking: "+ tname +"...")
    inobs = TideGauge(filename)
    eobs.append(inobs)


savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)




### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

#Plot obs location
f=plt.figure()
ax=plt.axes([.125,.1,.775,.8])
ax.triplot(data['trigrid'],lw=.2)
prettyplot_ll(ax,setregion=region)
plotcoast(ax,filename='pacific_harbour.nc',color='0.6',fcolor='0.6',fill=True)

for key in obs:    
    ax.plot(obs[key]['lon'],obs[key]['lat'],'b*',markersize=8)

ax.annotate('ADCPs',xy=(obs[key]['lon']-.01,obs[key]['lat']-.01),xycoords='data',xytext=(obs[key]['lon']-.13,obs[key]['lat']-.05), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='w',headwidth=3),color='w')

    
for tobs in eobs:
    ax.plot(tobs.Variables.lon,tobs.Variables.lat,'r*',markersize=8)
    if tobs.Variables.RBR.name[-4:]=='7795':
        ax.annotate(tobs.Variables.RBR.name[-4:],xy=(tobs.Variables.lon+.01,tobs.Variables.lat+.01),xycoords='data',xytext=(tobs.Variables.lon+.03,tobs.Variables.lat+.1), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='w',headwidth=3),color='w')
    else:
        ax.annotate(tobs.Variables.RBR.name[-4:],xy=(tobs.Variables.lon+.01,tobs.Variables.lat+.01),xycoords='data',xytext=(tobs.Variables.lon+.05,tobs.Variables.lat+.05), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='w',headwidth=3),color='w')



    
f.savefig(savepath + grid + '_' + regionname +'_obs_location.png',dpi=300)
plt.close(f)


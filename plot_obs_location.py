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
from pyseidon_dvt import *
mpl.rcParams.update(mpl.rcParamsDefault)

# Define names and types of data
name='2012-02-01_2012-03-01_0.01_0.001'
grid='vh_high'
datatype='2d'
regionname='fr_whole'
region=regions(regionname)
region=expand_region(region,dist=[-32000,-18000], shift=[-28000,6000])

region2=regions('secondnarrows')
region2=expand_region(region2,dist=[-1000,-800], shift=[-400,-400])

# eobs
TGobs = []
Aobs = []

path2obs = "data/misc/vhfr_obs/VancouverBC_Harbour_Currents/"
obsnamelist = [s for s in os.listdir(path2obs) if "pad.mat" in s]
obsnamelist.sort()
for nameo in obsnamelist:
    filename = path2obs + nameo
    print("Stacking: "+ nameo +"...")
    inobs = ADCP(filename)
    inobs.Variables.ua=inobs.Variables.u
    inobs.Variables.va=inobs.Variables.v    
    Aobs.append(inobs)

path2obs = "data/misc/vhfr_obs/slev/"
obsnamelist = [s for s in os.listdir(path2obs) if ".mat" in s]
for tname in obsnamelist:
    filename = path2obs + tname
    print("Stacking: "+ tname +"...")
    inobs = TideGauge(filename)
    TGobs.append(inobs)


savepath='figures/png/' + grid + '_' + datatype + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)




### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

#Plot obs location
f=plt.figure()
ax=f.add_axes([.125,.1,.75,.8])
ax.triplot(data['trigrid'],lw=.2)
prettyplot_ll(ax,setregion=region)
plotcoast(ax,filename='pacific_harbour.nc',color='None',fill=True)

#for key in obs:    
    #ax.plot(obs[key]['lon'],obs[key]['lat'],'b*',markersize=8)

#ax.annotate('ADCPs',xy=(obs[key]['lon']-.01,obs[key]['lat']-.01),xycoords='data',xytext=(obs[key]['lon']-.13,obs[key]['lat']-.05), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='w',headwidth=3),color='w')

for tobs in Aobs:
    ax.plot(tobs.Variables.lon,tobs.Variables.lat,'b*',markersize=8)
    #if tobs.Variables.RBR.name[-4:]=='7795':
    #    ax.annotate(tobs.Variables.RBR.name[-4:],xy=(tobs.Variables.lon+.01,tobs.Variables.lat+.01),xycoords='data',xytext=(tobs.Variables.lon+.03,tobs.Variables.lat+.1), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='w',headwidth=3),color='w')
    #else:
    #    ax.annotate(tobs.Variables.RBR.name[-4:],xy=(tobs.Variables.lon+.01,tobs.Variables.lat+.01),xycoords='data',xytext=(tobs.Variables.lon+.05,tobs.Variables.lat+.05), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='w',headwidth=3),color='w')

ax.annotate('ADCPs',xy=(tobs.Variables.lon,tobs.Variables.lat),xycoords='data',xytext=(tobs.Variables.lon-.13,tobs.Variables.lat-.05), textcoords='data',arrowprops=dict(width=.5,shrink=0.05,color='w',headwidth=3),color='w')


    
for tobs in TGobs:
    ax.plot(tobs.Variables.lon,tobs.Variables.lat,'r*',markersize=8)
    if tobs.Variables.RBR.name[-4:]=='7795':
        ax.annotate(tobs.Variables.RBR.name[-4:],xy=(tobs.Variables.lon,tobs.Variables.lat),xycoords='data',xytext=(tobs.Variables.lon+.03,tobs.Variables.lat+.1), textcoords='data',arrowprops=dict(width=.5,shrink=0.05,color='w',headwidth=3),color='w')
    else:
        ax.annotate(tobs.Variables.RBR.name[-4:],xy=(tobs.Variables.lon,tobs.Variables.lat),xycoords='data',xytext=(tobs.Variables.lon+.05,tobs.Variables.lat+.05), textcoords='data',arrowprops=dict(width=.5,shrink=0.05,color='w',headwidth=3),color='w')

plot_box(ax,region2,'r',1.5)

ax0=f.add_axes([.4,.525,.6,.375])
ax0.xaxis.set_tick_params(labeltop='on',labelbottom='off')
ax0.yaxis.set_tick_params(labelright='on',labelleft='off')
ax0.triplot(data['trigrid'],lw=.2)

prettyplot_ll(ax0,setregion=region2)
plotcoast(ax0,filename='pacific_harbour.nc',color='None',fill=True)
ax0.set_xlabel('')
ax0.set_ylabel('')
ax0.set_xticklabels(ax0.get_xticks(),rotation=30)
ax0.set_yticklabels(ax0.get_yticks(),rotation=30)

for i,tobs in enumerate(Aobs):  
    j=i  
    ax0.plot(tobs.Variables.lon,tobs.Variables.lat,'b*',markersize=4)
    ax0.annotate("%d"%(j+1),(tobs.Variables.lon,tobs.Variables.lat),(tobs.Variables.lon+.002,tobs.Variables.lat-.003+j*.0008),arrowprops=dict(width=.5,shrink=0.15,color='k',headwidth=3),color='k')

ax0.set_xticklabels(-1*(ax0.get_xticks()))


plt.draw()

ax0bb=ax0.get_axes().get_position().bounds
ax.annotate("",xy=(ax0bb[0],ax0bb[1]),xycoords='figure fraction',xytext=(region2['region'][0],region2['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='r',headwidth=3))
ax.annotate("",xy=(ax0bb[0]+ax0bb[2],ax0bb[1]),xycoords='figure fraction',xytext=(region2['region'][1],region2['region'][2]), textcoords='data',arrowprops=dict(width=.5,shrink=0,color='r',headwidth=3))


    
f.savefig(savepath + grid + '_' + regionname +'_obs_location.png',dpi=300)
plt.close(f)


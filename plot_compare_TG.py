from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from folderpath import *
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
import pandas as pd
import ttide

# Define names and types of data
name='sjh_hr_v3_0.0175_shallow'
grid='sjh_hr_v3'

starttime=1008
endtime=-1
region=regions('sfmwhole')
region2=regions('bof_nemo')

savepath='{}/png/{}_{}/compare_TG/{}_{}_{}/'.format(figpath,grid,datatype,name,starttime,endtime)
if not os.path.exists(savepath): os.makedirs(savepath)

save=np.load('dataout/sjh_hr_v3_2d/compare_TG/{}_1008_-1/tg_compare_out_allcon.npy'.format(name))
save=save[()]

cons=['M2  ','N2  ','S2  ','K1  ','O1  ']

for con in cons:


    amp=np.array([])
    phase=np.array([])
    lon=np.array([])
    lat=np.array([])
    for key in save:
        if con in save[key]['df'].index:
            lon=np.append(lon,save[key]['lon'])
	    lat=np.append(lat,save[key]['lat'])
            amp=np.append(amp,save[key]['df'].loc[con,'Amp diff'])
            phase=np.append(phase,save[key]['df'].loc[con,'Phase diff'])


    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])
    plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc',filepath=coastpath, color='k', fcolor='0.75', fill=True)
    cbax=ax.scatter(lon,lat,c=amp,s=10,edgecolor='None',vmin=-.1,vmax=.1,cmap=mpl.cm.seismic)
    plt.colorbar(cbax)
    ax.axis(region['region'])
    f.savefig('{}{}_{}_amp.png'.format(savepath,region['regionname'],con.replace(' ','')),dpi=300)
    ax.axis(region2['region'])
    f.savefig('{}{}_{}_amp.png'.format(savepath,region2['regionname'],con.replace(' ','')),dpi=300)

    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])
    plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc',filepath=coastpath, color='k', fcolor='0.75', fill=True)
    cbax=ax.scatter(lon,lat,c=phase,s=10,edgecolor='None',vmin=-20,vmax=20,cmap=mpl.cm.seismic)
    plt.colorbar(cbax)
    ax.axis(region['region'])
    f.savefig('{}{}_{}_phase.png'.format(savepath,region['regionname'],con.replace(' ','')),dpi=300)
    ax.axis(region2['region'])
    f.savefig('{}{}_{}_phase.png'.format(savepath,region2['regionname'],con.replace(' ','')),dpi=300)


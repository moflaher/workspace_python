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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pandas as pd
import netCDF4 as n4
import copy

# Define names and types of data
name='sjh_hr_v3_year_reduce_0'
grid='sjh_hr_v3'
datatype='2d'
starttime=0
endtime=-1


### load the .nc file #####
#data = loadnc(runpath+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data = loadnc('/fs/vnas_Hdfo/odis/mif001/scratch/sjh_hr_v3/{}/output_all/'.format(name),singlename=grid + '_2016-02-01.nc')
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
print('done load')

alldata=n4.MFDataset('/fs/vnas_Hdfo/odis/mif001/scratch/sjh_hr_v3/{}/output_all/sjh_hr_v3_*.nc'.format(name))
alldata=alldata.variables
wetnodes=alldata['wet_nodes'][:]
time=alldata['time'][:]
zeta=alldata['zeta'][:]
locations=np.loadtxt('tcon.csv')




tout=alldata['Times'][starttime:endtime,]
tclean=np.empty((len(tout),),dtype='|S26')
for i in range(len(tout)):
    tclean[i]=''.join(tout[i,])


savepath='{}/{}_{}/zeta/{}_{}_{}/'.format(datapath,grid,datatype,name,starttime,endtime)
if not os.path.exists(savepath): os.makedirs(savepath)


for i,loc in enumerate(locations):
    print('='*80)
    print(i)
    xloc,yloc = data['proj'](loc[2],loc[1])
    xl,yl = data['proj'](xloc-5000,yloc-5000,inverse=True)
    xr,yr = data['proj'](xloc+5000,yloc+5000,inverse=True)
    region={}
    region['region']=np.array([xl,xr,yl,yr])


    dist=np.sqrt((data['x']-xloc)**2+(data['y']-yloc)**2)
    asort=np.argsort(dist)
    close=0
    while np.sum(wetnodes[:,asort[close]])<len(time):
	close+=1

    node=asort[close]

    print(close)
    print(dist[node])

    #nidx=get_nodes(data,region)
    #if len(nidx)==0:
    #    f,ax=plottri(data,data['h'],show=False)
    #else:	
    #    f,ax=plottri(data,data['h'],minmax=[data['h'][nidx].min(), data['h'][nidx].max()],show=False)
    #prettyplot_ll(ax,setregion=region)
    #plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc',filepath=coastpath, color='k', fcolor='0.75', fill=True)  
    #ax.plot(loc[2],loc[1],'k*',markersize=10)
    #ax.plot(data['lon'][node],data['lat'][node],'r*',markersize=10,alpha=.5)
    #f.savefig('{}{}_{}_{}_dist_{:.2f}_depth.png'.format(savepath,loc[0].astype(int),loc[2],loc[1],dist[node]),dpi=600)
    #plt.close(f)

    #zeta=ipt.interpN_at_loc(data,'zeta',[loc[2],loc[1]])
    #zetac=zeta[starttime:endtime]
    zetac=zeta[starttime:endtime,node]

    df=pd.DataFrame(np.vstack([tclean,zetac]).T,columns=['time','zeta'])
    df.to_csv('{}{}_{}_{}_dist_{:.2f}_{}.csv'.format(savepath,loc[0].astype(int),loc[2],loc[1],dist[node],node))























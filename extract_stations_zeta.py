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
import netCDF4 as n4
import copy

# Define names and types of data
name='sjh_hr_v3_year_reduce_0'
grid='sjh_hr_v3'

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

out={}
out['names']=np.array(['ADCP_588', 'ADCP_585', 'ADCP_582', 'ADCP_583','FORCE_Shoreline_ADCP', 'ADCP_569', 'ADCP_577', 'ADCP_576','ADCP_575', 'ADCP_573', 'ADCP_571', 'ADCP_570', 'SA_Buoy'],dtype='|S24')
out['lon']=np.array([-66.04198, -65.9896 , -66.02997, -66.0448 , -64.40494, -66.02398,-65.99   , -66.05323, -66.0243 , -66.04222, -66.04454, -65.99186,-66.0968 ])
out['lat']=np.array([ 45.24085,  45.2046 ,  45.2213 ,  45.2132 ,  45.36964,  45.22296,45.2041 ,  45.25328,  45.22312,  45.2413 ,  45.21382,  45.20397,45.20865])


node=np.array([ 46278,  69890,  38953,  37565,   1371,  79945,  69889,  50899,79944,  46360,  37630,  69400, 114863], dtype=int)

tout=alldata['Times'][starttime:endtime,]
tclean=np.empty((len(tout),),dtype='|S26')
for i in range(len(tout)):
    tclean[i]=''.join(tout[i,])


savepath='{}/{}_{}/zeta/{}_{}_{}/'.format(datapath,grid,datatype,name,starttime,endtime)
if not os.path.exists(savepath): os.makedirs(savepath)


for i,ni in enumerate(node):
    zetac=zeta[starttime:endtime,data['nv'][ni,:]].mean(axis=1)
    df=pd.DataFrame(np.vstack([tclean,zetac]).T,columns=['time','zeta'])
    df.to_csv('{}{}_{}_{}_{}.csv'.format(savepath,ni,out['lon'][i],out['lat'][i],out['names'][i]))

























from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from mytools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pandas as pd
import netCDF4 as n4
import copy
import matplotlib.dates as dates
from collections import OrderedDict
import ttide


# Define names and types of data
grids=OrderedDict()
grids['sjh_lr_v1_sub']=['test_1','year_wet']
grids['sjh_lr_v2_double']=['year_fvcom41']


levels=['2','5','10']
adcps=['ADCP_569','ADCP_571','ADCP_575','ADCP_577']
#  ADCP_583  ADCP_585  ADCP_590  ADCP_592 ADCP_570  ADCP_573  ADCP_576  ADCP_582  ADCP_584  ADCP_588  ADCP_591]

cl=len(grids.keys())

def grab_adcp_stats(grid,name,adcp,level):
    
    loadpath='{}/{}_2d/adcp/{}/{}/'.format(datapath,grid,name,adcp)
    tcon_mod=pd.read_csv('{}{}_mod_ttide_tidecon_at_{}m.csv'.format(loadpath,adcp,level))
    tcon_obs=pd.read_csv('{}{}_obs_ttide_tidecon_at_{}m.csv'.format(loadpath,adcp,level))
    ts=pd.read_csv('{}{}_timeseries_at_{}m.csv'.format(loadpath,adcp,level))
    stats=pd.read_csv('{}{}_timeseries_stats_at_{}m.csv'.format(loadpath,adcp,level))


    #out_mod=pd.read_csv('{}{}_mod_ttide_output_at_{}m.txt'.format(loadpath,adcp,adcp,level))
    #out_obs=pd.read_csv('{}{}_obs_ttide_output_at_{}m.txt'.format(loadpath,adcp,adcp,level))


for i,grid in enumerate(grids):
    for j,name in enumerate(grids[grid]):
        for k,adcp in enumerate(adcps):
            for l,level in enumerate(levels):
                print(grid,name,adcp,level)
                
                #try:
                    
                    #model = np.load('{}ADCP_{}_model_ministation.npy'.format(lpath,adcp['metadata']['ADCP_number']))
                    #model = model[()]
                    
                grab_adcp_stats(grid,name,adcp,level)
                    
                #except:
                    #print('failed')
                    #continue
            
        

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
import matplotlib.dates as dates
import argparse

def pair(arg):
    # For simplity, assume arg is a pair of floats
    # separated by a comma. If you want to do more
    # validation, raise argparse.ArgumentError if you
    # encounter a problem.
    return [float(x) for x in arg.split(',')]

parser = argparse.ArgumentParser()
parser.add_argument("grid", help="name of the grid", type=str)
parser.add_argument("name", help="name of the run", type=str)
parser.add_argument("ncfile", help="name of the ncfile", type=str)
parser.add_argument("-l", help="lon,lat", nargs=2, action='append')
args = parser.parse_args()

print("The current commandline arguments being used are")
print(args)

name=args.name
grid=args.grid
ncfile=args.ncfile
ncloc=ncfile.rindex('/')

locs=np.array(args.l).astype(float)

# Define names and types of data
#name='test01'
#grid='sjh_lr_v1'



### load the .nc file #####
#data = loadnc(runpath+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
#data = loadnc('/fs/vnas_Hdfo/odis/mif001/scratch/sjh_lr_v1/testing/{}/output/'.format(name),singlename=grid + '_0001.nc')
data = loadnc(ncfile[:ncloc+1],ncfile[ncloc+1:])
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
data['xc'] = data['x'][data['nv']].mean(axis=1)
data['yc'] = data['y'][data['nv']].mean(axis=1)
print('done load')


savepath='{}/{}_{}/loc/{}/'.format(datapath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)


for i,loc in enumerate(locs):
    print('='*80)
    print(i)
    print(loc)
    xloc,yloc = data['proj'](loc[0],loc[1])

    dist=np.sqrt((data['xc']-xloc)**2+(data['yc']-yloc)**2)
    asort=np.argsort(dist)
    ele=asort[0]
    elen=data['nv'][ele,:]
    
    print(data['lonc'][ele],data['latc'][ele])
    print(dist[ele])
    

    out=OrderedDict()
    out['time']=data['time']
    out['Time']=data['Time']
    print('Extracted time')

    out['h']=data['h'][elen].mean()
    out['zeta']=data['zeta'][:,elen].mean(axis=1)
    out['ua']=data['ua'][:,ele]
    out['va']=data['va'][:,ele]
    print('Extracted 2d')
    
    out['u']=data['u'][:,:,ele]
    out['v']=data['v'][:,:,ele]
    out['ww']=data['ww'][:,:,ele]
    out['temp']=data['temp'][:,:,elen].mean(axis=2)
    out['salinity']=data['salinity'][:,:,elen].mean(axis=2)
    print('Extracted 3d')
    
    out['siglev']=data['siglev'][:,elen[0]]
    out['siglay']=data['siglay'][:,elen[0]]
    out['lon']=data['lonc'][ele]
    out['lat']=data['latc'][ele]
    print('Extracted misc')
    
    for key in out:
        out[key]=np.squeeze(out[key])
    
    kill
    savepath2='{}ADCP_{}'.format(savepath,''.join(data['name_station'][idx,:]).strip())
    if not os.path.exists(savepath2): os.makedirs(savepath2)
    np.save('{}/ADCP_{}_model_ministation.npy'.format(savepath2,''.join(data['name_station'][idx,:]).strip()),out)
    print('Saved')


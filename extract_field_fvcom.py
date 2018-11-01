from __future__ import division,print_function
import numpy as np
import scipy as sp
from mytools import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import os, sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pandas as pd
import matplotlib.dates as dates
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("grid", help="name of the grid", type=str)
parser.add_argument("name", help="name of the run", type=str)
parser.add_argument("ncfile", help="name of the ncfile", type=str)
parser.add_argument("-f", help="field name", type=str)
parser.add_argument("-l", help="field layer", type=int, default=None)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-t',help='timestep to use',type=int)
group.add_argument('-d',help='datestr to use',type=str)
    
args = parser.parse_args()

print("The current commandline arguments being used are")
print(args)


name=args.name
grid=args.grid
ncfile=args.ncfile
ncloc=ncfile.rindex('/')


datatype='2d'


### load the .nc file #####
data = loadnc(ncfile[:ncloc+1],ncfile[ncloc+1:])
print('done load')
    
if args.f not in data.keys():
    print('{} is not a valid field'.format(args.f))
    sys.exit()    

savepath='{}/{}_{}/field/{}/{}/'.format(datapath,grid,datatype,name,args.f)
if not os.path.exists(savepath): os.makedirs(savepath)

if args.t is None:
    args.t=np.argmin(np.fabs(data['time']-dates.datestr2num(args.d)))

args.d=data['Time'][args.t]

if len(data[args.f].shape)==2:
    field=data[args.f][args.t,:]
    savepath2='{}field_{}_timestep_{}_date_{}.dat'.format(savepath,args.f,args.t,args.d)
elif len(data[args.f].shape)==3:
    if args.l is not None:
        field=data[args.f][args.t,args.l,:]
        savepath2='{}field_{}_layer_{}_timestep_{}_date_{}.dat'.format(savepath,args.f,args.l,args.t,args.d)
    else:
        field=data[args.f][args.t,:,:].T
        savepath2='{}field_{}_timestep_{}_date_{}.dat'.format(savepath,args.f,args.t,args.d)
else:
    print('ooops!')


save_array(field,savepath2)

print('Saved')


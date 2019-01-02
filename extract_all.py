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
from collections import OrderedDict



parser = argparse.ArgumentParser()
parser.add_argument("grid", help="name of the grid", type=str)
parser.add_argument("name", help="name of the run", type=str)
parser.add_argument("ncfile", help="specify ncfile", type=str)
parser.add_argument("--station", help="switch to station output instead of fvcom output", default=False,action='store_true')
parser.add_argument("-dist", help="max distance from obs to be allowed", type=float,default=10000)
parser.add_argument("-snr", help="signal to noise ratio value used for constituent cutoff", type=float,default=2.0)
parser.add_argument("-days", help="Min. record length for wlev file to be used", type=float, default=29.0)
args = parser.parse_args()

print("The current commandline arguments being used are")
print(args)


mainline='{} {} {}'.format(args.name,args.grid,args.ncfile)

if args.dist != 10000:
    mainline='{} -dist {}'.format(mainline,args.dist)
if args.snr != 2.0:
    mainline='{} -snr {}'.format(mainline,args.snr)
if args.days != 29.0:
    mainline='{} -days {}'.format(mainline,args.days)
if args.station:
    mainline='{} --station'.format(mainline)


os.system('python extract_buoy.py {}'.format(mainline))
os.system('python extract_tg.py {}'.format(mainline))
os.system('python extract_ctd.py {}'.format(mainline))
os.system('python extract_adcp.py {}'.format(mainline))
os.system('python extract_wlev.py {}'.format(mainline))





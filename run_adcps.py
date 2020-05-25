from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from folderpath import *
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
from stattools import *
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
from collections import OrderedDict
import ttide
import argparse


# Define names and types of data
grids=OrderedDict()
grids['sjh_lr_v1']=['sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1_jcool0']
grids['sjh_lr_v1_sub']=['test_1','year_wet']
grids['sjh_lr_v2_double']=['year_fvcom41','year_fvcom41_wet']
grids['sjh_lr_v3']=['year_fvcom41']



for i,grid in enumerate(grids):
    for j,name in enumerate(grids[grid]):
        os.system("python plot_adcp_density.py {} {} 5&".format(grid,name))

from __future__ import division,print_function

import sys
sys.path.append('/home/moflaher/Desktop/workspace_python/')
sys.path.append('/home/moe46/Desktop/workspace_python/')
sys.path.append('/home/mif001/workspace_python/')
sys.path.append('/home/moflaher/src/workspace_python/')


import numpy as np
import scipy as sp
import matplotlib as mpl
mpl.use('Agg')
#mpl.use('Qt4Agg')
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import scipy.io as sio
#from mpl_toolkits.basemap import Basemap
import os as os
import sys

from folderpath import *
from fvcomtools import *
from gridtools import *
from datatools import *
from misctools import *
from plottools import *
from projtools import *

from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)



#import my tools again but as something, this is mostly to beable to easily check for function names
import gridtools as gt
import datatools as dt
import misctools as mt
import plottools as pt
import interptools as ipt
import projtools as pjt
import folderpath as fpath
import fvcomtools as ft

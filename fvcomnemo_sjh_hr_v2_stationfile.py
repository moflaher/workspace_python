from __future__ import division,print_function
import matplotlib as mpl
mpl.use('Agg')
import scipy as sp
from folderpath import *
from fvcomtools import *
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import collections




data=loadnc('/media/moflaher/runs/sjh_hr_v2/sjh_hr_v2_2_0.5/output','sjh_hr_v2_0001.nc')


station=collections.OrderedDict()

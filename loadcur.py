from __future__ import division,print_function
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import scipy.io as sio
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
from StringIO import StringIO
from gridtools import *
from datatools import *
from misctools import *
from plottools import *
from projtools import *
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)



filename='data/misc/vhfr_obs/VancouverBC_Harbour_Currents/04100_20110621_bin1pad.cur'


fp=open(filename,'r')


indata={}





for line in fp.readlines():
    if '||' in line:
        if '!Observed' in line:
            sline=line.split()            
            indata['lon']=-1*(float(sline[3])+float(sline[4][:-1])/60)
            indata['lat']=1*(float(sline[1])+float(sline[2][:-1])/60)
        if 'Computed from spatial average bin' in line:
            sline=line.split()  
            indata['bin']=int(sline[5][:-1])
            indata['range']=np.array([int(val) for val in sline[6][:-1].split('-')])




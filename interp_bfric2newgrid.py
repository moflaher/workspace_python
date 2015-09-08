from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from scipy.interpolate import Rbf, InterpolatedUnivariateSpline
from scipy import interpolate


data = loadnc('/media/moflaher/My Book/cages/cage_0.6_baserun_2/output/',singlename='sfm6_musq_0001.nc')
data = ncdatasort(data)


data2 = loadnc('/media/moflaher/My Book/cages/sfm6_musq2/output/',singlename='sfm6_musq2_0001.nc')
data2 = ncdatasort(data2)

bfric=np.genfromtxt('NS_GoM_bfric2.dat',skiprows=1)



#host=data['trigrid'].TriInterpolator.__call__(data2['uvnodell'][:,0],data2['uvnodell'][:,1])


#newbfric=mpl.tri.TriInterpolator(data['trigrid'],bfric[:,1]).__call__(data2['uvnodell'][1:10,0],data2['uvnodell'][1:10,1])



#rbf = Rbf(data['uvnodell'][:,0],data['uvnodell'][:,0], bfric[:,1])


#tck = interpolate.bisplrep(data['uvnodell'][:,0],data['uvnodell'][:,0], bfric[:,1])
#newbfric = interpolate.bisplev(np.squeeze(data2['uvnodell'][:,0]),np.squeeze(data2['uvnodell'][:,1],tck)
#newbfric = interpolate.bisplev(-66,45,tck)



newbfric = interpolate.NearestNDInterpolator(data['uvnodell'], bfric[:,1]).__call__(data2['uvnodell'])


fp=open('sfm6_musq2_bfric.dat','w')


fp.write('BFRIC Node Number= %d\n' % newbfric.shape[0])
for i in range(0,newbfric.shape[0]):
    fp.write('%d %f\n' % (i+1, newbfric[i]) )


fp.close()

from __future__ import division,print_function
import numpy as np
import matplotlib as mpl
import scipy as sp
from datatools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os



name='kit4'

xyz=np.genfromtxt(name + '.xyz')
ele=np.genfromtxt(name + '.ele')




if 1==0:

    maxnei=np.histogram(ele,bins=ele.max()-1)[0].max()
    nnodes=xyz.shape[0]
    noderange=np.arange(1,nnodes+1)

    xmin=xyz[:,0].min()
    xmax=xyz[:,0].max()
    ymin=xyz[:,1].min()
    ymax=xyz[:,1].max()


    neighbourlist=np.zeros([xyz.shape[0],maxnei])

    for i in range(1,xyz.shape[0]+1):
        print i
        idx=np.where(ele==i)[0]
        tneilist=np.unique(ele[idx,:])
        tneilist=tneilist[tneilist!=i]
        neighbourlist[i-1,0:len(tneilist)]=tneilist



fp=open(name + '.nei','w')

fp.write('%d\n' % nnodes)
fp.write('%d\n' % maxnei)
fp.write('%f %f %f %f\n' % (xmax, ymin, xmin, ymax))

for i in range(0,nnodes):
    fp.write('%d %f %f %d %f %u %u %u %u %u %u %u %u\n' % (i+1, xyz[i,0], xyz[i,1], 0 ,xyz[i,2],neighbourlist[i,0],neighbourlist[i,1],neighbourlist[i,2],neighbourlist[i,3],neighbourlist[i,4],neighbourlist[i,5],neighbourlist[i,6],neighbourlist[i,7])    )

fp.close()

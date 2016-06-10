from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from gridtools import *
from datatools import *
from misctools import *
from plottools import *
from projtools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import numpy as np
import os as os
import sys
import copy
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


neifile=load_neifile('voucher.nei')
neifile=get_nv(neifile)
neifile['x'],neifile['y'],proj=lcc(neifile['lon'],neifile['lat'])
neifile=ncdatasort(neifile)
neifile=get_sidelength(neifile)
segfile=nei2seg(neifile)

#idx=neifile['bcode']==0
#segfile['1']=np.vstack([segfile['1'],np.vstack([neifile['lon'][idx],neifile['lat'][idx]]).T])
#save_nodfile(segfile,'test8.nod')

#add the interior points as last "boundary"
idx=np.argwhere(neifile['bcode']==0)

newlat=copy.deepcopy(neifile['lat'])
newlon=copy.deepcopy(neifile['lon'])
nei=neifile['neighbours']
x=neifile['x']
y=neifile['y']
xs=.75
ys=.75
#add code here to jiggle the points a bit to fix the consistency
for e,i in enumerate(idx):
    print(e)
    minx=100000
    miny=100000
    for j in nei[i,:].flatten():
        #maybe remove this depending
        if j==0:
            break
        xdist=x[i]-x[j-1]
        ydist=y[i]-y[j-1]
        if xdist<minx:
            minx=xdist
        if ydist<miny:
            miny=ydist
    newx=x[i]+((np.random.rand(1)-.5)*minx*xs)
    newy=y[i]+((np.random.rand(1)-.5)*miny*ys)
    newlon[i],newlat[i]=proj(newx,newy,inverse=True)

segfile['14']=np.hstack([newlon[idx],newlat[idx]]) 
save_nodfile(segfile,'test.nod')

#have to open nod file after and subtract 1 from the boundary number.
#in this case change 14 to 13 other wise triangle -pj barfs.

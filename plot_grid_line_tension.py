from __future__ import division
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




data = loadnc('/home/moe46/workspace_matlab/runs/dngrid/2d/westport/output/',singlename='dngrid_0001.nc')
data = ncdatasort(data)

neifile=loadnei('/home/moe46/workspace_matlab/nei_files/grids/dngrid_final_10_ppolex_save.nei')

xloc1=np.empty([1,])
yloc1=np.empty([1,])

xloc2=np.empty([1,])
yloc2=np.empty([1,])

runningdist=np.empty([1,])
runningdistt=np.empty([1,])


for i in range(0,len(data['nodell'])):
    tdist=0
    runningdistt=0
    print i
    for j in np.flatnonzero(neifile['neighbours'][i,]!=0):
        #print j
        dist=np.sqrt( (data['nodell'][i,0]-data['nodell'][neifile['neighbours'][i,j]-1,0])**2 +      (data['nodell'][i,1]-data['nodell'][neifile['neighbours'][i,j]-1,1])**2         )
        tdist+=dist
        xloc1=np.append(xloc1,data['nodell'][i,0])
        yloc1=np.append(yloc1,data['nodell'][i,1])
        xloc2=np.append(xloc2,data['nodell'][neifile['neighbours'][i,j]-1,0])
        yloc2=np.append(yloc2,data['nodell'][neifile['neighbours'][i,j]-1,1])
        runningdistt=np.append(runningdistt,dist)
    runningdist=np.append(runningdist,runningdistt/tdist)
    #print tdist




#plt.close()
#plt.tripcolor(data['trigrid'],np.zeros([len(data['nv']),1]))
#plt.grid()
#plt.title(grid + ' Grid')
    #plt.savefig(savepath + grid +'_grid.png',dpi=600)
#plt.close()


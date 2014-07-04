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



#Load data
data = loadnc('/home/moflaher/workspace_matlab/runs/beaufort3/3d/try16/output/',singlename='beaufort3_0001.nc')
data = ncdatasort(data)
neifile=loadnei('/home/moflaher/workspace_matlab/runs/beaufort3/3d/try16/input/beaufort3.nei')

#Empty arrays (how does lines related to elements or nodes? , probably a big speed up for not using append)
xloc1=np.array([])
yloc1=np.array([])
xloc2=np.array([])
yloc2=np.array([])
runningdist=np.array([])
tnd=np.empty([len(data['nodell']),])


#Find total length of lines connecting node to its neighbours
for i in range(0,len(data['nodell'])):
    tdist=0    
    print "1" , i
    for j in np.flatnonzero(neifile['neighbours'][i,]!=0):
        dist=np.sqrt( (data['nodell'][i,0]-data['nodell'][neifile['neighbours'][i,j]-1,0])**2 +      (data['nodell'][i,1]-data['nodell'][neifile['neighbours'][i,j]-1,1])**2         )
        tdist+=dist
       
    tnd[i]=tdist



#Calculate each lines percentage of total distance per node. Save max percentage value for each line.
#Set any points on a boundary to zero, they throw off the color scale.
for i in range(0,len(data['nodell'])):
    print "2" , i
    for j in np.flatnonzero(neifile['neighbours'][i,]!=0):
        if (neifile['bcode'][i]==0):
            dist=np.sqrt( (data['nodell'][i,0]-data['nodell'][neifile['neighbours'][i,j]-1,0])**2 +      (data['nodell'][i,1]-data['nodell'][neifile['neighbours'][i,j]-1,1])**2         )
            
            idx=np.where((xloc2==data['nodell'][i,0]) & (yloc2==data['nodell'][i,1]) & (xloc1==data['nodell'][neifile['neighbours'][i,j]-1,0]) & (yloc1==data['nodell'][neifile['neighbours'][i,j]-1,1]) )[0]

            if (idx.size>0):            
                runningdist[idx]=np.max([runningdist[idx],(dist/tnd[i])*(6/sum(neifile['neighbours'][i,]!=0))])
        
            else:        
                xloc1=np.append(xloc1,data['nodell'][i,0])
                yloc1=np.append(yloc1,data['nodell'][i,1])
                xloc2=np.append(xloc2,data['nodell'][neifile['neighbours'][i,j]-1,0])
                yloc2=np.append(yloc2,data['nodell'][neifile['neighbours'][i,j]-1,1])
                runningdist=np.append(runningdist,dist/tnd[i])
        else:
            idx=np.where((xloc2==data['nodell'][i,0]) & (yloc2==data['nodell'][i,1]) & (xloc1==data['nodell'][neifile['neighbours'][i,j]-1,0]) & (yloc1==data['nodell'][neifile['neighbours'][i,j]-1,1]) )[0]

            if (idx.size>0):            
                runningdist[idx]=np.max([runningdist[idx],0])
        
            else:        
                xloc1=np.append(xloc1,data['nodell'][i,0])
                yloc1=np.append(yloc1,data['nodell'][i,1])
                xloc2=np.append(xloc2,data['nodell'][neifile['neighbours'][i,j]-1,0])
                yloc2=np.append(yloc2,data['nodell'][neifile['neighbours'][i,j]-1,1])
                runningdist=np.append(runningdist,0)


#Slow hacky plot, use jet reversed as it is better for my vision.
jet = cm = plt.get_cmap('jet_r') 
cNorm  = mpl.colors.Normalize(vmin=runningdist[runningdist!=0].min(), vmax=runningdist.max())
scalarMap = mpl.cm.ScalarMappable(norm=cNorm, cmap=jet)
print scalarMap.get_clim()

plt.close()


for i in range(0,len(xloc1)):
    print i
    colorVal = scalarMap.to_rgba(runningdist[i])
    plt.plot([xloc1[i],xloc2[i]],[yloc1[i],yloc2[i]],color=colorVal)

#Add colorbar, how?
plt.show()



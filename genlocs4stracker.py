from __future__ import division
import matplotlib as mpl
import scipy as sp
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
sys.path.append('/home/moe46/Desktop/school/workspace_python/ttide_py/ttide/')
sys.path.append('/home/moflaher/Desktop/workspace_python/ttide_py/ttide/')
from t_tide import t_tide
from t_predic import t_predic
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import time


savepath='figures/png/misc/genlocs4stracker/'
if not os.path.exists(savepath): os.makedirs(savepath)



f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])


lons=np.array([-130,-131,-132.5,-133.75])
lats=np.array([51.75,53.25,54.5,53])

boxes=np.empty((len(lats),4))

#ax.plot(lons,lats,'r*',markersize=2)
for i in range(len(lats)):
	boxes[i,:]=meter_box(ax,[lons[i],lats[i]],[200,100],lw=.5,retbox=True)


region={}
region['region']=np.array([-136,-126,50,56])

prettyplot_ll(ax,setregion=region)
plotcoast(ax,filename='pacific.nc',color='None',fill=True)

 
f.show()   
#f.savefig(savepath +'genlocs_' +time.ctime()+ '.png',dpi=300)

locs=np.empty((0,2))

for i in range(len(boxes)):
	xl=np.linspace(boxes[i,0],boxes[i,1],100)
	yl=np.linspace(boxes[i,2],boxes[i,3],50)
	XL,YL=np.meshgrid(xl,yl)
	locs=np.vstack([locs,np.vstack([XL.flatten(),YL.flatten()]).T])
	


np.savetxt('data/stracker_input/helens_work_200mx100m_4locs.dat',locs,fmt='%.12f')

    

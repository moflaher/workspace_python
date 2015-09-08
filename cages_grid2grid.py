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


data1 = loadnc('/home/moe46/Desktop/school/workspace_python/',singlename='sfm6_musq_small.nc')
data1 = ncdatasort(data1)


data2 = loadnc('/home/moe46/Desktop/school/workspace_python/',singlename='sfm6_musq2_small.nc')
data2 = ncdatasort(data2)

cages=(np.genfromtxt('sfm6_musq_cage.dat')-1).astype(int)

savepath='figures/png/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)



host=data2['trigrid'].get_trifinder().__call__(data1['uvnodell'][cages,0],data1['uvnodell'][cages,1])

newhost=np.array([19555,19556, 19557, 19557, 20283, 19550, 19549, 18864, 18863, 19546,19547, 19548, 20281, 20282, 20285, 19558,20284], dtype=np.int32)

trihost2=np.zeros([data2['uvnodell'].shape[0],])
trihost2[newhost]=1

region=[-181000, -179000, 363000, 364000]

plt.close()
plt.tripcolor(data2['trigrid'],trihost2)
plt.triplot(data2['trigrid'],lw=.1)
plt.grid()
plt.axis(region)
ax=plt.gca()
#for i in range(0,len(data2['uvnodell'])):
#	ax.annotate( ("%d" %(i)),(data2['uvnodell'][i,0],data2['uvnodell'][i,1]),fontsize=4)

plt.savefig(savepath + 'sfm6_musq2_cages_original.png',dpi=1200)
plt.close()


trihost1=np.zeros([data1['uvnodell'].shape[0],])
trihost1[cages]=1

plt.tripcolor(data1['trigrid'],trihost1)
plt.triplot(data1['trigrid'],lw=.1)
plt.grid()
plt.axis(region)
plt.savefig(savepath + 'sfm6_musq_cages_original.png',dpi=1200)
plt.close()

drag=np.zeros([newhost.shape[0],])+0.6
depth=np.zeros([newhost.shape[0],])+10.0

fvcom_savecage('sfm6_musq2_cage.dat',newhost+1,drag,depth)





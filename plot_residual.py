from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
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

# Define names and types of data
name='kit4_kelp_nodrag'
grid='kit4_kelp'
regionname='kit4_kelp_tight2_kelpfield'
datatype='2d'
starttime=400
endtime=450
cmin=0
cmax=1


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

cages=None
with open('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat') as f_in:
    cages=np.genfromtxt(f_in,skiprows=1)
    if len(cages)>0:
        cages=(cages[:,0]-1).astype(int)
        tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
        color='g'
        lw=.2
        ls='solid'
    else:
        cages=None


region=regions(regionname)
eidx=get_elements(data,region)

savepath='figures/timeseries/' + grid + '_' + datatype + '/residual/' + name + '_' + regionname + '_' +("%f" %cmin) + '_' + ("%f" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)
plt.close()

uv=np.load('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv_all.npy')
uv=uv[()]

resu=np.zeros((data['nele'],len(data['time'][starttime:(endtime+1)])))
resv=np.zeros((data['nele'],len(data['time'][starttime:(endtime+1)])))
for j in range(0,len(eidx)):
    print ("%d"%j)+"              "+("%f"%(j/len(eidx)*100)) 
    i=eidx[j]    
    tp=t_predic(data['time'][starttime:(endtime+1)],uv['nameu'],uv['freq'],uv['tidecon'][i,:,:])
    resu[i,:]=data['ua'][starttime:(endtime+1),i]-np.real(tp).flatten()
    resv[i,:]=data['va'][starttime:(endtime+1),i]-np.imag(tp).flatten()


# Plot mesh
for i,timei in enumerate(range(starttime,endtime)):
    print i
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],np.sqrt(resu[:,i]**2+resv[:,i]**2),vmin=cmin,vmax=cmax)
    plotcoast(ax,filename='pacific.nc',color='k',fill=True)
    if cages!=None:   
        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        ax.add_collection(lseg_t) 
    prettyplot_ll(ax,setregion=region,cblabel=r'Residual (ms$^{-1}$)',cb=triax,grid=True)
    f.savefig(savepath + grid + '_' + regionname +'_residual_' + ("%04d" %(timei)) + '.png',dpi=300)
    plt.close(f)































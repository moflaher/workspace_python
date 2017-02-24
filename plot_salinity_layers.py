from __future__ import division,print_function
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
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import multiprocessing


global name
global grid
global regionname
global region
global tmparray
global savepath
global data
global cmin
global cmax
global vectorflag
global uniformvectorflag
global coastflag
global vidx
global vector_scale



# Define names and types of data
name='sfm5m_sjr_baroclinic_20150615-20150905'
grid='sfm5m_sjr'
datatype='2d'
regionname='stjohn_harbour'
starttime=120
endtime=288
spacing=1
cmin=0
cmax=28


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data,trifinder=False,uvhset=False)
print('done sort')

vectorflag=True
coastflag=True
uniformvectorflag=False
vector_spacing=500
vector_scale=150

#vector_spacing=600
#vector_scale=150

#vector_spacing=75
#vector_scale=1250

#vector_spacing=125
#vector_scale=750

cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
if np.shape(cages)!=():
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.2
    ls='solid'


region=regions(regionname)
#region={}
#region['regionname']='kelpfield_rightisland'
#region['region']=np.array([-129.46,-129.48,52.640,52.665])
vidx=equal_vectors(data,region,vector_spacing)


savepath='figures/timeseries/' + grid + '_' + datatype + '/salinity_layers/' + name + '_' + region['regionname'] + '_' +("%f" %cmin) + '_' + ("%f" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)


def speed_plot(i):
    print(i) 
    
    f,ax=place_axes(region,2)  
    triax0=ax[0].tripcolor(data['trigrid'],data['salinity'][i,0,:],vmin=cmin,vmax=cmax)
    triax1=ax[1].tripcolor(data['trigrid'],data['salinity'][i,-1,:],vmin=cmin,vmax=cmax)
    ppll_sub(ax,setregion=region,cb=triax0,cblabel=r'Salinity',llfontsize=10,fontsize=8,cblabelsize=6,cbticksize=6,cbtickrotation=-45)
    ABC=['A','B']
    figW, figH = f.get_size_inches()
    f.canvas.draw()    

    Q0=ax[0].quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],data['u'][i,0,vidx],data['v'][i,0,vidx],angles='xy',scale_units='xy',scale=vector_scale,zorder=100,width=.0025)    
    Q1=ax[1].quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],data['u'][i,-1,vidx],data['v'][i,-1,vidx],angles='xy',scale_units='xy',scale=vector_scale,zorder=100,width=.0025)    


    for j,axi in enumerate(ax):
        if coastflag:
            plotcoast(ax[j],filename='mid_nwatl6c_sjh_lr.nc',color='k',fill=True,lw=.5,zorder=100)
        axbb=ax[j].get_axes().get_position().bounds
        ax[j].annotate(ABC[j],xy=(axbb[0]+.0075,axbb[1]+axbb[3]-.03),xycoords='figure fraction')
        sand=np.argwhere(data['wet_cells'][i,:]==0)
        tmparray=[list(zip(data['nodell'][data['nv'][k,[0,1,2]],0],data['nodell'][data['nv'][k,[0,1,2]],1])) for k in sand ]
        lseg_sand=PC(tmparray,facecolor = 'tan',edgecolor='tan')
        ax[j].add_collection(lseg_sand) 

           
    f.savefig(savepath + grid + '_' + region['regionname'] +'_salinity_' + ("%04d" %(i)) + '.png',dpi=150)
    plt.close(f)



pool = multiprocessing.Pool(20)
pool.map(speed_plot,range(starttime,endtime,spacing))































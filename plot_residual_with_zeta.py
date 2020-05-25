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
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
sys.path.append('/home/moe46/Desktop/school/workspace_python/ttide_py/ttide/')
sys.path.append('/home/moflaher/Desktop/workspace_python/ttide_py/ttide/')
from t_tide import t_tide
from t_predic import t_predic
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import multiprocessing

# Define names and types of data
name='2012-02-01_2012-03-01_0.01_0.001'
grid='vh_high'

regionname='secondnarrows'
starttime=0
endtime=1000
cmin=0
cmax=0.5


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

vectorflag=False
coastflag=True
uniformvectorflag=True
#vector_spacing=125
#vector_scale=750
vector_spacing=75
vector_scale=1250
zetanode=2500

cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
if np.shape(cages)!=():
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.2
    ls='solid'


region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)
vidx=equal_vectors(data,region,vector_spacing)

savepath='figures/timeseries/' + grid + '_'  + '/residual_with_zeta/' + name + '_' + regionname + '_' +("%f" %cmin) + '_' + ("%f" %cmax) + '/'
if not os.path.exists(savepath): os.makedirs(savepath)


uv=np.load('data/ttide/'+grid+'_'+name+'_'+'_uv_all.npy')
uv=uv[()]

resu=np.zeros((data['nele'],len(data['time'][starttime:(endtime+1)])))
resv=np.zeros((data['nele'],len(data['time'][starttime:(endtime+1)])))
for j in range(0,len(eidx)):
    print( ("%d"%j)+"              "+("%f"%(j/len(eidx)*100)))
    i=eidx[j]    
    tp=t_predic(data['time'][starttime:(endtime+1)],uv['nameu'],uv['freq'],uv['tidecon'][i,:,:])
    resu[i,:]=data['ua'][starttime:(endtime+1),i]-np.real(tp).flatten()
    resv[i,:]=data['va'][starttime:(endtime+1),i]-np.imag(tp).flatten()


ymax=np.max(data['zeta'][starttime:endtime,nidx[zetanode]])
ymin=np.min(data['zeta'][starttime:endtime,nidx[zetanode]])


def res_plot(i):
    print(i)
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],np.sqrt(resu[:,i]**2+resv[:,i]**2),vmin=cmin,vmax=cmax)
    if coastflag==True:
        plotcoast(ax,filename='pacific_harbour.nc',color='None', fcolor='darkgreen', fill=True)
    if np.shape(cages)!=():   
        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        ax.add_collection(lseg_t) 
    if vectorflag==True:
        Q1=ax.quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],resu[vidx,i],resv[vidx,i],angles='xy',scale_units='xy',scale=vector_scale,zorder=100,width=.0025)    
    if uniformvectorflag==True:
        norm=np.sqrt(resu[vidx,i]**2+resv[vidx,i]**2)
        Q1=ax.quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],np.divide(resu[vidx,i],norm),np.divide(resv[vidx,i],norm),angles='xy',scale_units='xy',scale=vector_scale,zorder=100,width=.002,color='k') 
    prettyplot_ll(ax,setregion=region,cblabel=r'Residual (ms$^{-1}$)',cb=triax)
    
    #ax1=plt.axes([.125,.675,.675,.2])
    ax1=plt.axes([.125,.545,.675,.2])
    ax1.plot(data['time'][starttime:i]-data['time'][starttime],data['zeta'][starttime:i,nidx[zetanode]])
    ax1.set_ylabel(r'Elevation (m)')
    ax1.set_xlabel(r'Time (days)')
    ax1.xaxis.set_tick_params(labeltop='on',labelbottom='off')
    ax1.axis([data['time'][starttime]-data['time'][starttime],data['time'][endtime]-data['time'][starttime],ymin,ymax])
    _formatter = mpl.ticker.ScalarFormatter(useOffset=False)
    ax1.yaxis.set_major_formatter(_formatter)
    ax1.xaxis.set_major_formatter(_formatter)
    ax1.xaxis.set_label_coords(0.5, 1.4) 
    
    
    
    f.savefig(savepath + grid + '_' + region['regionname'] +'_residual_' + ("%04d" %(i)) + '.png',dpi=150)
    plt.close(f)



pool = multiprocessing.Pool(2)
pool.map(res_plot,range(starttime,endtime))



























from __future__ import division,print_function
import matplotlib as mpl
mpl.use('Agg')
import scipy as sp
from folderpath import *
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import multiprocessing
import pymp
import seawater as sw



# Define names and types of data
name='sjh_lr_v1_sub_fit_N4_test_nest'
grid='sjh_lr_v1_sub'

regionname='sfmwhole'
starttime=1000
endtime=1025
layer=0
cmin=0
cmax=2
field='speed'

coastflag=True
vectorflag=False
uniformvectorflag=False
vector_spacing=800
vector_scale=100


### load the .nc file #####
data = loadnc('/home/suh001/scratch/{}/runs/{}/output/'.format(grid,name),singlename=grid + '_0001.nc')
print('done load')

if endtime==-1:
    endtime=len(data['time'])
    print('Plotting {} timesteps'.format(endtime-starttime))
region=regions(regionname)
#region['region']=np.array([1.5,2.5,1.9,2.1])
vidx=equal_vectors(data,region,vector_spacing)

savepath='{}timeseries/{}/{}/{}/{}_{}_{:.4f}_{:.4f}/'.format(figpath,grid,field,name,region['regionname'],layer,cmin,cmax)
if not os.path.exists(savepath): os.makedirs(savepath)



def plot_fun(i):
    print(i)
    
    fieldout, fieldname = select_field(data, field, i, layer) 

    f=plt.figure(figsize=region['figsize'])
    ax=f.add_axes(region['axes'])    
    if coastflag:
        plotcoast(ax,filename=region['coast'], filepath=coastpath, color='k', fill=True)   
    
    triax=ax.tripcolor(data['trigrid'],fieldout,vmin=cmin,vmax=cmax)    
    
    if vectorflag:
        Q1=ax.quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],data['ua'][i,vidx],data['va'][i,vidx],angles='xy',scale_units='xy',scale=vector_scale,zorder=100,width=.001)    
        qaxk=ax.quiverkey(Q1,.775,.9,.5, r'.5 ms$^{-1}$')
    if uniformvectorflag:
        norm=np.sqrt(data['u'][i,layer,vidx]**2+data['v'][i,layer,vidx]**2)
        Q1=ax.quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],np.divide(data['u'][i,layer,vidx],norm),np.divide(data['v'][i,layer,vidx],norm),angles='xy',scale_units='xy',scale=vector_scale,zorder=100,width=.002,color='k')  
    
    cb=plt.colorbar(triax)
    cb.set_label(fieldname,fontsize=10)    
    ax.set_xlabel(r'Longitude ($^{\circ}$)')
    ax.set_ylabel(r'Latitude ($^{\circ}$)')
    ax.axis(region['region'])
    #ax.annotate('{} {}'.format(data['Time'][i][:10],data['Time'][i][11:19]),xy=region['textloc'],xycoords='axes fraction')
    for label in ax.get_xticklabels()[::2]:
        label.set_visible(False)
    f.savefig('{}{}_{}_{}_{}_{:05d}.png'.format(savepath,grid,name,region['regionname'],field,i),dpi=300)
    plt.close(f)



for i in range(starttime,endtime):
    plot_fun(i)

#pool = multiprocessing.Pool(30)
#pool.map(plot_fun,range(starttime,endtime))

#with pymp.Parallel(4) as p:
    #for i in p.range(starttime,endtime):
        #plot_fun(i)





























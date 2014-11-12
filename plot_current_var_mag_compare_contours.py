from __future__ import division
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
import time
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC

# Define names and types of data
name_orig='kit4_45days_3'
name_change='kit4_kelp_20m_0.018'
grid='kit4'
datatype='2d'
regionname='kit4_kelp_tight5'
starttime=384

cbfix=True


### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name_orig+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('runs/'+grid+'/'+name_change+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'





cages=np.genfromtxt('runs/'+grid+'/' +name_change+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)

region=regions(regionname)
nidx=get_nodes(data,region)
eidx=get_elements(data,region)

#PC
tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2]],0],data['nodell'][data['nv'][i,[0,1,2]],1])) for i in cages ]
#LC
tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
color='g'
lw=.5
ls='solid'



savepath='figures/png/' + grid + '_' + datatype + '/current_var_mag_subplot_contours/' + name_orig + '_' + name_change + '/'
if not os.path.exists(savepath): os.makedirs(savepath)

start = time.clock()
uvar_o=data['ua'][starttime:,:].var(axis=0)
vvar_o=data['va'][starttime:,:].var(axis=0)
uvar_c=data2['ua'][starttime:,:].var(axis=0)
vvar_c=data2['va'][starttime:,:].var(axis=0)

cvarm_o=np.sqrt(uvar_o+vvar_o)
cvarm_c=np.sqrt(uvar_c+vvar_c)

cvarm_diff=cvarm_c-cvarm_o
cvarm_diff_rel=np.divide(cvarm_diff,cvarm_o)*100

print ('calc current mag: %f' % (time.clock() - start))


ngridx = 1000
ngridy = 1000


start = time.clock()
xi = np.linspace(region['region'][0],region['region'][1], ngridx)
yi = np.linspace(region['region'][2],region['region'][3], ngridy)
cvarm_o_interp=mpl.mlab.griddata(data['uvnodell'][:,0],data['uvnodell'][:,1], cvarm_o, xi, yi)
cvarm_diff_rel_interp=mpl.mlab.griddata(data['uvnodell'][:,0],data['uvnodell'][:,1], cvarm_diff_rel, xi, yi)

tmpxy=np.meshgrid(xi,yi)
xii=tmpxy[0]
yii=tmpxy[1]
host=data['trigrid'].get_trifinder().__call__(xii,yii)

cvarm_o_interp_mask = np.ma.masked_where(host==-1,cvarm_o_interp)
cvarm_diff_rel_interp_mask = np.ma.masked_where(host==-1,cvarm_diff_rel_interp)

print ('griddata interp: %f' % (time.clock() - start))



f=plt.figure()

xtarget=.4
ytarget=.675

aspect=get_aspectratio(region)
dr=get_data_ratio(region)
figW, figH = f.get_size_inches()
fa = figH / figW

if aspect>=1.1:    
    finalspace=((ytarget*fa)/aspect/dr)
    if finalspace>.4:
        finalspace[0]=.4
        ax0f=[.125,.25,finalspace[0],ytarget]
        ax1f=[ax0f[0]+finalspace[0]+.025,.25,finalspace[0],ytarget]
    else:
        ax0f=[.125,.25,1,ytarget]
        ax1f=[ax0f[0]+finalspace[0]+.025,.25,1,ytarget]
else:    
    finalspace=((((xtarget*fa)/aspect/dr)*aspect*dr)/fa)
    #ax1f=[.125,.1,.75,xtarget]
    #ax0f=[.125,ax1f[1]+finalspace[0]+.05,.75,xtarget]
    #finalspace=((ytarget*fa)/aspect/dr)
    ax1f=[.125,.1,1,xtarget]
    ax0f=[.125,ax1f[1]+finalspace[0]+.025,1,xtarget]




ax0=f.add_axes(ax0f)
ax1=f.add_axes(ax1f)



if cbfix==True:
    #V=np.array([-80,-70,-60,-50,-40,-30,-20,-10,0,5,10,15,20])
    V=np.array([-80,-60,-40,-20,0,5,10,15,20])
    CS1=ax0.contour(xi,yi,cvarm_o_interp_mask,colors='k',zorder=30)
    CS2=ax1.contour(xi,yi,cvarm_diff_rel_interp_mask,V,colors='k',zorder=30)
    ax0.clabel(CS1, fontsize=9, inline=1,zorder=30)
    ax1.clabel(CS2, fontsize=9, inline=1,zorder=30)
else:
    CS1=ax0.contour(xi,yi,cvarm_o_interp_mask,colors='k',zorder=30)
    CS2=ax1.contour(xi,yi,cvarm_diff_rel_interp_mask,colors='k',zorder=30)
    ax0.clabel(CS1, fontsize=9, inline=1,zorder=30)
    ax1.clabel(CS2, fontsize=9, inline=1,zorder=30)


prettyplot_ll(ax0,setregion=region)
prettyplot_ll(ax1,setregion=region)
ax_label_spacer(ax0)
ax_label_spacer(ax1)


if aspect>=1.1:
    ax1.yaxis.set_tick_params(labelleft='off')
else:
    ax0.xaxis.set_tick_params(labelleft='off')
    ax0.set_xlabel('')


plotcoast(ax0,filename='pacific.nc',color='r')
plotcoast(ax1,filename='pacific.nc',color='r')


lseg0=PC(tmparray,facecolor = 'g',edgecolor='None')
lseg0=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
ax0.add_collection(lseg0)
lseg1=PC(tmparray,facecolor = 'g',edgecolor='None')
lseg1=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
ax1.add_collection(lseg1)


ax0.annotate("A",xy=(.025,1-(.05/dr)),xycoords='axes fraction')
ax1.annotate("B",xy=(.025,1-(.05/dr)),xycoords='axes fraction')

#plotcoast(ax0,filename='pacific.nc',color='k')
#plotcoast(ax1,filename='pacific.nc',color='k')

f.savefig(savepath + grid + '_' + regionname+'_current_variance_magnitude_diff_relative_subplot_contour.png',dpi=600)
#plt.close(f)












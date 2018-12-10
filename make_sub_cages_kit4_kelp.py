from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import time
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import matplotlib.path as path

# Define names and types of data
name='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'





### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

cages=loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
if np.shape(cages)!=():
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.1
    ls='solid'


def plot_kelp(data,cages,filename):
    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2]],0],data['nodell'][data['nv'][i,[0,1,2]],1])) for i in cages ]
    seg=PC(tmparray,facecolor = 'g',edgecolor='None')
    
    f=plt.figure()

    ax=f.add_axes([.125,.1,.775,.8])
    ax.add_collection(seg)
    ax.triplot(data['trigrid'],color='k',lw=.25)
    prettyplot_ll(ax,setregion=region)
    plotcoast(ax,color='None',fill=True)
    
    f.savefig(filename,dpi=600)
    plt.close(f)


#this region contains all the highres grid
region={}
region['region']=np.array([-129.615566168,-129.215178942,52.44600635,52.83665705])

#get the kelp excluding the high res area
eidx=get_elements(data,region)
nohighres=cages[~np.in1d(cages,eidx)]


#kit4_kelp_tight2 east region
region['region']=np.array([-129.514803056,-129.463767195,52.6104051862,52.6771413475])

#get kelp in region and add to no kelp in high res
eidx=get_elements(data,region)
addcages=cages[np.in1d(cages,eidx)]
newcage1=np.unique(np.sort(np.append(nohighres,addcages)))

#add depth and drag and save cage file
depth=np.zeros((len(newcage1),))+40
drag=np.zeros((len(newcage1),))+0.018
fvcom_savecage('data/cage_files/'+grid+'_cage_kelpfield1.dat',newcage1+1,drag,depth)

#plot the area
plot_kelp(data,newcage1,'data/cage_files/kelpfield1.png')


#kit4_kelp_tight2 west region
region['region']=np.array([-129.460713767,-129.38365107,52.6218895934,52.7132222802])

#get kelp in region and add to no kelp in high res
eidx=get_elements(data,region)
addcages=cages[np.in1d(cages,eidx)]
newcage2=np.unique(np.sort(np.append(newcage1,addcages)))

#add depth and drag and save cage file
depth=np.zeros((len(newcage2),))+40
drag=np.zeros((len(newcage2),))+0.018
fvcom_savecage('data/cage_files/'+grid+'_cage_kelpfield2.dat',newcage2+1,drag,depth)

plot_kelp(data,newcage2,'data/cage_files/kelpfield2.png')


#kit4_kelp_tight5 region
region['region']=np.array([-129.465075806,-129.372164366,52.5021623881,52.6047081969])

#get kelp in region and add to no kelp in high res
eidx=get_elements(data,region)
addcages=cages[np.in1d(cages,eidx)]
newcage3=np.unique(np.sort(np.append(newcage2,addcages)))

#add depth and drag and save cage file
depth=np.zeros((len(newcage3),))+40
drag=np.zeros((len(newcage3),))+0.018
fvcom_savecage('data/cage_files/'+grid+'_cage_kelpfield3.dat',newcage3+1,drag,depth)

plot_kelp(data,newcage3,'data/cage_files/kelpfield3.png')

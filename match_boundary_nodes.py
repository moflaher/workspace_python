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
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
import netCDF4 as n4





# Define names and types of data
name='2011-08-25_2011-09-08_0.0025'
grid='acadia_force_2d'


###load old grid stuff
data = loadnc('runs_acadia/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')
indata=load_fvcom_files('runs_acadia/'+grid+'/'+name+'/input',grid,grid+'_spectide.nc')
indata['nodell']=data['nodell']



###load new grid stuff
#name2='vhhigh_v3_clean_hpc'
grid2='sjh_hr_v1'



#indata2=load_fvcom_files('runs/'+grid2+'/'+name2+'/input',grid2)
#neifile=load_neifile('runs/'+grid2+'/'+name2+'/input/'+grid2+'.nei')
indata2=load_fvcom_files('/home/moe46/Desktop/dfo/data/misc/bathymetry/sj_harbour/redepth_folder/sjh_hr/makerun_1/sjh_hr_v1/input/',grid2)
neifile=load_neifile('/home/moe46/Desktop/dfo/data/misc/bathymetry/sj_harbour/redepth_folder/sjh_hr/makerun_1/sjh_hr_v1/input/'+grid2+'.nei')
indata2.update(neifile)
indata2=ncdatasort(indata2)

newbnodes=np.empty((len(indata['spgf_nodes']),1),dtype=int)

#have to minus 1 from spgf_nodes to account for python indexing
for i in range(0,len(indata['spgf_nodes'])):
    newbnodes[i]=np.argmin( (indata2['nodell'][:,0]-indata['nodell'][indata['spgf_nodes'][i]-1,0])**2+(indata2['nodell'][:,1]-indata['nodell'][indata['spgf_nodes'][i]-1,1])**2)



import copy
indatasave=copy.deepcopy(indata)
#have to add 1 to new spgf_nodes to account for python indexing
indatasave['spgf_nodes']=newbnodes+1
indatasave['obcf_nodes']=newbnodes+1




save_spgfile(indatasave,'data/grid_stuff/',grid2)
save_obcfile(indatasave,'data/grid_stuff/',grid2)


#new ncfile name
ncid = n4.Dataset('data/grid_stuff/'+grid2+'_spectide.nc', 'r+',format='NETCDF3_CLASSIC')
ncid.variables['obc_nodes'][:]=newbnodes+1
ncid.close()


f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.scatter(indata2['nodell'][:,0],indata2['nodell'][:,1],s=1,c='b',edgecolor='None')
ax.scatter(indata2['nodell'][newbnodes,0],indata2['nodell'][newbnodes,1],s=15,c='r',edgecolor='None')
f.show()

f=plt.figure()
ax=f.add_axes([.125,.1,.775,.8])
ax.scatter(indata['nodell'][:,0],indata['nodell'][:,1],s=1,c='b',edgecolor='None')
ax.scatter(indata['nodell'][(indata['spgf_nodes']-1).astype(int),0],indata['nodell'][(indata['spgf_nodes']-1).astype(int),1],s=15,c='r',edgecolor='None')
f.show()









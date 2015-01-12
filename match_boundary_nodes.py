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
import netCDF4 as n4





# Define names and types of data
name='kit4_kelp_20m_0.018'
grid='kit4'
datatype='2d'

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'
indata=load_fvcom_files('runs/'+grid+'/'+name+'/input','kit4','kit4_non_julian_obc.nc')



# Define names and types of data
name2='kit4_kelp_clean'
grid2='kit4_kelp'
datatype='2d'


indata2=load_fvcom_files('runs/'+grid2+'/'+name2+'/input','kit4_kelp')


newbnodes=np.empty((len(indata['spgf_nodes']),1),dtype=int)

#have to minus 1 from spgf_nodes to account for python indexing
for i in range(0,len(indata['spgf_nodes'])):
    newbnodes[i]=np.argmin( (indata2['nodell'][:,0]-data['nodell'][indata['spgf_nodes'][i]-1,0])**2+(indata2['nodell'][:,1]-data['nodell'][indata['spgf_nodes'][i]-1,1])**2)




#have to add 1 to new spgf_nodes to account for python indexing
indata['spgf_nodes']=newbnodes+1
indata['obcf_nodes']=newbnodes+1




save_spgfile(indata,'data/grid_stuff/','kit4_kelp')
save_obcfile(indata,'data/grid_stuff/','kit4_kelp')

ncid = n4.Dataset('data/grid_stuff/kit4_kelp_non_julian_obc.nc', 'r+',format='NETCDF3_CLASSIC')
ncid.variables['obc_nodes'][:]=newbnodes+1
ncid.close()

plt.scatter(indata2['nodell'][:,0],indata2['nodell'][:,1],s=1,c='b',edgecolor='None')
plt.scatter(indata2['nodell'][newbnodes,0],indata2['nodell'][newbnodes,1],s=15,c='r',edgecolor='None')
plt.show()










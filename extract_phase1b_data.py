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
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import multiprocessing
import pymp
import seawater as sw



# Define names and types of data
name='sjh_lr_v1_year_wd_gotm-my25_bathy20171109_dt30_calib1_jcool0_summer'
grid='sjh_lr_v1'

starttime=0
endtime=-1



### load the .nc file #####
data = loadnc('/home/suh001/scratch/sjh_lr_v1/runs/{}/output/'.format(name),singlename=grid + '_0001.nc')
print('done load')
trifinder=data['trigrid'].get_trifinder()
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
data['nodexy']=np.vstack([data['x'],data['y']]).T

savepath='{}{}_{}/phase1b/{}/'.format(datapath,grid,datatype,name)
if not os.path.exists(savepath): os.makedirs(savepath)



time=data['Time']


##single node
node=48549

temp=data['temp'][:,:,node]
sal=data['salinity'][:,:,node]
zeta=data['zeta'][:,node]

save_array(time,'{}{}_time.dat'.format(savepath,name))
save_array(temp,'{}{}_temperature_{}.dat'.format(savepath,name,node))
save_array(sal,'{}{}_salinity_{}.dat'.format(savepath,name,node))
save_array(zeta,'{}{}_zeta_{}.dat'.format(savepath,name,node))
#save_array(np.array(data['h'][node]),'{}{}_h_{}.dat'.format(savepath,name,node))
print(data['h'][node])

##spec lines

line1=np.genfromtxt('data/nemofvcom/line1.ll')
line2=np.genfromtxt('data/nemofvcom/line2.ll')

lines=np.vstack([line1,line2])

zetaline=np.empty((len(lines),len(time)))
templine=np.empty((len(lines),len(time)))
salline=np.empty((len(lines),len(time)))
uline=np.empty((len(lines),len(time)))
vline=np.empty((len(lines),len(time)))

#sl=np.array([])
#hosts=np.array([])
for i in range(len(lines)):
    print(i/(len(lines)*1.))
    #host=trifinder(lines[i,0],lines[i,1])
    #hosts=np.append(host,hosts)
    #for j in range(3):
    #    sl=np.append(np.sqrt((data['nodexy'][data['nv'][host,j-1],0]-data['nodexy'][data['nv'][host,j],0])**2+(data['nodexy'][data['nv'][host,j-1],1]-data['nodexy'][data['nv'][host,j],1])**2),sl)
         
    zetaline[i,:]=ipt.interpN_at_loc(data,'zeta',lines[i,:])
    templine[i,:]=ipt.interpN_at_loc(data,'temp',lines[i,:],layer=0)
    salline[i,:]=ipt.interpN_at_loc(data,'salinity',lines[i,:],layer=0)
    uline[i,:]=ipt.interpE_at_loc(data,'u',lines[i,:],layer=0)
    vline[i,:]=ipt.interpE_at_loc(data,'v',lines[i,:],layer=0)


save_array(zetaline[:len(line1),],'{}{}_zeta_{}.dat'.format(savepath,name,'line1'))
save_array(zetaline[len(line1):,],'{}{}_zeta_{}.dat'.format(savepath,name,'line2'))
save_array(templine[:len(line1),],'{}{}_temperature_{}.dat'.format(savepath,name,'line1'))
save_array(templine[len(line1):,],'{}{}_temperature_{}.dat'.format(savepath,name,'line2'))
save_array(salline[:len(line1),],'{}{}_salinity_{}.dat'.format(savepath,name,'line1'))
save_array(salline[len(line1):,],'{}{}_salinity_{}.dat'.format(savepath,name,'line2'))
save_array(uline[:len(line1),],'{}{}_usurf_{}.dat'.format(savepath,name,'line1'))
save_array(uline[len(line1):,],'{}{}_usurf_{}.dat'.format(savepath,name,'line2'))
save_array(vline[:len(line1),],'{}{}_vsurf_{}.dat'.format(savepath,name,'line1'))
save_array(vline[len(line1):,],'{}{}_vsurf_{}.dat'.format(savepath,name,'line2'))


cross1=np.genfromtxt('data/nemofvcom/river_cross_section_hor.ll')
cross2=np.genfromtxt('data/nemofvcom/river_cross_section_perp.ll')

cross=np.vstack([cross1,cross2])

zetacross=np.empty((len(cross),len(time)))
uacross=np.empty((len(cross),len(time)))
vacross=np.empty((len(cross),len(time)))
hcross=np.empty((len(cross),len(time)))

for i in range(len(cross)):
    print(i/(len(cross)*1.))
    hcross[i,:]=ipt.interpN_at_loc(data,'h',cross[i,:])
    zetacross[i,:]=ipt.interpN_at_loc(data,'zeta',cross[i,:])
    uacross[i,:]=ipt.interpE_at_loc(data,'ua',cross[i,:])
    vacross[i,:]=ipt.interpE_at_loc(data,'va',cross[i,:])    
    

save_array(hcross[:len(cross1),],'{}{}_h_{}.dat'.format(savepath,name,'cross_hor'))
save_array(hcross[len(cross1):,],'{}{}_h_{}.dat'.format(savepath,name,'cross_perp'))
save_array(zetacross[:len(cross1),],'{}{}_zeta_{}.dat'.format(savepath,name,'cross_hor'))
save_array(zetacross[len(cross1):,],'{}{}_zeta_{}.dat'.format(savepath,name,'cross_perp'))
save_array(uacross[:len(cross1),],'{}{}_ua_{}.dat'.format(savepath,name,'cross_hor'))
save_array(uacross[len(cross1):,],'{}{}_ua_{}.dat'.format(savepath,name,'cross_perp'))
save_array(vacross[:len(cross1),],'{}{}_va_{}.dat'.format(savepath,name,'cross_hor'))
save_array(vacross[len(cross1):,],'{}{}_va_{}.dat'.format(savepath,name,'cross_perp')) 
    
    

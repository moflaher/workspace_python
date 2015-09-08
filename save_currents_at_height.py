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


# Define names and types of data
name='kit4_45days_3'
grid='kit4'
regionname='kit4_area4'
datatype='2d'
starttime=384
spacing=500
interpheight=1

### load the .nc file #####
data = loadnc('/media/moflaher/My Book/kit4_runs/' + name + '/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')


region=regions(regionname)
eidx=get_elements(data,region)
sidx=equal_vectors(data,region,spacing)

savepath='figures/png/' + grid + '_' + datatype + '/currents_' + ("%d" %interpheight)+ 'm/'
if not os.path.exists(savepath): os.makedirs(savepath)

base_dir = os.path.dirname(__file__)
filename='_' + grid + '_' +name+ '_' + ("%d" %interpheight) + 'm.npy'
if (os.path.exists(os.path.join(base_dir,'data', 'u' + filename)) & os.path.exists(os.path.join(base_dir,'data', 'v' + filename))):
    print 'Loading old interpolated currents'
    newu=np.load(os.path.join(base_dir,'data', 'u' + filename))
    newv=np.load(os.path.join(base_dir,'data', 'v' + filename))
    print 'Loaded old interpolated currents'
else:
    print 'Interpolate currents first'
    sys.exit(0)






zeta_grad=np.gradient(data['zeta'][starttime:,:])[0]


#find biggest fld and save
hour=np.argmax(np.sum(zeta_grad>0,axis=1))

#save data
usave=newu[hour,eidx]
vsave=newv[hour,eidx]
lonsave=data['uvnodell'][eidx,0]
latsave=data['uvnodell'][eidx,1]


filename2='' +grid + '_' +name+ '_' +regionname +'_' + ("%d" %interpheight) + 'm_time_' +("%d" %(hour+starttime))+ '.dat'
fp=open(os.path.join(base_dir,'data', filename2),'w')
for i in range(0,len(usave)):
        fp.write('%f %f %f %f\n' % (lonsave[i],latsave[i],usave[i],vsave[i]) )
fp.close()

#find biggest ebb and save
hour=np.argmax(np.sum(zeta_grad<0,axis=1))

#save data
usave=newu[hour,eidx]
vsave=newv[hour,eidx]

filename2='' +grid + '_' +name+ '_' +regionname +'_' + ("%d" %interpheight) + 'm_time_'+ ("%d"%(hour+starttime)) +'.dat'
fp=open(os.path.join(base_dir,'data', filename2),'w')
for i in range(0,len(usave)):
        fp.write('%f %f %f %f\n' % (lonsave[i],latsave[i],usave[i],vsave[i]) )
fp.close()






#find biggest current and save
hour=np.argmax(np.sum(zeta_grad<0,axis=1))

#save data
tspeed=np.argmax(np.sqrt(newu**2+newv**2),axis=0)
usavet=newu[tspeed,range(0,data['nele'])]
vsavet=newv[tspeed,range(0,data['nele'])]
usave=usavet[eidx]
vsave=vsavet[eidx]

filename2='' +grid + '_' +name+ '_' +regionname +'_' + ("%d" %interpheight) + 'm_max_currents.dat'
fp=open(os.path.join(base_dir,'data', filename2),'w')
for i in range(0,len(usave)):
        fp.write('%f %f %f %f\n' % (lonsave[i],latsave[i],usave[i],vsave[i]) )
fp.close()
















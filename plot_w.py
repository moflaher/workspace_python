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


# Define names and types of data
name='kit4_45days_3'
grid='kit4'
regionname='doubleisland'
datatype='2d'
starttime=384
level=19


### load the .nc file #####
data = loadnc('/media/moe46/My Passport/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

region=regions(regionname)

savepath='figures/png/' + grid + '_' + datatype + '/w/' + name + '_' + regionname +'/'
if not os.path.exists(savepath): os.makedirs(savepath)



nidx=get_nodes(data,region)
eidx=get_elements(data,region)

zeta_grad=np.gradient(data['zeta'][starttime:,nidx])[0]
fld=np.argmax(np.sum(zeta_grad>1,axis=1))
ebb=np.argmax(np.sum(zeta_grad<1,axis=1))



f=plt.figure()

ax_fld=f.add_axes([.125,.1,.8,.85])
triax=ax_fld.tripcolor(data['trigrid'],data['ww'][starttime+fld,level,:],vmin=data['ww'][starttime+fld,level,eidx].min(),vmax=data['ww'][starttime+fld,level,eidx].max())

prettyplot_ll(ax_fld,setregion=region,cblabel=r'W (ms$^{-1}$)',cb=triax)
plotcoast(ax_fld,filename='pacific.nc',color='k')

f.savefig(savepath + grid + '_fld_w_at_' + ("%04d" %(starttime+fld)) + '.png',dpi=600)
plt.close(f)




f=plt.figure()
ax_ebb=f.add_axes([.125,.1,.8,.85])
triax=ax_ebb.tripcolor(data['trigrid'],data['ww'][starttime+ebb,level,:],vmin=data['ww'][starttime+ebb,level,eidx].min(),vmax=data['ww'][starttime+ebb,level,eidx].max())

prettyplot_ll(ax_ebb,setregion=region,cblabel=r'W (ms$^{-1}$)',cb=triax)
plotcoast(ax_ebb,filename='pacific.nc',color='k')

f.savefig(savepath + grid + '_ebb_w_at_' + ("%04d" %(starttime+ebb)) + '.png',dpi=600)
plt.close(f)






















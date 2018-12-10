from __future__ import division,print_function
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import scipy.io as sio
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
from StringIO import StringIO
from gridtools import *
from datatools import *
from misctools import *
from plottools import *
from projtools import *
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)


# Define names and types of data
name='kit4_baroclinic'
grid='kit4'
regionname='kit4_area5'

starttime=384
interpheight=1

### load the .nc file #####
data = loadnc('runs/'+grid+'/' + name + '/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')


region=regions(regionname)
nidx=get_nodes(data,region)

savepath='figures/png/' + grid + '_'  + '/currents_' + ("%d" %interpheight)+ 'm/'
if not os.path.exists(savepath): os.makedirs(savepath)

print('Loading old interpolated currents')
currents=np.load('data/interp_currents/'+ grid + '_' +name+ '_' + ("%d" %interpheight) + 'm.npy')
currents=currents[()]
print('Loaded old interpolated currents')




testing=False

kl=[.775,.025,.2,.07]
scale1=10
scale2=10
vectorspacing=250
ax_r=[.125,.1,.775,.8]
ebbfldscale=r'0.1'
resscale='0.25'
ABC=[.05,.925]
fcolor='b'
arrowshift1=.13








eidx=equal_vectors(data,region,vectorspacing)



zeta_grad=np.gradient(data['zeta'][starttime:,nidx])[0]
fld=np.argmax(np.sum(zeta_grad,axis=1))
ebb=np.argmin(np.sum(zeta_grad,axis=1))



f=plt.figure()

ax_fld=f.add_axes(ax_r)

q2u1=newu[fld,eidx]
q2v1=newv[fld,eidx]
triax=ax_fld.tripcolor(data['trigrid'],data['h'],vmin=data['h'][nidx].min(),vmax=data['h'][nidx].max())
Q2=ax_fld.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],q2u1,q2v1,angles='xy',scale_units='xy',scale=scale1,color='k',zorder=10)
prettyplot_ll(ax_fld,setregion=region,cb=triax,cblabel=r'Depth (m)')
plt.draw()
rec=mpl.patches.Rectangle((kl[0],kl[1]),kl[2],kl[3],transform=ax_fld.transAxes,fc='w',zorder=20)
ax_fld.add_patch(rec)
aqk2=ax_fld.quiverkey(Q2,kl[0]+arrowshift1,kl[1]+.03,float(ebbfldscale), ebbfldscale +r'm s$^{-1}$', labelpos='W',fontproperties={'size': 8})
aqk2.set_zorder(30)

plotcoast(ax_fld,filename='pacific.nc',color='k',fill=True)
f.savefig(savepath + grid + '_'+ name+'_'+regionname+'_fld.png',dpi=600)
plt.close(f)



f=plt.figure()

ax_ebb=f.add_axes(ax_r)

q2u1=newu[ebb,eidx]
q2v1=newv[ebb,eidx]
triax=ax_ebb.tripcolor(data['trigrid'],data['h'],vmin=data['h'][nidx].min(),vmax=data['h'][nidx].max())
Q2=ax_ebb.quiver(data['uvnodell'][eidx,0],data['uvnodell'][eidx,1],q2u1,q2v1,angles='xy',scale_units='xy',scale=scale1,color='k',zorder=10)
prettyplot_ll(ax_ebb,setregion=region,cb=triax,cblabel=r'Depth (m)')
plt.draw()
rec=mpl.patches.Rectangle((kl[0],kl[1]),kl[2],kl[3],transform=ax_ebb.transAxes,fc='w',zorder=20)
ax_ebb.add_patch(rec)
aqk2=ax_ebb.quiverkey(Q2,kl[0]+arrowshift1,kl[1]+.03,float(ebbfldscale), ebbfldscale +r'm s$^{-1}$', labelpos='W',fontproperties={'size': 8})
aqk2.set_zorder(30)

plotcoast(ax_ebb,filename='pacific.nc',color='k',fill=True)
f.savefig(savepath + grid + '_'+ name+'_'+regionname+'_ebb.png',dpi=600)
plt.close(f)





























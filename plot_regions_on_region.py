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
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)



# Define names and types of data
name='kit4_45days_3'
grid='kit4'
regionname='mostchannels'

regionsub=['kit4_area1','kit4_area2','kit4_area3','kit4_area4']


### load the .nc file #####
data = loadnc('runs/'+grid+'/' + name + '/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')


region=regions(regionname)
savepath='figures/png/' + grid + '_'  + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)


plt.close()
plt.triplot(data['trigrid'],lw=.1)
plt=prettyplot_ll(plt,setregion=region,grid=True)

for i in regionsub:
    tregion=regions(i)
    tpatch=plt.Rectangle((tregion['region'][0],tregion['region'][2]),tregion['region'][1]-tregion['region'][0],tregion['region'][3]-tregion['region'][2],fill=False,lw=2,edgecolor='red')
    plt.gca().add_patch(tpatch)
    plt.text(tregion['region'][0],tregion['region'][2]-.1,tregion['passageP'],fontsize=14,color='red',bbox={'facecolor':'white', 'alpha':0.75, 'pad':3})    


#plt.show()
subregionname=''
for i in regionsub:
    subregionname = subregionname + '_' + i 

plt.savefig(savepath + grid + '_' + regionname +'_with_subregions' +subregionname+ '.png',dpi=1200)

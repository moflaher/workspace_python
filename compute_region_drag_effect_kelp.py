from __future__ import division
import matplotlib as mpl
import scipy as sp
import numpy as np
from datatools import *
from gridtools import *
from plottools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pandas as pd

pd.options.display.float_format = '{:,.3f}'.format


# Define names and types of data
baserun='kit4_45days_3'
dragrunlist=['kit4_kelp_20m_0.018','kit4_kelp_20m_0.011','kit4_kelp_20m_0.007']
grid='kit4'
regionlist=['kit4_crossdouble','kit4_ftb','kit4_kelp_tight2_small','kit4_kelp_tight5','kit4_kelp_tight6']
datatype='2d'
starttime=384
endtime=400
offset=0
cagecolor='r'





### load the .nc file #####
data = loadnc('runs/'+grid+'/'+baserun+'/output/',singlename=grid + '_0001.nc')

dragdata=[]
for i in range(0,len(dragrunlist)):
    print i
    dragdata = dragdata+[loadnc('runs/'+grid+'/'+dragrunlist[i]+'/output/',singlename=grid + '_0001.nc')]

print 'done load'
data = ncdatasort(data)
print 'done sort'




cages=np.genfromtxt('runs/'+grid+'/' +dragrunlist[0]+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)

regionnameout=[]
cageout=np.empty((0))

for i in range(0,len(regionlist)):
    print ("%d"%i)+"              "+("%f"%(i/len(regionlist)*100)) 
    regionname=regionlist[i]
    region=regions(regionname)

    #nidx=get_nodes(data,region)
    eidx=get_elements(data,region)

    #np.in1d is the same as matlab ismember or close
    cageidx=np.in1d(eidx,cages)
    cageidx=eidx[cageidx]

    uvar_b=data['ua'][starttime:,cageidx].var(axis=0)
    vvar_b=data['va'][starttime:,cageidx].var(axis=0)

    uvar_d=np.empty((len(dragrunlist),len(cageidx)))
    vvar_d=np.empty((len(dragrunlist),len(cageidx)))

    for k in range(0,len(dragrunlist)):
        print k
        uvar_d[k,:]=dragdata[k]['ua'][starttime:,cageidx].var(axis=0)
        vvar_d[k,:]=dragdata[k]['va'][starttime:,cageidx].var(axis=0)

    cvarm_b=np.sqrt(uvar_b+vvar_b)
    cvarm_d=np.sqrt(uvar_d+vvar_d)

    cvmb_mean=cvarm_b.mean()
    cvmd_mean=cvarm_d.mean(axis=1)

    stringlist=[]
    cagevalues=cvmb_mean
    for i in range(0,len(dragrunlist)):
        cagevalues=np.append(cagevalues,[cvmd_mean[i],(cvmd_mean[i]-cvmb_mean)/cvmb_mean])
        stringlist=stringlist+[dragrunlist[i]]
        stringlist=stringlist+['<- Rel. Change']  

    regionnameout=regionnameout+[regionname]
    cageout=np.append(cageout,cagevalues)





  
cageout=cageout.reshape(len(regionlist),(len(dragrunlist)*2)+1)

df=pd.DataFrame(cageout,regionnameout,['VarMag Base']+stringlist)

print df

df.to_pickle('data/dragnodrag/dragnodrag_kelp_regions.panda')
df.to_csv('data/dragnodrag/dragnodrag_kelp_regions.csv')



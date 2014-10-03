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
sys.path.append('/home/moe46/Desktop/school/workspace_python/ttide_py/ttide/')
sys.path.append('/home/moflaher/Desktop/workspace_python/ttide_py/ttide/')
from t_tide import t_tide
from t_predic import t_predic
import pandas as pd

pd.options.display.float_format = '{:,.3f}'.format


# Define names and types of data
name='kit4_kelp_20m_0.018'
name2='kit4_45days_3'
grid='kit4'
regionname='kit4_kelp_tight2'
datatype='2d'
starttime=384
endtime=400
offset=0
cagecolor='r'




region=regions(regionname)

### load the .nc file #####
data = loadnc('/media/moflaher/MB_3TB/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data2 = loadnc('/media/moflaher/My Book/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')
#data2 = loadnc('/media/moe46/My Passport/'+grid+'/'+name2+'/output/',singlename=grid + '_0001.nc')
#data = loadnc('/media/moe46/Hardy/spet_18_work/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'




cages=np.genfromtxt('/media/moflaher/MB_3TB/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat',skiprows=1)
#cages=np.genfromtxt('/media/moe46/Hardy/spet_18_work/' +name+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)


#nidx=get_nodes(data,region)
eidx=get_elements(data,region)

#zeta_grad=np.gradient(data['zeta'][starttime:,nidx])[0]
#fld=np.argmax(np.sum(zeta_grad>1,axis=1))
#ebb=np.argmax(np.sum(zeta_grad<1,axis=1))






resu=np.empty((len(eidx),len(data['time'][starttime:])))
resv=np.empty((len(eidx),len(data['time'][starttime:])))
resu2=np.empty((len(eidx),len(data['time'][starttime:])))
resv2=np.empty((len(eidx),len(data['time'][starttime:])))
tideconsave1=np.empty((len(eidx),7,8))
tideconsave2=np.empty((len(eidx),7,8))
for j in range(0,len(eidx)):
    print j
    i=eidx[j]
    [nameu, freq, tidecon_uv, xout]=t_tide(data['ua'][starttime:,i]+1j*data['va'][starttime:,i],lat=data['uvnodell'][i,1],output=False,constitnames=np.array([['M2  '],['N2  '],['S2  '],['K1  '],['O1  '],['M4  '],['M6  ']]))
    resu[j,:]=data['ua'][starttime:,i]-np.real(t_predic(data['time'][starttime:],nameu,freq,tidecon_uv)).flatten()
    resv[j,:]=data['va'][starttime:,i]-np.imag(t_predic(data['time'][starttime:],nameu,freq,tidecon_uv)).flatten()
    tideconsave1[j,]=tidecon_uv

    [nameu, freq, tidecon_uv, xout]=t_tide(data2['ua'][starttime:,i]+1j*data2['va'][starttime:,i],lat=data['uvnodell'][i,1],output=False,constitnames=np.array([['M2  '],['N2  '],['S2  '],['K1  '],['O1  '],['M4  '],['M6  ']]))
    resu2[j,:]=data2['ua'][(starttime+offset):,i]-np.real(t_predic(data2['time'][(starttime+offset):],nameu,freq,tidecon_uv)).flatten()
    resv2[j,:]=data2['va'][(starttime+offset):,i]-np.imag(t_predic(data2['time'][(starttime+offset):],nameu,freq,tidecon_uv)).flatten()
    tideconsave2[j,]=tidecon_uv


#np.in1d is the same as matlab ismember or close
cageidx=np.in1d(eidx,cages)



tidecon_cages=np.divide(tideconsave1[cageidx,:,:],tideconsave2[cageidx,:,:])
tidecon_nocages=np.divide(tideconsave1[~cageidx,:,:],tideconsave2[~cageidx,:,:])



uvar_o=data2['ua'][starttime:,eidx].var(axis=0)
vvar_o=data2['va'][starttime:,eidx].var(axis=0)
uvar_c=data['ua'][starttime:,eidx].var(axis=0)
vvar_c=data['va'][starttime:,eidx].var(axis=0)

cvarm_o=np.sqrt(uvar_o+vvar_o)
cvarm_c=np.sqrt(uvar_c+vvar_c)


cvarm_cages=np.divide(cvarm_c[cageidx],cvarm_o[cageidx])
cvarm_nocages=np.divide(cvarm_c[~cageidx],cvarm_o[~cageidx])


tcc_mean=tidecon_cages.mean(axis=0)
tcnc_mean=tidecon_nocages.mean(axis=0)
cvmc_mean=cvarm_cages.mean()
cvmnc_mean=cvarm_nocages.mean()

cages_values=np.hstack([cvmc_mean,tcc_mean[:,0]])
nocages_values=np.hstack([cvmnc_mean,tcnc_mean[:,0]])



df=pd.DataFrame(np.vstack([cages_values, nocages_values]),['Cages','No Cages'],['VarMag']+[nameu[i].encode('ascii') for i in range(0,len(nameu))])

print df

df.to_pickle('data/cagenocage' + regionname +'.panda')



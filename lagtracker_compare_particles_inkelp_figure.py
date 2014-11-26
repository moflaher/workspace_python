from __future__ import division
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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import h5py as h5
from matplotlib.collections import PolyCollection as PC



# Define names and types of data
name='kit4_45days_3'
name2='kit4_kelp_20m_0.018'
grid='kit4'
regionname='kit4_kelp_tight2_kelpfield'
datatype='2d'
lname='element_80185_s0'
lname2='element_80185_s3'
lname3='element_80185_s6'
#averaging length (breaks code if zero). N=1 for original data
N=150
plotend=2

### load the .nc file #####
data = loadnc('runs/'+grid+'/' + name +'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'

savepath='figures/png/' + grid + '_' + datatype + '/lagtracker/particles_inkelp/' + name + '_'+name2+'/'
if not os.path.exists(savepath): os.makedirs(savepath)

data['trigridxy'] = mplt.Triangulation(data['x'], data['y'],data['nv'])
region=regions(regionname)
region=regionll2xy(data,region)
eidx=get_elements(data,region)


if 'savelag1' not in globals():
    print "Loading savelag1"
    fileload=h5.File('savedir/'+name+'/'+lname+'.mat')
    savelag1={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag1[i]=fileload['savelag'][i].value.T

if 'savelag2' not in globals():
    print "Loading savelag2"
    fileload=h5.File('savedir/'+name2+'/'+lname+'.mat')
    savelag2={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag2[i]=fileload['savelag'][i].value.T

if 'savelag3' not in globals():
    print "Loading savelag3"
    fileload=h5.File('savedir/'+name+'/'+lname2+'.mat')
    savelag3={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag3[i]=fileload['savelag'][i].value.T

if 'savelag4' not in globals():
    print "Loading savelag4"
    fileload=h5.File('savedir/'+name2+'/'+lname2+'.mat')
    savelag4={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag4[i]=fileload['savelag'][i].value.T

if 'savelag5' not in globals():
    print "Loading savelag5"
    fileload=h5.File('savedir/'+name+'/'+lname3+'.mat')
    savelag5={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag3[i]=fileload['savelag'][i].value.T

if 'savelag6' not in globals():
    print "Loading savelag6"
    fileload=h5.File('savedir/'+name2+'/'+lname3+'.mat')
    savelag6={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag4[i]=fileload['savelag'][i].value.T



cages=np.genfromtxt('runs/'+grid+'/' +name2+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)
#comment out this line for any kelp not just kelp in the start box
cages=eidx[np.in1d(eidx,cages)]
tmparray=[list(zip(data['nodexy'][data['nv'][i,[0,1,2]],0],data['nodexy'][data['nv'][i,[0,1,2]],1])) for i in cages ]
sidx=np.where((savelag1['x'][:,0]>region['regionxy'][0])&(savelag1['x'][:,0]<region['regionxy'][1])&(savelag1['y'][:,0]>region['regionxy'][2])&(savelag1['y'][:,0]<region['regionxy'][3]))[0]
host=data['trigridxy'].get_trifinder().__call__(savelag1['x'][sidx,0],savelag1['y'][sidx,0])
cidx=np.in1d(host,cages)
npts=savelag1['x'].shape[0]
timediff=savelag1['time'][2]-savelag1['time'][1]
expand=0
region['regionxy']=[region['regionxy'][0]-expand,region['regionxy'][1]+expand,region['regionxy'][2]-expand,region['regionxy'][3]+expand]


#find particles in kelp from region start
numberin1=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag1['x'][sidx,:],savelag1['y'][sidx,:]),cages).reshape(savelag1['x'][sidx,:].shape),axis=0)/npts
numberin2=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag2['x'][sidx,:],savelag2['y'][sidx,:]),cages).reshape(savelag2['x'][sidx,:].shape),axis=0)/npts
numberin3=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag3['x'][sidx,:],savelag3['y'][sidx,:]),cages).reshape(savelag3['x'][sidx,:].shape),axis=0)/npts
numberin4=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag4['x'][sidx,:],savelag4['y'][sidx,:]),cages).reshape(savelag4['x'][sidx,:].shape),axis=0)/npts
numberin5=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag5['x'][sidx,:],savelag5['y'][sidx,:]),cages).reshape(savelag5['x'][sidx,:].shape),axis=0)/npts
numberin6=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag6['x'][sidx,:],savelag6['y'][sidx,:]),cages).reshape(savelag6['x'][sidx,:].shape),axis=0)/npts

f, (ax0,ax1,ax2) = plt.subplots(3, sharex=True, sharey=True)

ax1.plot((savelag1['time']-savelag1['time'].min())/3600,numberin1,'k',label='No drag - Start t=0')
ax1.plot((savelag2['time']-savelag2['time'].min())/3600,numberin2,'r',label='Drag - Start t=0')
ax1.plot((savelag3['time']-savelag3['time'].min())/3600,numberin3,'k--',label='No drag - Start t=3')
ax1.plot((savelag4['time']-savelag4['time'].min())/3600,numberin4,'r--',label='Drag - Start t=3')
ax1.plot((savelag5['time']-savelag5['time'].min())/3600,numberin5,'k-.',label='No drag - Start t=6')
ax1.plot((savelag6['time']-savelag6['time'].min())/3600,numberin6,'r-.',label='Drag - Start t=6')
ax1.set_xlim([0,plotend*24])
handles, labels = ax1.get_legend_handles_labels()
legend=ax1.legend(handles, labels,prop={'size':8})
ax1.set_ylabel(r'Ratio of particles',fontsize=8)
for label in (ax1.get_xticklabels() + ax1.get_yticklabels()):
    label.set_fontsize(8)



lname='element_80169_s0'
lname2='element_80169_s3'
lname2='element_80169_s6'

if True:
    print "Loading savelag1"
    fileload=h5.File('savedir/'+name+'/'+lname+'.mat')
    savelag1={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag1[i]=fileload['savelag'][i].value.T

if True:
    print "Loading savelag2"
    fileload=h5.File('savedir/'+name2+'/'+lname+'.mat')
    savelag2={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag2[i]=fileload['savelag'][i].value.T

if True:
    print "Loading savelag3"
    fileload=h5.File('savedir/'+name+'/'+lname2+'.mat')
    savelag3={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag3[i]=fileload['savelag'][i].value.T

if True:
    print "Loading savelag4"
    fileload=h5.File('savedir/'+name2+'/'+lname2+'.mat')
    savelag4={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag4[i]=fileload['savelag'][i].value.T

if True:
    print "Loading savelag5"
    fileload=h5.File('savedir/'+name+'/'+lname3+'.mat')
    savelag5={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag3[i]=fileload['savelag'][i].value.T

if True:
    print "Loading savelag6"
    fileload=h5.File('savedir/'+name2+'/'+lname3+'.mat')
    savelag6={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag4[i]=fileload['savelag'][i].value.T



#find particles in kelp from region start
numberin1=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag1['x'][sidx,:],savelag1['y'][sidx,:]),cages).reshape(savelag1['x'][sidx,:].shape),axis=0)/npts
numberin2=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag2['x'][sidx,:],savelag2['y'][sidx,:]),cages).reshape(savelag2['x'][sidx,:].shape),axis=0)/npts
numberin3=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag3['x'][sidx,:],savelag3['y'][sidx,:]),cages).reshape(savelag3['x'][sidx,:].shape),axis=0)/npts
numberin4=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag4['x'][sidx,:],savelag4['y'][sidx,:]),cages).reshape(savelag4['x'][sidx,:].shape),axis=0)/npts
numberin5=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag5['x'][sidx,:],savelag5['y'][sidx,:]),cages).reshape(savelag5['x'][sidx,:].shape),axis=0)/npts
numberin6=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag6['x'][sidx,:],savelag6['y'][sidx,:]),cages).reshape(savelag6['x'][sidx,:].shape),axis=0)/npts

ax2.plot((savelag1['time']-savelag1['time'].min())/3600,numberin1,'k',label='No drag - Start t=0')
ax2.plot((savelag2['time']-savelag2['time'].min())/3600,numberin2,'r',label='Drag - Start t=0')
ax2.plot((savelag3['time']-savelag3['time'].min())/3600,numberin3,'k--',label='No drag - Start t=3')
ax2.plot((savelag4['time']-savelag4['time'].min())/3600,numberin4,'r--',label='Drag - Start t=3')
ax2.plot((savelag5['time']-savelag5['time'].min())/3600,numberin5,'k-.',label='No drag - Start t=6')
ax2.plot((savelag6['time']-savelag6['time'].min())/3600,numberin6,'r-.',label='Drag - Start t=6')
ax2.set_xlim([0,plotend*24])
handles, labels = ax2.get_legend_handles_labels()
legend=ax2.legend(handles, labels,prop={'size':8})
ax2.set_ylabel(r'Ratio of particles',fontsize=8)
ax2.set_xlabel(r'Time (h)',fontsize=8)
for label in (ax2.get_xticklabels() + ax2.get_yticklabels()):
    label.set_fontsize(8)



lname='element_77567_s0'
lname2='element_77567_s3'
lname2='element_77567_s6'

if True:
    print "Loading savelag1"
    fileload=h5.File('savedir/'+name+'/'+lname+'.mat')
    savelag1={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag1[i]=fileload['savelag'][i].value.T

if True:
    print "Loading savelag2"
    fileload=h5.File('savedir/'+name2+'/'+lname+'.mat')
    savelag2={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag2[i]=fileload['savelag'][i].value.T

if True:
    print "Loading savelag3"
    fileload=h5.File('savedir/'+name+'/'+lname2+'.mat')
    savelag3={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag3[i]=fileload['savelag'][i].value.T

if True:
    print "Loading savelag4"
    fileload=h5.File('savedir/'+name2+'/'+lname2+'.mat')
    savelag4={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag4[i]=fileload['savelag'][i].value.T

if True:
    print "Loading savelag5"
    fileload=h5.File('savedir/'+name+'/'+lname3+'.mat')
    savelag5={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag3[i]=fileload['savelag'][i].value.T

if True:
    print "Loading savelag6"
    fileload=h5.File('savedir/'+name2+'/'+lname3+'.mat')
    savelag6={}
    for i in fileload['savelag'].keys():
        if (i=='u' or i=='v' or i=='w' or i=='sig' or i=='z'):
            continue
        savelag4[i]=fileload['savelag'][i].value.T



#find particles in kelp from region start
numberin1=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag1['x'][sidx,:],savelag1['y'][sidx,:]),cages).reshape(savelag1['x'][sidx,:].shape),axis=0)/npts
numberin2=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag2['x'][sidx,:],savelag2['y'][sidx,:]),cages).reshape(savelag2['x'][sidx,:].shape),axis=0)/npts
numberin3=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag3['x'][sidx,:],savelag3['y'][sidx,:]),cages).reshape(savelag3['x'][sidx,:].shape),axis=0)/npts
numberin4=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag4['x'][sidx,:],savelag4['y'][sidx,:]),cages).reshape(savelag4['x'][sidx,:].shape),axis=0)/npts
numberin5=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag5['x'][sidx,:],savelag5['y'][sidx,:]),cages).reshape(savelag5['x'][sidx,:].shape),axis=0)/npts
numberin6=np.sum(np.in1d(data['trigridxy'].get_trifinder().__call__(savelag6['x'][sidx,:],savelag6['y'][sidx,:]),cages).reshape(savelag6['x'][sidx,:].shape),axis=0)/npts

ax0.plot((savelag1['time']-savelag1['time'].min())/3600,numberin1,'k',label='No drag - Start t=0')
ax0.plot((savelag2['time']-savelag2['time'].min())/3600,numberin2,'r',label='Drag - Start t=0')
ax0.plot((savelag3['time']-savelag3['time'].min())/3600,numberin3,'k--',label='No drag - Start t=3')
ax0.plot((savelag4['time']-savelag4['time'].min())/3600,numberin4,'r--',label='Drag - Start t=3')
ax0.plot((savelag5['time']-savelag5['time'].min())/3600,numberin5,'k-.',label='No drag - Start t=6')
ax0.plot((savelag6['time']-savelag6['time'].min())/3600,numberin6,'r-.',label='Drag - Start t=6')
ax0.set_xlim([0,plotend*24])
handles, labels = ax0.get_legend_handles_labels()
legend=ax0.legend(handles, labels,prop={'size':8})
ax0.set_ylabel(r'Ratio of particles',fontsize=8)
ax0.set_xlabel(r'Time (h)',fontsize=8)
for label in (ax0.get_xticklabels() + ax0.get_yticklabels()):
    label.set_fontsize(8)

ax1.annotate("B",xy=(.975,.025),xycoords='axes fraction')
ax2.annotate("C",xy=(.975,.025),xycoords='axes fraction')
ax0.annotate("A",xy=(.975,.025),xycoords='axes fraction')

f.savefig(savepath +''+name+'_'+name2+'_'+regionname+'_'+lname+'_'+lname2+'_18runs.png',dpi=150)
plt.close(f)












from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from folderpath import *
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pandas as pd
import ttide

# Define names and types of data
name='sjh_hr_v3_0.02'
grid='sjh_hr_v3'
datatype='2d'
starttime=1008
endtime=-1


### load the .nc file #####
#data = loadnc(runpath+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
data = loadnc('/home/mif001/scratch/sjh_hr_v3/test_bfric/sjh_hr_v3_0.02/output/',singlename=grid + '_0001.nc')
data['lon']=data['lon']-360
data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
print('done load')
del data['trigrid']
data = ncdatasort(data)
print('done sort')



filenames=glob.glob('/home/mif001/scratch/obs/wlev/*.wlev')
wlev={}
for filename in filenames:
    wlev[filename.split('/')[-1][:5]]=load_wlev(filename)


tout=data['Times'][starttime:endtime,]
tclean=np.empty((len(tout),),dtype='|S26')
for i in range(len(tout)):
    tclean[i]=''.join(tout[i,])


savepath='{}/{}_{}/compare_TG/{}_{}_{}/'.format(datapath,grid,datatype,name,starttime,endtime)
if not os.path.exists(savepath): os.makedirs(savepath)

save={}

for i,key in enumerate(wlev):
    #print('='*80)
    #print(i)
    #print(key)
    xloc,yloc = data['proj'](wlev[key]['lon'],wlev[key]['lat'])
    xl,yl = data['proj'](xloc-5000,yloc-5000,inverse=True)
    xr,yr = data['proj'](xloc+5000,yloc+5000,inverse=True)
    region={}
    region['region']=np.array([xl,xr,yl,yr])


    dist=np.sqrt((data['x']-xloc)**2+(data['y']-yloc)**2)
    asort=np.argsort(dist)
    close=0
    while np.sum(data['wet_nodes'][:,asort[close]])<len(data['time']):
	close+=1

    node=asort[close]

    #print(close)
    #print(dist[node])
    if dist[node]>5000:
        continue
    #nidx=get_nodes(data,region)
    #if len(nidx)==0:
    #    f,ax=plottri(data,data['h'],show=False)
    #else:	
    #    f,ax=plottri(data,data['h'],minmax=[data['h'][nidx].min(), data['h'][nidx].max()],show=False)
    #prettyplot_ll(ax,setregion=region)
    #plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc',filepath=coastpath, color='k', fcolor='0.75', fill=True)  
    #ax.plot(loc[2],loc[1],'k*',markersize=10)
    #ax.plot(data['lon'][node],data['lat'][node],'r*',markersize=10,alpha=.5)
    #f.savefig('{}{}_{}_{}_dist_{:.2f}_depth.png'.format(savepath,loc[0].astype(int),loc[2],loc[1],dist[node]),dpi=600)
    #plt.close(f)

    #zeta=ipt.interpN_at_loc(data,'zeta',[loc[2],loc[1]])
    #zetac=zeta[starttime:endtime]
    zetac=data['zeta'][starttime:endtime,node]
    timec=data['time'][starttime:endtime]

    out=ttide.t_tide(zetac,stime=timec[0]-4/24.0,dt=.25,synth=-1,out_style=None,constitnames=['M2','N2','S2','K1','O1'])	     	
    
    idxw=np.array([],dtype=int)
    idx=np.array([],dtype=int)
    for j,name in enumerate(ttide.t_utils.fourpad(wlev[key]['name'])):
        tidx=np.argwhere(out['nameu']==name)
	if len(tidx)>0:
	    idxw=np.append(idxw,j)
	    idx=np.append(idx,tidx[0])
   


    print('='*80)
    print(wlev[key]['snum']) 
    print(wlev[key]['sname'])
    print(dist[node])
    diff=wlev[key]['tidecon'][idxw,][:,1:]-out['tidecon'][idx,][:,np.array([0,2])]
    diff[diff[:,1]<-180,1]=diff[diff[:,1]<-180,1]+360
    diff[diff[:,1]>180,1]=diff[diff[:,1]>180,1]-360
    df=pd.DataFrame(diff,columns=['Amp diff','Phase diff'],index=out['nameu'][idx])
    print(df)

    save[key]={}
    save[key]['sname']=wlev[key]['sname']
    save[key]['snum']=wlev[key]['snum']
    save[key]['lon']=wlev[key]['lon']
    save[key]['lat']=wlev[key]['lat']
    save[key]['diff']=diff
    save[key]['df']=df



np.save('{}tg_compare_out_5con.npy'.format(savepath),save)




















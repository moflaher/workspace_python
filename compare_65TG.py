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
import subprocess

# Define names and types of data
#name='sjh_hr_v3_nest1'
grid='sjh_lr_v1'
datatype='2d'
starttime=912
endtime=3984

#namelist=['sjh_hr_v3_0.015','sjh_hr_v3_0.015_shallow','sjh_hr_v3_0.02','sjh_hr_v3_0.03','sjh_hr_v3_0.035','sjh_hr_v3_0.04','sjh_hr_v3_0.045','sjh_hr_v3_0.05']
#namelist=['sjh_hr_v3_0.02_newnest','sjh_hr_v3_0.025_newnest','sjh_hr_v3_0.03_newnest','sjh_hr_v3_0.035_newnest']
namelist=['geometric_gotm_wd','geometric_gotm_wet_v2','geometric_my25_wd','uniform_gotm_wd','uniform_my25_wd','geometric_gotm_wet','geometric_gotm_wet_v3','geometric_my25_wet','uniform_gotm_wet','uniform_my25_wet']
namelist=[]

for d in os.listdir('/fs/vnas_Hdfo/odis/suh001/scratch/sjh_lr_v1/runs/jul2015_runs/'):
    line = subprocess.check_output(['tail', '-1', "/fs/vnas_Hdfo/odis/suh001/scratch/sjh_lr_v1/runs/jul2015_runs/{}/run_output".format(d)])
    if 'TADA' in line:
	namelist+=[d]
    else:
        print('Nope {}'.format(d))





for name in namelist:
    
    ### load the .nc file #####
    #data = loadnc('/home/mif001/scratch/sjh_lr_v1/{}/output/'.format(name),singlename=grid + '_0001.nc')
    try:
        data = loadnc('/home/suh001/scratch/sjh_lr_v1/runs/jul2015_runs/{}/output/'.format(name),singlename=grid + '_0001.nc')
    except:
        continue
    print('done load')
    data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
    
    filenames=glob.glob('/home/mif001/scratch/obs/wlev/*.wlev')
    wlev={}
    for filename in filenames:
        wlev[filename.split('/')[-1][:5]]=load_wlev(filename)
    
    
    savepath='{}/{}_{}/compare_TG/{}_{}_{}/'.format(datapath,grid,datatype,name,starttime,endtime)
    if not os.path.exists(savepath): os.makedirs(savepath)
    
    save={}
    
    for i,key in enumerate(wlev):
        xloc,yloc = data['proj'](wlev[key]['lon'],wlev[key]['lat'])
        dist=np.sqrt((data['x']-xloc)**2+(data['y']-yloc)**2)
        asort=np.argsort(dist)
        close=0
        #while np.sum(data['wet_nodes'][:,asort[close]])<len(data['time']):
        #    close+=1
    
        node=asort[close]
        if dist[node]>10000:
            continue
        
        zetac=data['zeta'][starttime:endtime,node]
        timec=data['time'][starttime:endtime]
        print(np.diff(data['time'])[0]*24)
        out=ttide.t_tide(zetac,stime=timec[0]-4/24.0,dt=np.diff(data['time'])[0]*24,synth=-1,out_style=None,lat=data['lat'][node])             
        
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
        save[key]['out']=out
        save[key]['wlev']=wlev[key]
        save[key]['outc']=out['tidecon'][idx,][:,np.array([0,2])]
        save[key]['wlevc']=wlev[key]['tidecon'][idxw,][:,1:]
    
    
    np.save('{}tg_compare_out_allcon.npy'.format(savepath),save)




















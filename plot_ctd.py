from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from folderpath import *
from datatools import *
from gridtools import *
from plottools import *
from projtools import *
from stattools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pandas as pd
import netCDF4 as n4
import copy
import matplotlib.dates as dates
import argparse




parser = argparse.ArgumentParser()
parser.add_argument("grid", help="name of the grid", type=str)
parser.add_argument("name", help="name of the run", type=str,default=None, nargs='?')
parser.add_argument("--station", help="switch to station output instead of fvcom output", default=False,action='store_true')
args = parser.parse_args()

print("The current commandline arguments being used are")
print(args)


grid=args.grid
if args.name is None:
    tempa='ls {}/{}/ctd/'.format(datapath,grid)
    print('\n Model names available:')
    os.system('{}'.format(tempa))
    print('\n')
    sys.exit()
else:
    name=args.name
    
if args.station:
    tag='station'
else:
    tag='fvcom'  




#modpath='{}/{}/ctd/{}/'.format(datapath,grid,name)
#obsp='{}east/ctd/'.format(obspath)
#ctdnum=np.genfromtxt(obsp+'NEMO-FVCOM_SaintJohn_BOF_Observations_ctd_SABS.txt',skip_header=1,dtype=int)[:,0]

# filenames=glob.glob('{}east/all/ctd_*.nc'.format(obspath))
# filenames.sort()

#location of save model ncfiles
modpath='{}/{}/ctd/{}/'.format(datapath,grid,name)
filenames=glob.glob('{}ctd_*_{}.nc'.format(modpath,tag))
filenames.sort()

savepath='{}png/{}/ctd/{}/'.format(figpath,grid,name)
if not os.path.exists(savepath): os.makedirs(savepath)

other={}
other['grid']=grid
other['name']=name

Tstats={}
Sstats={}
vT=OrderedDict()
f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8]);
plotcoast(ax,filename='mid_nwatl6c_sjh_lr.nc', filepath=coastpath, color='k', fill=True)
#for num in ctdnum:
#    print(num)
for i,filename in enumerate(filenames):
    print('='*80)
    print(i)
    print(filename)
    
    ctdm=loadnc('',filename,False)
    ctdo = loadnc('{}east/all/'.format(obspath),'ctd_{}.nc'.format(ctdm['ctdnumber'][0]),False)
    num=ctdm['ctdnumber'][0]
    #try:

    #mod=load_ctd_mod('{}ctd_timeseries_{}.txt'.format(modpath,num))
    #zeta=load_ctd_zeta_mod('{}ctd_zeta_{}.txt'.format(modpath,num))
    #obs=load_ctd_obs('{}{}_ctd.dat'.format(obsp,num))        
    other['dt']=ctdm['time'][1]-ctdm['time'][0]*24*60
    other['num']=num
    tidx=np.argmin(np.fabs(ctdm['time']-ctdo['time']))
    other['tidx']=tidx
    
    #for i in range(mod['arrays']['depth'].shape[1]):
    Tmod=ipt.interp1d(-1*ctdm['siglay']*(ctdm['h']+ctdm['zeta'][tidx]),ctdm['temp'][tidx,:],ctdo['depth'])
    Smod=ipt.interp1d(-1*ctdm['siglay']*(ctdm['h']+ctdm['zeta'][tidx]),ctdm['salinity'][tidx,:],ctdo['depth'])

    cTmod, cTobs = remove_common_nan(Tmod,ctdo['temp'])
    cSmod, cSobs = remove_common_nan(Smod,ctdo['salinity'])

    Tstats['{}'.format(num)]=residual_stats(cTmod, cTobs)
    Sstats['{}'.format(num)]=residual_stats(cSmod, cSobs)
            
    other['filename']='{}ctd_timeseries_{}.png'.format(savepath,num)
    #plot_tsmap2(mod,obs,other,Tstats,Sstats)

    #compute stats for all times
    Tstatst=OrderedDict()
    Tmodt=np.empty((len(ctdo['depth'].T),len(ctdm['time'])))
    Sstatst=OrderedDict()
    Smodt=np.empty((len(ctdo['depth'].T),len(ctdm['time'])))
    for j in range(len(ctdm['time'])):
        Tmodt[:,j]=ipt.interp1d(-1*ctdm['siglay']*(ctdm['h']+ctdm['zeta'][j]),ctdm['temp'][j,:],ctdo['depth'])
        cTmodt, cTobst = remove_common_nan(Tmodt[:,j],ctdo['temp'][0,:])    
        
        Smodt[:,j]=ipt.interp1d(-1*ctdm['siglay']*(ctdm['h']+ctdm['zeta'][j]),ctdm['salinity'][j,:],ctdo['depth'])
        cSmodt, cSobst = remove_common_nan(Smodt[:,j],ctdo['salinity'][0,:])   

        Tstatst['{}'.format(j)]=residual_stats(cTmodt, cTobst)
        Sstatst['{}'.format(j)]=residual_stats(cSmodt, cSobst)


    #put them in an array 
    bTstats=np.empty((7,len(Tstatst.keys())))
    bSstats=np.empty((7,len(Sstatst.keys())))
    for ii,key in enumerate(Tstatst.keys()):
        for jj,key2 in enumerate(Tstatst[key].keys()):
            bTstats[jj,ii]=Tstatst[key][key2]
            bSstats[jj,ii]=Sstatst[key][key2]


    #find the "best"
    Tidx=np.argmin(np.fabs(bTstats),axis=1)
    #fix the ones where "best" isnt the min
    Tidx2=np.argmin(np.fabs(bTstats-1),axis=1)
    Tidx[4]=Tidx2[4]
    Tidx[6]=Tidx2[6]

    #find the "best"
    Sidx=np.argmin(np.fabs(bSstats),axis=1)
    #fix the ones where "best" isnt the min
    Sidx2=np.argmin(np.fabs(bSstats-1),axis=1)
    Sidx[4]=Sidx2[4]
    Sidx[6]=Sidx2[6]
    

    #plot_tsmap2(mod,obs,zeta,other,Tstats,Sstats,bTstats,bSstats,Tidx,Sidx)
    
    TstatsV=OrderedDict()
    SstatsV=OrderedDict()
    for j,h in enumerate(np.arange(-7,7.1,.1)):
        Tmod=ipt.interp1d(-1*ctdm['siglay']*(ctdm['h']+ctdm['zeta'][tidx]+h),ctdm['temp'][tidx,:],ctdo['depth'][0,:])
        Smod=ipt.interp1d(-1*ctdm['siglay']*(ctdm['h']+ctdm['zeta'][tidx]+h),ctdm['salinity'][tidx,:],ctdo['depth'][0,:])

        cTmod, cTobs = remove_common_nan(Tmod,ctdo['temp'][0,:])
        cSmod, cSobs = remove_common_nan(Smod,ctdo['salinity'][0,:])

        TstatsV['{}'.format(j)]=residual_stats(cTmod, cTobs)
        SstatsV['{}'.format(j)]=residual_stats(cSmod, cSobs)
    
    bTstatsV=np.empty((7,len(TstatsV.keys())))
    bSstatsV=np.empty((7,len(SstatsV.keys())))
    for ii,key in enumerate(TstatsV.keys()):
        for jj,key2 in enumerate(TstatsV[key].keys()):
            bTstatsV[jj,ii]=TstatsV[key][key2]
            bSstatsV[jj,ii]=SstatsV[key][key2]
            
    #for k in range(7):
        #f=plt.figure(); ax=f.add_axes([.125,.1,.775,.8]); ax.plot(bTstatsV[k,:]); f.show()
    VidxT=np.argmin(bTstatsV[3,:])
    VidxS=np.argmin(bSstatsV[3,:])
    ht=np.arange(-7,7.1,.1)[VidxT]
    Tmod=ipt.interp1d(-1*ctdm['siglay']*(ctdm['h']+ctdm['zeta'][tidx]+ht),ctdm['temp'][tidx,:],ctdo['depth'][0,:])
    hs=np.arange(-7,7.1,.1)[VidxS]
    Smod=ipt.interp1d(-1*ctdm['siglay']*(ctdm['h']+ctdm['zeta'][tidx]+hs),ctdm['salinity'][tidx,:],ctdo['depth'][0,:])

    cTmod, cTobs = remove_common_nan(Tmod,ctdo['temp'][0,:])
    cSmod, cSobs = remove_common_nan(Smod,ctdo['salinity'][0,:])
    
    
    plot_tsmap2(ctdm,ctdo,other,Tstats,Sstats,bTstats,bSstats,Tidx,Sidx,ht)
    
    pdf=OrderedDict()
    print('T Vshift of {}'.format(ht))
    vT[str(num)]=ht
    if ht>=-1 and ht<=-.6:
        ax.plot(ctdo['lon'],ctdo['lat'],'*r',markersize=10)
    else:
        ax.plot(ctdo['lon'],ctdo['lat'],'*b',markersize=10)
    print('T hshift of {}'.format(bTstatsV[0,VidxT]))
    print('S Vshift of {}'.format(hs))
    print('S hshift of {}'.format(bSstatsV[0,VidxS]))
    pdf['vT']=residual_stats(cTmod, cTobs)
    pdf['hT']=residual_stats(cTmod-bTstatsV[0,VidxT], cTobs)
    pdf['vS']=residual_stats(cSmod, cSobs)
    pdf['hS']=residual_stats(cSmod-bSstatsV[0,VidxS], cSobs)
    df=pd.DataFrame(pdf).round(2).T
    print(df[['meansl','stdsl','rmsesl','relaverr','corsl','skewsl','skill']])
    print()
    print()
    
    
    other['filename']='{}ctd_t_vs_s_{}.png'.format(savepath,num)
    #plot_tsmap2(mod,obs,other,Tstats,Sstats)

    
    f=plt.figure(figsize=(4,4))
    ax=f.add_axes([.15,.15,.75,.75])
    ax.plot(ctdm['temp'],ctdm['salinity'],'b')
    ax.plot(ctdo['temp'].T,ctdo['salinity'].T,'r')
    f.savefig(other['filename'],dpi=300)
    plt.close('all')
        
    # except:
        # print('Pass on {}'.format(num))
        # pass

    

#f.show()
    



dfT=pd.DataFrame(Tstats).T
dfT=dfT[['meansl','stdsl','rmsesl','relaverr','corsl','skewsl','skill']]
dfS=pd.DataFrame(Sstats).T
dfS=dfS[['meansl','stdsl','rmsesl','relaverr','corsl','skewsl','skill']]



	








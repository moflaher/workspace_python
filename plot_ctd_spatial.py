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
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
import pandas as pd
import netCDF4 as n4
import copy
import matplotlib.dates as dates
import argparse




parser = argparse.ArgumentParser()
parser.add_argument("grid", help="name of the grid", type=str)
parser.add_argument("name", help="name of the run", type=str,default=None, nargs='?')
parser.add_argument("--station", help="switch to station output instead of fvcom output", default=False,action='store_true')
parser.add_argument("--coastline", help="disable coastline",type=bool,default=True)
parser.add_argument("-dpi", help="dpi of plot",type=int, default=150)
parser.add_argument("-zoom", help="specify zoom axis",type=float,nargs=4,default=None)
parser.add_argument("-region", help="specify predefined region",type=str,default=None)
parser.add_argument("-cmap", help="specify colormap",type=str,default='viridis')
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

coastflag=args.coastline




#location of save model ncfiles
modpath='{}/{}/ctd/{}/'.format(datapath,grid,name)
filenames=glob.glob('{}ctd_*_{}.nc'.format(modpath,tag))
filenames.sort()

savepath='{}png/{}/ctd_maps/{}/'.format(figpath,grid,name)
if not os.path.exists(savepath): os.makedirs(savepath)

other={}
other['grid']=grid
other['name']=name

Tstats={}
Sstats={}
saveLL={}


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
    saveLL['{}'.format(num)]=np.array([ctdo['lon'],ctdo['lat']])        

    

ll=np.empty((len(saveLL.keys()),2))
T=np.empty((len(saveLL.keys()),7))
S=np.empty((len(saveLL.keys()),7))
for i,key in enumerate(saveLL.keys()):
    ll[i,]=saveLL[key][:,0]
    T[i,]=Tstats[key].values()
    S[i,]=Sstats[key].values()
  
  
regionname=args.region
if regionname is not None:
    region=regions(regionname)
else:
    if args.zoom is not None:
        region={'region':np.array([args.zoom])}
    else:
        region={'region': np.array([1.01*ll[:,0].min(),.99*ll[:,0].max(),.99*ll[:,1].min(),1.01*ll[:,1].max()])}
    region['regionname']='zoom_'+array2str(region['region'])[:-1]
    region['figsize']=(8,6)
    region['axes']=[.125,.1,.775,.8]
    region['coast']='mid_nwatl6c_sjh_lr.nc'
    
def plot_fun(fin,ftype,fname):
    f=plt.figure(figsize=region['figsize'])
    ax=f.add_axes(region['axes'])    
    if coastflag:
        plotcoast(ax,filename=region['coast'], filepath=coastpath, color='k', fill=True)   

    cmin,cmax=np.percentile(fin,[10,90])

    if fname=='bias':
        vv=np.max([np.fabs(cmin),np.fabs(cmax)])
        triax=ax.scatter(ll[:,0],ll[:,1],c=fin,vmin=-vv,vmax=vv,edgecolor='k',cmap=mpl.cm.get_cmap('seismic'))
    else:
        triax=ax.scatter(ll[:,0],ll[:,1],c=fin,vmin=cmin,vmax=cmax,cmap=mpl.cm.get_cmap(args.cmap))    

    # if vectorflag:
        # Q1=ax.quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],data['ua'][i,vidx],data['va'][i,vidx],angles='xy',scale_units='xy',scale=vector_scale,zorder=100,width=.001)    
        # qaxk=ax.quiverkey(Q1,.775,.9,.5, r'.5 ms$^{-1}$')
    # if uniformvectorflag:
        # norm=np.sqrt(data['u'][i,layer,vidx]**2+data['v'][i,layer,vidx]**2)
        # Q1=ax.quiver(data['uvnodell'][vidx,0],data['uvnodell'][vidx,1],np.divide(data['u'][i,layer,vidx],norm),np.divide(data['v'][i,layer,vidx],norm),angles='xy',scale_units='xy',scale=vector_scale,zorder=100,width=.002,color='k')  

    cb=plt.colorbar(triax)
    cb.set_label(fname,fontsize=10)    
    ax.set_xlabel(r'Longitude ($^{\circ}$)')
    ax.set_ylabel(r'Latitude ($^{\circ}$)')
    ax.axis(region['region'])
    #ax.annotate('{} {}'.format(data['Time'][i][:10],data['Time'][i][11:19]),xy=region['textloc'],xycoords='axes fraction')
    for label in ax.get_xticklabels()[::2]:
        label.set_visible(False)
    f.savefig('{}{}_{}_{}_{}_{}.png'.format(savepath,grid,name,region['regionname'],ftype,fname),dpi=300)
    plt.close(f)
	

fields=['bias','std','rmse','rae','corr','skew','skill']

for i,t in enumerate(fields):
    print(t)
    plot_fun(T[:,i],'temp',t)
    plot_fun(S[:,i],'salinity',t)





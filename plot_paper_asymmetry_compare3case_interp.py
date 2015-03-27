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
import time
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
mpl.rcParams['contour.negative_linestyle'] = 'solid'

# Define names and types of data
name='kit4_kelp_20m_drag_0.018'
grid='kit4_kelp'
datatype='2d'
#regionname='kit4_kelp_tight6'
regionlist=['kit4_ftb','kit4_crossdouble','kit4_kelp_tight2_small','kit4_kelp_tight2','kit4_kelp_tight4','kit4_kelp_tight5','kit4_kelp_tight6']
regionlist=['kit4_kelp_tight2_small','kit4_ftb','kit4_kelp_tight2_kelpfield']
regionlist=['kit4_kelp_tight5']
starttime=384
cmin=-1
cmax=1
fmt=r'%1.1f'

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print 'done load'
data = ncdatasort(data)
print 'done sort'


cages=np.genfromtxt('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat',skiprows=1)
cages=(cages[:,0]-1).astype(int)

savepath='figures/png/' + grid + '_' + datatype + '/paper_asymmetry_subplot3cases_interp/' + name+ '/'
if not os.path.exists(savepath): os.makedirs(savepath)


ttidein=np.load('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv_all.npy')
ttidein=ttidein[()]
tidecon=ttidein['tidecon']
nameu=ttidein['nameu']
freq=ttidein['freq']
resmean=np.load('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv_all_mean.npy')
resmean=resmean[()]
m2i=np.where(nameu=='M2  ')
m4i=np.where(nameu=='M4  ')
SEMAZ0 = np.sqrt(resmean['resumean']**2+resmean['resvmean']**2);
delta = np.divide(SEMAZ0,tidecon[:,m2i,0].flatten());
theta0 = np.arctan2(resmean['resvmean'],resmean['resumean']);
dtheta0 = theta0-tidecon[:,m2i,4].flatten()/180*np.pi;
epslon  = tidecon[:,m2i,2].flatten()/tidecon[:,m2i,0].flatten();
dtheta4 = (tidecon[:,m4i,4].flatten()-tidecon[:,m2i,4].flatten())/180*np.pi;
pusi = (2*tidecon[:,m2i,6].flatten()-tidecon[:,m4i,6].flatten())/180*np.pi;
ECCM4=np.sqrt(1-(tidecon[:,m4i,2].flatten()/tidecon[:,m4i,0].flatten())**2)
p_all = delta*np.cos(dtheta0)+epslon*(np.cos(dtheta4)*np.cos(pusi)-ECCM4*np.sin(dtheta4)*np.sin(pusi));

ttidein=np.load('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv_all.npy')
ttidein=ttidein[()]
tidecon=ttidein['tidecon']
nameu=ttidein['nameu']
freq=ttidein['freq']
resmean=np.load('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv_all_mean.npy')
resmean=resmean[()]
resmean['resumean']=resmean['resumean']*0
resmean['resvmean']=resmean['resvmean']*0
m2i=np.where(nameu=='M2  ')
m4i=np.where(nameu=='M4  ')
SEMAZ0 = np.sqrt(resmean['resumean']**2+resmean['resvmean']**2);
delta = np.divide(SEMAZ0,tidecon[:,m2i,0].flatten());
theta0 = np.arctan2(resmean['resvmean'],resmean['resumean']);
dtheta0 = theta0-tidecon[:,m2i,4].flatten()/180*np.pi;
epslon  = tidecon[:,m2i,2].flatten()/tidecon[:,m2i,0].flatten();
dtheta4 = (tidecon[:,m4i,4].flatten()-tidecon[:,m2i,4].flatten())/180*np.pi;
pusi = (2*tidecon[:,m2i,6].flatten()-tidecon[:,m4i,6].flatten())/180*np.pi;
ECCM4=np.sqrt(1-(tidecon[:,m4i,2].flatten()/tidecon[:,m4i,0].flatten())**2)
p_noz0 = delta*np.cos(dtheta0)+epslon*(np.cos(dtheta4)*np.cos(pusi)-ECCM4*np.sin(dtheta4)*np.sin(pusi));

ttidein=np.load('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv_all.npy')
ttidein=ttidein[()]
tidecon=ttidein['tidecon']
nameu=ttidein['nameu']
freq=ttidein['freq']
resmean=np.load('data/ttide/'+grid+'_'+name+'_'+datatype+'_uv_all_mean.npy')
resmean=resmean[()]
m2i=np.where(nameu=='M2  ')
m4i=np.where(nameu=='M4  ')
tidecon[:,m4i,:]=tidecon[:,m4i,:]*0
SEMAZ0 = np.sqrt(resmean['resumean']**2+resmean['resvmean']**2);
delta = np.divide(SEMAZ0,tidecon[:,m2i,0].flatten());
theta0 = np.arctan2(resmean['resvmean'],resmean['resumean']);
dtheta0 = theta0-tidecon[:,m2i,4].flatten()/180*np.pi;
epslon  = tidecon[:,m2i,2].flatten()/tidecon[:,m2i,0].flatten();
dtheta4 = (tidecon[:,m4i,4].flatten()-tidecon[:,m2i,4].flatten())/180*np.pi;
pusi = (2*tidecon[:,m2i,6].flatten()-tidecon[:,m4i,6].flatten())/180*np.pi;
ECCM4=1#np.sqrt(1-(tidecon[:,m4i,2].flatten()/tidecon[:,m4i,0].flatten())**2)
p_nom4 = delta*np.cos(dtheta0)+epslon*(np.cos(dtheta4)*np.cos(pusi)-ECCM4*np.sin(dtheta4)*np.sin(pusi));



for regionname in regionlist:
    print 'plotting region: ' +regionname

    region=regions(regionname)
    nidx=get_nodes(data,region)
    eidx=get_elements(data,region)

    tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
    color='g'
    lw=.1
    ls='solid'


    f,ax=place_axes(region,3,cb=True)  


    ngridx = 2000
    ngridy = 2000
    start = time.clock()
    xi = np.linspace(region['region'][0],region['region'][1], ngridx)
    yi = np.linspace(region['region'][2],region['region'][3], ngridy)
    efs_interp=mpl.mlab.griddata(data['uvnodell'][:,0],data['uvnodell'][:,1], p_all, xi, yi)
    tmpxy=np.meshgrid(xi,yi)
    xii=tmpxy[0]
    yii=tmpxy[1]
    host=data['trigrid'].get_trifinder().__call__(xii,yii)
    efs_interp_mask = np.ma.masked_where(host==-1,efs_interp)
    print ('griddata interp: %f' % (time.clock() - start))

    axtri=ax[0].pcolormesh(xi,yi,efs_interp_mask,vmin=cmin,vmax=cmax)
    Vpos=np.array([0,.4,.8])
    Vneg=np.array([-.8,-.4])
    CS2=ax[0].contour(xi,yi,efs_interp_mask,Vpos,colors='k',zorder=30,linestyles='solid',linewidths=.5)
    ax[0].clabel(CS2, fontsize=4, inline=1,zorder=30,fmt=fmt)
    CS3=ax[0].contour(xi,yi,efs_interp_mask,Vneg,colors='w',zorder=30,linestyles='solid',linewidths=.5)
    ax[0].clabel(CS3, fontsize=4, inline=1,zorder=30,fmt=fmt)


   
    start = time.clock()
    efs_interp=mpl.mlab.griddata(data['uvnodell'][:,0],data['uvnodell'][:,1], p_noz0, xi, yi)
    efs_interp_mask = np.ma.masked_where(host==-1,efs_interp)
    print ('griddata interp: %f' % (time.clock() - start))
 
    axtri=ax[1].pcolormesh(xi,yi,efs_interp_mask,vmin=cmin,vmax=cmax)
    Vpos=np.array([0,.4,.8])
    Vneg=np.array([-.8,-.4])
    CS2=ax[1].contour(xi,yi,efs_interp_mask,Vpos,colors='k',zorder=30,linestyles='solid',linewidths=.5)
    ax[1].clabel(CS2, fontsize=4, inline=1,zorder=30,fmt=fmt)
    CS3=ax[1].contour(xi,yi,efs_interp_mask,Vneg,colors='w',zorder=30,linestyles='solid',linewidths=.5)
    ax[1].clabel(CS3, fontsize=4, inline=1,zorder=30,fmt=fmt)



    start = time.clock()
    efs_interp=mpl.mlab.griddata(data['uvnodell'][:,0],data['uvnodell'][:,1], p_nom4, xi, yi)
    efs_interp_mask = np.ma.masked_where(host==-1,efs_interp)
    print ('griddata interp: %f' % (time.clock() - start))

    axtri=ax[2].pcolormesh(xi,yi,efs_interp_mask,vmin=cmin,vmax=cmax)
    Vpos=np.array([0,.4,.8])
    Vneg=np.array([-.8,-.4])
    CS2=ax[2].contour(xi,yi,efs_interp_mask,Vpos,colors='k',zorder=30,linestyles='solid',linewidths=.5)
    ax[2].clabel(CS2, fontsize=4, inline=1,zorder=30,fmt=fmt)
    CS3=ax[2].contour(xi,yi,efs_interp_mask,Vneg,colors='w',zorder=30,linestyles='solid',linewidths=.5)
    ax[2].clabel(CS3, fontsize=4, inline=1,zorder=30,fmt=fmt)



    ppll_sub(ax,setregion=region,cb=axtri,cblabel='Asymmetry')

    
    ABC=['A','B','C']


    figW, figH = f.get_size_inches()
    for i,axi in enumerate(ax):
        plotcoast(ax[i],filename='pacific.nc',color='None',fill=True)
        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        ax[i].add_collection(lseg_t)
        ax[i].annotate(ABC[i],xy=(.025,1-.05/get_data_ratio(region)/figH/figW),xycoords='axes fraction')




    f.savefig(savepath + grid + '_' + regionname+'_paper_asymmetry_subplot3case_contour.png',dpi=600)
    plt.close('all')












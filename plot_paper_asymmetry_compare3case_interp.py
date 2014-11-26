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
name='kit4_kelp_20m_0.018'
grid='kit4'
datatype='2d'
#regionname='kit4_kelp_tight6'
regionlist=['kit4_ftb','kit4_crossdouble','kit4_kelp_tight2_small','kit4_kelp_tight2','kit4_kelp_tight4','kit4_kelp_tight5','kit4_kelp_tight6']
regionlist=['kit4_kelp_tight2_small','kit4_ftb']
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
    lw=.5
    ls='solid'


    f=plt.figure()

    xtarget=.25
    ytarget=.675

    aspect=get_aspectratio(region)
    dr=get_data_ratio(region)
    figW, figH = f.get_size_inches()
    fa = figH / figW

    if aspect>=1.1:    
        finalspace=((ytarget*fa)/aspect/dr)
        if finalspace>.265:
            finalspace[0]=.265
            ax0f=[.125,.275,finalspace[0],ytarget]
            ax1f=[ax0f[0]+finalspace[0]+.025,.275,finalspace[0],ytarget]
            ax2f=[ax1f[0]+finalspace[0]+.025,.275,finalspace[0],ytarget]
        else:
            ax0f=[.125,.275,1,ytarget]
            ax1f=[ax0f[0]+finalspace[0]+.025,.275,1,ytarget]
            ax2f=[ax1f[0]+finalspace[0]+.025,.275,1,ytarget]
    else:    
        finalspace=((((xtarget*fa)/aspect/dr)*aspect*dr)/fa)
        #ax1f=[.125,.1,.75,xtarget]
        #ax0f=[.125,ax1f[1]+finalspace[0]+.05,.75,xtarget]
        #finalspace=((ytarget*fa)/aspect/dr)
        ax2f=[.125,.1,1,xtarget]
        ax1f=[.125,ax2f[1]+finalspace[0]+.025,1,xtarget]
        ax0f=[.125,ax1f[1]+finalspace[0]+.025,1,xtarget]



    ngridx = 500
    ngridy = 500
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

    ax0=f.add_axes(ax0f)  
    axtri0=ax0.pcolor(xi,yi,efs_interp_mask,vmin=cmin,vmax=cmax)
    Vpos=np.array([0,.2,.4,.6,.8])
    Vneg=np.array([-.8,-.6,-.4,-.2])
    CS2=ax0.contour(xi,yi,efs_interp_mask,Vpos,colors='w',zorder=30,linestyles='dashed')
    ax0.clabel(CS2, fontsize=6, inline=1,zorder=30,fmt=fmt)
    CS3=ax0.contour(xi,yi,efs_interp_mask,Vneg,colors='w',zorder=30,linestyles='solid')
    ax0.clabel(CS3, fontsize=6, inline=1,zorder=30,fmt=fmt)

   
    start = time.clock()
    efs_interp=mpl.mlab.griddata(data['uvnodell'][:,0],data['uvnodell'][:,1], p_noz0, xi, yi)
    efs_interp_mask = np.ma.masked_where(host==-1,efs_interp)
    print ('griddata interp: %f' % (time.clock() - start))
    ax1=f.add_axes(ax1f)  
    axtri1=ax1.pcolor(xi,yi,efs_interp_mask,vmin=cmin,vmax=cmax)
    Vpos=np.array([0,.2,.4,.6,.8])
    Vneg=np.array([-.8,-.6,-.4,-.2])
    CS2=ax1.contour(xi,yi,efs_interp_mask,Vpos,colors='w',zorder=30,linestyles='dashed')
    ax1.clabel(CS2, fontsize=6, inline=1,zorder=30,fmt=fmt)
    CS3=ax1.contour(xi,yi,efs_interp_mask,Vneg,colors='w',zorder=30,linestyles='solid')
    ax1.clabel(CS3, fontsize=6, inline=1,zorder=30,fmt=fmt)


    start = time.clock()
    efs_interp=mpl.mlab.griddata(data['uvnodell'][:,0],data['uvnodell'][:,1], p_nom4, xi, yi)
    efs_interp_mask = np.ma.masked_where(host==-1,efs_interp)
    print ('griddata interp: %f' % (time.clock() - start))
    ax2=f.add_axes(ax2f)  
    axtri2=ax2.pcolor(xi,yi,efs_interp_mask,vmin=cmin,vmax=cmax)
    Vpos=np.array([0,.2,.4,.6,.8])
    Vneg=np.array([-.8,-.6,-.4,-.2])
    CS2=ax2.contour(xi,yi,efs_interp_mask,Vpos,colors='w',zorder=30,linestyles='dashed')
    ax2.clabel(CS2, fontsize=6, inline=1,zorder=30,fmt=fmt)
    CS3=ax2.contour(xi,yi,efs_interp_mask,Vneg,colors='w',zorder=30,linestyles='solid')
    ax2.clabel(CS3, fontsize=6, inline=1,zorder=30,fmt=fmt)

    prettyplot_ll(ax0,setregion=region)
    prettyplot_ll(ax1,setregion=region)
    prettyplot_ll(ax2,setregion=region)
    ax_label_spacer(ax0)
    ax_label_spacer(ax1)
    ax_label_spacer(ax2)


    if aspect>=1.1:
        ax1.yaxis.set_tick_params(labelleft='off')
        ax2.yaxis.set_tick_params(labelleft='off')
    else:
        ax0.xaxis.set_tick_params(labelleft='off')
        ax0.set_xlabel('')
        ax1.xaxis.set_tick_params(labelleft='off')
        ax1.set_xlabel('')

    plt.draw()
    ax0bb=ax0.get_axes().get_position().bounds
    ax1bb=ax1.get_axes().get_position().bounds
    ax2bb=ax2.get_axes().get_position().bounds

    if aspect>=1.1:
        ax0ca=f.add_axes([ax0bb[0],ax0bb[1]-.125,ax2bb[2]+ax2bb[0]-ax0bb[0],0.025])
        #ax1ca=f.add_axes([ax1bb[0],ax1bb[1]-.125,ax1bb[2],0.025])
        cb=plt.colorbar(axtri0,cax=ax0ca,orientation='horizontal')
        cb.set_label(r'Asymmetry',fontsize=6)
        for label in cb.ax.get_xticklabels():
            label.set_rotation(90)

        #cb2=plt.colorbar(axtri1,cax=ax1ca,orientation='horizontal')
        #cb2.set_label(r'Asymmetry',fontsize=6)
        ax1.set_ylabel('')
        ax2.set_ylabel('')
        #for label in cb2.ax.get_xticklabels():
        #    label.set_rotation(90)

    else:
        ax0ca=f.add_axes([ax0bb[0]+ax0bb[2]+.025,ax2bb[1],.025,ax0bb[1]+ax0bb[3]-ax2bb[1]])
        #ax1ca=f.add_axes([ax1bb[0]+ax1bb[2]+.025,ax1bb[1],.025,ax1bb[3]])
        cb=plt.colorbar(axtri0,cax=ax0ca)
        cb.set_label(r'Asymmetry',fontsize=8)
        #cb2=plt.colorbar(axtri1,cax=ax1ca)
        #cb2.set_label(r'Asymmetry',fontsize=8)

    plotcoast(ax0,filename='pacific.nc',color='k')
    plotcoast(ax1,filename='pacific.nc',color='k')
    plotcoast(ax2,filename='pacific.nc',color='k')


    lseg0=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    ax0.add_collection(lseg0)
    lseg1=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    ax1.add_collection(lseg1)
    lseg2=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
    ax2.add_collection(lseg2)

    ax0.annotate("A",xy=(.025,1-(.075/dr)),xycoords='axes fraction')
    ax1.annotate("B",xy=(.025,1-(.075/dr)),xycoords='axes fraction')
    ax2.annotate("C",xy=(.025,1-(.075/dr)),xycoords='axes fraction')

    #add_num_label(ax1,data,1000,74845,'e')

    #plotcoast(ax0,filename='pacific.nc',color='k')
    #plotcoast(ax1,filename='pacific.nc',color='k')

    f.savefig(savepath + grid + '_' + regionname+'_paper_asymmetry_subplot3case_contour.png',dpi=600)
    plt.close('all')












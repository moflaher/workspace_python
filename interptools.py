from __future__ import division
import numpy as np
import matplotlib as mpl
import scipy as sp
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
from StringIO import StringIO

import gridtools as gt
import datatools as dt
import plottools as pt
import projtools as pjt
from matplotlib.collections import LineCollection as LC
import seawater as sw
np.set_printoptions(precision=16,suppress=True,threshold=np.nan)
import bisect


"""
Front Matter
=============

Created in 2014

Author: Mitchell O'Flaherty-Sproul

A bunch of functions dealing with fvcom interpolation.
            
"""
def interpE_at_loc(data,varname,loc,layer=None,ll=True):
    """
    Interpolate element data at a location. If variable is 3d then specify a layer, defaults to surface layer otherwise.
    Note: 1d element data will break this, should be possible to handle. I will work out the logic another day.
    
    :Parameters:
    data - data dictionary from loadnc
    varname - element data variable name. (2d or 3d)
    loc - location

    :Optional:
    layer - default None. Specify which layer of 3d data to use
    ll - default True. Is point lon/lat or xy.    
    """   


    ###############################################################################
    # Error and corner case checking
    if ll==True:
        trifinder='trigrid_finder'
        trigrid='trigrid'
    else:
        trifinder='trigridxy_finder'
        trigrid='trigridxy'

    if (data.has_key(trifinder)==False and data.has_key(trigrid)):
        print 'No trifinder initialized. Initializing now.'
        data[trifinder]=data[trigrid].get_trifinder()
    elif data.has_key(trigrid)==False:
        print 'No trifinder or trigrid to initialize it.'
        return

    if ((len(data[varname].shape)>2) and (layer==None)):
        print '3d variable specified without layer. Returning surface layer.'
        layer=0
    elif ((len(data[varname].shape)==2) and (layer!=None)):
        print '2d variable specified with layer. That would break things, unspecifing layer.'
        layer=None

    loc=np.array(loc)
    host=data[trifinder].__call__(loc[0],loc[1])
    if host==-1:
        print 'Point at: (' + ('%f'%loc[0]) + ', ' +('%f'%loc[1]) + ') is external to the grid.'
        out=np.empty(shape=(data[varname][:,layer,host]).squeeze().shape)
        out[:]=np.nan
        return out
    ###############################################################################


    #code for ll adapted from mod_utils.F
    if ll==True:
        x0c,y0c=pjt.ll2m(data['uvnodell'][host,:],loc)
    else:       
        x0c=loc[0]-data['uvnode'][host,0]
        y0c=loc[1]-data['uvnode'][host,1] 


    e0=data['nbe'][host,0]
    e1=data['nbe'][host,1]
    e2=data['nbe'][host,2]
      
    var_e=(data[varname][:,layer,host]).squeeze()
    if e0==-1:
        var_0=np.zeros(shape=var_e.shape,dtype=var_e.dtype)
    else:
        var_0=(data[varname][:,layer,e0]).squeeze()
    if e1==-1:
        var_1=np.zeros(shape=var_e.shape,dtype=var_e.dtype)
    else:
        var_1=(data[varname][:,layer,e1]).squeeze()
    if e2==-1:
        var_2=np.zeros(shape=var_e.shape,dtype=var_e.dtype)
    else:
        var_2=(data[varname][:,layer,e2]).squeeze()

    dvardx= data['a1u'][0,host]*var_e+data['a1u'][1,host]*var_0+data['a1u'][2,host]*var_1+data['a1u'][3,host]*var_2
    dvardy= data['a2u'][0,host]*var_e+data['a2u'][1,host]*var_0+data['a2u'][2,host]*var_1+data['a2u'][3,host]*var_2
    var= var_e + dvardx*x0c + dvardy*y0c

        
    return var


def interpN_at_loc(data,varname,loc,layer=None,ll=True):
    """
    Interpolate nodal data at a location. If variable is 3d then specify a layer, defaults to surface layer otherwise.
    Note: 1d element data will break this, should be possible to handle. I will work out the logic another day.
    
    data - data dictionary from loadnc
    varname - nodal data variable name. (1d or 2d or 3d)
    loc - location
    
    Optional:
    layer - default None. Specify which layer of 3d data to use
    ll - default True. Is point lon/lat or xy.    
    """   


    ###############################################################################
    # Error and corner case checking
    if ll==True:
        trifinder='trigrid_finder'
        trigrid='trigrid'
    else:
        trifinder='trigridxy_finder'
        trigrid='trigridxy'

    if (data.has_key(trifinder)==False and data.has_key(trigrid)):
        print 'No trifinder initialized. Initializing now.'
        data[trifinder]=data[trigrid].get_trifinder()
    elif data.has_key(trigrid)==False:
        print 'No trifinder or trigrid to initialize it.'
        return

    if ((len(data[varname].shape)>2) and (layer==None)):
        print '3d variable specified without layer. Returning surface layer.'
        layer=0
    elif ((len(data[varname].shape)==2) and (layer!=None)):
        print '2d variable specified with layer. That would break things, unspecifing layer.'
        layer=None

    loc=np.array(loc)
    host=data[trifinder].__call__(loc[0],loc[1])
    if host==-1:
        print 'Point at: (' + ('%f'%loc[0]) + ', ' +('%f'%loc[1]) + ') is external to the grid.'
        if len(data[varname].shape)==1:
            out=np.nan
        else:
            out=np.empty(shape=(data[varname][:,layer,host]).squeeze().shape)
            out[:]=np.nan
        return out
    ###############################################################################


    #code for ll adapted from mod_utils.F
    if ll==True:
        x0c,y0c=pjt.ll2m(data['uvnodell'][host,:],loc)
    else:       
        x0c=loc[0]-data['uvnode'][host,0]
        y0c=loc[1]-data['uvnode'][host,1] 


    n0=data['nv'][host,0]
    n1=data['nv'][host,1]
    n2=data['nv'][host,2]
      

    #To deal with 1d data, should be a better way to handle this....
    #This can all be vectorized, checkout robies code could make a factor of 2 difference.
    if len(data[varname].shape)==1:
        nvar0=data[varname][n0]
        nvar1=data[varname][n1]
        nvar2=data[varname][n2]
    else:
        nvar0=(data[varname][:,layer,n0]).squeeze()
        nvar1=(data[varname][:,layer,n1]).squeeze()
        nvar2=(data[varname][:,layer,n2]).squeeze()

    var_0=data['aw0'][0,host]*nvar0+data['aw0'][1,host]*nvar1+data['aw0'][2,host]*nvar2
    var_x=data['awx'][0,host]*nvar0+data['awx'][1,host]*nvar1+data['awx'][2,host]*nvar2
    var_y=data['awy'][0,host]*nvar0+data['awy'][1,host]*nvar1+data['awy'][2,host]*nvar2

    var= var_0 + var_x*x0c + var_y*y0c
        
    return var


def cross_shore_transect_2d(grid,name,region,vec,npt):
    data = dt.loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
    print 'done load'
    data = dt.ncdatasort(data,trifinder=True)
    print 'done sort'

    cages=gt.loadcage('runs/'+grid+'/' +name+ '/input/' +grid+ '_cage.dat')
    if np.shape(cages)!=():
        tmparray=[list(zip(data['nodell'][data['nv'][i,[0,1,2,0]],0],data['nodell'][data['nv'][i,[0,1,2,0]],1])) for i in cages ]
        color='g'
        lw=.2
        ls='solid'
   
    vectorstart=np.array(vec[0])
    vectorend=np.array(vec[1])
    vectorx=np.array([vectorstart[0],vectorend[0]])
    vectory=np.array([vectorstart[1],vectorend[1]])
    snv=(vectorend-vectorstart)/np.linalg.norm(vectorend-vectorstart)

    xi=np.linspace(vectorstart[0],vectorend[0],npt)
    yi=np.linspace(vectorstart[1],vectorend[1],npt)
    us=data['ua'].shape

    savepath='data/cross_shore_transect/'
    if not os.path.exists(savepath): os.makedirs(savepath)

    plotpath='figures/png/'+grid+'_2d/cross_shore_transect/'
    if not os.path.exists(plotpath): os.makedirs(plotpath)



    nidx=dt.get_nodes(data,region)
    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])
    triax=ax.tripcolor(data['trigrid'],data['h'],vmin=data['h'][nidx].min(),vmax=data['h'][nidx].max())
    ax.plot(xi,yi,'k',lw=3)  
    if np.shape(cages)!=():   
        lseg_t=LC(tmparray,linewidths = lw,linestyles=ls,color=color)
        coast=ax.add_collection(lseg_t)
        coast.set_zorder(30)
    pt.prettyplot_ll(ax,setregion=region,cb=triax,cblabel=r'Depth (m)') 
    f.savefig(plotpath + name+'_'+('%f'%vectorx[0])+'_'+('%f'%vectorx[1])+'_'+('%f'%vectory[0])+'_'+('%f'%vectory[1])+'_'+('%d'%len(xi))+'_line_location.png',dpi=600)
    plt.close(f)

    fillarray_u=np.empty((us[0],npt))
    fillarray_v=np.empty((us[0],npt))
    fillalong=np.empty((us[0],npt))
    fillcross=np.empty((us[0],npt))
    dist=np.empty((npt,))
    h=np.empty((npt,))

    print 'interp uvw on path'
    for i in range(0,len(xi)):
        print i
        fillarray_u[:,i],fillarray_v[:,i]=interp_vel(data,[xi[i],yi[i]])
        h[i]=interpN_at_loc(data,'h',[xi[i],yi[i]])

    print 'Calc along path current'
    for i in range(0,len(xi)):
        print i
        inner=np.inner(np.vstack([fillarray_u[:,i],fillarray_v[:,i]]).T,snv)
        along=np.vstack([inner*snv[0],inner*snv[1]]).T
        tmpa=np.multiply(np.sign(np.arctan2(along[:,1],along[:,0])),np.linalg.norm(along,axis=1))
        fillalong[:,i]=tmpa
        cross=np.vstack([fillarray_u[:,i],fillarray_v[:,i]]).T-along
        tmpc=np.multiply(np.sign(np.arctan2(cross[:,1],cross[:,0])),np.linalg.norm(cross,axis=1))
        fillcross[:,i]=tmpc

        dist[i]=(sw.dist([vectorstart[1], yi[i]],[vectorstart[0], xi[i]],'km'))[0]*1000;
        
    if np.shape(cages)!=():
        incage=np.zeros((len(xi),))
        host=data['trigrid'].get_trifinder().__call__(xi,yi)
        incage[np.in1d(host,cages)]=1


    savedic={}

    savedic['u']=fillarray_u
    savedic['v']=fillarray_v
    savedic['along']=fillalong
    savedic['cross']=fillcross
    savedic['distance']=dist
    savedic['h']=h
    savedic['lon']=xi
    savedic['lat']=yi
    if np.shape(cages)!=():
        savedic['incage']=incage

    np.save(savepath+grid+'_'+name+'_'+('%f'%vectorx[0])+'_'+('%f'%vectorx[1])+'_'+('%f'%vectory[0])+'_'+('%f'%vectory[1])+'_'+('%d'%len(xi))+'_2d.npy',savedic)
    sio.savemat(savepath+'matfiles/'+grid+'_'+name+'_'+('%f'%vectorx[0])+'_'+('%f'%vectorx[1])+'_'+('%f'%vectory[0])+'_'+('%f'%vectory[1])+'_'+('%d'%len(xi))+'_2d.mat',mdict=savedic)




from __future__ import division,print_function
import numpy as np
import matplotlib as mpl
import scipy as sp
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import gridtools as gt
import datatools as dt
import plottools as pt
from regions import makeregions
np.set_printoptions(precision=16,suppress=True,threshold=np.nan)
import seawater as sw

"""
Front Matter
=============

Created in 2015

Author: Mitchell O'Flaherty-Sproul

A bunch of functions dealing regions and projections.

"""
def gridproj(grid):

    try:
        import pyproj as pyp
    except ImportError:
        print("pyproj is not installed, please install pyproj.")
        return

    projstr={}
    projstr['smallcape_force']='lcc +lon_0=-64.55880 +lat_0=41.84493 +lat_1=39.72147 +lat_2=43.96838'
    projstr['voucher']='lcc +lon_0=-64.55880 +lat_0=41.84492 +lat_1=39.72147 +lat_2=43.96838'
    projstr['dngrid']='lcc +lon_0=-64.55880 +lat_0=41.78504 +lat_1=39.69152 +lat_2=43.87856'
    projstr['dn_coarse']='lcc +lon_0=-64.55880 +lat_0=41.78504 +lat_1=39.69152 +lat_2=43.87856'    
    
    projstr['acadia_force']='lcc +lon_0=-64.55880 +lat_0=41.84493 +lat_1=39.72147 +lat_2=43.96838'
    projstr['acadia_BoF']='lcc +lon_0=-64.55880 +lat_0=41.84492 +lat_1=39.72147 +lat_2=43.96838'
    projstr['acadia_dn']='lcc +lon_0=-64.55880 +lat_0=41.78504 +lat_1=39.69152 +lat_2=43.87856'

    projstr['kit4_kelp']='lcc +lon_0=-129.4954 +lat_0=53.55285 +lat_1=52.36906 +lat_2=54.73664'
    projstr['vhfr_low']='lcc +lon_0=-122.9842 +lat_0=49.24705 +lat_1=49.02230 +lat_2=49.47181'
    projstr['vh_high']='lcc +lon_0=-122.9842 +lat_0=49.24705 +lat_1=49.02230 +lat_2=49.47181'
    projstr['vhhigh_v2']='lcc +lon_0=-122.9842 +lat_0=49.24705 +lat_1=49.02230 +lat_2=49.47181'
    projstr['fr_high']='lcc +lon_0=-122.9842 +lat_0=49.24705 +lat_1=49.02230 +lat_2=49.47181'
    
    projstr['sfm6_musq2']='lcc +lon_0=-64.62943 lat_0=45.39876 lat_1=45.11211 lat_2=45.68542'
    

    return pyp.Proj(proj=projstr[grid])


def ll2m(locs,loce):
    TPI=111194.92664455874
    y0c = TPI * (loce[1] - locs[1])
    dx_sph = loce[0] - locs[0]
    if (dx_sph > 180.0):
        dx_sph=dx_sph-360.0
    elif (dx_sph < -180.0):
        dx_sph =dx_sph+360.0
    x0c = TPI * np.cos(np.deg2rad(loce[1] + locs[1])*0.5) * dx_sph

    return x0c,y0c


def mdist(locs,loce):
    dist=np.linalg.norm( ll2m(locs,loce) )

    return dist


def regionll2xy(data,region):
    """
    Take an FVCOM data dictionary, a region dictionary and return a region dictionary with regionxy added which best approximates the ll region in xy.
 
    """
    try:
        np.shape(region['center'])
    except KeyError:
        region['center']=[(region['region'][0]+region['region'][1])/2,(region['region'][2]+region['region'][3])/2]

    ehost=dt.closest_element(data,region['center'])
    nhost=dt.closest_node(data,region['center'])

    edist=ll2m(data['uvnodell'][ehost,:],region['center'])
    ndist=ll2m(data['nodell'][nhost,:],region['center'])

    if ( np.linalg.norm(edist)>np.linalg.norm(ndist) ):
        region['centerxy']=data['nodexy'][nhost,:]
        xp,yp=ll2m(data['nodell'][nhost,:],region['region'][[1,3]])
        xn,yn=ll2m(data['nodell'][nhost,:],region['region'][[0,2]])
    else:
        region['centerxy']=data['uvnode'][ehost,:]
        xp,yp=ll2m(data['uvnodell'][ehost,:],region['region'][[1,3]])
        xn,yn=ll2m(data['uvnodell'][ehost,:],region['region'][[0,2]])

    region['regionxy']=[region['centerxy'][0]+xn,region['centerxy'][0]+xp,region['centerxy'][1]+yn,region['centerxy'][1]+yp]      

    #old code leave this in till the new code above is tested
    #    left=np.argmin(np.sqrt((data['uvnodell'][:,0]-region['region'][0])**2+(data['uvnodell'][:,1]-(region['region'][2]+region['region'][3])*.5)**2))
    #    right=np.argmin(np.sqrt((data['uvnodell'][:,0]-region['region'][1])**2+(data['uvnodell'][:,1]-(region['region'][2]+region['region'][3])*.5)**2))
    #    
    #    top=np.argmin(np.sqrt((data['uvnodell'][:,1]-region['region'][3])**2+(data['uvnodell'][:,0]-(region['region'][0]+region['region'][1])*.5)**2))
    #    bottom=np.argmin(np.sqrt((data['uvnodell'][:,1]-region['region'][2])**2+(data['uvnodell'][:,0]-(region['region'][0]+region['region'][1])*.5)**2))

    #    region['regionxy']=[data['uvnode'][left,0],data['uvnode'][right,0],data['uvnode'][bottom,1],data['uvnode'][top,1]]

    return region


def regions(region=None, group=None):
    """Returns region locations and full names

    :Parameters:
    	regionname
    """

    allregions=makeregions()

    #list all regions
    if region==None and group=='all':
        print('Valid regions are')
        return allregions.keys() 
        
    #list all groups
    if region==None and group==None:
        tmp=[]
        for key in allregions:
            tmp+=[allregions[key]['group']]
        print('Valid groups are')
        return np.unique(np.array(tmp)).tolist()
        
    #list all regions in a group
    if group!=None and group!='all' and region==None:
        tmp=[]
        for key in allregions:
            if group in allregions[key]['group']:
                tmp+=[key]
        print('Valid regions in group {} are'.format(group))
        return tmp
        
    #return a region
    if region!=None:
        tmpregion=allregions[region]
        tmpregion['center']=[(tmpregion['region'][0]+tmpregion['region'][1])/2,(tmpregion['region'][2]+tmpregion['region'][3])/2]
        return tmpregion


def ll_dist(region,dist):
    """
    Given a region and a distance in meters returns longitude interval approximately equalivent to the distance.
    NOTE: Clearly this is crude, hacky, and inaccurate over large areas. However, over small areas the error is small.

    :Parameters:
    	region - The region being plotted, needed for average latitude.
    	dist - The distance in meters to match.
    """
    lat=region['region'][2:4].mean()
    mlat=sw.dist([lat, lat],[0, 1],'km')[0]*1000
#    print mlat
#    mtest=ll2m([0,lat],[1,lat])[0]
#    print mtest
    
    return dist/mlat


def expand_region(region,dist=0,shift=0):
    """
    Given a region expands and/or shifts the region by a distance (1d or 2d) in meters.
    Also saves how much it was expanded or shifted by.
     

    :Parameters:
        region -  The region to expand.
    	dist - The distance in meters the expand the region.
        shift - The distance in meters to move the region.
    """
    if dist!=0:
        dist=np.atleast_1d(np.array(dist))
        lon_space=ll_dist(region,dist[0])[0]
        if len(dist)==2:
            lat_space=dist[1]/111120 
            y_dist=dist[1]   
        else:
            lat_space=dist[0]/111120  
            y_dist=dist[0]   

        region['region']=region['region']+np.array([-lon_space,+lon_space,-lat_space,+lat_space])
        region['lon_edist']=lon_space
        region['lat_edist']=lat_space


    if shift!=0:
        shift=np.atleast_1d(np.array(shift))
        lon_space=ll_dist(region,shift[0])[0]
        if len(shift)==2:
            lat_space=shift[1]/111120 
            y_dist=shift[1]   
        else:
            lat_space=shift[0]/111120  
            y_dist=shift[0]   

        region['region']=region['region']+np.array([+lon_space,+lon_space,+lat_space,+lat_space])
        region['lon_sdist']=lon_space
        region['lat_sdist']=lat_space

        #    region['regionxy']=region['regionxy']+[-dist[0],+dist[0],-y_dist,+y_dist]
        #    region['x_edist']=dist[0]
        #    region['y_edist']=y_dist

    return region


def region2path(region):
    region['path']=[[region['region'][0],region['region'][2]],[region['region'][0],region['region'][3]],[region['region'][1],region['region'][3]],[region['region'][1],region['region'][2]]]
    
    try:
        region['pathxy']=[[region['regionxy'][0],region['regionxy'][2]],[region['regionxy'][0],region['regionxy'][3]],[region['regionxy'][1],region['regionxy'][3]],[region['regionxy'][1],region['regionxy'][2]]]
    except KeyError:
        print("No regionxy. pathxy could not be added.")
    
    return region


def regionarea(region):
    return mdist(region['region'][[0,2]],region['region'][[0,3]])*mdist(region['region'][[0,2]],region['region'][[1,2]])


def smallestregion(data,host):
    minarea=10000000000
    for regionname in regions():
        region=regions(regionname)
        eidx=dt.get_elements(data,region)
        if ((np.sum(np.in1d(host,eidx))==len(host)) and (regionarea(region)<minarea)):
            minarea=regionarea(region)
            bestregion=regionname

    return bestregion

def lcc(lon,lat):
    """
    Given a lon lat converts to x,y and return them and the projection     
    """
    try:
        import pyproj as pyp
    except ImportError:
        print("pyproj is not installed, please install pyproj.")
        return
    
    
    #define the lcc projection
    xmax=np.nanmax(lon)
    xmin=np.nanmin(lon)
    ymax=np.nanmax(lat)
    ymin=np.nanmin(lat)
    xavg = ( xmax + xmin ) * 0.5;
    yavg = ( ymax + ymin ) * 0.5;
    ylower = ( ymax - ymin ) * 0.25 + ymin;
    yupper = ( ymax - ymin ) * 0.75 + ymin;
    
    projstr='lcc +lon_0='+str(xavg)+' +lat_0='+str(yavg)+' +lat_1='+str(ylower)+' +lat_2='+str(yupper)
    proj=pyp.Proj(proj=projstr)
    
    x,y=proj(lon,lat)     
    
    return x,y,proj
    
    
def degree2decdeg(degree_in):
    
    if len(degree_in)>degree_in.size:
        print('Vectors only!')
        return 
    
    array_out=np.empty((len(degree_in),))
    sign=1
    
    for i,cord in enumerate(degree_in):
        if 'panda' in str(type(cord)):
            cord=cord[0]
        if 'W' in cord:
            sign=-1
        if 's' in cord:
            sign=-1
        
        a,b=cord.split('\xc2\xb0')
        c,d=b.split("'")
        e,f=d.split('"')
        array_out[i] = sign*(float(a) + float(c)/60.0 + float(e)/3600.0)
        
    return array_out
    
    



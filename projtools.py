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
from regions import makeregions
np.set_printoptions(precision=16,suppress=True,threshold=np.nan)
from regions import makeregions
import seawater as sw

"""
Front Matter
=============

Created in 2015

Author: Mitchell O'Flaherty-Sproul

A bunch of functions dealing regions and projections.

"""
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
    ehost=dt.closest_element(data,region['center'])
    nhost=dt.closest_node(data,region['center'])

    edist=ll2m(data['uvnodell'][ehost,:],region['center'])
    ndist=ll2m(data['nodell'][nhost,:],region['center'])

    if ( np.linalg.norm(edist)>np.linalg.norm(ndist) ):
        region['centerxy']=data['nodexy'][nhost,:]
        xp,yp=ll2m(data['nodell'][nhost,:],region['region'][[1,3]])
        xn,yn=ll2m(data['nodell'][nhost,:],region['region'][[0,2]])
    else:
        region['centerxy']=data['uvnode'][nhost,:]
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


def regions(regionname=None):
    """Returns region locations and full names

    :Parameters:
    	regionname

 
    """

    allregions=makeregions()

    if regionname==None:
        print 'Valid regions are'
        return allregions.keys()        
    else:
        tmpregion=allregions[regionname]
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
    print mlat
    mtest=ll2m([0,lat],[1,lat])[0]
    print mtest
    
    return dist/mlat


def expand_region(region,dist):
    """
    Given a region expands the region by a distance (1d or 2d) in meters.
    Also saves how much it was expand by.
     

    :Parameters:
        region -  The region to expand.
    	dist - The distance in meters around the box to plot.
    """
    dist=np.atleast_1d(np.array(dist))
    lon_space=ll_dist(region,dist[0])
    if len(dist)==2:
        lat_space=dist[1]/111120 
        y_dist=dist[1]   
    else:
        lat_space=dist[0]/111120  
        y_dist=dist[0]   

    region['region']=region['region']+[-lon_space,+lon_space,-lat_space,+lat_space]
    region['lon_edist']=lon_space
    region['lat_edist']=lat_space

    #    region['regionxy']=region['regionxy']+[-dist[0],+dist[0],-y_dist,+y_dist]
    #    region['x_edist']=dist[0]
    #    region['y_edist']=y_dist

    return region


def region2path(region):
    region['path']=[[region['region'][0],region['region'][2]],[region['region'][0],region['region'][3]],[region['region'][1],region['region'][3]],[region['region'][1],region['region'][2]]]
    
    try:
        region['pathxy']=[[region['regionxy'][0],region['regionxy'][2]],[region['regionxy'][0],region['regionxy'][3]],[region['regionxy'][1],region['regionxy'][3]],[region['regionxy'][1],region['regionxy'][2]]]
    except KeyError:
        print "No regionxy. pathxy could not be added."
    
    return region





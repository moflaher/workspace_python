from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from misctools import *
from plottools import *
from projtools import *
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from osgeo import ogr
from osgeo import osr


# Define names and types of data
name='2012-02-01_2012-03-01_0.01_0.001'
grid='vh_high'
datatype='2d'
regionname='fr_whole'
region=regions(regionname)

data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid+'_0001.nc')
data =ncdatasort(data)

#save_poly_shp(data,'uvh','data/test/'+grid+'_depth.shp')



filename='data/test/'+grid+'_speed_dir_100.shp'
epsg_in=4326

lon = data['uvnodell'][:,0]
lat = data['uvnodell'][:,1]
trinodes = data['nv']
speed_100=speeder(data['ua'][100,:],data['va'][100,:])
dir_100=np.arctan2(data['va'][100,:],data['ua'][100,:])


driver = ogr.GetDriverByName('ESRI Shapefile')
shapeData = driver.CreateDataSource(filename)

spatialRefi = osr.SpatialReference()
spatialRefi.ImportFromEPSG(epsg_in)
lyr = shapeData.CreateLayer("point_layer", spatialRefi, ogr.wkbPoint )

#var is just a rdm string?
lyr.CreateField(ogr.FieldDefn('speed_100', ogr.OFTReal))


for i,row in enumerate(trinodes):
    val1 = -999
    pt = ogr.Geometry(ogr.wkbPoint)
    #Add 1st point to close ring
    pt.AddPoint(lon[i], lat[i])

    #Now add field values from array
    feat = ogr.Feature(lyr.GetLayerDefn())
    feat.SetGeometry(pt)
    feat.SetField('speed_100', float(speed_100[i]))

    lyr.CreateFeature(feat)
    feat.Destroy()
    pt.Destroy()

    val1 = -999 







#var is just a rdm string?
lyr.CreateField(ogr.FieldDefn('dir_100', ogr.OFTReal))


for i,row in enumerate(trinodes):
    val1 = -999
    pt = ogr.Geometry(ogr.wkbPoint)
    #Add 1st point to close ring
    pt.AddPoint(lon[i], lat[i])

    #Now add field values from array
    feat = ogr.Feature(lyr.GetLayerDefn())
    feat.SetGeometry(pt)
    feat.SetField('dir_100', float(dir_100[i]))

    lyr.CreateFeature(feat)
    feat.Destroy()
    pt.Destroy()

    val1 = -999
    
shapeData.Destroy()

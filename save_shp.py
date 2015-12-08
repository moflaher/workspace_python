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

save_poly_shp(data,'uvh','data/test/'+grid+'_depth.shp')




filename='data/test/'+grid+'_speed_dir_100.shp'
epsg_in=4326

lon = data['lon']
lat = data['lat']
trinodes = data['nv']
speed_100=speeder(data['ua'][100,:],data['va'][100,:])
dir_100=np.arctan2(data['va'][100,:],data['ua'][100,:])


driver = ogr.GetDriverByName('ESRI Shapefile')
shapeData = driver.CreateDataSource(filename)

spatialRefi = osr.SpatialReference()
spatialRefi.ImportFromEPSG(epsg_in)
lyr = shapeData.CreateLayer("poly_layer", spatialRefi, ogr.wkbPolygon )

#var is just a rdm string?
lyr.CreateField(ogr.FieldDefn('speed_100', ogr.OFTReal))

cnt = 0
for row in trinodes:
    val1 = -999
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for val in row:
        if val1 == -999:
            val1 = val
        ring.AddPoint(lon[val], lat[val])
    #Add 1st point to close ring
    ring.AddPoint(lon[val1], lat[val1])

    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)

    #Now add field values from array
    feat = ogr.Feature(lyr.GetLayerDefn())
    feat.SetGeometry(poly)
    feat.SetField(varLabel, float(var[cnt]))

    lyr.CreateFeature(feat)
    feat.Destroy()
    poly.Destroy()

    val1 = -999
    cnt += 1
    
shapeData.Destroy()
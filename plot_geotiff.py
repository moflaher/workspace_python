from osgeo import osr, gdal
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

gdal.UseExceptions()
ds = gdal.Open('data/misc/vhfr_obs/misc/3481_Geotiff.tif')
band = ds.GetRasterBand(1)
ct=band.GetColorTable()
elevation = ds.ReadAsArray()

## plot with indice values on the axes:
#import matplotlib.pyplot as plt
#plt.imshow(elevation, cmap='gist_earth')
#plt.show()

ncols=band.XSize
nrows=band.YSize
# plot with x,y values on the axes:
x0, dx, dxdy, y0, dydx, dy = ds.GetGeoTransform()
x1 = x0 + dx * ncols
y1 = y0 + dy * nrows
#plt.imshow(elevation, cmap='gist_earth', extent=[x0, x1, y1, y0])
#plt.show()

# But we really need lon/lat:
old_cs= osr.SpatialReference()
old_cs.ImportFromWkt(ds.GetProjectionRef())
# create the new coordinate system (This might not be exactly what we want to do because we know the reference system is NAD83 (Not WGS84) but I did a test and you get the lon,lat values that are given in the geotiff for the corners.
 
wgs84_wkt = """
GEOGCS["WGS 84",
    DATUM["WGS_1984",
        SPHEROID["WGS 84",6378137,298.257223563,
            AUTHORITY["EPSG","7030"]],
        AUTHORITY["EPSG","6326"]],
    PRIMEM["Greenwich",0,
        AUTHORITY["EPSG","8901"]],
    UNIT["degree",0.01745329251994328,
        AUTHORITY["EPSG","9122"]],
    AUTHORITY["EPSG","4326"]]"""
new_cs = osr.SpatialReference()
new_cs.ImportFromWkt(wgs84_wkt)

# create a transform object to convert between coordinate systems
transform = osr.CoordinateTransformation(old_cs,new_cs) 

#get the point to transform, pixel (0,0) in this case
width = ds.RasterXSize
height = ds.RasterYSize
gt = ds.GetGeoTransform()
minx = gt[0]
miny = gt[3] + width*gt[4] + height*gt[5] 
maxx = gt[0] + width*gt[1] + height*gt[2]
maxy = gt[3]  

#get the coordinates in lat long
latlongBL = transform.TransformPoint(minx,miny)
latlongBR = transform.TransformPoint(maxx,miny)
latlongTL = transform.TransformPoint(minx,maxy)
latlongTR = transform.TransformPoint(maxx,maxy) 

elevation2 = np.array(gt)

cb=np.array([])
for i in range(ct.GetCount()):
    cb=np.append(cb,ct.GetColorEntry(i)[:])
cb=cb.reshape(-1,4)

mycmap=LinearSegmentedColormap.from_list('my_colormap',cb[:13,:]/256,13)



plt.
# zoom in on our region
plt.axis([-123.18,-123.08,49.28,49.33])
plt.show()





from __future__ import division,print_function
import matplotlib as mpl
import scipy as sp
from datatools import *
from gridtools import *
from misctools import *
from plottools import *
from projtools import *
import interptools as ipt
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
from scipy.interpolate import interp1d
from matplotlib import patches as pp
from osgeo import osr, gdal
from matplotlib.colors import LinearSegmentedColormap

# Define names and types of data
#name='2012-02-01_2012-03-01_0.01_0.001'
name='sfm5m_sjr_basicrun'
grid='sfm5m_sjr'
datatype='2d'
regionname='stjohn_harbour'
region=regions(regionname)
starttime=0
endtime=24
useKnots=True

savepath='figures/timeseries/' + grid + '_' + datatype + '/enav_region/' + regionname + '/'
if not os.path.exists(savepath): os.makedirs(savepath)

### load the .nc file #####
data = loadnc('runs/'+grid+'/'+name+'/output/',singlename=grid + '_0001.nc')
print('done load')
data = ncdatasort(data)
print('done sort')

if useKnots:
    cv=1.9455252918287937
else:
    cv=1

#find spacing
dist=mdist([region['region'][0],region['region'][2]],[region['region'][1],region['region'][2]])
spacing=dist/20.0
vidx=equal_vectors(data,region,spacing)

srange=np.array([.1,.5,1,2,3,5,7,10,13,99])*0.514*cv
crange=np.array(['#7652e2','#4898d3','#61cbe5','#6dbc45','#b4dc00','#cdc100','#f8a718','#f7a29d','#ff1e1e'])

def load_geotiff(filename):
    
    gdal.UseExceptions()
    ds = gdal.Open(filename)
    band = ds.GetRasterBand(1)
    ct=band.GetColorTable()
    elevation = ds.ReadAsArray()

    cb=np.array([])
    for i in range(ct.GetCount()):
        cb=np.append(cb,ct.GetColorEntry(i)[:])
    cb=cb.reshape(-1,4)
    mycmap=LinearSegmentedColormap.from_list('my_colormap',cb[:13,:]/256,13)

    old_cs= osr.SpatialReference()
    old_cs.ImportFromWkt(ds.GetProjectionRef())

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
    
    extent=[latlongBL[0],latlongTR[0],latlongBL[1],latlongTR[1]]
    
    return elevation, mycmap, extent


def plot_vector_map(i):
    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])
    #prettyplot_ll(ax,setregion=region)
    #plotcoast(ax,filename='pacific_harbour.nc',color='None',fcolor='darkgreen',fill=True)
    ax.imshow(geotiff, cmap=cmap,vmax=13, extent=extent)
    

    ua=data['ua'][i,vidx]
    va=data['va'][i,vidx]
    
    for idx,u,v in zip(vidx,ua,va):
        x,y=data['uvnodell'][idx,:]
        dx=scale*u
        dy=scale*v
        al=np.sqrt(u**2+v**2)
        sl=np.sqrt(dx**2+dy**2)
        cidx=np.argwhere(al>=srange)
        if len(cidx) > 0:
            cidx=np.max(cidx)
            fcolor=crange[cidx]
        
        if al>=srange[0]:
            a=pp.FancyArrow(x,y,dx,dy,width_base=sl*.1,width_top=sl*.2,
                            head_length=sl*.35,head_width=sl*.4,
                            length_includes_head=True, edgecolor='None',
                            facecolor=fcolor)
            ax.add_artist(a)
    for label in ax.get_xticklabels()[::2]:
        label.set_visible(False)     
    prettyplot_ll(ax,setregion=region)   
      
    f.savefig(savepath + grid + '_enav_region_'+"{:06.6f}".format(data['time'][i])+'.png',dpi=300)
    plt.close(f)



geotiff, cmap, extent = load_geotiff('data/misc/vhfr_obs/misc/3481_Geotiff.tif')

idx=range(starttime,endtime)
ua=data['ua'][idx,:][:,vidx]
va=data['va'][idx,:][:,vidx]
s_vec=speeder(ua,va)
scale=((region['region'][1]-region['region'][0])*.0475)/s_vec.max()

for tt in range(starttime,endtime):
    print(tt)
    plot_vector_map(tt)


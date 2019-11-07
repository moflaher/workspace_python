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
import projtools as pjt
np.set_printoptions(precision=16,suppress=True,threshold=np.nan)
import pandas as pd
import netCDF4 as n4
import time as ttime
import ttide
import matplotlib.dates as dates

def runstats(datain=None):
    """Takes an array and returns basic stats on it. Max,Min,Mean,Std
    :Parameters:    
    """

    if datain==None:
        print('Need to pass in data array')
    else:
        maxval=np.nanmax(datain)
        minval=np.nanmin(datain)
        meanval=np.nanmean(datain)
        stdval=np.nanstd(datain)
        np.sum(np.isnan(datain))

        return maxval,minval,meanval,stdval,np.sum(np.isnan(datain))/np.size(datain)


def ne_fv(casename,h=False,is31=False):    
    depdata=gt.load_nodfile(casename+'.nod',h)
    grddata=gt.load_elefile(casename+'.ele')
    gt.save_grdfile(grddata,depdata,casename+'_grd.dat',is31)
    gt.save_depfile(depdata,casename+'_dep.dat',is31)


def dic_shape(indic):
    df=pd.DataFrame([str(np.shape(indic[key])) for key in indic.keys()],indic.keys())
    print(df)


def dic_shape2(d,parent=''):
    for k, v in d.iteritems():
        if isinstance(v, dict):
            if parent!='':
                k= '{} - {}'.format(parent,k)
            dic_shape2(v,k)
        else:
            if parent != '':
                print("{} - {} : {}".format(parent, k, np.shape(v)))
            else:
                print("{0} : {1}".format(k, np.shape(v)))



def dic_shape3(d,level=0):
    for k, v in d.iteritems():
        if isinstance(v, dict):
            print("    "*level + k+":")
            dic_shape3(v,level+1)
        else:
            print("    "*level +"{0} : {1}".format(k, np.shape(v)))


def speeder(ua,va):
    return np.sqrt(ua**2+va**2)


def myprint(d):
  """
    Print nested dictionaries in a readable manner.
    Code from Stack overflow - Scharron    
  """  
    
  for k, v in d.iteritems():
    if isinstance(v, dict):
      myprint(v)
    else:
      print("{0} : {1}".format(k, v))
      

def tg2csv(npyfile,outname):
    data=np.load(npyfile)
    data=data[()]

    mykeys=['00065','00060','00055','00053','00046']#,'00129']
    cons=['M2  ','N2  ','S2  ','K1  ','O1  ','M4  ']
    consout=['M2 A','M2 P','N2 A','N2 P','S2 A','S2 P','K1 A','K1 P','O1 A','O1 P','M4 A','M4 P']
    
    tidecon=np.empty((5,12))
    for i in range(5):
        for j in range(6):
            tidecon[i,2*j]=data[mykeys[i]]['df'].lookup([cons[j]],['Amp diff'])
            tidecon[i,(2*j)+1]=data[mykeys[i]]['df'].lookup([cons[j]],['Phase diff'])    

    df=pd.DataFrame(tidecon,columns=consout,index=mykeys)
    df.to_csv(outname)


def tg2csv_nodiff(npyfile,outname):
    data=np.load(npyfile)
    data=data[()]

    mykeys=['00065','00060','00055','00053','00046']#,'00129']
    cons=['M2  ','N2  ','S2  ','K1  ','O1  ','M4  ']
    consout=['M2 O','M2 M','M2 D','N2 O','N2 M','N2 D','S2 O','S2 M','S2 D','K1 O','K1 M','K1 D','O1 O','O1 M','O1 D','M4 O','M4 M','M4 D']
    
    tidecon=np.empty((5,18))
    for i in range(5):
        for j in range(6):
            idx=np.argwhere(data[mykeys[i]]['df'].index==cons[j])
            tidecon[i,3*j]=data[mykeys[i]]['wlevc'][idx,0]
            tidecon[i,(3*j)+1]=data[mykeys[i]]['outc'][idx,0]
            tidecon[i,(3*j)+2]=data[mykeys[i]]['df'].lookup([cons[j]],['Amp diff'])

    df=pd.DataFrame(tidecon,columns=consout,index=mykeys)
    df.to_csv(outname+'_amp.csv')


    tidecon=np.empty((5,18))
    for i in range(5):
        for j in range(6):
            idx=np.argwhere(data[mykeys[i]]['df'].index==cons[j])
            tidecon[i,3*j]=data[mykeys[i]]['wlevc'][idx,1]
            tidecon[i,(3*j)+1]=data[mykeys[i]]['outc'][idx,1]
            tidecon[i,(3*j)+2]=data[mykeys[i]]['df'].lookup([cons[j]],['Phase diff'])

    df=pd.DataFrame(tidecon,columns=consout,index=mykeys)
    df.to_csv(outname+'_phase.csv')


def checkrestart():
    import glob
    filenames=glob.glob('*restart*')
    filenames.sort()
    for filename in filenames:
        print(filename)
        data=dt.loadnc('',filename)
        print(data['zeta'][:,1000].max())
    print(data['Time'])
    print('='*30)
    
    
def boxminmax(arr):
    """
    Returns the min max for all columns of the array.
    """
    
    llmin = np.min(arr,axis=0)
    llmax = np.max(arr,axis=0)
    
    return [llmin[0], llmax[0], llmin[1], llmax[1]]


def run_ttide(time,zeta,lat,constitnames=None):
    
    if constitnames is None:
        out=ttide.t_tide(zeta,stime=time[0],dt=np.diff(time)[0]*24,synth=-1,out_style=None,lat=lat)
    else:
        out=ttide.t_tide(zeta,stime=time[0],dt=np.diff(time)[0]*24,synth=-1,out_style=None,lat=lat,constitnames=constitnames)

    return out


def save_adcpnc(adcp, filename):
    
    ncid = n4.Dataset(filename, 'w',format='NETCDF3_CLASSIC')

    #create dimensions
    ncid.createDimension('time',None)
    ncid.createDimension('ndepth',len(adcp['h']*adcp['siglay']))
    ncid.createDimension('one',1) 
    ncid.createDimension('DateStrLen',19)

    #define variables 
    cast = ncid.createVariable('adcpnumber','i',('one',))  
    lon = ncid.createVariable('lon','d',('one',))
    lat = ncid.createVariable('lat','d',('one',))
    h = ncid.createVariable('h','d',('one',))
    dist = ncid.createVariable('dist','d',('one',))
    time = ncid.createVariable('time','d',('time',))
    timestamp = ncid.createVariable('Times','c',('time','DateStrLen'))
    bins = ncid.createVariable('bins','d',('ndepth',))
    siglay = ncid.createVariable('siglay','d',('ndepth',))
    u = ncid.createVariable('u','d',('time','ndepth'))
    v = ncid.createVariable('v','d',('time','ndepth'))
    ww = ncid.createVariable('ww','d',('time','ndepth'))
    ua = ncid.createVariable('ua','d',('time',))
    va = ncid.createVariable('va','d',('time',))
    zeta = ncid.createVariable('zeta','d',('time',))    
       
    
    cast[:] = adcp['ADCP_number']   
    cast.__setattr__('long_name','ADCP Deployment Number matched to model location')
    
    lon[:] = adcp['lon']
    lon.__setattr__('long_name','Longitude')
    lon.__setattr__('units','degrees')   
    
    lat[:] = adcp['lat']   
    lat.__setattr__('long_name','latitude')
    lat.__setattr__('units','degrees')  
      
    time[:] = adcp['time']
    time.__setattr__('long_name','time')
    time.__setattr__('units','days')
    time.__setattr__('comments','python datenum')  
      
    tstr=dates.num2date(dates.datestr2num(adcp['Time']))
    tnew=np.array([ t.strftime('%Y-%m-%dT%H:%M:%S') for t in tstr])
    timestamp[:]=np.array([list(tt) for tt in tnew])[:]
    timestamp.__setattr__('long_name','Time string')
    timestamp.__setattr__('units','yyyy-mm-dd HH:MM:SS')   
            
    bins[:]=adcp['h']*adcp['siglay']    
    bins.__setattr__('long_name','Level Depth')
    bins.__setattr__('units','meters') 
    
    siglay[:]=adcp['siglay']    
    siglay.__setattr__('long_name','Siglay')
    
    h[:]=adcp['h']   
    h.__setattr__('long_name','Depth')
    h.__setattr__('units','meters') 
    
    dist[:]=adcp['dist']   
    dist.__setattr__('long_name','Distance between obs and model')
    dist.__setattr__('units','meters') 
    
    u[:] = adcp['u']   
    u.__setattr__('long_name','Eastward Water Velocity')
    u.__setattr__('units','meters s-1') 
    
    v[:] = adcp['v']  
    v.__setattr__('long_name','Northward Water Velocity')
    v.__setattr__('units','meters s-1') 
     
    ww[:] = adcp['ww']  
    ww.__setattr__('long_name','Upward Water Velocity')
    ww.__setattr__('units','meters s-1') 
     
    ua[:] = adcp['ua']   
    ua.__setattr__('long_name','Depth-Averaged Eastward Water Velocity')
    ua.__setattr__('units','meters s-1') 
    
    va[:] = adcp['va']  
    va.__setattr__('long_name','Depth-Averaged Northward Water Velocity')
    va.__setattr__('units','meters s-1') 
           
    zeta[:] = adcp['zeta']   
    zeta.__setattr__('long_name','Water Elevation')
    zeta.__setattr__('units','meters') 

    ncid.__setattr__('type','ADCP-like ncfile')
    ncid.__setattr__('history','Created ' +ttime.ctime(ttime.time()) )

    ncid.close()    


def save_tgnc(tg, filename):
    
    ncid = n4.Dataset(filename, 'w',format='NETCDF3_CLASSIC')

    #create dimensions
    ncid.createDimension('time',None)
    ncid.createDimension('one',1) 
    ncid.createDimension('DateStrLen',19)

    #define variables 
    cast = ncid.createVariable('tgnumber','i',('one',))  
    lon = ncid.createVariable('lon','d',('one',))
    lat = ncid.createVariable('lat','d',('one',))
    h = ncid.createVariable('h','d',('one',))
    dist = ncid.createVariable('dist','d',('one',))
    time = ncid.createVariable('time','d',('time',))
    timestamp = ncid.createVariable('Times','c',('time','DateStrLen'))
    zeta = ncid.createVariable('zeta','d',('time',))    
       
    
    cast[:] = tg['tg_number']   
    cast.__setattr__('long_name','TG Deployment Number matched to model location')
    
    lon[:] = tg['lon']
    lon.__setattr__('long_name','Longitude')
    lon.__setattr__('units','degrees')   
    
    lat[:] = tg['lat']   
    lat.__setattr__('long_name','latitude')
    lat.__setattr__('units','degrees')  
      
    time[:] = tg['time']
    time.__setattr__('long_name','time')
    time.__setattr__('units','days')
    time.__setattr__('comments','python datenum')  
      
    tstr=dates.num2date(dates.datestr2num(tg['Time']))
    tnew=np.array([ t.strftime('%Y-%m-%dT%H:%M:%S') for t in tstr])
    timestamp[:]=np.array([list(tt) for tt in tnew])[:]
    timestamp.__setattr__('long_name','Time string')
    timestamp.__setattr__('units','yyyy-mm-dd HH:MM:SS')   
            
    h[:]=tg['h']   
    h.__setattr__('long_name','Depth')
    h.__setattr__('units','meters') 
    
    dist[:]=tg['dist']   
    dist.__setattr__('long_name','Distance between obs and model')
    dist.__setattr__('units','meters') 
               
    zeta[:] = tg['zeta']   
    zeta.__setattr__('long_name','Water Elevation')
    zeta.__setattr__('units','meters') 

    ncid.__setattr__('type','TG-like ncfile')
    ncid.__setattr__('history','Created ' +ttime.ctime(ttime.time()) )

    ncid.close()    


def save_wlevnc(wlev, filename):
    
    ncid = n4.Dataset(filename, 'w',format='NETCDF3_CLASSIC')

    #create dimensions
    ncid.createDimension('time',None)
    ncid.createDimension('one',1) 
    ncid.createDimension('four',4) 
    ncid.createDimension('DateStrLen',19)
    ncid.createDimension('allnamelen',len(wlev['ttideall']['nameu']))
    ncid.createDimension('rnamelen',len(wlev['rtide']['0']['nameu']))

    #define variables 
    cast = ncid.createVariable('wlevnumber','i',('one',))  
    lon = ncid.createVariable('lon','d',('one',))
    lat = ncid.createVariable('lat','d',('one',))
    h = ncid.createVariable('h','d',('one',))
    dist = ncid.createVariable('dist','d',('one',))
    snr = ncid.createVariable('snr','d',('one',))
    time = ncid.createVariable('time','d',('time',))
    timestamp = ncid.createVariable('Times','c',('time','DateStrLen'))    
    zeta = ncid.createVariable('zeta','d',('time',))    
    
    all_name = ncid.createVariable('all_name','c',('allnamelen','four'))
    all_freq = ncid.createVariable('all_freq','d',('allnamelen',))
    all_tidecon = ncid.createVariable('all_tidecon','d',('allnamelen','four')) 
    all_z0 = ncid.createVariable('all_z0','d',('one',)) 
    
    mmm_name = ncid.createVariable('min_name','c',('rnamelen','four'))
    mmm_freq = ncid.createVariable('min_freq','d',('rnamelen',))
    
    min_tidecon = ncid.createVariable('min_tidecon','d',('rnamelen','four')) 
    min_z0 = ncid.createVariable('min_z0','d',('one',)) 

    max_tidecon = ncid.createVariable('max_tidecon','d',('rnamelen','four')) 
    max_z0 = ncid.createVariable('max_z0','d',('one',))
    
    mean_tidecon = ncid.createVariable('mean_tidecon','d',('rnamelen','four')) 
    mean_z0 = ncid.createVariable('mean_z0','d',('one',))
    
    
    cast[:] = wlev['wlev_number']   
    cast.__setattr__('long_name','Wlev Deployment Number matched to model location')
    
    lon[:] = wlev['lon']
    lon.__setattr__('long_name','Longitude')
    lon.__setattr__('units','degrees')   
    
    lat[:] = wlev['lat']   
    lat.__setattr__('long_name','latitude')
    lat.__setattr__('units','degrees')  
      
    time[:] = wlev['time']
    time.__setattr__('long_name','time')
    time.__setattr__('units','days')
    time.__setattr__('comments','python datenum')  
      
    tstr=dates.num2date(dates.datestr2num(wlev['Time']))
    tnew=np.array([ t.strftime('%Y-%m-%dT%H:%M:%S') for t in tstr])
    timestamp[:]=np.array([list(tt) for tt in tnew])[:]
    timestamp.__setattr__('long_name','Time string')
    timestamp.__setattr__('units','yyyy-mm-dd HH:MM:SS')   
            
    h[:]=wlev['h']   
    h.__setattr__('long_name','Depth')
    h.__setattr__('units','meters') 
    
    dist[:]=wlev['dist']   
    dist.__setattr__('long_name','Distance between obs and model')
    dist.__setattr__('units','meters') 
               
    snr[:]=wlev['snr']   
    snr.__setattr__('long_name','Signal to noise ratio for tidal constituent cutoff')

    zeta[:] = wlev['zeta']   
    zeta.__setattr__('long_name','Water Elevation')
    zeta.__setattr__('units','meters') 
    
    all_name[:] = np.array([list(name) for name in wlev['ttideall']['nameu']])
    all_name.__setattr__('long_name','Names of tidal contituents for entire run')

    all_freq[:] = wlev['ttideall']['fu']
    all_freq.__setattr__('long_name','Frequencies of tidal contituents for entire run')
    
    all_tidecon[:] = wlev['ttideall']['tidecon']
    all_tidecon.__setattr__('long_name','Results of tidal contituents analysis for entire run')
    all_tidecon.__setattr__('units','meters and degrees')
    all_tidecon.__setattr__('comments','amp amp_err phase phase_err')
    
    all_z0[:] =wlev['ttideall']['z0']
    all_z0.__setattr__('long_name','Mean offset (z0) for entire run')
    all_z0.__setattr__('units','meters')
    
    
    rtide=np.stack([wlev['rtide'][key]['tidecon'] for key in wlev['rtide']])    
    rz0=np.stack([wlev['rtide'][key]['z0'] for key in wlev['rtide']])
    
    mmm_name[:] = np.array([list(name) for name in wlev['rtide']['0']['nameu']])
    mmm_name.__setattr__('long_name','Names of tidal contituents for wlev length runs')

    mmm_freq[:] = wlev['rtide']['0']['fu']
    mmm_freq.__setattr__('long_name','Frequencies of tidal contituents for wlev length runs')
    
    min_tidecon[:] = rtide.min(axis=0)
    min_tidecon.__setattr__('long_name','Results of tidal contituents analysis for wlev length run (min)')
    min_tidecon.__setattr__('units','meters and degrees')
    min_tidecon.__setattr__('comments','amp amp_err phase phase_err')
    
    min_z0[:] = rz0.min(axis=0)
    min_z0.__setattr__('long_name','Mean offset (z0) for wlev length run (min)')
    min_z0.__setattr__('units','meters')
    
    max_tidecon[:] = rtide.max(axis=0)
    max_tidecon.__setattr__('long_name','Results of tidal contituents analysis for wlev length run (max)')
    max_tidecon.__setattr__('units','meters and degrees')
    max_tidecon.__setattr__('comments','amp amp_err phase phase_err')
    
    max_z0[:] = rz0.max(axis=0)
    max_z0.__setattr__('long_name','Mean offset (z0) for wlev length run (max)')
    max_z0.__setattr__('units','meters')
    
    mean_tidecon[:] = rtide.mean(axis=0)
    mean_tidecon.__setattr__('long_name','Results of tidal contituents analysis for wlev length run (mean)')
    mean_tidecon.__setattr__('units','meters and degrees')
    mean_tidecon.__setattr__('comments','amp amp_err phase phase_err')
    
    mean_z0[:] = rz0.mean(axis=0)
    mean_z0.__setattr__('long_name','Mean offset (z0) for wlev length run (mean)')
    mean_z0.__setattr__('units','meters')

    ncid.__setattr__('type','Wlev-like ncfile')
    ncid.__setattr__('history','Created ' +ttime.ctime(ttime.time()) )

    ncid.close()    



def save_ctdnc(ctd, filename):
    
    ncid = n4.Dataset(filename, 'w',format='NETCDF3_CLASSIC')

    #create dimensions
    ncid.createDimension('time',None)
    ncid.createDimension('ndepth',len(ctd['h']*ctd['siglay']))
    ncid.createDimension('one',1) 
    ncid.createDimension('DateStrLen',19)

    #define variables 
    cast = ncid.createVariable('ctdnumber','i',('one',))  
    lon = ncid.createVariable('lon','d',('one',))
    lat = ncid.createVariable('lat','d',('one',))
    h = ncid.createVariable('h','d',('one',))
    dist = ncid.createVariable('dist','d',('one',))
    time = ncid.createVariable('time','d',('time',))
    timestamp = ncid.createVariable('Times','c',('time','DateStrLen'))
    bins = ncid.createVariable('bins','d',('ndepth',))
    siglay = ncid.createVariable('siglay','d',('ndepth',))
    temp = ncid.createVariable('temp','d',('time','ndepth'))
    sal = ncid.createVariable('salinity','d',('time','ndepth'))
    zeta = ncid.createVariable('zeta','d',('time',))    
       
    
    cast[:] = ctd['CTD_number']   
    cast.__setattr__('long_name','CTD Deployment Number matched to model location')
    
    lon[:] = ctd['lon']
    lon.__setattr__('long_name','Longitude')
    lon.__setattr__('units','degrees')   
    
    lat[:] = ctd['lat']   
    lat.__setattr__('long_name','latitude')
    lat.__setattr__('units','degrees')  
      
    time[:] = ctd['time']
    time.__setattr__('long_name','time')
    time.__setattr__('units','days')
    time.__setattr__('comments','python datenum')  
      
    tstr=dates.num2date(dates.datestr2num(ctd['Time']))
    tnew=np.array([ t.strftime('%Y-%m-%dT%H:%M:%S') for t in tstr])
    timestamp[:]=np.array([list(tt) for tt in tnew])[:]
    timestamp.__setattr__('long_name','Time string')
    timestamp.__setattr__('units','yyyy-mm-dd HH:MM:SS')   
            
    bins[:]=ctd['h']*ctd['siglay']    
    bins.__setattr__('long_name','Level Depth')
    bins.__setattr__('units','meters') 
    
    siglay[:]=ctd['siglay']    
    siglay.__setattr__('long_name','Siglay')
    
    h[:]=ctd['h']   
    h.__setattr__('long_name','Depth')
    h.__setattr__('units','meters') 
    
    dist[:]=ctd['dist']   
    dist.__setattr__('long_name','Distance between obs and model')
    dist.__setattr__('units','meters') 
    
    temp[:] = ctd['temp']   
    temp.__setattr__('long_name','Temperature')
    temp.__setattr__('units','degrees') 
    
    sal[:] = ctd['salinity']  
    sal.__setattr__('long_name','Salinity')
    sal.__setattr__('units','PSU') 
               
    zeta[:] = ctd['zeta']   
    zeta.__setattr__('long_name','Water Elevation')
    zeta.__setattr__('units','meters') 

    ncid.__setattr__('type','CTD-like ncfile')
    ncid.__setattr__('history','Created ' +ttime.ctime(ttime.time()) )

    ncid.close()    
    
    
def gencirc(rad):
    '''Generate a circle from a radius.
    '''    
    s=.0025    
    x=rad*np.cos(2*np.pi*np.arange(0,1+s,s))
    y=rad*np.sin(2*np.pi*np.arange(0,1+s,s))

    return x,y


def gencages(ll,rad):
    '''Generate circles for cages.
    '''
    
    ll=np.atleast_2d(ll)
    
    x,y,proj=pjt.lcc(ll[:,0],ll[:,1])
    
    xt,yt=gencirc(rad)
    xl=np.array([]); yl=np.array([])
    for i in range(len(x)):
        xl=np.append(xl,x[i]+xt)
        yl=np.append(yl,y[i]+yt)
        xl=np.append(xl,np.nan)
        yl=np.append(yl,np.nan)
        

    lon,lat=proj(xl,yl,inverse=True)
    
    lon[lon>1e20]=np.nan
    lat[lat>1e20]=np.nan

    return lon,lat


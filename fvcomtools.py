from __future__ import division,print_function
import os, sys, time
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
np.set_printoptions(precision=16,suppress=True,threshold=np.nan)

from scipy.io import netcdf





################################################################################
#
# Code to load FVCOM input files
#
################################################################################

def _load_grdfile(casename=None):
    """
    Loads an FVCOM grd input file and returns the data as a dictionary. 
    """
    
    data={}    

    if casename==None:
        print('_load_grdfile requires a filename to load.')
        return
    try:
        fp=open(casename+'_grd.dat','r')
    except IOError:
        print('_load_grdfiles: invalid case name.')
        return data

    nodes_str=fp.readline().split('=')
    elements_str=fp.readline().split('=')
    nnodes=int(nodes_str[1])
    nele=int(elements_str[1])
    t_data1=np.genfromtxt(casename+'_grd.dat',skip_header=2, skip_footer=nnodes,dtype='int64')
    t_data2=np.genfromtxt(casename+'_grd.dat',skip_header=2+nele,dtype='float64')
    fp.close()

    data['nnodes']=nnodes
    data['nele']=nele
    data['nodexy']=t_data2[:,1:3]
    data['x']=t_data2[:,1]
    data['y']=t_data2[:,2]
    data['nv']=t_data1[:,1:4].astype(int)-1
    data['trigridxy'] = mplt.Triangulation(data['x'], data['y'],data['nv'])
    
    return data


def _load_depfile(casename=None):
    """
    Loads an FVCOM dep input file and returns the data as a dictionary. 
    """

    data={}
    
    if casename==None:
        print('_load_depfile requires a filename to load.')
        return
    try:
        fp=open(casename+'_dep.dat','r')
    except IOError:
        print('_load_depfile: invalid case name.')
        return data

    dep_str=fp.readline().split('=')
    dep_num=int(dep_str[1])
    t_data1=np.genfromtxt(casename+'_dep.dat',skip_header=1)
    fp.close()

    data['dep_num']=dep_num
    data['x']=t_data1[:,0]
    data['y']=t_data1[:,1]
    data['h']=t_data1[:,2]
    data['nodexy']=t_data1[:,0:2]
    
    return data


def _load_spgfile(casename=None):
    """
    Loads an FVCOM spg input file and returns the data as a dictionary. 
    """

    data={}
    
    if casename==None:
        print('_load_spgfile requires a filename to load.')
        return
    try:
        fp=open(casename+'_spg.dat','r')
    except IOError:
        print('_load_spgfile: invalid case name.')
        return data

    spg_str=fp.readline().split('=')
    spg_num=int(spg_str[1])
    t_data1=np.genfromtxt(casename+'_spg.dat',skip_header=1)
    fp.close()

    data['spgf_num']=spg_num
    data['spgf_nodes']=t_data1[:,0]
    data['spgf_distance']=t_data1[:,1]
    data['spgf_value']=t_data1[:,2]

    
    return data


def _load_obcfile(casename=None):
    """
    Loads an FVCOM obc input file and returns the data as a dictionary. 
    """    

    data={}

    if casename==None:
        print('_load_obcfile requires a filename to load.')
        return
    try:
        fp=open(casename+'_obc.dat','r')
    except IOError:
        print('_load_obcfile: invalid case name.')
        return data

    obc_str=fp.readline().split('=')
    obc_num=int(obc_str[1])
    t_data1=np.genfromtxt(casename+'_obc.dat',skip_header=1)
    fp.close()

    data['obcf_num']=obc_num
    data['obcf_numbers']=t_data1[:,0]
    data['obcf_nodes']=t_data1[:,1]
    data['obcf_value']=t_data1[:,2]

    
    return data
    
    
def _load_llfiles(casename=None):
    """
    Loads an long/lat files and returns the data as a dictionary. 
    """

    data={}
    
    if casename==None:
        print('_load_llfiles requires a filename to load.')
        return
    try:
        fp=open(casename+'_long.dat','r')
    except IOError:
        print('_load_llfiles: long file is invalid.')
        return data

    lon=np.genfromtxt(casename+'_long.dat')
    fp.close()

    try:
        fp=open(casename+'_lat.dat','r')
    except IOError:
        print('_load_llfiles: lat file is invalid.')
        return data

    lat=np.genfromtxt(casename+'_lat.dat')
    fp.close()

    data['nodell']=np.vstack([lon,lat]).T
    data['lat']=lat
    data['lon']=lon
    
    return data


def _load_nc(filename=None):
    """
    Loads an .nc  data file      
    """

    ncid = netcdf.netcdf_file(filename, 'r',mmap=True)
    
    data={}

    for i in ncid.variables.keys():
        data[i]=ncid.variables[i].data

    return data


def load_fvcom_files(filepath=None,casename=None,ncname=None,neifile=None):
    """
    Loads FVCOM input files and returns the data as a dictionary. 
    """

    currdir=os.getcwd()
    os.chdir(filepath)

    data=_load_grdfile(casename)

    data.update(_load_depfile(casename))
    
    data.update(_load_spgfile(casename))

    data.update(_load_obcfile(casename))

    data.update(_load_llfiles(casename))

    if ncname!=None:
        data.update(_load_nc(ncname))

    if neifile!=None:
        data.update(loadnei(neifile))

    os.chdir(currdir)

    return data
    
    
def load_cage(filepath):
    cages=None
    try:
        with open(filepath) as f_in:
            cages=np.genfromtxt(f_in,skip_header=1)
            if len(cages)>0:
                cages=(cages[:,0]-1).astype(int)
            else:
                cages=None
    except:
        cages=None

    return cages
    
    
def load_rivfile(filename=None):
    """
    Loads an FVCOM riv input file and returns the data as a dictionary. 
    """    

    data={}

    if filename==None:
        print('load_rivfile requires a filename to load.')
        return
    try:
        fp=open(filename,'r')
    except IOError:
        print('load_rivfile: invalid filename.')
        return data
    
    data['RIVER_NAME']=''
    data['RIVER_GRID_LOCATION']=0
    data['RIVER_VERTICAL_DISTRIBUTION']=''


    for line in fp:
        if line.strip().startswith('RIVER_NAME'):
            data['RIVER_NAME']=np.append(data['RIVER_NAME'],line[line.find('"')+1:line.rfind('"')])
        if line.strip().startswith('RIVER_GRID_LOCATION'):
            data['RIVER_GRID_LOCATION']=np.append(data['RIVER_GRID_LOCATION'],int(line[line.find('=')+1:line.rfind(',')]))
        if line.strip().startswith('RIVER_VERTICAL_DISTRIBUTION'):
            data['RIVER_VERTICAL_DISTRIBUTION']=np.append(data['RIVER_VERTICAL_DISTRIBUTION'],line[line.find('"')+1:line.rfind('"')])

    data['RIVER_NAME']=np.delete(data['RIVER_NAME'],0)
    data['RIVER_GRID_LOCATION']=np.delete(data['RIVER_GRID_LOCATION'],0)
    data['RIVER_VERTICAL_DISTRIBUTION']=np.delete(data['RIVER_VERTICAL_DISTRIBUTION'],0)

    
    return data
    
    
def load_stationfile(filename=None):
    """
    Loads an FVCOM station input file and returns the data as a dictionary. 
    """
    
    data={}    

    if filename==None:
        print('load_stationfile requires a filename to load.')
        return
    try:
        fp=open(filename,'r')
    except IOError:
        print('load_stationfile: invalid filename.')
        return data

    headerstr=fp.readline()
    data_str=np.genfromtxt(filename,skip_header=1,dtype=str)
    fp.close()

    data['header']=headerstr
    data['station_num']=data_str[:,0].astype(np.int32)
    data['cell']=data_str[:,3].astype(np.int32)
    data['x']=data_str[:,1].astype(np.float64)
    data['y']=data_str[:,2].astype(np.float64)
    data['h']=data_str[:,4].astype(np.float64)
    data['station_name'] = data_str[:,5]
    
    return data
    
################################################################################
#
# Code to save FVCOM input files
#
################################################################################

def save_spgfile(datain,filepath,casename=None):
    """
    Save an FVCOM spg input file. 
    """

    data={}
    
    if casename==None:
        print('save_spgfile requires a filename to save.')
        return
    try:
        fp=open(filepath + casename+'_spg.dat','w')
    except IOError:
        print('save_spgfile: invalid case name.')
        return data

    fp.write('Sponge Node Number = %d\n' % datain['spgf_num'] )
    for i in range(0,datain['spgf_num']):
        fp.write('%d %f %f\n'% (datain['spgf_nodes'][i],datain['spgf_distance'][i],datain['spgf_value'][i]))
    fp.close()


def save_obcfile(datain,filepath,casename=None):
    """
    Save an FVCOM obc input file. 
    """

    data={}
    
    if casename==None:
        print('save_obcfile requires a filename to save.')
        return
    try:
        fp=open(filepath + casename+'_obc.dat','w')
    except IOError:
        print('save_obcfile: invalid case name.')
        return data

    fp.write('OBC Node Number = %d\n' % datain['obcf_num'] )
    for i in range(0,datain['obcf_num']):
        fp.write('%d %d %d\n'% (datain['obcf_numbers'][i],datain['obcf_nodes'][i],datain['obcf_value'][i]))
    fp.close()

def save_grdfile(grddata,depdata,outname,is31=True):
    """
    Save an FVCOM grd input file. 
    """
    
    if outname==None:
        print('save_grdfile requires a filename to save.')
        return
    try:
        fp=open(outname,'w')
    except IOError:
        print('save_grdfile: invalid filename.')
        return data
    if is31:
        fp.write('Node Number = %d\n' % len(depdata['node_num']) )
        fp.write('Cell Number = %d\n' % len(grddata['nv']) )
    for i in range(0,len(grddata['nv'])):
        fp.write('%d %d %d %d %d\n'% (grddata['ele_num'][i],grddata['nv'][i,0],grddata['nv'][i,1],grddata['nv'][i,2],0))

    for i in range(0,len(depdata['node_num'])):
        fp.write('%d %f %f %f\n'% (depdata['node_num'][i],depdata['x'][i],depdata['y'][i],depdata['h'][i]))
    fp.close()
   
    return 


def save_depfile(depdata,outname,is31=True):
    """
    Save an FVCOM dep input file. 
    """  

    if outname==None:
        print('save_depfile requires a filename to save.')
        return
    try:
        fp=open(outname,'w')
    except IOError:
        print('save_depfile: invalid filename.')
        return data
    if is31:
        fp.write('Node Number = %d\n' % len(depdata['node_num']) )
    for i in range(0,len(depdata['node_num'])):
        fp.write('%f %f %f\n'% (depdata['x'][i],depdata['y'][i],depdata['h'][i]))
    fp.close()
   
    return 


def save_rivfile(rivdata,filename=None):
    """
    Saves an FVCOM riv input file. 
    """    

    data={}

    if filename==None:
        print('save_rivfile requires a filename to save.')
        return
    try:
        fp=open(filename,'w')
    except IOError:
        print('save_rivfile: invalid filename.')
        return data
    
    for i in range(len(rivdata['RIVER_NAME'])):
        block='''&NML_RIVER
        RIVER_NAME          = "{0}",
        RIVER_GRID_LOCATION = {1},
        RIVER_VERTICAL_DISTRIBUTION = "{2}" / '''.format(rivdata['RIVER_NAME'][i],rivdata['RIVER_GRID_LOCATION'][i],rivdata['RIVER_VERTICAL_DISTRIBUTION'][i])    

        print >> fp, block
     

def save_stationfile(sdata,outname):
    """
    Save an FVCOM station input file. 
    """
    
    if outname==None:
        print('save_stationfile requires a filename to save.')
        return
    try:
        fp=open(outname,'w')
    except IOError:
        print('save_stationfile: invalid filename.')
        return data
        

    fp.write('%s' % " No           X        Y      Node (Cell)        Station Name\n" )        
    for i in range(0,len(sdata['x'])):
        fp.write('%d %f %f %d %f %s\n'% (sdata['station_num'][i],sdata['x'][i],sdata['y'][i],sdata['cell'][i],sdata['h'][i],sdata['station_name'][i] )   )

    fp.close()

   
    return 
    
       
    
def save_elobc(elobc,outname):
    
    try:
        import netCDF4 as n4
    except ImportError:
        print("netCDF4 is not installed, please install netCDF4.")
        return

    ncid = n4.Dataset(outname, 'w',format='NETCDF3_CLASSIC')


    #create dimensions
    ncid.createDimension('nobc',len(elobc['obc_nodes']))
    ncid.createDimension('tidal_components',len(elobc['tide_period'])) 
    ncid.createDimension('TideLen',np.shape(elobc['equilibrium_tide_type'])[1])
    ncid.createDimension('DateStrLen',len(elobc['time_origin']))

    #define variables
    obc_nodes = ncid.createVariable('obc_nodes','i4',('nobc',))    
    tide_period = ncid.createVariable('tide_period','f',('tidal_components',))
    tide_Eref = ncid.createVariable('tide_Eref','f',('nobc',))
    tide_Ephase = ncid.createVariable('tide_Ephase','f',('tidal_components','nobc'))
    tide_Eamp = ncid.createVariable('tide_Eamp','f',('tidal_components','nobc'))
    equilibrium_tide_Eamp = ncid.createVariable('equilibrium_tide_Eamp','f',('tidal_components',))
    equilibrium_beta_love = ncid.createVariable('equilibrium_beta_love','f',('tidal_components',))
    equilibrium_tide_type = ncid.createVariable('equilibrium_tide_type','c',('tidal_components','TideLen'))
    time_origin = ncid.createVariable('time_origin','c',('DateStrLen',))

    obc_nodes[:] = elobc['obc_nodes']   
    obc_nodes.__setattr__('long_name','Open Boundary Node Number')
    obc_nodes.__setattr__('grid','obc_grid')
    
    tide_period[:] = elobc['tide_period']
    tide_period.__setattr__('long_name','tide angular period')
    tide_period.__setattr__('units','seconds')
    
    tide_Eref[:] = elobc['tide_Eref']
    tide_Eref.__setattr__('long_name','tidal elevation reference level')
    tide_Eref.__setattr__('units','meters')
    
    tide_Ephase[:] = elobc['tide_Ephase']
    tide_Ephase.__setattr__('long_name','tidal elevation phase angle')
    tide_Ephase.__setattr__('units','degrees, time of maximum elevation with respect to chosen time origin')
    
    tide_Eamp[:] = elobc['tide_Eamp']
    tide_Eamp.__setattr__('long_name','tidal elevation amplitude')
    tide_Eamp.__setattr__('units','meters')
    
    equilibrium_tide_Eamp[:] = elobc['equilibrium_tide_Eamp']
    equilibrium_tide_Eamp.__setattr__('long_name','equilibrium tidal elevation amplitude')
    equilibrium_tide_Eamp.__setattr__('units','meters')
    
    equilibrium_beta_love[:] = elobc['equilibrium_beta_love']
    equilibrium_beta_love.__setattr__('formula','beta=1+klove-hlove')
    
    equilibrium_tide_type[:] = elobc['equilibrium_tide_type']
    equilibrium_tide_type.__setattr__('long_name','formula')
    equilibrium_tide_type.__setattr__('units','beta=1+klove-hlove')
    
    time_origin[:] = elobc['time_origin']
    time_origin.__setattr__('long_name','time')
    time_origin.__setattr__('units','yyyy-mm-dd HH:MM:SS')
    time_origin.__setattr__('time_zone','UTC')
    time_origin.__setattr__('comments','tidal harmonic origin_date')
        
    ncid.__setattr__('type','FVCOM SPECTRAL ELEVATION FORCING FILE')
    ncid.__setattr__('history','Created ' +time.ctime(time.time()) )

    ncid.close()    
    
def save_cagefile(filename=None,nodes=None,drag=None,depth=None):
    """
    Saves a fvcom cage file. 
    """
    #Check for filename and open, catch expection if it can't create file.
    if filename==None:
        print('fvcom_savecage requires a filename to save.')
        return
    try:
        fp=open(filename,'w')
    except IOError:
        print('Can''t make ' + filename)
        return

    #Make sure all arrays were given
    if ((nodes==None) or (drag==None) or (depth==None)):
        print('Need to gives arrays of nodes,drag, and depth.')
        fp.close()
        return
    #Make sure they are all the same size
    if ((nodes.size!=drag.size) or (nodes.size!=depth.size)):
        print('Arrays are not the same size.')
        fp.close()
        return 
    #Make sure that the arrays are single columns or rank 1. If not then transpose them.
    #Check if the transposed arrays are the same as size, if not then they have more then one column/row so exit
    if (nodes.shape[0]<nodes.size):
        nodes=nodes.T
        drag=drag.T
        depth=depth.T
        if (nodes.shape[0]<nodes.size):  
            fp.close()
            return     
  
    fp.write('%s %d\n' % ('CAGE Node Number = ',np.max(nodes.shape) ) )

    for i in range(0,len(nodes)):
        fp.write('%d %f %f\n' % (nodes[i],drag[i],depth[i]) )

    
    fp.close()

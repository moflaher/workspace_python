from scipy.io import netcdf
import numpy as np

infile=netcdf.netcdf_file('multi_5_z0.nc')
outfile = netcdf.netcdf_file('5dTide.nc', 'w')

outfile.components=infile.components.replace('O1','O1 D5')
outfile.title='Spectral forcing data 5 Constituents plus long term period'
outfile.history='Added long term period to multi_5_z0.nc'
outfile.type=infile.type


outfile.createDimension( 'nobc', infile.variables['obc_nodes'].data.shape[0] )
outfile.createDimension( 'DateStrLen', 26 )
outfile.createDimension( 'tidal_components', 6 )

# Create and write the obc_nodes variable
data = outfile.createVariable('obc_nodes',np.dtype(np.int32).char,('nobc',))
data[:] = infile.variables['obc_nodes'].data
# Add attributes for the variables to be a CF compliance netcdf file
data.long_name='Open Boundary Node Number' 
data.grid='obc_grid' 

data = outfile.createVariable('tide_period',np.dtype(np.float32).char,('tidal_components',))
data[:] = np.append(infile.variables['tide_period'].data,432000)
data.long_name='tide angular period' 
data.units='seconds' 

# Create and write the 
idx=np.where(infile.variables['tide_Eref'].data==.1)[0]
amps=np.vstack([infile.variables['tide_Eamp'].data,np.zeros((1,infile.variables['obc_nodes'].data.shape[0]))])
amps[5,idx]=.1
data = outfile.createVariable('tide_Eamp',np.dtype(np.float32).char,('tidal_components','nobc',))
data[:] = amps
data.long_name='tidal elevation amplitude' 
data.units='meters'

# Create and write the 
phases=np.vstack([infile.variables['tide_Ephase'].data,np.zeros((1,infile.variables['obc_nodes'].data.shape[0]))])
data = outfile.createVariable('tide_Ephase',np.dtype(np.float32).char,('tidal_components','nobc',))
data[:] = phases
data.long_name='tidal elevation phase angle'
data.units='degrees, time of maximum elevation with respect to chosen time origin' 



# Create and write the tidal elevation reference level
dtmp = np.zeros( infile.variables['obc_nodes'].data.shape[0], dtype=np.float32 )
data = outfile.createVariable('tide_Eref',np.dtype(np.float32).char,('nobc',))
data[:] = dtmp
data.long_name='tidal elevation reference level' 
data.units='meters'

# Create and write the equilibrium tide amplitude
dtmp = np.zeros( 6, dtype=np.float32 )
data = outfile.createVariable('equilibrium_tide_Eamp',np.dtype(np.float32).char,('tidal_components',))
data[:] = dtmp
data.long_name='equilibrium tidal elevation amplitude' 
data.units='meters'

# Create and write the equilibrium tide beta
dtmp = np.zeros( 6, dtype=np.float32 )
data = outfile.createVariable('equilibrium_beta_love',np.dtype(np.float32).char,('tidal_components',))
data[:] = dtmp
data.formula='beta=1+klove-hlove'

# Create and write the equilibirum tide type
stmp=np.vstack([infile.variables['equilibrium_tide_type'].data,infile.variables['equilibrium_tide_type'].data[-1,:]])
tmpstr='LONGTERM'
for i in range(0,len(tmpstr)):
  stmp[-1,i]=tmpstr[i]
data = outfile.createVariable('equilibrium_tide_type','c',('tidal_components','DateStrLen',))
data[:] = stmp
data.long_name='formula'
data.units='beta=1+klove-hlove'

# Create and write the time origin variable
data = outfile.createVariable('time_origin',np.dtype(np.float32).char,())
data.assignValue( 0.0 )
data.long_name='time'
data.units='days since 0.0'
data.time_zone='none'

outfile.close()

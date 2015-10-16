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
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import scipy.io as sio
import scipy.fftpack as fftp
import pandas as pd
import pyseidon as pys
from pyseidon.validationClass import tidalStats
from datetime import timedelta
from scipy.interpolate import interp1d
import time
import scipy.stats as stats


# Define names and types of data
namelist=['2012-02-01_2012-03-01_0.01_0.001', '2012-02-01_2012-03-01_0.01_0.01', '2012-02-01_2012-03-01_0.02_0.001', '2012-02-01_2012-03-01_0.02_0.01', '2012-02-01_2012-03-01_0.03_0.001', '2012-02-01_2012-03-01_0.03_0.01']
#name='2012-02-01_2012-03-01_0.01_0.01'
grid='vhfr_low'
datatype='2d'
regionname='secondnarrows'
region=regions(regionname)

obspath='data/misc/vhfr_obs/VancouverBC_Harbour_Currents/'
obsname='04100_20110621'
obs=loadcur(obspath+obsname+'*')
#shifttime because PST
for key in obs:
    obs[key]['time']=obs[key]['time']


savepath='figures/png/' + grid + '_' + datatype + '/obs_speed_linreg/' +obsname + '/'
if not os.path.exists(savepath): os.makedirs(savepath)


       
        
def interpol(data_1, data_2, time_step=5.0/(24*60)):    
    dt_1 = data_1['time']
    dt_2 = data_2['time']

    # generate interpolation functions using linear interpolation
    f1 = interp1d(dt_1, data_1['pts'])
    f2 = interp1d(dt_2, data_2['pts'])

    # choose interval on which to interpolate
    start = max(dt_1[0], dt_2[0])
    end = min(dt_1[-1], dt_2[-1])

    # create timestamp array for new data and perform interpolation
    output_times = np.arange(start,end,time_step)

    series_1 = f1(output_times)
    series_2 = f2(output_times)

    dt_start = max(dt_1[0], dt_2[0])

    return (series_1, series_2, output_times, time_step)
    
    
def linReg(mod,obs, alpha=0.05, debug=False):
        '''
        Does linear regression on the model data vs. recorded data.

        Gives a 100(1-alpha)% confidence interval for the slope
        '''

        obs_mean = np.mean(obs)
        mod_mean = np.mean(mod)
        n = mod.size
        df = n - 2

        # calculate square sums
        SSxx = np.sum(mod**2) - np.sum(mod)**2 / n
        SSyy = np.sum(obs**2) - np.sum(obs)**2 / n
        SSxy = np.sum(mod * obs) - np.sum(mod) * np.sum(obs) / n
        SSE = SSyy - SSxy**2 / SSxx
        MSE = SSE / df

        # estimate parameters
        slope = SSxy / SSxx
        intercept = obs_mean - slope * mod_mean
        sd_slope = np.sqrt(MSE / SSxx)
        r_squared = 1 - SSE / SSyy

        # calculate 100(1 - alpha)% CI for slope
        width = stats.t.isf(0.5 * alpha, df) * sd_slope
        lower_bound = slope - width
        upper_bound = slope + width
        slope_CI = (lower_bound, upper_bound)

        # calculate 100(1 - alpha)% CI for intercept
        lower_intercept = obs_mean - lower_bound * mod_mean
        upper_intercept = obs_mean - upper_bound * mod_mean
        intercept_CI = (lower_intercept, upper_intercept)

        # estimate 100(1 - alpha)% CI for predictands
        predictands = slope * mod + intercept
        sd_resid = np.std(obs - predictands)
        y_CI_width = stats.t.isf(0.5 * alpha, df) * sd_resid * \
            np.sqrt(1 - 1 / n)

        # return data in a dictionary
        data = {}
        data['slope'] = slope
        data['intercept'] = intercept
        data['r_2'] = r_squared
        data['slope_CI'] = slope_CI
        data['intercept_CI'] = intercept_CI
        data['pred_CI_width'] = y_CI_width
        data['conf_level'] = 100 * (1 - alpha)



        return data
    


for name in namelist:

    ### load the .nc file #####
    data = loadnc('runs/'+grid+'/calibration/'+name+'/output/',singlename=grid + '_0001.nc')
    print('done load')
    data = ncdatasort(data,trifinder=True)
    print('done sort')
    
    nidx=get_nodes(data,region)
    eidx=get_elements(data,region)

    for key in obs:
        ##Plot obs location
        #clims=np.percentile(data['h'][nidx],[5,95])
        #f=plt.figure()
        #ax=plt.axes([.125,.1,.775,.8])
        #triax=ax.tripcolor(data['trigrid'],data['h'],vmin=clims[0],vmax=clims[1])
        #ax.plot(obs[key]['lon'],obs[key]['lat'],'*',markersize=12)
        #prettyplot_ll(ax,setregion=region,grid=True,cblabel='Depth (m)',cb=triax)
        #f.savefig(savepath + grid + '_' + regionname +'_obs_location_'+obsname+'_bin_'+("%d"%key)+'.png',dpi=600)
        #plt.close(f)


        ua=ipt.interpE_at_loc(data,'ua',[obs[key]['lon'],obs[key]['lat']]) 
        va=ipt.interpE_at_loc(data,'va',[obs[key]['lon'],obs[key]['lat']]) 
        zeta=ipt.interpN_at_loc(data,'zeta',[obs[key]['lon'],obs[key]['lat']]) 

        modelin={}
        modelin['time']=data['time']
        modelin['pts']=ua        
        obsin={}
        obsin['time']=obs[key]['time']
        obsin['pts']=obs[key]['u']
        
        #removenan
        removethis=~np.isnan(obsin['pts'])
        obsin['time']=obsin['time'][removethis]
        obsin['pts']=obsin['pts'][removethis]
        mu,ou,time,dt=interpol(modelin,obsin)
    
        modelin['pts']=va 
        obsin['pts']=obs[key]['v']
        obsin['pts']=obsin['pts'][removethis]
        mv,ov,time,dt=interpol(modelin,obsin)

        
        ms=speeder(mu,mv)
        os=speeder(ou,ov)
        
        lr=linReg(ms,os)
        

        fig = plt.figure(figsize=(18,10))
        ax = fig.add_subplot(111)

        ax.scatter(ms, os, c='b', marker='+', alpha=0.5)

        ## plot regression line
        mod_max = np.amax(ms)
        mod_min = np.amin(ms)
        upper_intercept = lr['intercept'] + lr['pred_CI_width']
        lower_intercept = lr['intercept'] - lr['pred_CI_width']
        ax.plot([mod_min, mod_max], [mod_min * lr['slope'] + lr['intercept'],
                mod_max * lr['slope'] + lr['intercept']],
                color='k', linestyle='-', linewidth=2, label='Linear fit')

        ## plot CI's for slope
        ax.plot([mod_min, mod_max], [mod_min * lr['slope_CI'][0] + lr['intercept_CI'][0],
                                     mod_max * lr['slope_CI'][0] + lr['intercept_CI'][0]],
                 color='r', linestyle='--', linewidth=2)
        ax.plot([mod_min, mod_max], [mod_min * lr['slope_CI'][1] + lr['intercept_CI'][1],
                                     mod_max * lr['slope_CI'][1] + lr['intercept_CI'][1]],
                 color='r', linestyle='--', linewidth=2, label='Slope CI')

        ## plot CI's for predictands
        ax.plot([mod_min, mod_max], [mod_min * lr['slope'] + upper_intercept,
                                     mod_max * lr['slope'] + upper_intercept],
                 color='g', linestyle='--', linewidth=2)
        ax.plot([mod_min, mod_max], [mod_min * lr['slope'] + lower_intercept,
                                     mod_max * lr['slope'] + lower_intercept],
                 color='g', linestyle='--', linewidth=2, label='Predictand CI')

        ax.set_xlabel('Modeled Data')
        ax.set_ylabel('Observed Data')
        fig.suptitle('Modeled vs. Observed {}: Linear Fit'.format('ADCP'))
        plt.legend(loc='lower right', shadow=True)

        r_string = 'R Squared: {}'.format(np.around(lr['r_2'], decimals=3))
        plt.title(r_string)
        fig.savefig(savepath + grid + '_' + name +'_'+obsname+'_bin_'+("%d"%key)+'_model_obs_linreg.png',dpi=300)
        plt.close(fig)
















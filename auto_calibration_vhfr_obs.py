#!/usr/bin/python2.7
# encoding: utf-8

from __future__ import division
from pyseidon_dvt import *
#from pyseidon.utilities.pyseidon_error import PyseidonError
import os


grid='vhhigh_v2'
datatype='2d'

startdir=os.getcwd()+'/'
path2runs = 'runs/'+grid+'/'
folder2results=['vhhigh_v2_2012-02-01_2012-03-01']


path2results = 'figures/png/'+grid+'_'+datatype+'/calibration_short/'


# obs
obs = []

# ADCP
path2obs = "data/misc/vhfr_obs/VancouverBC_Harbour_Currents/"
obsnamelist = [s for s in os.listdir(path2obs) if "pad.mat" in s]
obsnamelist.sort()
for name in obsnamelist:
    filename = path2obs + name
    print "Stacking: "+ name +"..."
    inobs = ADCP(filename)
    inobs.Variables.ua=inobs.Variables.u
    inobs.Variables.va=inobs.Variables.v    
    obs.append(inobs)
    
# TG
path2obs = "data/misc/vhfr_obs/slev/"
obsnamelist = [s for s in os.listdir(path2obs) if ".mat" in s]
for name in obsnamelist:
    filename = path2obs + name
    print "Stacking: "+ name +"..."
    inobs = TideGauge(filename)
    obs.append(inobs)
    
# runs
for case in folder2results:
    if not os.path.exists(startdir+path2results+case): os.makedirs(startdir+path2results+case)
    #os.chdir(startdir+path2results+case)
    #print "Working in: " + os.getcwd() +"..."
    folders = [s for s in folder2results if case in s]
    for f in folders:
        try:
            print "Validating: "+ f +"..."
            filename = startdir+path2runs+f+'/output/'+grid+'_0001.nc'
            fvcom = FVCOM(filename,tx=['2012-02-13 00:00:00','2012-02-20 00:00:00'])
            #print station._origin_file
            val = Validation(obs, fvcom,outpath=path2results+case+'/',debug=True)
            val.validate_data(filename = f+'_FVCOM_vs_OBS_data', save_csv=True)
            #val.validate_harmonics(filename = f+'_FVCOM_vs_OBS_harmo', save_csv=True)
        except (PyseidonError, IndexError) as e:
            pass


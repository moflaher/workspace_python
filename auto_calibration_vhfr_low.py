#!/usr/bin/python2.7
# encoding: utf-8

from __future__ import division
from pyseidon import *
from pyseidon.utilities.pyseidon_error import PyseidonError
import os

startdir=os.getcwd()+'/'
path2runs = 'runs/vhfr_low/calibration/'
folder2results=os.listdir(path2runs)

path2results = 'figures/png/vhfr_low_2d/calibration/'


path2obs = "data/misc/vhfr_obs/slev/"
obsnamelist = [s for s in os.listdir(path2obs) if ".mat" in s]

# obs
obs = []
for name in obsnamelist:
    filename = path2obs + name
    print "Stacking: "+ name +"..."
    inobs = TideGauge(filename)
    obs.append(inobs)
    
# runs
for case in folder2results:
    if not os.path.exists(startdir+path2results+case): os.makedirs(startdir+path2results+case)
    os.chdir(startdir+path2results+case)
    print "Working in: " + os.getcwd() +"..."
    folders = [s for s in folder2results if case in s]
    for f in folders:
        try:
            print "Validating: "+ f +"..."
            filename = startdir+path2runs+f+'/output/vhfr_low_0001.nc'
            fvcom = FVCOM(filename)
            #print station._origin_file
            val = Validation(obs, fvcom,closefallback=True)
            val.validate_data(filename = f+'_FVCOM_vs_tidegauges', save_csv=True)
            val.validate_harmonics(filename = f+'_FVCOM_vs_tidegauges', save_csv=True)
        except (PyseidonError, IndexError) as e:
            pass


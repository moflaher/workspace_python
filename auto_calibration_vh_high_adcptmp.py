#!/usr/bin/python2.7
# encoding: utf-8

from __future__ import division
from pyseidon import *
from pyseidon.utilities.pyseidon_error import PyseidonError
import os

startdir=os.getcwd()+'/'
path2runs = 'runs/vh_high/'
folder2results=['2012-02-01_2012-03-01_0.01_0.001']

path2results = 'figures/png/vh_high_2d/calibration_adcp2/'


path2obs = "data/misc/vhfr_obs/VancouverBC_Harbour_Currents/"
obsnamelist = [s for s in os.listdir(path2obs) if ".mat" in s]
obsnamelist.sort()
# obs
obs = []
for name in obsnamelist:
    filename = path2obs + name
    print "Stacking: "+ name +"..."
    inobs = basicADCP(filename)
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
            filename = startdir+path2runs+f+'/output/vh_high_0001.nc'
            fvcom = FVCOM(filename,tx = ['2012-02-18 00:00:00','2012-02-22 00:00:00'])
            #print station._origin_file
            val = Validation(obs, fvcom,closefallback=True)
            val.validate_data(filename = f+'_FVCOM_vs_basicadcp', save_csv=True)
            #val.validate_harmonics(filename = f+'_FVCOM_vs_basicadcp', save_csv=True)
        except (PyseidonError, IndexError) as e:
            pass


# -*- coding: utf-8 -*-
"""
Front Matter
=============

Created on Thursday June 12, 2014

Author: Mitchell O'Flaherty-Sproul

A set of predefined regions to select from based on name.

Requirements
===================================
Absolutely Necessary:


Optional, but recommended:


Functions
=========
makeregions - function creates all the regions and returns a dictionary containing them.
            
"""
import numpy as np


def makeregions():
    allregions={}    

    #Petit Passage regions   
    tmpdic={}  
    tmpdic['region']=np.array([-66.225, -66.195, 44.37, 44.41])
    tmpdic['passage']='pp'
    tmpdic['passageP']='Petit Passage'
    allregions['pp']=tmpdic

    #Grand Passage regions   
    tmpdic={}    
    tmpdic['region']=np.array([-66.38, -66.29, 44.213, 44.32])
    tmpdic['passage']='gp'
    tmpdic['passageP']='Grand Passage'
    allregions['gp']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-66.355, -66.32, 44.245, 44.2925])
    tmpdic['passage']='gp_tight'
    tmpdic['passageP']='Grand Passage Tight'
    allregions['gp_tight']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-66.345, -66.33, 44.26, 44.275])
    tmpdic['passage']='gp3'
    tmpdic['passageP']='Grand Passage Site 3'
    allregions['gp3']=tmpdic

    #Digby Gut regions
    tmpdic={}  
    tmpdic['region']=np.array([-65.79, -65.73, 44.65, 44.7])
    tmpdic['passage']='dg'
    tmpdic['passageP']='Digby Gut'
    allregions['dg']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-65.794, -65.743, 44.66, 44.71])
    tmpdic['passage']='dg_upper'
    tmpdic['passageP']='Digby Gut Upper'
    allregions['dg_upper']=tmpdic


    #Kitimat regions
    tmpdic={}  
    tmpdic['region']=np.array([-132.32,  -126.665,  51.16,  55.925])
    tmpdic['passage']='kitimat3'
    tmpdic['passageP']='Kitimat Grid'
    allregions['kitimat3']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-132.32,  -126.665,  51.16,  55.925])
    tmpdic['passage']='kit4'
    tmpdic['passageP']='Kitimat Grid'
    allregions['kit4']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-132.32,  -126.665,  51.16,  55.925])
    tmpdic['passage']='kit4_tight'
    tmpdic['passageP']='Kitimat Grid'
    allregions['kit4_tight']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.5, -128.25,  53.25,  54.1])
    tmpdic['passage']='douglas'
    tmpdic['passageP']='Douglas Channel'
    allregions['douglas']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129, -128.6,  53.7,  54.01])
    tmpdic['passage']='kitimat'
    tmpdic['passageP']='Kitimat'
    allregions['kitimat']=tmpdic    

    tmpdic={}  
    tmpdic['region']=np.array([-129.75,  -128.5,  52.5,  54.05])
    tmpdic['passage']='douglaslarge'
    tmpdic['passageP']='Douglas Channel'
    allregions['douglaslarge']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.75,  -129,  52.75,  53.5])
    tmpdic['passage']='gilisland'
    tmpdic['passageP']='Gil Island'
    allregions['gilisland']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.7,  -129.4,  52.9,  53.1])
    tmpdic['passage']='fasttip'
    tmpdic['passageP']='fasttip'
    allregions['fasttip']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.9,  -129.6,  53.0,  53.35])
    tmpdic['passage']='fasttip_back'
    tmpdic['passageP']='fasttip_back'
    allregions['fasttip_back']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-130.1,  -128.9,  52.4,  53.6])
    tmpdic['passage']='kelparea'
    tmpdic['passageP']='kelparea'
    allregions['kelparea']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-130.0,  -129.0,  52.4,  53.4])
    tmpdic['passage']='kelparea2'
    tmpdic['passageP']='kelparea2'
    allregions['kelparea2']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-131, -128.5, 52.25, 54.1])
    tmpdic['passage']='shiparea1'
    tmpdic['passageP']='Shipping Area 1'
    allregions['shiparea1']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.15, -128.65, 53.4, 53.8])
    tmpdic['passage']='kit4_area1'
    tmpdic['passageP']='Area 1'
    allregions['kit4_area1']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.65, -129.35, 52.85, 53.15])
    tmpdic['passage']='kit4_area2'
    tmpdic['passageP']='Area 2'
    allregions['kit4_area2']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.4, -128.9, 52.4, 53.0])
    tmpdic['passage']='kit4_area3'
    tmpdic['passageP']='Area 3'
    allregions['kit4_area3']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-128.975, -128.825, 53.52, 53.6])
    tmpdic['passage']='kit4_area4'
    tmpdic['passageP']='Area 4'
    allregions['kit4_area4']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-130, -128, 52, 54.1])
    tmpdic['passage']='mostchannels'
    tmpdic['passageP']='mostchannels'
    allregions['mostchannels']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.7, -129.1, 52.3, 52.9])
    tmpdic['passage']='aristazabal_west'
    tmpdic['passageP']='West of Aristazabal Island'
    allregions['aristazabal_west']=tmpdic
    
    tmpdic={}  
    tmpdic['region']=np.array([-129.675, -129.45, 52.98, 53.14])
    tmpdic['passage']='cross_shore_1'
    tmpdic['passageP']='cross_shore_1'
    allregions['cross_shore_1']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.85, -129.25, 52.9, 53.225])
    tmpdic['passage']='doubleisland'
    tmpdic['passageP']='doubleisland'
    allregions['doubleisland']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.6, -129.1, 52.45, 52.825])
    tmpdic['passage']='kelpchain'
    tmpdic['passageP']='kelpchain'
    allregions['kelpchain']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.45, -129.38, 52.97, 53.01])
    tmpdic['passage']='kit4_kelp_tight'
    tmpdic['passageP']='kit4_kelp_tight'
    allregions['kit4_kelp_tight']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.53, -129.38, 52.6, 52.75])
    tmpdic['passage']='kit4_kelp_tight2'
    tmpdic['passageP']='kit4_kelp_tight2'
    allregions['kit4_kelp_tight2']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.52, -129.41, 52.6, 52.7])
    tmpdic['passage']='kit4_kelp_tight2_small'
    tmpdic['passageP']='kit4_kelp_tight2_small'
    allregions['kit4_kelp_tight2_small']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.50, -129.47, 52.63, 52.67])
    tmpdic['passage']='kit4_kelp_tight2_kelpfield'
    tmpdic['passageP']='kit4_kelp_tight2_kelpfield'
    allregions['kit4_kelp_tight2_kelpfield']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.52, -129.48, 52.64, 52.66])
    tmpdic['passage']='kit4_kelp_tight2_tiny_left'
    tmpdic['passageP']='kit4_kelp_tight2_tiny_left'
    allregions['kit4_kelp_tight2_tiny_left']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.54, -129.39, 52.95, 53.04])
    tmpdic['passage']='kit4_crossdouble'
    tmpdic['passageP']='kit4_crossdouble'
    allregions['kit4_crossdouble']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.825, -129.675, 53.1, 53.19])
    tmpdic['passage']='kit4_ftb'
    tmpdic['passageP']='kit4_ftb'
    allregions['kit4_ftb']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.5, -129.25, 52.45, 52.625])
    tmpdic['passage']='conroy_island'
    tmpdic['passageP']='conroy_island'
    allregions['conroy_island']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.5, -129.44, 53.04, 53.08])
    tmpdic['passage']='kit4_kelp_tight3'
    tmpdic['passageP']='kit4_kelp_tight3'
    allregions['kit4_kelp_tight3']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.61, -129.5, 52.96, 53.02])
    tmpdic['passage']='kit4_kelp_tight4'
    tmpdic['passageP']='kit4_kelp_tight4'
    allregions['kit4_kelp_tight4']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.47, -129.28, 52.48, 52.62])
    tmpdic['passage']='kit4_kelp_tight5'
    tmpdic['passageP']='kit4_kelp_tight5'
    allregions['kit4_kelp_tight5']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.43, -129.29, 52.725, 52.88])
    tmpdic['passage']='kit4_kelp_tight6'
    tmpdic['passageP']='kit4_kelp_tight6'
    allregions['kit4_kelp_tight6']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-129.526, -129.286, 52.4576, 52.7178])
    tmpdic['passage']='kit4_4island'
    tmpdic['passageP']='kit4_4island'
    allregions['kit4_4island']=tmpdic

    #General regions
    tmpdic={}  
    tmpdic['region']=np.array([-67.5, -66, 44.5, 45.3])
    tmpdic['passage']='musq'
    tmpdic['passageP']='musq'
    allregions['musq']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-66.925, -66.8,45.0,45.075])
    tmpdic['passage']='musq_cage'
    tmpdic['passageP']='musq_cage'
    allregions['musq_cage']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-66.90,-66.815,45.025,45.06])
    tmpdic['passage']='musq_cage_tight'
    tmpdic['passageP']='musq_cage_tight'
    allregions['musq_cage_tight']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-66.88,-66.815,45.015,45.065])
    tmpdic['passage']='musq_cage_tight2'
    tmpdic['passageP']='musq_cage_tight2'
    allregions['musq_cage_tight2']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-66.85,-66.82,45.0275,45.0475])
    tmpdic['passage']='musq_4cage'
    tmpdic['passageP']='musq_4cage'
    allregions['musq_4cage']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-67.6,-66.45,44.3,45.1])
    tmpdic['passage']='musq_large'
    tmpdic['passageP']='musq_large'
    allregions['musq_large']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-71.5,   -57.5,    37.5,    46])
    tmpdic['passage']='sfmwhole'
    tmpdic['passageP']='Scotia Fundy Maine'
    allregions['sfmwhole']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-67.6,   -63.4,    43.8,    46])
    tmpdic['passage']='bof'
    tmpdic['passageP']='Bay of Fundy'
    allregions['bof']=tmpdic


    tmpdic={}  
    tmpdic['region']=np.array([-152.51,   -106.04,    68.65,    79.34])
    tmpdic['passage']='beaufort3'
    tmpdic['passageP']='Beaufort Sea'
    allregions['beaufort3']=tmpdic


    tmpdic={}  
    tmpdic['region']=np.array([-140.0,   -106.04,    68.65,    79.34])
    tmpdic['passage']='beaufort3_sub'
    tmpdic['passageP']='Beaufort Sea'
    allregions['beaufort3_sub']=tmpdic


    tmpdic={}  
    tmpdic['region']=np.array([-140,   -125,    67,    72])
    tmpdic['passage']='beaufort3_southcoast'
    tmpdic['passageP']='Beaufort Sea'
    allregions['beaufort3_southcoast']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-140,   -127,    68.5,    71])
    tmpdic['passage']='beaufort3_southcoast_tight'
    tmpdic['passageP']='Beaufort Sea'
    allregions['beaufort3_southcoast_tight']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-138,   -132.5,    68.5,    70])
    tmpdic['passage']='beaufort3_oilmap_1'
    tmpdic['passageP']='Beaufort Sea'
    allregions['beaufort3_oilmap_1']=tmpdic

    
    return allregions

































        

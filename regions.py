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
    tmpdic['region']=np.array([-71.5,   -57.5,    37.5,    46])
    tmpdic['passage']='sfmwhole'
    tmpdic['passageP']='Scotia Fundy Maine'
    allregions['sfmwhole']=tmpdic

    tmpdic={}  
    tmpdic['region']=np.array([-67.6,   -63.4,    43.8,    46])
    tmpdic['passage']='bof'
    tmpdic['passageP']='Bay of Fundy'
    allregions['bof']=tmpdic













    
    return allregions

































        

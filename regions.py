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
regions -   given no input regions returns a list of regions, given a valid location it returns long/lat of the region and the passage name in file format and title format.
            
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
    tmpdic['region']=np.array([-131, -128.5, 52.25, 54.1])
    tmpdic['passage']='hiparea1'
    tmpdic['passageP']='Shipping Area 1'
    allregions['hiparea1']=tmpdic














    
    return allregions
    



        

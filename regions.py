# -*- coding: utf-8 -*-
"""
Front Matter
=============

Created in 2014

Author: Mitchell O'Flaherty-Sproul

A set of predefined regions to select from based on name.


"""
import numpy as np

def makeregions():
    tl=np.empty((1,3),dtype=object)    
    
    #bof
    tl=np.vstack([tl,        [[-66.225, -66.195, 44.37, 44.41],'pp','Petit Passage']])
    tl=np.vstack([tl,        [[-66.38, -66.29, 44.213, 44.32],'gp','Grand Passage']])
    tl=np.vstack([tl,        [[-66.355, -66.32, 44.245, 44.2925],'gp_tight','Grand Passage Tight']])
    tl=np.vstack([tl,        [[-66.345, -66.33, 44.26, 44.275],'gp3','Grand Passage Site 3']])
    tl=np.vstack([tl,        [[-65.79, -65.73, 44.65, 44.7],'dg','Digby Gut']])
    tl=np.vstack([tl,        [[-65.794, -65.743, 44.66, 44.71],'dg_upper','Digby Gut Upper']])
    tl=np.vstack([tl,        [[-71.5,   -57.5,    37.5,    46.5],'sfmwhole','Scotia Fundy Maine']])
    tl=np.vstack([tl,        [[-67.6,   -63.4,    43.8,    46],'bof','Bay of Fundy']])
    tl=np.vstack([tl,        [[-64.52, -64.3, 45.3, 45.4],'mp','Minas Passage']])
    tl=np.vstack([tl,        [[-64.45, -64.375, 45.35, 45.39],'blackrock','Black Rock']])
    tl=np.vstack([tl,        [[-64.42, -64.38, 45.35, 45.38],'blackrock_fld','Black Rock']])
    tl=np.vstack([tl,        [[-64.43, -64.4085, 45.361, 45.372],'blackrock_ebb','Black Rock']])

    #fishcage and slr
    tl=np.vstack([tl,        [[-65.5, -63.25, 44, 46],'slr_upperbof','slr_upperbof']])
    tl=np.vstack([tl,        [[-67.5, -66, 44.5, 45.3],'musq','musq']])
    tl=np.vstack([tl,        [[-66.925, -66.8,45.0,45.075],'musq_cage','musq_cage']])
    tl=np.vstack([tl,        [[-66.90,-66.815,45.025,45.06],'musq_cage_tight','musq_cage_tight']])
    tl=np.vstack([tl,        [[-66.88,-66.815,45.015,45.065],'musq_cage_tight2','musq_cage_tight2']])
    tl=np.vstack([tl,        [[-66.85,-66.82,45.0275,45.0475],'musq_4cage','musq_4cage']])
    tl=np.vstack([tl,        [[-67.6,-66.45,44.3,45.1],'musq_large','musq_large']])

    #Kitimat regions    
    tl=np.vstack([tl,        [[-132.32,  -126.665,  51.16,  55.925],'kit4','Kitimat Grid']])
    tl=np.vstack([tl,        [[-132.32,  -126.665,  51.16,  55.925],'kit4_tight','Kitimat Grid']])
    tl=np.vstack([tl,        [[-129.75,  -129,  52.75,  53.5],'gilisland','Gil Island']])
    tl=np.vstack([tl,        [[-129.5, -128.25,  53.25,  54.1],'douglas','Douglas Channel']])
    tl=np.vstack([tl,        [[-130.0,  -129.0,  52.4,  53.4],'kelparea2','kelparea2']])
    tl=np.vstack([tl,        [[-130, -128, 52, 54.1],'mostchannels','mostchannels']])
    tl=np.vstack([tl,        [[-129.85, -129.25, 52.9, 53.225],'doubleisland','doubleisland']])
    tl=np.vstack([tl,        [[-129.45, -129.38, 52.97, 53.01],'kit4_kelp_tight','kit4_kelp_tight']])
    tl=np.vstack([tl,        [[-129.53, -129.38, 52.6, 52.75],'kit4_kelp_tight2','kit4_kelp_tight2']])
    tl=np.vstack([tl,        [[-129.52, -129.41, 52.6, 52.7],'kit4_kelp_tight2_small','kit4_kelp_tight2_small']])
    tl=np.vstack([tl,        [[-129.505, -129.46, 52.63, 52.67],'kit4_kelp_tight2_kelpfield','kit4_kelp_tight2_kelpfield']])
    tl=np.vstack([tl,        [[-129.505, -129.475, 52.635, 52.665],'kit4_kelpfield','kit4_kelpfield']])
    tl=np.vstack([tl,        [[-129.5, -129.4775, 52.6375, 52.6625],'kit4_kelpfield_oil','kit4_kelpfield_oil']])
    tl=np.vstack([tl,        [[-129.54, -129.39, 52.95, 53.04],'kit4_crossdouble','kit4_crossdouble']])
    tl=np.vstack([tl,        [[-129.825, -129.675, 53.1, 53.19],'kit4_ftb','kit4_ftb']])
    tl=np.vstack([tl,        [[-129.5, -129.44, 53.04, 53.08],'kit4_kelp_tight3','kit4_kelp_tight3']])
    tl=np.vstack([tl,        [[-129.61, -129.5, 52.96, 53.02],'kit4_kelp_tight4','kit4_kelp_tight4']])
    tl=np.vstack([tl,        [[-129.47, -129.28, 52.48, 52.62],'kit4_kelp_tight5','kit4_kelp_tight5']])
    tl=np.vstack([tl,        [[-129.36849, -129.3585, 52.54049, 52.5505],'kit4_kelp_tight5_A2','kit4_kelp_tight5_A2']])
    tl=np.vstack([tl,        [[-129.4187, -129.40769, 52.56615, 52.578849],'kit4_kelp_tight5_A6','kit4_kelp_tight5_A6']])
    tl=np.vstack([tl,        [[-129.43, -129.29, 52.725, 52.88],'kit4_kelp_tight6','kit4_kelp_tight6']])
    tl=np.vstack([tl,        [[-129.47, -129.28, 52.452, 52.648],'kit4_kelp_tight5_tall','kit4_kelp_tight5_tall']])
    tl=np.vstack([tl,        [[-129.526, -129.286, 52.4576, 52.7178],'kit4_4island','kit4_4island']])
    tl=np.vstack([tl,        [[-129.6, -129.1, 52.45, 52.825],'kelpchain','kelpchain']])
    tl=np.vstack([tl,        [[-128.9, -128.75, 53.525, 53.625],'kit4_area5','Area 5']])

    # arctic
    tl=np.vstack([tl,        [[-152.51,   -106.04,    68.65,    79.34],'beaufort3','Beaufort Sea']])
    tl=np.vstack([tl,        [[-140.0,   -106.04,    68.65,    79.34],'beaufort3_sub','Beaufort Sea']])
    tl=np.vstack([tl,        [[-140,   -125,    67,    72],'beaufort3_southcoast','Beaufort Sea']])
    tl=np.vstack([tl,        [[-140,   -127,    68.5,    71],'beaufort3_southcoast_tight','Beaufort Sea']])
    tl=np.vstack([tl,        [[-138,   -132.5,    68.5,    70],'beaufort3_oilmap_1','Beaufort Sea']])

    #vhfr
    tl=np.vstack([tl,        [[-124,   -121.95,    48.65,    49.8],'vhfr_whole','Complete Domain for vhfr grids']])
    tl=np.vstack([tl,        [[-123.96833,   -122,    48.797548,   49.69656],'vhfr_tight','Complete Domain for vhfr grids']])
    tl=np.vstack([tl,        [[-123.325,   -121.975,    48.95,    49.6],'fr_whole','fr_whole']])
    tl=np.vstack([tl,        [[-123.3,   -123.0,    49,    49.275],'fr_mouth','fr_mouth']])
    tl=np.vstack([tl,        [[-122.75,   -122.45,    49.25,    49.55],'pitt_lake','pitt_lake']])
    tl=np.vstack([tl,        [[-123.1,   -122.8,    49.075,    49.235],'fr_area1','fr_area1']])
    tl=np.vstack([tl,        [[-122.8,   -122.525,    49.14,    49.27],'fr_area2','fr_area2']])
    tl=np.vstack([tl,        [[-122.2,   -122.0,    49.11,    49.21],'fr_area3','fr_area3']])


    allregions={}  

    tl=np.delete(tl,0,axis=0)
    for row in tl:
        tmpdic={}  
        tmpdic['region']=np.array(row[0])
        tmpdic['passage']=row[1]
        tmpdic['regionname']=row[1]
        tmpdic['passageP']=row[2]
        allregions[row[1]]=tmpdic

    return allregions  










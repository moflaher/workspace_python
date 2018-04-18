# -*- coding: utf-8 -*-
"""
Front Matter
=============
Created in 2014
Author: Mitchell O'Flaherty-Sproul
A set of predefined regions to select from based on name.

"""
import numpy as np
from collections import OrderedDict
def makeregions():
    
    allregions=OrderedDict()    
    
    #BOF
    allregions['sfmwhole'] = {'regionname' : 'sfmwhole', 'group' : 'bof', 'region' : [-71.5, -57.5, 37.5, 46.5]}
    allregions['bof_nemo'] = {'regionname' : 'bof_nemo', 'group' : 'bof', 'region' : [-68.425, -62.85, 44.2, 46.1]}
    allregions['bof'] = {'regionname' : 'bof', 'group' : 'bof', 'region' : [-67.6, -63.4, 43.8, 46.0]}
    
    
    #UPPERBOF
    allregions['blackrock_fld'] = {'regionname' : 'blackrock_fld', 'group' : 'upperbof', 'region' : [-64.42, -64.38, 45.35, 45.38]}
    allregions['northgrid_cape'] = {'regionname' : 'northgrid_cape', 'group' : 'upperbof', 'region' : [-64.91, -64.64, 45.45, 45.675]}
    allregions['blackrock'] = {'regionname' : 'blackrock', 'group' : 'upperbof', 'region' : [-64.45, -64.375, 45.35, 45.39]}
    allregions['mp'] = {'regionname' : 'mp', 'group' : 'upperbof', 'region' : [-64.52, -64.3, 45.3, 45.4]}    
    allregions['seaview'] = {'regionname' : 'seaview', 'group' : 'upperbof', 'region' : [-66.25, -66.1, 45.075, 45.2]}    
    allregions['capeenrage'] = {'regionname' : 'capeenrage', 'group' : 'upperbof', 'region' : [-65.05, -64.5, 45.425, 45.75]}
    allregions['blackrock_ebb'] = {'regionname' : 'blackrock_ebb', 'group' : 'upperbof', 'region' : [-64.43, -64.4085, 45.361, 45.372]}
    allregions['capedor'] = {'regionname' : 'capedor', 'group' : 'upperbof', 'region' : [-64.89, -64.66, 45.125, 45.36]}
    allregions['northgrid'] = {'regionname' : 'northgrid', 'group' : 'upperbof', 'region' : [-65.03, -64.221, 45.43, 46.15]}
    
    
    #AQUACULTURE
    allregions['musq_large'] = {'regionname' : 'musq_large', 'group' : 'aquaculture', 'region' : [-67.6, -66.45, 44.3, 45.1]} 
    allregions['musq_cage'] = {'regionname' : 'musq_cage', 'group' : 'aquaculture', 'region' : [-66.925, -66.8, 45.0, 45.075]}
    allregions['musq_cage_tight'] = {'regionname' : 'musq_cage_tight', 'group' : 'aquaculture', 'region' : [-66.9, -66.815, 45.025, 45.06]}
    allregions['musq_cage_tight2'] = {'regionname' : 'musq_cage_tight2', 'group' : 'aquaculture', 'region' : [-66.88, -66.815, 45.015, 45.065]}
    allregions['musq'] = {'regionname' : 'musq', 'group' : 'aquaculture', 'region' : [-67.5, -66.0, 44.5, 45.3]}   
    allregions['musq_4cage'] = {'regionname' : 'musq_4cage', 'group' : 'aquaculture', 'region' : [-66.85, -66.82, 45.0275, 45.0475]}
    
    
    #STJOHN
    allregions['stjohn_harbour'] = {'regionname' : 'stjohn_harbour', 'group' : 'stjohn', 'region' : [-66.14, -65.98, 45.18, 45.29]}
    allregions['stjohn_harbour_tight'] = {'regionname' : 'stjohn_harbour_tight', 'group' : 'stjohn', 'region' : [-66.07, -66.02, 45.2326, 45.275]}
    allregions['stjohn_ship_approach1'] = {'regionname' : 'stjohn_ship_approach1', 'group' : 'stjohn', 'region' : [-71.0, -58.2, 39.6, 46.5]}
    allregions['sjr_kl'] = {'regionname' : 'sjr_kl', 'group' : 'stjohn', 'region' : [-66.3, -65.75, 45.05, 45.7]}
    allregions['stjohn_harbour_large'] = {'regionname' : 'stjohn_harbour_large', 'group' : 'stjohn', 'region' : [-66.25, -65.83, 45.1, 45.7]}
    allregions['stjohn_nemo'] = {'regionname' : 'stjohn_nemo', 'group' : 'stjohn', 'region' : [-66.14, -65.98, 45.2, 45.29]}
    allregions['sjr'] = {'regionname' : 'sjr', 'group' : 'stjohn', 'region' : [-66.35, -65.95, 45.0, 45.3]}
    allregions['slr_upperbof'] = {'regionname' : 'slr_upperbof', 'group' : 'stjohn', 'region' : [-65.5, -63.25, 44.0, 46.0]}
    allregions['enav_sjr_large'] = {'regionname' : 'enav_sjr_large', 'group' : 'stjohn', 'region' : [-70, -62, 40, 46]}
    allregions['reversing_falls'] = {'regionname' : 'reversing_falls', 'group' : 'stjohn', 'region' : [-66.1055, -66.055, 45.2475, 45.29]}
    allregions['longreach'] = {'regionname' : 'longreach', 'group' : 'stjohn', 'region' : [-66.3, -65.9, 45.3, 45.6]}
    allregions['nemofvcom_100m_grid'] = {'regionname' : 'nemofvcom_100m_grid', 'group' : 'stjohn', 'region' : [-66.45, -65.55, 44.9, 45.325], 'figsize' : (25/2.539, 15/2.536), 'axes' : [.13,.11,.8825,.8125], 'textloc' : (.425,.93)}
    
    
    #DIGBYNECK
    allregions['gp'] = {'regionname' : 'gp', 'group' : 'digbyneck', 'region' : [-66.38, -66.29, 44.213, 44.32]}
    allregions['dg'] = {'regionname' : 'dg', 'group' : 'digbyneck', 'region' : [-65.79, -65.73, 44.65, 44.7]}
    allregions['dg_upper'] = {'regionname' : 'dg_upper', 'group' : 'digbyneck', 'region' : [-65.794, -65.743, 44.66, 44.71]}
    allregions['pp'] = {'regionname' : 'pp', 'group' : 'digbyneck', 'region' : [-66.225, -66.195, 44.37, 44.41]}
    allregions['gp_tight'] = {'regionname' : 'gp_tight', 'group' : 'digbyneck', 'region' : [-66.355, -66.32, 44.245, 44.2925]} 
    allregions['gp3'] = {'regionname' : 'gp3', 'group' : 'digbyneck', 'region' : [-66.345, -66.33, 44.26, 44.275]} 
    
        
    #VHFR
    allregions['fr_sandbar_island1'] = {'regionname' : 'fr_sandbar_island1', 'group' : 'vhfr', 'region' : [-122.83, -122.746, 49.2, 49.25]}
    allregions['fr_mouth'] = {'regionname' : 'fr_mouth', 'group' : 'vhfr', 'region' : [-123.33, -123.0, 49.0, 49.275]}
    allregions['vh_whole'] = {'regionname' : 'vh_whole', 'group' : 'vhfr', 'region' : [-123.286, -122.815, 49.242, 49.488]}
    allregions['vh_high_large'] = {'regionname' : 'vh_high_large', 'group' : 'vhfr', 'region' : [-124.0, -122.7, 48.85, 49.5]}
    allregions['douglas'] = {'regionname' : 'douglas', 'group' : 'vhfr', 'region' : [-129.5, -128.25, 53.25, 54.1]}
    allregions['secondnarrows'] = {'regionname' : 'secondnarrows', 'group' : 'vhfr', 'region' : [-123.04, -123.0, 49.288, 49.31]}
    allregions['firstnarrows'] = {'regionname' : 'firstnarrows', 'group' : 'vhfr', 'region' : [-123.16, -123.095, 49.291, 49.332]}
    allregions['vh_harbour_tight'] = {'regionname' : 'vh_harbour_tight', 'group' : 'vhfr', 'region' : [-123.125, -123.025, 49.256, 49.348]}
    allregions['pitt_lake'] = {'regionname' : 'pitt_lake', 'group' : 'vhfr', 'region' : [-122.75, -122.45, 49.25, 49.55]}
    allregions['vhfr_whole'] = {'regionname' : 'vhfr_whole', 'group' : 'vhfr', 'region' : [-124.0, -121.95, 48.65, 49.8]}
    allregions['vh_harbour'] = {'regionname' : 'vh_harbour', 'group' : 'vhfr', 'region' : [-123.191, -122.968, 49.256, 49.348]}
    allregions['vhfr_tight'] = {'regionname' : 'vhfr_tight', 'group' : 'vhfr', 'region' : [-123.96833, -122.0, 48.797548, 49.69656]}
    allregions['secondnarrows_tight'] = {'regionname' : 'secondnarrows_tight', 'group' : 'vhfr', 'region' : [-123.0325, -123.015, 49.29, 49.302]}
    allregions['fr_area1'] = {'regionname' : 'fr_area1', 'group' : 'vhfr', 'region' : [-123.1, -122.8, 49.075, 49.235]}
    allregions['fr_area2'] = {'regionname' : 'fr_area2', 'group' : 'vhfr', 'region' : [-122.8, -122.525, 49.14, 49.27]}
    allregions['fr_area3'] = {'regionname' : 'fr_area3', 'group' : 'vhfr', 'region' : [-122.2, -122.0, 49.11, 49.21]}
    allregions['secondnarrows_zoom'] = {'regionname' : 'secondnarrows_zoom', 'group' : 'vhfr', 'region' : [-123.035, -123.0175, 49.2925, 49.301]}
    allregions['pitt_lake_sandbar'] = {'regionname' : 'pitt_lake_sandbar', 'group' : 'vhfr', 'region' : [-122.7, -122.55, 49.3, 49.4]}  
    allregions['fr_whole'] = {'regionname' : 'fr_whole', 'group' : 'vhfr', 'region' : [-123.325, -121.975, 48.95, 49.6]}
    allregions['vh_high_ship_approach1'] = {'regionname' : 'vh_high_ship_approach1', 'group' : 'vhfr', 'region' : [-123.17, -122.99, 49.25, 49.34]}
    
    
    #KIT4
    allregions['doubleisland'] = {'regionname' : 'doubleisland', 'group' : 'kit4', 'region' : [-129.85, -129.25, 52.9, 53.225]}    
    allregions['gilisland_south'] = {'regionname' : 'gilisland_south', 'group' : 'kit4', 'region' : [-129.33, -129.152, 52.98, 53.11]} 
    allregions['kit4_kelp_tight5_A2'] = {'regionname' : 'kit4_kelp_tight5_A2', 'group' : 'kit4', 'region' : [-129.36849, -129.3585, 52.54049, 52.5505]}
    allregions['kit4_kelp_tight5_A6'] = {'regionname' : 'kit4_kelp_tight5_A6', 'group' : 'kit4', 'region' : [-129.4187, -129.40769, 52.56615, 52.578849]}
    allregions['kit4_ftb'] = {'regionname' : 'kit4_ftb', 'group' : 'kit4', 'region' : [-129.825, -129.675, 53.1, 53.19]}
    allregions['kit4_4island'] = {'regionname' : 'kit4_4island', 'group' : 'kit4', 'region' : [-129.526, -129.286, 52.4576, 52.7178]}
    allregions['kit4'] = {'regionname' : 'kit4', 'group' : 'kit4', 'region' : [-132.32, -126.665, 51.16, 55.925]}
    allregions['kit4_kelp_tight5_tall'] = {'regionname' : 'kit4_kelp_tight5_tall', 'group' : 'kit4', 'region' : [-129.47, -129.28, 52.452, 52.648]}   
    allregions['kelp_channel'] = {'regionname' : 'kelp_channel', 'group' : 'kit4', 'region' : [1.98, 2.018, 1.996, 2.0045]}
    allregions['gilisland_east'] = {'regionname' : 'gilisland_east', 'group' : 'kit4', 'region' : [-129.23, -129.0, 53.1, 53.33]}    
    allregions['kelpchain'] = {'regionname' : 'kelpchain', 'group' : 'kit4', 'region' : [-129.6, -129.1, 52.45, 52.825]}
    allregions['douglaslarge'] = {'regionname' : 'douglaslarge', 'group' : 'kit4', 'region' : [-129.75, -128.5, 52.9, 54.05]}
    allregions['kelparea2'] = {'regionname' : 'kelparea2', 'group' : 'kit4', 'region' : [-130.0, -129.0, 52.4, 53.4]}
    allregions['kit4_area5'] = {'regionname' : 'kit4_area5', 'group' : 'kit4', 'region' : [-128.9, -128.75, 53.525, 53.625]}
    allregions['kit4_kelp_tight2_small'] = {'regionname' : 'kit4_kelp_tight2_small', 'group' : 'kit4', 'region' : [-129.52, -129.41, 52.6, 52.7]}    
    allregions['kit4_kelp_tight6'] = {'regionname' : 'kit4_kelp_tight6', 'group' : 'kit4', 'region' : [-129.43, -129.29, 52.725, 52.88]}
    allregions['kit4_kelp_tight4'] = {'regionname' : 'kit4_kelp_tight4', 'group' : 'kit4', 'region' : [-129.61, -129.5, 52.96, 53.02]}
    allregions['kit4_kelp_tight5'] = {'regionname' : 'kit4_kelp_tight5', 'group' : 'kit4', 'region' : [-129.47, -129.28, 52.48, 52.62]}
    allregions['kit4_kelp_tight2'] = {'regionname' : 'kit4_kelp_tight2', 'group' : 'kit4', 'region' : [-129.53, -129.38, 52.6, 52.75]}
    allregions['kit4_kelp_tight3'] = {'regionname' : 'kit4_kelp_tight3', 'group' : 'kit4', 'region' : [-129.5, -129.44, 53.04, 53.08]}
    allregions['kit4_kelp_tight'] = {'regionname' : 'kit4_kelp_tight', 'group' : 'kit4', 'region' : [-129.45, -129.38, 52.97, 53.01]}
    allregions['kit4_tight'] = {'regionname' : 'kit4_tight', 'group' : 'kit4', 'region' : [-132.32, -126.665, 51.16, 55.925]}
    allregions['gilisland_west'] = {'regionname' : 'gilisland_west', 'group' : 'kit4', 'region' : [-129.56, -129.29, 53.136, 53.32]}
    allregions['kit4_kelpfield'] = {'regionname' : 'kit4_kelpfield', 'group' : 'kit4', 'region' : [-129.505, -129.475, 52.635, 52.665]}
    allregions['gilisland_tight'] = {'regionname' : 'gilisland_tight', 'group' : 'kit4', 'region' : [-129.8, -129.0, 52.9, 53.4]}
    allregions['kit4_crossdouble'] = {'regionname' : 'kit4_crossdouble', 'group' : 'kit4', 'region' : [-129.54, -129.39, 52.95, 53.04]}
    allregions['gilisland'] = {'regionname' : 'gilisland', 'group' : 'kit4', 'region' : [-129.75, -129.0, 52.75, 53.5]}
    allregions['mostchannels'] = {'regionname' : 'mostchannels', 'group' : 'kit4', 'region' : [-130.0, -128.0, 52.0, 54.1]}
    allregions['kit4_kelp_tight2_kelpfield'] = {'regionname' : 'kit4_kelp_tight2_kelpfield', 'group' : 'kit4', 'region' : [-129.505, -129.46, 52.63, 52.67]}
    allregions['kit4_kelpfield_oil'] = {'regionname' : 'kit4_kelpfield_oil', 'group' : 'kit4', 'region' : [-129.5, -129.4775, 52.6375, 52.6625]}
    
    
    #ARCTIC
    allregions['beaufort3_southcoast'] = {'regionname' : 'beaufort3_southcoast', 'group' : 'arctic', 'region' : [-140, -125, 67, 72]}
    allregions['beaufort3_sub'] = {'regionname' : 'beaufort3_sub', 'group' : 'arctic', 'region' : [-140.0, -106.04, 68.65, 79.34]}
    allregions['beaufort3_southcoast_tight'] = {'regionname' : 'beaufort3_southcoast_tight', 'group' : 'arctic', 'region' : [-140.0, -127.0, 68.5, 71.0]}
    allregions['beaufort3_oilmap_1'] = {'regionname' : 'beaufort3_oilmap_1', 'group' : 'arctic', 'region' : [-138.0, -132.5, 68.5, 70.0]}
    allregions['beaufort3'] = {'regionname' : 'beaufort3', 'group' : 'arctic', 'region' : [-152.51, -106.04, 68.65, 79.34]}
   
   
    #idealchannel
    allregions['ideal_channel_whole'] = {'regionname' : 'ideal_channel_whole', 'group' : 'ideal_channel', 'region' : [1.88, 2.12, 1.975, 2.025]}
    
      
    eastgroups=['bof','upperbof','aquaculture','stjohn','digbyneck']
    westgroups=['vhfr','kit4']
    arcticgroups=['arctic']
    for tdict in allregions.keys():
        allregions[tdict]['region'] = np.array(allregions[tdict]['region'])
        if 'figsize' not in allregions[tdict]:
            allregions[tdict]['figsize']=(8,6)
        if 'axes' not in allregions[tdict]:
            allregions[tdict]['axes']=[.125, .1, .775, .8]
        
        if 'coast' not in allregions[tdict]:
            if allregions[tdict]['group'] in eastgroups: 
                allregions[tdict]['coast']='mid_nwatl6c_sjh_lr.nc'
            if allregions[tdict]['group'] in westgroups: 
                allregions[tdict]['coast']='pacific_harbour.nc'
            if allregions[tdict]['group'] in arcticgroups: 
                allregions[tdict]['coast']='world_GSHHS_f_L1.nc'
                
        if 'textloc' not in allregions[tdict]:
            allregions[tdict]['textloc']=(.35,1.025)

    return allregions  





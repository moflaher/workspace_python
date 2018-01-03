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
    
   

    
    ##bof
    #tl=np.vstack([tl, [[-66.225, -66.195, 44.37, 44.41], 'pp','']])
    #tl=np.vstack([tl, [[-66.38, -66.29, 44.213, 44.32], 'gp','']])
    #tl=np.vstack([tl, [[-66.355, -66.32, 44.245, 44.2925], 'gp_tight', 'Grand Passage Tight']])
    #tl=np.vstack([tl, [[-66.345, -66.33, 44.26, 44.275], 'gp3', 'Grand Passage Site 3']])
    #tl=np.vstack([tl, [[-65.79, -65.73, 44.65, 44.7], 'dg', 'Digby Gut']])
    #tl=np.vstack([tl, [[-65.794, -65.743, 44.66, 44.71], 'dg_upper', 'Digby Gut Upper']])
    #tl=np.vstack([tl, [[-71.5, -57.5, 37.5, 46.5], 'sfmwhole', 'Scotia Fundy Maine']])
    #tl=np.vstack([tl, [[-67.6, -63.4, 43.8, 46], 'bof', 'Bay of Fundy']])
    #tl=np.vstack([tl, [[-64.52, -64.3, 45.3, 45.4], 'mp', 'Minas Passage']])
    #tl=np.vstack([tl, [[-64.45, -64.375, 45.35, 45.39], 'blackrock', 'Black Rock']])
    #tl=np.vstack([tl, [[-64.42, -64.38, 45.35, 45.38], 'blackrock_fld', 'Black Rock']])
    #tl=np.vstack([tl, [[-64.43, -64.4085, 45.361, 45.372], 'blackrock_ebb', 'Black Rock']])
    #tl=np.vstack([tl, [[-64.89, -64.66, 45.125, 45.36], 'capedor', 'capedor']])
    #tl=np.vstack([tl, [[-65.05, -64.5, 45.425, 45.75], 'capeenrage', 'capeenrage']])
    #tl=np.vstack([tl, [[-65.03, -64.221, 45.43, 46.15], 'northgrid', 'northgrid']])
    #tl=np.vstack([tl, [[-64.91, -64.64, 45.45, 45.675], 'northgrid_cape', 'northgrid_cape']])
    #tl=np.vstack([tl, [[-66.35, -65.95, 45.0, 45.3], 'sjr', 'sjr']])
    #tl=np.vstack([tl, [[-66.25, -66.1, 45.075, 45.2], 'seaview', 'seaview']])
    #tl=np.vstack([tl, [[-66.3, -65.75, 45.05, 45.7], 'sjr_kl', 'sjr_kl']])
    #tl=np.vstack([tl, [[-66.3, -65.9, 45.3, 45.6], 'longreach', 'longreach']])
    #tl=np.vstack([tl, [[-66.1055, -66.055, 45.2475, 45.290], 'reversing_falls', 'reversing_falls']])
    
    ##fishcage and slr
    #tl=np.vstack([tl, [[-65.5, -63.25, 44, 46], 'slr_upperbof', 'slr_upperbof']])
    #tl=np.vstack([tl, [[-67.5, -66, 44.5, 45.3], 'musq', 'musq']])
    #tl=np.vstack([tl, [[-66.925, -66.8, 45.0, 45.075], 'musq_cage', 'musq_cage']])
    #tl=np.vstack([tl, [[-66.90, -66.815, 45.025, 45.06], 'musq_cage_tight', 'musq_cage_tight']])
    #tl=np.vstack([tl, [[-66.88, -66.815, 45.015, 45.065], 'musq_cage_tight2', 'musq_cage_tight2']])
    #tl=np.vstack([tl, [[-66.85, -66.82, 45.0275, 45.0475], 'musq_4cage', 'musq_4cage']])
    #tl=np.vstack([tl, [[-67.6, -66.45, 44.3, 45.1], 'musq_large', 'musq_large']])
    ##Kitimat regions    
    #tl=np.vstack([tl, [[-132.32, -126.665, 51.16, 55.925], 'kit4', 'Kitimat Grid']])
    #tl=np.vstack([tl, [[-132.32, -126.665, 51.16, 55.925], 'kit4_tight', 'Kitimat Grid']])
    #tl=np.vstack([tl, [[-129.75, -129, 52.75, 53.5], 'gilisland', 'Gil Island']])
    #tl=np.vstack([tl, [[-129.8, -129, 52.9, 53.4], 'gilisland_tight', 'Gil Island']])
    #tl=np.vstack([tl, [[-129.5, -128.25, 53.25, 54.1], 'douglas', 'Douglas Channel']])
    #tl=np.vstack([tl, [[-129.75, -128.5, 52.9, 54.05], 'douglaslarge', 'Douglas Channel']])
    #tl=np.vstack([tl, [[-130.0, -129.0, 52.4, 53.4], 'kelparea2', 'kelparea2']])
    #tl=np.vstack([tl, [[-130, -128, 52, 54.1], 'mostchannels', 'mostchannels']])
    #tl=np.vstack([tl, [[-129.85, -129.25, 52.9, 53.225], 'doubleisland', 'doubleisland']])
    #tl=np.vstack([tl, [[-129.45, -129.38, 52.97, 53.01], 'kit4_kelp_tight', 'kit4_kelp_tight']])
    #tl=np.vstack([tl, [[-129.53, -129.38, 52.6, 52.75], 'kit4_kelp_tight2', 'kit4_kelp_tight2']])
    #tl=np.vstack([tl, [[-129.52, -129.41, 52.6, 52.7], 'kit4_kelp_tight2_small', 'kit4_kelp_tight2_small']])
    #tl=np.vstack([tl, [[-129.505, -129.46, 52.63, 52.67], 'kit4_kelp_tight2_kelpfield', 'kit4_kelp_tight2_kelpfield']])
    #tl=np.vstack([tl, [[-129.505, -129.475, 52.635, 52.665], 'kit4_kelpfield', 'kit4_kelpfield']])
    #tl=np.vstack([tl, [[-129.5, -129.4775, 52.6375, 52.6625], 'kit4_kelpfield_oil', 'kit4_kelpfield_oil']])
    #tl=np.vstack([tl, [[-129.54, -129.39, 52.95, 53.04], 'kit4_crossdouble', 'kit4_crossdouble']])
    #tl=np.vstack([tl, [[-129.825, -129.675, 53.1, 53.19], 'kit4_ftb', 'kit4_ftb']])
    #tl=np.vstack([tl, [[-129.5, -129.44, 53.04, 53.08], 'kit4_kelp_tight3', 'kit4_kelp_tight3']])
    #tl=np.vstack([tl, [[-129.61, -129.5, 52.96, 53.02], 'kit4_kelp_tight4', 'kit4_kelp_tight4']])
    #tl=np.vstack([tl, [[-129.47, -129.28, 52.48, 52.62], 'kit4_kelp_tight5', 'kit4_kelp_tight5']])
    #tl=np.vstack([tl, [[-129.36849, -129.3585, 52.54049, 52.5505], 'kit4_kelp_tight5_A2', 'kit4_kelp_tight5_A2']])
    #tl=np.vstack([tl, [[-129.4187, -129.40769, 52.56615, 52.578849], 'kit4_kelp_tight5_A6', 'kit4_kelp_tight5_A6']])
    #tl=np.vstack([tl, [[-129.43, -129.29, 52.725, 52.88], 'kit4_kelp_tight6', 'kit4_kelp_tight6']])
    #tl=np.vstack([tl, [[-129.47, -129.28, 52.452, 52.648], 'kit4_kelp_tight5_tall', 'kit4_kelp_tight5_tall']])
    #tl=np.vstack([tl, [[-129.526, -129.286, 52.4576, 52.7178], 'kit4_4island', 'kit4_4island']])
    #tl=np.vstack([tl, [[-129.6, -129.1, 52.45, 52.825], 'kelpchain', 'kelpchain']])
    #tl=np.vstack([tl, [[-128.9, -128.75, 53.525, 53.625], 'kit4_area5', 'Area 5']])
    #tl=np.vstack([tl, [[-129.23, -129, 53.1, 53.33], 'gilisland_east', 'gilisland_east']])
    #tl=np.vstack([tl, [[-129.56, -129.29, 53.136, 53.32], 'gilisland_west', 'gilisland_west']])
    #tl=np.vstack([tl, [[-129.33, -129.152, 52.98, 53.11], 'gilisland_south', 'gilisland_south']])

    ## arctic
    #tl=np.vstack([tl, [[-152.51, -106.04, 68.65, 79.34], 'beaufort3', 'Beaufort Sea']])
    #tl=np.vstack([tl, [[-140.0, -106.04, 68.65, 79.34], 'beaufort3_sub', 'Beaufort Sea']])
    #tl=np.vstack([tl, [[-140, -125, 67, 72], 'beaufort3_southcoast', 'Beaufort Sea']])
    #tl=np.vstack([tl, [[-140, -127, 68.5, 71], 'beaufort3_southcoast_tight', 'Beaufort Sea']])
    #tl=np.vstack([tl, [[-138, -132.5, 68.5, 70], 'beaufort3_oilmap_1', 'Beaufort Sea']])
    ##vhfr
    #tl=np.vstack([tl, [[-124, -121.95, 48.65, 49.8], 'vhfr_whole', 'Complete Domain for vhfr grids']])
    #tl=np.vstack([tl, [[-123.96833, -122, 48.797548, 49.69656], 'vhfr_tight', 'Complete Domain for vhfr grids']])
    #tl=np.vstack([tl, [[-123.325, -121.975, 48.95, 49.6], 'fr_whole', 'fr_whole']])
    #tl=np.vstack([tl, [[-123.33, -123.0, 49, 49.275], 'fr_mouth', 'fr_mouth']])
    #tl=np.vstack([tl, [[-122.75, -122.45, 49.25, 49.55], 'pitt_lake', 'pitt_lake']])
    #tl=np.vstack([tl, [[-122.7, -122.55, 49.3, 49.4], 'pitt_lake_sandbar', 'pitt_lake_sandbar']])
    #tl=np.vstack([tl, [[-123.1, -122.8, 49.075, 49.235], 'fr_area1', 'fr_area1']])
    #tl=np.vstack([tl, [[-122.8, -122.525, 49.14, 49.27], 'fr_area2', 'fr_area2']])
    #tl=np.vstack([tl, [[-122.2, -122.0, 49.11, 49.21], 'fr_area3', 'fr_area3']])
    #tl=np.vstack([tl, [[-122.83, -122.746, 49.20, 49.25], 'fr_sandbar_island1', 'fr_sandbar_island1']])
    #tl=np.vstack([tl, [[-123.286, -122.815, 49.242, 49.488], 'vh_whole', 'vh_whole']])
    #tl=np.vstack([tl, [[-123.191, -122.968, 49.256, 49.348], 'vh_harbour', 'vh_harbour']])
    #tl=np.vstack([tl, [[-123.125, -123.025, 49.256, 49.348], 'vh_harbour_tight', 'vh_harbour_tight']])
    #tl=np.vstack([tl, [[-123.16, -123.095, 49.291, 49.332], 'firstnarrows', 'firstnarrows']])
    #tl=np.vstack([tl, [[-123.04, -123.0, 49.288, 49.310], 'secondnarrows', 'secondnarrows']])
    #tl=np.vstack([tl, [[-123.0325, -123.015, 49.29, 49.302], 'secondnarrows_tight', 'secondnarrows_tight']])
    #tl=np.vstack([tl, [[-123.035, -123.0175, 49.2925, 49.301], 'secondnarrows_zoom', 'secondnarrows_zoom']])
    
    ##enav  
    ## vhfr  
    #tl=np.vstack([tl, [[-123.17, -122.99, 49.25, 49.34], 'vh_high_ship_approach1', 'vh_high_ship_approach1']])
    #tl=np.vstack([tl, [[-124, -122.7, 48.85, 49.5], 'vh_high_large', 'Large scale for vh_high']])
    ## stjohn
    #tl=np.vstack([tl, [[ -71.0, -58.2, 39.60, 46.5], 'stjohn_ship_approach1', 'stjohn_ship_approach1']])
    #tl=np.vstack([tl, [[ -66.14, -65.98, 45.18, 45.29], 'stjohn_harbour', 'stjohn_harbour']])
    #tl=np.vstack([tl, [[ -66.25, -65.83, 45.10, 45.70], 'stjohn_harbour_large', 'stjohn_harbour_large']])
    #tl=np.vstack([tl, [[ -66.07, -66.02, 45.2326, 45.275], 'stjohn_harbour_tight', 'stjohn_harbour_tight']])
    #tl=np.vstack([tl, [[-70, -62, 40, 46], 'enav_sjr_large', '']])
    #tl=np.vstack([tl, [[ 1.98, 2.018, 1.996, 2.0045], 'kelp_channel', 'kelp_channel']])
    #tl=np.vstack([tl, [[ -68.425, -62.85, 44.2, 46.1], 'bof_nemo', 'bof_nemo']])
    #tl=np.vstack([tl, [[ -66.14, -65.98, 45.20, 45.29], 'stjohn_nemo', 'stjohn_nemo']])


    allregions=OrderedDict()    
    
    #BOF


    allregions['doubleisland'] = {'regionname' : 'doubleisland', 'region' : [-129.85, -129.25, 52.9, 53.225]}
    allregions['sfmwhole'] = {'regionname' : 'sfmwhole', 'region' : [-71.5, -57.5, 37.5, 46.5]}
    allregions['gp'] = {'regionname' : 'gp', 'region' : [-66.38, -66.29, 44.213, 44.32]}
    allregions['musq_4cage'] = {'regionname' : 'musq_4cage', 'region' : [-66.85, -66.82, 45.0275, 45.0475]}
    allregions['blackrock_fld'] = {'regionname' : 'blackrock_fld', 'region' : [-64.42, -64.38, 45.35, 45.38]}
    allregions['gilisland_south'] = {'regionname' : 'gilisland_south', 'region' : [-129.33, -129.152, 52.98, 53.11]}
    allregions['stjohn_harbour_large'] = {'regionname' : 'stjohn_harbour_large', 'region' : [-66.25, -65.83, 45.1, 45.7]}
    allregions['stjohn_nemo'] = {'regionname' : 'stjohn_nemo', 'region' : [-66.14, -65.98, 45.2, 45.29]}
    allregions['fr_sandbar_island1'] = {'regionname' : 'fr_sandbar_island1', 'region' : [-122.83, -122.746, 49.2, 49.25]}
    allregions['fr_mouth'] = {'regionname' : 'fr_mouth', 'region' : [-123.33, -123.0, 49.0, 49.275]}
    allregions['kit4_kelp_tight5_A2'] = {'regionname' : 'kit4_kelp_tight5_A2', 'region' : [-129.36849, -129.3585, 52.54049, 52.5505]}
    allregions['kit4_kelp_tight5_A6'] = {'regionname' : 'kit4_kelp_tight5_A6', 'region' : [-129.4187, -129.40769, 52.56615, 52.578849]}
    allregions['kit4_ftb'] = {'regionname' : 'kit4_ftb', 'region' : [-129.825, -129.675, 53.1, 53.19]}
    allregions['blackrock'] = {'regionname' : 'blackrock', 'region' : [-64.45, -64.375, 45.35, 45.39]}
    allregions['kit4_4island'] = {'regionname' : 'kit4_4island', 'region' : [-129.526, -129.286, 52.4576, 52.7178]}
    allregions['dg'] = {'regionname' : 'dg', 'region' : [-65.79, -65.73, 44.65, 44.7]}
    allregions['northgrid_cape'] = {'regionname' : 'northgrid_cape', 'region' : [-64.91, -64.64, 45.45, 45.675]}
    allregions['beaufort3_southcoast'] = {'regionname' : 'beaufort3_southcoast', 'region' : [-140, -125, 67, 72]}
    allregions['kit4'] = {'regionname' : 'kit4', 'region' : [-132.32, -126.665, 51.16, 55.925]}
    allregions['kit4_kelp_tight5_tall'] = {'regionname' : 'kit4_kelp_tight5_tall', 'region' : [-129.47, -129.28, 52.452, 52.648]}
    allregions['longreach'] = {'regionname' : 'longreach', 'region' : [-66.3, -65.9, 45.3, 45.6]}
    allregions['kelp_channel'] = {'regionname' : 'kelp_channel', 'region' : [1.98, 2.018, 1.996, 2.0045]}
    allregions['vh_whole'] = {'regionname' : 'vh_whole', 'region' : [-123.286, -122.815, 49.242, 49.488]}
    allregions['vh_high_large'] = {'regionname' : 'vh_high_large', 'region' : [-124.0, -122.7, 48.85, 49.5]}
    allregions['slr_upperbof'] = {'regionname' : 'slr_upperbof', 'region' : [-65.5, -63.25, 44.0, 46.0]}
    allregions['beaufort3_sub'] = {'regionname' : 'beaufort3_sub', 'region' : [-140.0, -106.04, 68.65, 79.34]}
    allregions['gilisland_east'] = {'regionname' : 'gilisland_east', 'region' : [-129.23, -129.0, 53.1, 53.33]}
    allregions['beaufort3_southcoast_tight'] = {'regionname' : 'beaufort3_southcoast_tight', 'region' : [-140.0, -127.0, 68.5, 71.0]}
    allregions['enav_sjr_large'] = {'regionname' : 'enav_sjr_large', 'region' : [-70, -62, 40, 46]}
    allregions['kelpchain'] = {'regionname' : 'kelpchain', 'region' : [-129.6, -129.1, 52.45, 52.825]}
    allregions['douglaslarge'] = {'regionname' : 'douglaslarge', 'region' : [-129.75, -128.5, 52.9, 54.05]}
    allregions['kelparea2'] = {'regionname' : 'kelparea2', 'region' : [-130.0, -129.0, 52.4, 53.4]}
    allregions['kit4_area5'] = {'regionname' : 'kit4_area5', 'region' : [-128.9, -128.75, 53.525, 53.625]}
    allregions['musq_large'] = {'regionname' : 'musq_large', 'region' : [-67.6, -66.45, 44.3, 45.1]}
    allregions['secondnarrows'] = {'regionname' : 'secondnarrows', 'region' : [-123.04, -123.0, 49.288, 49.31]}
    allregions['douglas'] = {'regionname' : 'douglas', 'region' : [-129.5, -128.25, 53.25, 54.1]}
    allregions['stjohn_ship_approach1'] = {'regionname' : 'stjohn_ship_approach1', 'region' : [-71.0, -58.2, 39.6, 46.5]}
    allregions['musq_cage'] = {'regionname' : 'musq_cage', 'region' : [-66.925, -66.8, 45.0, 45.075]}
    allregions['mp'] = {'regionname' : 'mp', 'region' : [-64.52, -64.3, 45.3, 45.4]}
    allregions['kit4_kelp_tight2_small'] = {'regionname' : 'kit4_kelp_tight2_small', 'region' : [-129.52, -129.41, 52.6, 52.7]}
    allregions['dg_upper'] = {'regionname' : 'dg_upper', 'region' : [-65.794, -65.743, 44.66, 44.71]}
    allregions['kit4_kelp_tight6'] = {'regionname' : 'kit4_kelp_tight6', 'region' : [-129.43, -129.29, 52.725, 52.88]}
    allregions['kit4_kelp_tight4'] = {'regionname' : 'kit4_kelp_tight4', 'region' : [-129.61, -129.5, 52.96, 53.02]}
    allregions['kit4_kelp_tight5'] = {'regionname' : 'kit4_kelp_tight5', 'region' : [-129.47, -129.28, 52.48, 52.62]}
    allregions['kit4_kelp_tight2'] = {'regionname' : 'kit4_kelp_tight2', 'region' : [-129.53, -129.38, 52.6, 52.75]}
    allregions['kit4_kelp_tight3'] = {'regionname' : 'kit4_kelp_tight3', 'region' : [-129.5, -129.44, 53.04, 53.08]}
    allregions['kit4_kelp_tight'] = {'regionname' : 'kit4_kelp_tight', 'region' : [-129.45, -129.38, 52.97, 53.01]}
    allregions['beaufort3_oilmap_1'] = {'regionname' : 'beaufort3_oilmap_1', 'region' : [-138.0, -132.5, 68.5, 70.0]}
    allregions['firstnarrows'] = {'regionname' : 'firstnarrows', 'region' : [-123.16, -123.095, 49.291, 49.332]}
    allregions['sjr'] = {'regionname' : 'sjr', 'region' : [-66.35, -65.95, 45.0, 45.3]}
    allregions['seaview'] = {'regionname' : 'seaview', 'region' : [-66.25, -66.1, 45.075, 45.2]}
    allregions['vh_harbour_tight'] = {'regionname' : 'vh_harbour_tight', 'region' : [-123.125, -123.025, 49.256, 49.348]}
    allregions['pitt_lake'] = {'regionname' : 'pitt_lake', 'region' : [-122.75, -122.45, 49.25, 49.55]}
    allregions['sjr_kl'] = {'regionname' : 'sjr_kl', 'region' : [-66.3, -65.75, 45.05, 45.7]}
    allregions['bof'] = {'regionname' : 'bof', 'region' : [-67.6, -63.4, 43.8, 46.0]}
    allregions['vhfr_whole'] = {'regionname' : 'vhfr_whole', 'region' : [-124.0, -121.95, 48.65, 49.8]}
    allregions['capeenrage'] = {'regionname' : 'capeenrage', 'region' : [-65.05, -64.5, 45.425, 45.75]}
    allregions['vh_harbour'] = {'regionname' : 'vh_harbour', 'region' : [-123.191, -122.968, 49.256, 49.348]}
    allregions['kit4_tight'] = {'regionname' : 'kit4_tight', 'region' : [-132.32, -126.665, 51.16, 55.925]}
    allregions['pp'] = {'regionname' : 'pp', 'region' : [-66.225, -66.195, 44.37, 44.41]}
    allregions['vh_high_ship_approach1'] = {'regionname' : 'vh_high_ship_approach1', 'region' : [-123.17, -122.99, 49.25, 49.34]}
    allregions['kit4_kelpfield_oil'] = {'regionname' : 'kit4_kelpfield_oil', 'region' : [-129.5, -129.4775, 52.6375, 52.6625]}
    allregions['bof_nemo'] = {'regionname' : 'bof_nemo', 'region' : [-68.425, -62.85, 44.2, 46.1]}
    allregions['gilisland_west'] = {'regionname' : 'gilisland_west', 'region' : [-129.56, -129.29, 53.136, 53.32]}
    allregions['kit4_kelpfield'] = {'regionname' : 'kit4_kelpfield', 'region' : [-129.505, -129.475, 52.635, 52.665]}
    allregions['gilisland_tight'] = {'regionname' : 'gilisland_tight', 'region' : [-129.8, -129.0, 52.9, 53.4]}
    allregions['stjohn_harbour'] = {'regionname' : 'stjohn_harbour', 'region' : [-66.14, -65.98, 45.18, 45.29]}
    allregions['vhfr_tight'] = {'regionname' : 'vhfr_tight', 'region' : [-123.96833, -122.0, 48.797548, 49.69656]}
    allregions['secondnarrows_tight'] = {'regionname' : 'secondnarrows_tight', 'region' : [-123.0325, -123.015, 49.29, 49.302]}
    allregions['capedor'] = {'regionname' : 'capedor', 'region' : [-64.89, -64.66, 45.125, 45.36]}
    allregions['musq'] = {'regionname' : 'musq', 'region' : [-67.5, -66.0, 44.5, 45.3]}
    allregions['gilisland'] = {'regionname' : 'gilisland', 'region' : [-129.75, -129.0, 52.75, 53.5]}
    allregions['pitt_lake_sandbar'] = {'regionname' : 'pitt_lake_sandbar', 'region' : [-122.7, -122.55, 49.3, 49.4]}
    allregions['gp_tight'] = {'regionname' : 'gp_tight', 'region' : [-66.355, -66.32, 44.245, 44.2925]}
    allregions['fr_area1'] = {'regionname' : 'fr_area1', 'region' : [-123.1, -122.8, 49.075, 49.235]}
    allregions['fr_area2'] = {'regionname' : 'fr_area2', 'region' : [-122.8, -122.525, 49.14, 49.27]}
    allregions['fr_area3'] = {'regionname' : 'fr_area3', 'region' : [-122.2, -122.0, 49.11, 49.21]}
    allregions['gp3'] = {'regionname' : 'gp3', 'region' : [-66.345, -66.33, 44.26, 44.275]}
    allregions['musq_cage_tight'] = {'regionname' : 'musq_cage_tight', 'region' : [-66.9, -66.815, 45.025, 45.06]}
    allregions['musq_cage_tight2'] = {'regionname' : 'musq_cage_tight2', 'region' : [-66.88, -66.815, 45.015, 45.065]}
    allregions['blackrock_ebb'] = {'regionname' : 'blackrock_ebb', 'region' : [-64.43, -64.4085, 45.361, 45.372]}
    allregions['beaufort3'] = {'regionname' : 'beaufort3', 'region' : [-152.51, -106.04, 68.65, 79.34]}
    allregions['secondnarrows_zoom'] = {'regionname' : 'secondnarrows_zoom', 'region' : [-123.035, -123.0175, 49.2925, 49.301]}
    allregions['kit4_crossdouble'] = {'regionname' : 'kit4_crossdouble', 'region' : [-129.54, -129.39, 52.95, 53.04]}
    allregions['stjohn_harbour_tight'] = {'regionname' : 'stjohn_harbour_tight', 'region' : [-66.07, -66.02, 45.2326, 45.275]}
    allregions['mostchannels'] = {'regionname' : 'mostchannels', 'region' : [-130.0, -128.0, 52.0, 54.1]}
    allregions['reversing_falls'] = {'regionname' : 'reversing_falls', 'region' : [-66.1055, -66.055, 45.2475, 45.29]}
    allregions['fr_whole'] = {'regionname' : 'fr_whole', 'region' : [-123.325, -121.975, 48.95, 49.6]}
    allregions['kit4_kelp_tight2_kelpfield'] = {'regionname' : 'kit4_kelp_tight2_kelpfield', 'region' : [-129.505, -129.46, 52.63, 52.67]}
    allregions['northgrid'] = {'regionname' : 'northgrid', 'region' : [-65.03, -64.221, 45.43, 46.15]}
      

    for tdict in allregions.keys():
        allregions[tdict]['region'] = np.array(allregions[tdict]['region'])
        if not allregions[tdict].haskey('figsize'):
            allregions[tdict]['figsize']=(8,6)
        #tmpdic['regionname']=row[1]
        #allregions[row[1]]=tmpdic
    return allregions  





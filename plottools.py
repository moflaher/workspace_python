from __future__ import division
import matplotlib.pyplot as plt

"""
Front Matter
=============

Created in 2014

Author: Mitchell O'Flaherty-Sproul

functions to make plotting faster or easier, or have cleaner code.

Requirements
===================================
Absolutely Necessary:


Optional, but recommended:


Functions
=========
prettyplotll -   sets axis labels and stuff for long lat plots.
            
"""


def prettyplot_ll(plt,**kwargs):

    if kwargs is not None:
        for key, value in kwargs.iteritems():
            if ((key=='grid') and (value==True)):
                plt.grid()
            if (key=='title'):
                plt.title(value)
            if (key=='setregion'):
                plt.axis(value['region'])

    plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
    plt.gca().set_xticklabels(-1*(plt.gca().get_xticks()))
    plt.gca().set_xlabel(r'Longitude $(W^{\circ})$')
    plt.gca().set_ylabel(r'Latitude $(N^{\circ})$')

    return plt

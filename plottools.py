from __future__ import division
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seawater as sw
from mpl_toolkits.axes_grid1 import make_axes_locatable

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
                plt.gca().set_aspect(get_aspectratio(value))
            if (key=='cblabel'):
                cblabel=value    
               

    plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    plt.gca().set_xticklabels(-1*(plt.gca().get_xticks()))
    plt.gca().set_xlabel(r'Longitude (W$^{\circ}$)')
    plt.gca().set_ylabel(r'Latitude (N$^{\circ}$)')

    aspect=plt.gca().get_aspect()
    if (aspect>1):
        slicer=(np.floor(aspect).astype(int)+1)
        for label in plt.gca().get_xticklabels()[::slicer]:
            label.set_visible(False)
    
    if (cblabel != None):
        divider = make_axes_locatable(plt.gca())
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(cax=cax)

    return plt


def get_aspectratio(region,LL=1):
    if (LL==0):
        H=region['region'][3]-region['region'][2]
        L=region['region'][1]-region['region'][0]
    else:
        H1=(sw.dist([region['region'][3], region['region'][2]],[region['region'][0], region['region'][0]],'km'))[0];
        H2=(sw.dist([region['region'][3], region['region'][2]],[region['region'][1], region['region'][1]],'km'))[0];
        H=1/2*(H1+H2);
        
        W1=(sw.dist([region['region'][3], region['region'][3]],[region['region'][0], region['region'][1]],'km'))[0];
        W2=(sw.dist([region['region'][2], region['region'][2]],[region['region'][0], region['region'][1]],'km'))[0];
        W=1/2*(W1+W2);


    return H/W

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


def prettyplot_ll(axin,**kwargs):

    cblabel=None

    if kwargs is not None:
        for key, value in kwargs.iteritems():
            if ((key=='grid') and (value==True)):
                axin.grid()
            if (key=='title'):
                axin.set_title(value)
            if (key=='setregion'):
                axin.axis(value['region'])
                axin.set_aspect(get_aspectratio(value))
            if (key=='cblabel'):
                cblabel=value    
               


    _formatter = mpl.ticker.ScalarFormatter(useOffset=False)
    axin.yaxis.set_major_formatter(_formatter)
    axin.xaxis.set_major_formatter(_formatter)
    axin.set_xticklabels(-1*(axin.get_xticks()))
    axin.set_xlabel(r'Longitude (W$^{\circ}$)')
    axin.set_ylabel(r'Latitude (N$^{\circ}$)')

    aspect=axin.get_aspect()
    if (aspect>1):
        slicer=(np.floor(aspect).astype(int)+1)
        for label in axin.get_xticklabels()[::slicer]:
            label.set_visible(False)
    
    if (cblabel != None):
        #doesnt really work        
        #divider = make_axes_locatable(axin)
        #cax = divider.append_axes("right", size="5%", pad=0.25)
        #plt.colorbar(cax=cax)
        plt.draw()
        box=axin.get_position()
        box.set_points(np.array([[box.xmin,box.ymin],[box.xmax-.1,box.ymax]]))
        axin.set_position(box)
        plt.draw()
        box=axin.get_position()
        cax=plt.gcf().add_axes([box.xmax + .05, box.ymin, .025, box.height])
        cb=plt.colorbar(cax=cax)
        cb.set_label(cblabel,fontsize=10)

    return axin


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

from __future__ import division,print_function
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seawater as sw
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import gridtools as gt
import datatools as dt
import misctools as mt
import projtools as pjt
from folderpath import *
import os
import inspect
#from osgeo import osr, gdal
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter
import matplotlib.path as path
import pandas as pd
import matplotlib.dates as dates
from collections import OrderedDict


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
"""


def prettyplot_ll(axin,**kwargs):
    """
    Formats an axes.    
    NOTE*: This code is dirty and old. It should be updated at some point....


    :Parameters:
        axin - a plt axes
    :Optional:
        grid - True/False to enable grid (default False)
        setregion - Which region to zoom in on and set the aspect ratio. (default N/A)
        cb - The colorbar value.
        cblabel - The colorbar label. Must specify cb if cblabel is specified.
        title -  Adds a title to the axes.

 
    """

    cblabel=None
    skinny=False
    fontsize=12
    ticksin=True
    axlabels=True

    if kwargs is not None:
        for key, value in kwargs.iteritems():
            if ((key=='grid') and (value==True)):
                axin.grid()
            if (key=='title'):
                axin.set_title(value)
            if (key=='setregion'):
                axin.axis(value['region'])
                axin.set_aspect(get_aspectratio(value),anchor='SW')
            if (key=='cblabel'):
                cblabel=value    
            if (key=='cb'):
                colorax=value    
            if (key=='fontsize'):
                fontsize=value 
            if (key=='ticksin'):
                ticksin=value 
            if (key=='axlabels'):
                axlabels=value
               
               
    f=axin.get_figure()
    _formatter = mpl.ticker.ScalarFormatter(useOffset=False)
    axin.yaxis.set_major_formatter(_formatter)
    axin.xaxis.set_major_formatter(_formatter)
    axin.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: -1*x))
    #axin.set_xticklabels(-1*(axin.get_xticks()))
    if axlabels:
        axin.set_xlabel(r'Longitude ($^{\circ}$W)')
        axin.set_ylabel(r'Latitude ($^{\circ}$N)')
    else:
        axin.xaxis.set_tick_params(labelbottom='off')
        axin.yaxis.set_tick_params(labelleft='off')



    for label in axin.get_xticklabels() +axin.get_yticklabels():
        label.set_fontsize(fontsize)
        
    if ticksin:
        axin.tick_params(direction='in')


    aspect=axin.get_aspect()
    if (aspect!='auto'):
        if (aspect>1.3):
            skinny=True
            #slicer=(np.floor(aspect).astype(int)+1)
            for label in axin.get_xticklabels()[::2]:
                label.set_visible(False)
    
    if (cblabel != None):
        f.canvas.draw()
        #Find the bounding box and if its too big for a colorbar then reduce size
        box=axin.get_position()
        cbarwidth=box.xmax+0.1+0.1
        if cbarwidth>1.0:
            resize=cbarwidth-1.0+.01
            box.set_points(np.array([[box.xmin,box.ymin],[box.xmax-resize,box.ymax]]))
            axin.set_position(box)
            f.canvas.draw()            
            box=axin.get_position()
            
        cax=f.add_axes([box.xmax + .025, box.ymin, .025, box.height])

        cb=plt.colorbar(colorax,cax=cax)
        cb.set_label(cblabel,fontsize=10)


def setplot(region):
    """
    Setup the figure, axes, and colorbar location for a plot.
    
    Takes a region
    """
    f=plt.figure()
    ax=plt.axes([.125,.1,.775,.8])   
    _formatter = mpl.ticker.ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(_formatter)
    ax.xaxis.set_major_formatter(_formatter)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: -1*x))
    ax.set_xlabel(r'Longitude ($^{\circ}$W)')
    ax.set_ylabel(r'Latitude ($^{\circ}$N)')
    ax.axis(region['region'])
    #ax.set_aspect(get_aspectratio(region),anchor='SW')
    f.canvas.draw()

    #Find the bounding box and if its too big for a colorbar then reduce size
    box=ax.get_position()
    cbarwidth=box.xmax+0.1+0.1
    if cbarwidth>1.0:
        resize=cbarwidth-1.0+.01
        box.set_points(np.array([[box.xmin,box.ymin],[box.xmax-resize,box.ymax]]))
        ax.set_position(box)
        f.canvas.draw()
        
    box=ax.get_position()
    cax=f.add_axes([box.xmax + .025, box.ymin, .025, box.height])    
    
    
    return f,ax,cax



def get_data_ratio(region):
    """
    Returns the aspect ratio of the region data.
    
    :Parameters:
        region - a region as defined in regions.py
    """

    xsize = np.max(np.hstack([np.fabs(region['region'][1] - region['region'][0]), 1e-30]))
    ysize = np.max(np.hstack([np.fabs(region['region'][3] - region['region'][2]), 1e-30]))

    return ysize / xsize


def get_aspectratio(region,LL=1):
    """
    Takes a region and returns the average aspect ratio of the data.


    :Parameters:
        region - a region as defined in regions.py
    :Optional:
        LL - if LL is 0 then uses an xy region instead of a region.

 
    """
    if (LL==0):
        H=region['regionxy'][3]-region['regionxy'][2]
        W=region['regionxy'][1]-region['regionxy'][0]
    else:
        H1=(sw.dist([region['region'][3], region['region'][2]],[region['region'][0], region['region'][0]],'km'))[0];
        H2=(sw.dist([region['region'][3], region['region'][2]],[region['region'][1], region['region'][1]],'km'))[0];
        H=1/2*(H1+H2);
        
        W1=(sw.dist([region['region'][3], region['region'][3]],[region['region'][0], region['region'][1]],'km'))[0];
        W2=(sw.dist([region['region'][2], region['region'][2]],[region['region'][0], region['region'][1]],'km'))[0];
        W=1/2*(W1+W2);


    return H/W


def plot_box(axin,region,color='k',lw=1):
    """
    Plots a box defined by a region on an axes.

    :Parameters:
        axin - a plt axes to plot on.
        region - a region as defined in regions.py
    :Optional:
        color - the color on the box (default black).
        lw - the width of the box's lines (default 1). 
    """
    axin.plot([region['region'][0],region['region'][0]],[region['region'][2],region['region'][3]],color,lw=lw)
    axin.plot([region['region'][1],region['region'][1]],[region['region'][2],region['region'][3]],color,lw=lw)
    axin.plot([region['region'][0],region['region'][1]],[region['region'][2],region['region'][2]],color,lw=lw)
    axin.plot([region['region'][0],region['region'][1]],[region['region'][3],region['region'][3]],color,lw=lw)


def fix_osw(axin):
    """
    Reformats an ax. Disables offset, and reverses x-axis.

    :Parameters:
        axin - a plt ax to modify.
    """
    _formatter = mpl.ticker.ScalarFormatter(useOffset=False)
    axin.yaxis.set_major_formatter(_formatter)
    axin.xaxis.set_major_formatter(_formatter)
    axin.set_xticklabels(-1*(axin.get_xticks()))


def plotcoast(axin,**kwargs):
    """
    Plots the coastline on an ax.

    :Parameters:
        axin - a plt axes to plot on.
    :Optional:
        filename - which coastline file to use. Use nc coastline format from xscan. (default mid_nwatl6b.nc)
        color - the color on the coastline (default black).
        lw - the width of the coastline's lines (default 1).
        ls - the style of the coastline's lines (default 1).
        fill - True/False to fill in the coastline (default False)
        fcolor - the color used to fill the coastline (default 0.75, dark gray)
        ticksout - Face the axis ticksout  (R style - default False) 
    """ 

   
    color='k'
    lw=1
    ls='solid'
    filename='mid_nwatl6c.nc'
    fcolor='0.75'
    fill=False
    filepath=[]
    zorder=1

    if kwargs is not None:
        for key, value in kwargs.iteritems():            
            if (key=='color'):
                color=value
            if (key=='lw'):
                lw=value
            if (key=='ls'):
                ls=value    
            if (key=='filename'):
                filename=value   
            if (key=='fill'):
                fill=value 
            if (key=='fcolor'):
                fcolor=value
            if (key=='filepath'):
                filepath=value     
            if (key=='zorder'):
                zorder=value 
    if filepath==[]:
        _base_dir = os.path.realpath(inspect.stack()[0][1])
        idx=_base_dir.rfind('/')
        sl=dt.loadnc(_base_dir[:idx],singlename='/data/shorelines/'+filename, fvcom=False)
    else:
        sl=dt.loadnc(filepath,singlename=filename, fvcom=False)

    idx=np.where(sl['count']!=0)[0]
    sl['count']=sl['count'][idx]
    sl['start']=sl['start'][idx]

    tmparray=[list(zip(sl['lon'][sl['start'][i]:(sl['start'][i]+sl['count'][i])],sl['lat'][sl['start'][i]:(sl['start'][i]+sl['count'][i])])) for i in range(0,len(sl['start']))]

    if fill==True:
        coastseg=PC(tmparray,facecolor = fcolor,edgecolor=color,linewidths=lw,zorder=zorder)
    else:
        coastseg=LC(tmparray,linewidths = lw,linestyles=ls,color=color,zorder=zorder)



    

    axin.add_collection(coastseg)


def plotgrid_num(data,size,num,nore):
    if nore=='n':
        region={}
        region['region']=[data['nodexy'][num,0]-size,data['nodexy'][num,0]+size,data['nodexy'][num,1]-size,data['nodexy'][num,1]+size]
        idx=dt.get_nodes_xy(data,region)
        plt.triplot(data['trigridxy'],lw=.5)
        for i in idx:
            plt.text(data['nodexy'][i,0],data['nodexy'][i,1],("%d"%i),fontsize=10,bbox={'facecolor':'white', 'alpha':.7, 'pad':3})
        region2={}
        region2['region']=[data['nodexy'][num,0]-(size*2),data['nodexy'][num,0]+(size*2),data['nodexy'][num,1]-(size*2),data['nodexy'][num,1]+(size*2)]
        plt.axis(region2['region'])
        plt.show()
    if nore=='e':
        region={}
        region['region']=[data['uvnode'][num,0]-size,data['uvnode'][num,0]+size,data['uvnode'][num,1]-size,data['uvnode'][num,1]+size]
        idx=dt.get_elements_xy(data,region)
        plt.triplot(data['trigridxy'],lw=.5)
        for i in idx:
            plt.text(data['uvnode'][i,0],data['uvnode'][i,1],("%d"%i),fontsize=10,bbox={'facecolor':'white', 'alpha':.7, 'pad':3})
        region2={}
        region2['region']=[data['uvnode'][num,0]-(size*2),data['uvnode'][num,0]+(size*2),data['uvnode'][num,1]-(size*2),data['uvnode'][num,1]+(size*2)]
        plt.axis(region2['region'])
        plt.show()


def add_num_label(axin,data,size,num,nore):
    if nore=='n':
        region={}
        region['region']=[data['nodexy'][num,0]-size,data['nodexy'][num,0]+size,data['nodexy'][num,1]-size,data['nodexy'][num,1]+size]
        idx=dt.get_nodes_xy(data,region)
        for i in idx:
            axin.text(data['nodell'][i,0],data['nodell'][i,1],("%d"%i),fontsize=10,bbox={'facecolor':'white', 'alpha':.7, 'pad':3})
       
    if nore=='e':
        region={}
        region['region']=[data['uvnode'][num,0]-size,data['uvnode'][num,0]+size,data['uvnode'][num,1]-size,data['uvnode'][num,1]+size]
        idx=dt.get_elements_xy(data,region)
        for i in idx:
            axin.text(data['uvnodell'][i,0],data['uvnodell'][i,1],("%d"%i),fontsize=10,bbox={'facecolor':'white', 'alpha':.7, 'pad':3})
        

def plotgrid_ll(data,size,ll,nore):
    if nore=='n':
        num=dt.closest_node(data,ll)
        region={}
        region['region']=[data['nodexy'][num,0]-size,data['nodexy'][num,0]+size,data['nodexy'][num,1]-size,data['nodexy'][num,1]+size]
        idx=dt.get_nodes_xy(data,region)
        plt.triplot(data['trigridxy'],lw=.5)
        for i in idx:
            plt.text(data['nodexy'][i,0],data['nodexy'][i,1],("%d"%i),fontsize=10,bbox={'facecolor':'white', 'alpha':.7, 'pad':3})
        region2={}
        region2['region']=[data['nodexy'][num,0]-(size*2),data['nodexy'][num,0]+(size*2),data['nodexy'][num,1]-(size*2),data['nodexy'][num,1]+(size*2)]
        plt.axis(region2['region'])
        plt.show()
    if nore=='e':
        num=dt.closest_element(data,ll)
        region={}
        region['region']=[data['uvnode'][num,0]-size,data['uvnode'][num,0]+size,data['uvnode'][num,1]-size,data['uvnode'][num,1]+size]
        idx=dt.get_elements_xy(data,region)
        plt.triplot(data['trigridxy'],lw=.5)
        for i in idx:
            plt.text(data['uvnode'][i,0],data['uvnode'][i,1],("%d"%i),fontsize=10,bbox={'facecolor':'white', 'alpha':.7, 'pad':3})
        region2={}
        region2['region']=[data['uvnode'][num,0]-(size*2),data['uvnode'][num,0]+(size*2),data['uvnode'][num,1]-(size*2),data['uvnode'][num,1]+(size*2)]
        plt.axis(region2['region'])
        plt.show()


def ax_label_spacer(axin):
    """
    Removes every second x and y ticklabel.
    
    :Parameters:
        axin - a plt axes.
    """
    for label in axin.get_xticklabels()[::2] +axin.get_yticklabels()[::2]:
        label.set_visible(False)


def place_axes(region,numplots,cb=True,rotation=True):
    """
    For placing "subplot" axes when setting aspect ratio. Function starts and returns the figure and axes.

    :Parameters:
        region - The region being plotted, needed for aspect ratio
        numplots - The number of axes being define   
    :Optional:
        cb - True/False option for colorbar (default True So that plots of the same area appear the same in frame.)
    """

    #note to check region orientations this function uses aspect*fa. It is possible it may need to use dr as well. If weird axes orientation are return check into the effect of dr.
    f=plt.figure()
    axarr = np.empty(numplots, dtype=object)

    aspect=get_aspectratio(region)
    dr=get_data_ratio(region)
    figW, figH = f.get_size_inches()
    fa = figH / figW    
            
    #Define the working space for plotting
    #Default to assuming colorbar so regions are the same on the canvas regardless
    #Can override colorbar with cb=False
    ystart=0.1
    yspace=0.8
    xstart=0.125
    xspace=0.775
    axisgap=0.01   
    axf=np.zeros((numplots,4))
     
            
    if  (aspect>=1/fa):
        #For axes that are taller then wide
        
        #Left value is colorbar width in ppll_sub 
        #Right value is a guess at a general text width
        if cb==True:
            cbspace=0.1
        else:
            cbspace=0
            
        if rotation==True:
            rotspace=0.05
        else:
            rotspace=0  
            
        #How much space per plot
        spaceper=(xspace-axisgap*(numplots-1))/numplots
        
        #Given the available horizontal space per plot where will the axes width endup
        ytarget=spaceper*dr*aspect/fa
        #If the axes width plus colorbar width is greater than the space.
        #Then decrease the axes width to the xspace minus the colorbar space
        if (ytarget+cbspace+rotspace)>yspace:
            ytarget=yspace-cbspace-rotspace
        #Figure out the final plot height so we can place the axes in the correct locations
        xtarget=ytarget*fa/aspect/dr
        
        
        axf[0,:]=[xstart,ystart+cbspace+rotspace,1,ytarget]
        for i in range(1,numplots):
            axf[i,:]=[xstart+(axisgap+xtarget)*i,ystart+cbspace+rotspace,1,ytarget]
        
    else:
        #For axes that are wider then tall       
        
        #Left value is colorbar width in ppll_sub 
        #Right value is a guess at a general text width
        if cb==True:
            cbspace=0.025+0.035+axisgap
        else:
            cbspace=0
        
        #How much space per plot
        spaceper=(yspace-axisgap*(numplots-1))/numplots
        
        #Given the available vertical space per plot where will the axes width endup
        xtarget=spaceper*fa/aspect/dr
        #If the axes width plus colorbar width is greater than the space.
        #Then decrease the axes width to the xspace minus the colorbar space
        if (xtarget+cbspace)>xspace:
            xtarget=xspace-cbspace
        #Figure out the final plot height so we can place the axes in the correct locations
        ytarget=xtarget*dr*aspect/fa
        
        axf[0,:]=[xstart,ystart,xtarget,1]
        for i in range(1,numplots):
            axf[i,:]=[xstart,ystart+(axisgap+ytarget)*i,xtarget,1]  
        axf=np.flipud(axf)
                    
    
    for i in range(numplots):
        axarr[i]=f.add_axes(axf[i,:])

    return f,axarr

    
def ppll_sub(axin,**kwargs):
    """
    Formats ax from place_axes. Looks similar to prettyplot_ll, but corrects for subplots.
    NOTE: If cblabel is specified then cb must be specified as well. len(cb)==len(cblabel) for code to function.

    :Parameters:
        axin - The axes to be modified.
    :Optional:
        grid - True/False to enable grid (default False)
        setregion - Which region to zoom in on and set the aspect ratio. (default N/A)
        cb - The colorbar value/s. If len(cb)==1 the colorbar will be used for all axes. Otherwise one colorbar per axes.       
        cblabel - The label or labels for the colorbar/s
        cblabelsize -  The fontsize of the colorbar labels.
        cbticksize -  The fontsize of the colorbar ticks.
        fontsize -  The fontsize of the x and y ticks.
        llfontsize -  The fontsize of the x and y axis labels.
        ticksout - Face the axis ticksout  (R style - default False) 
        
    """
    cblabel=None
    axspacer=True
    cblabelsize=8
    rotation=0
    fontsize=10
    cbticksize=8
    llfontsize=12
    cbtickrotation=0
    ticksin=True

    if kwargs is not None:
        for key, value in kwargs.iteritems():
            if ((key=='grid') and (value==True)):
                for ax in axin:
                    ax.grid()
            if (key=='setregion'):                
                for ax in axin:
                    ax.axis(value['region'])
                    ax.set_aspect(get_aspectratio(value),anchor='SW')
            if (key=='cblabel'):
                cblabel=value    
            if (key=='cb'):
                colorax=value    
            if (key=='cblabelsize'):
                cblabelsize=value     
            if (key=='cbticksize'):
                cbticksize=value     
            if (key=='rotation'):
                rotation=value 
            if (key=='fontsize'):
                fontsize=value 
            if (key=='llfontsize'):
                llfontsize=value 
            if (key=='cbtickrotation'):
                cbtickrotation=value 
            if (key=='ticksin'):
                ticksin=value 
               
    f=axin[0].get_figure()
    figW, figH = f.get_size_inches()
    fa = figH / figW
    
    if ticksin:
        for ax in axin:
            ax.tick_params(direction='in')
    

    aspect=axin[0].get_aspect()
    if (aspect>=1/fa):
        rotation=-45
        for ax in axin:
            ax.set_xlabel(r'Longitude ($^{\circ}$W)',fontsize=llfontsize)
            ax.yaxis.set_tick_params(labelleft='off')
        axin[0].yaxis.set_tick_params(labelleft='on')
        axin[0].set_ylabel(r'Latitude ($^{\circ}$N)',fontsize=llfontsize)
    else:
        for ax in axin:
            ax.set_ylabel(r'Latitude ($^{\circ}$N)',fontsize=llfontsize)
            ax.xaxis.set_tick_params(labelbottom='off')
        axin[-1].xaxis.set_tick_params(labelbottom='on')
        axin[-1].set_xlabel(r'Longitude ($^{\circ}$W)',fontsize=llfontsize)
    

    if axspacer==True:
        for ax in axin:
            for label in ax.get_xticklabels()[::2] +ax.get_yticklabels()[::2]:
                label.set_visible(False)


    _formatter = mpl.ticker.ScalarFormatter(useOffset=False)
    for ax in axin:
        ax.yaxis.set_major_formatter(_formatter)
        ax.xaxis.set_major_formatter(_formatter)
        ax.set_xticklabels(-1*(ax.get_xticks()),rotation=rotation)
        for label in ax.get_xticklabels() +ax.get_yticklabels():
            label.set_fontsize(fontsize)
    
   
    if (cblabel != None):
        f.canvas.draw()
        if np.shape(colorax)==np.shape(axin):
            if (aspect>=1/fa):
                for i,ax in enumerate(axin):
                    axbb=ax.get_axes().get_position().bounds
                    axca=f.add_axes([axbb[0],axbb[1]-.15,axbb[2],0.025])
                    cb=plt.colorbar(colorax[i],cax=axca,orientation='horizontal')
                    cb.set_label(cblabel[i],fontsize=cblabelsize)
                    for tick in cb.ax.get_yticklabels()+cb.ax.get_xticklabels():
                        tick.set_fontsize(cbticksize)
                        tick.set_rotation(cbtickrotation)
                    cb.ax.get_xticklabels()[-1].set_visible(False) 
            else:
                for i,ax in enumerate(axin):
                    axbb=ax.get_axes().get_position().bounds
                    axca=f.add_axes([axbb[0]+axbb[2]+.01,axbb[1],.025,axbb[3]])
                    cb=plt.colorbar(colorax[i],cax=axca)
                    cb.set_label(cblabel[i],fontsize=cblabelsize)     
                    for tick in cb.ax.get_yticklabels()+cb.ax.get_xticklabels():
                        tick.set_fontsize(cbticksize)        
                    cb.ax.get_yticklabels()[-1].set_visible(False)  

        else:
            axstart=axin[0].get_axes().get_position().bounds
            axend=axin[-1].get_axes().get_position().bounds
            if (aspect>=1/fa):
                #add color at current axis bottom
                ax0ca=f.add_axes([axstart[0],axstart[1]-.15,axend[2]+axend[0]-axstart[0],0.025])
                cb=plt.colorbar(colorax,cax=ax0ca,orientation='horizontal')
                cb.set_label(cblabel,fontsize=cblabelsize)
                for tick in cb.ax.get_yticklabels()+cb.ax.get_xticklabels():
                    tick.set_fontsize(cbticksize)

            else:
                ax0ca=f.add_axes([axstart[0]+axstart[2]+.01,axend[1],0.025,axstart[1]+axstart[3]-axend[1]])
                cb=plt.colorbar(colorax,cax=ax0ca)
                cb.set_label(cblabel,fontsize=cblabelsize)
                for tick in cb.ax.get_yticklabels()+cb.ax.get_xticklabels():
                    tick.set_fontsize(cbticksize)


def bboxer(bbc,bbin):
    bb=np.array(bbc)

    bb[0]=np.min([bbc[0],bbin[0]])    
    bb[1]=np.min([bbc[1],bbin[1]])  
    bb[2]=np.max([bbc[2]+bbc[0],bbin[2]+bbin[0]])  
    bb[3]=np.max([bbc[3]+bbc[1],bbin[3]+bbin[1]])  

    bb[2]=bb[2]-bb[0]    
    bb[3]=bb[3]-bb[1]  

    return bb
    

def meter_box(axin,loc,dist,color='k',lw=1,retbox=False):
    """
    Given axes and location in lon/lat and a distance (1d or 2d) in meters plots a box around that location.
    NOTE: This uses my hacky ll_dist, so will be correct over small region but not as accurate over large regions.

    :Parameters:
        axin -  The axes to plot the box on.
        loc - The center of the box being plotted.
        dist - The distance in meters around the box to plot.
    """
    dist=np.atleast_1d(np.array(dist))
    loc=np.array(loc)
    tr={}
    tr['region']=np.array([loc[0],loc[0],loc[1],loc[1]])
    lon_space=pjt.ll_dist(tr,dist[0])
    if len(dist)==2:
        lat_space=dist[1]/111120    
    else:
        lat_space=dist[0]/111120  

    tr['region'][0]=tr['region'][0]-lon_space
    tr['region'][1]=tr['region'][1]+lon_space
    tr['region'][2]=tr['region'][2]-lat_space
    tr['region'][3]=tr['region'][3]+lat_space

    plot_box(axin,tr,color=color,lw=lw)
    
    if retbox==True:
        return tr['region']


def axes_label(axin,label,**kwargs):
    loc=0
    drawn=False
    size=12
    color='k'

    if kwargs is not None:
        for key, value in kwargs.iteritems():
            if (key=='loc'):
                loc=value           
            if (key=='drawn'):
                drawn=value
            if (key=='color'):
                color=value
            if (key=='size'):
                size=value


    if drawn==False:
        plt.draw()

    if loc==0:
        axbb=axin.get_axes().get_position().bounds
        t=axin.annotate(label,xy=(axbb[0]+.0075,axbb[1]+axbb[3]-.03),xycoords='figure fraction',color=color,fontsize=size)
        t.set_zorder(100)


def scalebar(axin,region,dist,**kwargs):
    """
    Given axes, region, and distance plots a scalebar. 
    NOTE: Must be called AFTER prettyplot_ll or ppll_sub as the aspect ratio must be set first.

    :Parameters:
        axin -  The axes to plot the box on.
        region - The region being plotted.
        dist - The distance in meters of the scalebar.

        **loc -  Where to place the scalebar (only one option for now, lower left).
        **fontsize - Text fontsize (default - 8).
        **color - Color of scalebar and text (default - 'k').
        **label - Override label.
    """

    fontsize=8
    loc=0
    color='k'
    lw=1
    if dist<1000:
        label=("%d"%dist)+' m'
    else:
        label=("%.1f"%(dist/1000))+' km'
    drawn=False

    if kwargs is not None:
        for key, value in kwargs.iteritems():
            if (key=='fontsize'):
                fontsize=value 
            if (key=='loc'):
                loc=value
            if (key=='color'):
                color=value 
            if (key=='label'):
                label=value 
            if (key=='lw'):
                lw=value
            if (key=='drawn'):
                drawn=value

    if drawn==False:
        plt.draw()


    ftrans=axin.get_figure().transFigure
    dinv=axin.transData.inverted()

    if loc==0:
        lldist=pjt.ll_dist(region,dist)

        axbb=axin.get_axes().get_position().bounds
        t=axin.annotate(label,xy=(axbb[0]+.02,axbb[1]+.0275),xycoords='figure fraction',fontsize=fontsize,color=color)
        t.set_zorder(100)
        
        xtmp,ytmp=dinv.transform(ftrans.transform((axbb[0]+.02,axbb[1]+.02)))
        axin.plot([xtmp,xtmp+lldist],[ytmp,ytmp],color=color)

    if loc==2:
        lldist=pjt.ll_dist(region,dist)

        axbb=axin.get_axes().get_position().bounds
        t=axin.annotate(label,xy=(axbb[0]+axbb[2]-.085,axbb[1]+axbb[3]-.0225),xycoords='figure fraction',fontsize=fontsize,color=color)
        t.set_zorder(100)
        
        xtmp,ytmp=dinv.transform(ftrans.transform((axbb[0]+axbb[2]-.085,axbb[1]+axbb[3]-.03)))
        axin.plot([xtmp,xtmp+lldist],[ytmp,ytmp],color=color)



def plot_llz(data,show=True,crange=None,s=10,region=None,pretty=False):


    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])



    if isinstance(data,dict):
        if data.has_key('h'):  
            if crange==None:  
                vmin=data['h'].min()
                vmax=data['h'].max()  
            else:
                vmin=crange[0]
                vmax=crange[1]     
            if data.has_key('nodell'):
                px,py,ph=data['nodell'][:,0],data['nodell'][:,1],data['h']
            elif (data.has_key('lon') and data.has_key('lat')):
                px,py,ph=data['lon'],data['lat'],data['h']
            elif (data.has_key('x') and data.has_key('y')):
                px,py,ph=data['x'],data['y'],data['h']
    else:
        if crange==None:  
            vmin=data[:,2].min()
            vmax=data[:,2].max()
        else:
            vmin=crange[0]
            vmax=crange[1]
        px,py,ph=data[:,0],data[:,1],data[:,2]


    scb=ax.scatter(px,py,c=ph,edgecolor='None',s=s,vmin=vmin,vmax=vmax)   

    if region==None:
        region={}
        region['region']=np.array([np.min(px),np.max(px),np.min(py),np.max(py)])
    
    if pretty:
        prettyplot_ll(ax,setregion=region,cb=scb,cblabel='')
    else:
        plt.colorbar(scb)
  
    if show==True:
        f.show()
    else:
        return f,ax


def plotlinreg(model,obs,lr,savestr):
    
    f = plt.figure(figsize=(18,10))
    ax = f.add_subplot(111)

    ax.scatter(model, obs, c='b', marker='+', alpha=0.5)

    ## plot regression line
    mod_max = np.amax(model)
    mod_min = np.amin(obs)
    upper_intercept = lr['intercept'] + lr['pred_CI_width']
    lower_intercept = lr['intercept'] - lr['pred_CI_width']
    ax.plot([mod_min, mod_max], [mod_min * lr['slope'] + lr['intercept'],
            mod_max * lr['slope'] + lr['intercept']],
            color='k', linestyle='-', linewidth=2, label='Linear fit')

    ## plot CI's for slope
    ax.plot([mod_min, mod_max], [mod_min * lr['slope_CI'][0] + lr['intercept_CI'][0],
                                 mod_max * lr['slope_CI'][0] + lr['intercept_CI'][0]],
             color='r', linestyle='--', linewidth=2)
    ax.plot([mod_min, mod_max], [mod_min * lr['slope_CI'][1] + lr['intercept_CI'][1],
                                 mod_max * lr['slope_CI'][1] + lr['intercept_CI'][1]],
             color='r', linestyle='--', linewidth=2, label='Slope CI')

    ## plot CI's for predictands
    ax.plot([mod_min, mod_max], [mod_min * lr['slope'] + upper_intercept,
                                 mod_max * lr['slope'] + upper_intercept],
             color='g', linestyle='--', linewidth=2)
    ax.plot([mod_min, mod_max], [mod_min * lr['slope'] + lower_intercept,
                                 mod_max * lr['slope'] + lower_intercept],
             color='g', linestyle='--', linewidth=2, label='Predictand CI')

    ax.set_xlabel('Modeled Data')
    ax.set_ylabel('Observed Data')
    f.suptitle('Modeled vs. Observed {}: Linear Fit'.format('ADCP'))
    plt.legend(loc='lower right', shadow=True)

    r_string = 'R Squared: {}'.format(np.around(lr['r_2'], decimals=3))
    plt.title(r_string)
    f.savefig(savestr,dpi=300)
    plt.close(f)


def load_geotiff(filename):
    
    gdal.UseExceptions()
    ds = gdal.Open(filename)
    band = ds.GetRasterBand(1)
    ct=band.GetColorTable()
    elevation = ds.ReadAsArray()

    cb=np.array([])
    for i in range(ct.GetCount()):
        cb=np.append(cb,ct.GetColorEntry(i)[:])
    cb=cb.reshape(-1,4)
    mycmap=LinearSegmentedColormap.from_list('my_colormap',cb/255,256)

    old_cs= osr.SpatialReference()
    old_cs.ImportFromWkt(ds.GetProjectionRef())

    wgs84_wkt = """
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]]"""
    new_cs = osr.SpatialReference()
    new_cs.ImportFromWkt(wgs84_wkt)

    # create a transform object to convert between coordinate systems
    transform = osr.CoordinateTransformation(old_cs,new_cs) 

    #get the point to transform, pixel (0,0) in this case
    width = ds.RasterXSize
    height = ds.RasterYSize
    gt = ds.GetGeoTransform()
    minx = gt[0]
    miny = gt[3] + width*gt[4] + height*gt[5] 
    maxx = gt[0] + width*gt[1] + height*gt[2]
    maxy = gt[3]  

    #get the coordinates in lat long
    latlongBL = transform.TransformPoint(minx,miny)
    latlongBR = transform.TransformPoint(maxx,miny)
    latlongTL = transform.TransformPoint(minx,maxy)
    latlongTR = transform.TransformPoint(maxx,maxy) 
    
    extent=[latlongBL[0],latlongTR[0],latlongBL[1],latlongTR[1]]
    
    return elevation, mycmap, extent


def box2ax(axbox,axregion,region,letter,**kwargs):
    """
    Given two axes and a region draw a box and label with letters.
    """
    defaults={'color' : 'k',
              'lw' : 1,
              'textcolor' : 'k',

              'fontsize' : 8}
    
    for (option, value) in kwargs.iteritems():
        defaults[option]=value

    plot_box(axbox,region,color=defaults['color'],lw=defaults['lw'])
    xos=0.05*(region['region'][1]-region['region'][0])
    yos=0.05*(region['region'][3]-region['region'][2])
    axbox.annotate(letter,xy=(region['region'][0]+xos,region['region'][2]+yos),xycoords='data',color=defaults['textcolor'],fontsize=defaults['fontsize'])
    
    plt.draw()
    axbb=axregion.get_axes().get_position().bounds
    axregion.annotate(letter,xy=(axbb[0]+.0075,axbb[1]+.0075),xycoords='figure fraction',color=defaults['textcolor'],fontsize=defaults['fontsize'])

    return
    
    
def plottri(data, field, minmax=[],show=True,cm=mpl.cm.viridis):
    """
    Plot an FE data field.
    """
    
    f=plt.figure()
    ax=f.add_axes([0.125,.1,.775,.8])
    if minmax==[]:
        triax=ax.tripcolor(data['trigrid'],field,cmap=cm)
    else:
        triax=ax.tripcolor(data['trigrid'],field,vmin=minmax[0],vmax=minmax[1],cmap=cm)
    plt.colorbar(triax)
    
    if show==True:
        f.show()
        return f,ax
    else:
        return f,ax
    
    
def plot_zetares(time1, zeta1, time2, zeta2,show=True, tidecon=None):
    """
    Plot timeseries and residual.
    """
    ittide=True
    try:
        import ttide
    except ImportError:
        print("ttide is not installed, please install tide.")
        ittide=False
    
    f,ax=plt.subplots(2,1,sharex=True)
    ax[0].plot(time1, zeta1,'r',lw=2)
    ax[0].plot(time2, zeta2,'b',lw=.5)
    
    if ittide:        
        if tidecon is None:
            out1=ttide.t_tide(zeta1,stime=time1[0],dt=24*(time1[1]-time1[0]))
            out2=ttide.t_tide(zeta2,stime=time2[0],dt=24*(time2[1]-time2[0]))
        else:
            out1=ttide.t_tide(zeta1,stime=time1[0],dt=24*(time1[1]-time1[0]),constitnames=tidecon)
            out2=ttide.t_tide(zeta2,stime=time2[0],dt=24*(time2[1]-time2[0]),constitnames=tidecon)
        
        ax[1].plot(time1, zeta1-out1(time1),'r',lw=2)
        ax[1].plot(time2, zeta2-out2(time2),'b',lw=.5)
            
    if show==True:
        f.show()
        return f,ax,out1,out2
    else:
        return f,ax,out1,out2
    
def plot_gridsummary(filename,regionname=None,percentiles=[5,95],dpi=600,crange={}):
    """
    Plots a grid and its sidelength and bathymetry for a region.
    If not region then plots the whole grid.
    """
    
    data = gt.load_nei2fvcom(filename)
    data = gt.get_dhh(data)
    if regionname is not None:
        region = pjt.regions(regionname)
        nidx = gt.get_nodes(data,region)
        eidx = gt.get_elements(data,region)
    filename=filename.split('.')[0]
    
    # Plot grid
    f = plt.figure()
    ax=f.add_axes([.1, .125, .775, .8])
    ax.triplot(data['trigrid'], lw=.1, color='k')
    if regionname is not None:
        ax.axis(region['region'])
        f.savefig(filename+'_'+regionname+'_grid.png',dpi=dpi)
    else:
        f.savefig(filename+'_grid.png',dpi=dpi)
    
    # Plot sidelength
    f = plt.figure()
    ax=f.add_axes([.1, .125, .775, .8])
    if 'sl' not in crange:
        if regionname is not None:
            crange['sl']=np.percentile(data['sl'][eidx],percentiles)
        else:
            crange['sl']=np.percentile(data['sl'],percentiles)
    triax=ax.tripcolor(data['trigrid'], data['sl'],vmin=crange['sl'][0],vmax=crange['sl'][1])
    cb=plt.colorbar(triax)
    cb.set_label('Sidelength (m)')
    if regionname is not None:
        ax.axis(region['region'])
        f.savefig(filename+'_'+regionname+'_sidelength.png',dpi=dpi)
    else:
        f.savefig(filename+'_sidelength.png',dpi=dpi)
        
    # Plot bathymetry
    f = plt.figure()
    ax=f.add_axes([.1, .125, .775, .8])
    if 'h' not in crange:
        if regionname is not None:
            crange['h']=np.percentile(data['h'][nidx],percentiles)
        else:
            crange['h']=np.percentile(data['h'],percentiles)
    triax=ax.tripcolor(data['trigrid'], data['h'],vmin=crange['h'][0],vmax=crange['h'][1])
    cb=plt.colorbar(triax)
    cb.set_label('Depth (m)')
    if regionname is not None:
        ax.axis(region['region'])
        f.savefig(filename+'_'+regionname+'_depth.png',dpi=dpi)
    else:
        f.savefig(filename+'_depth.png',dpi=dpi)
    
    # Plot dhh
    f = plt.figure()
    ax=f.add_axes([.1, .125, .775, .8])
    if 'dhh' not in crange:
        if regionname is not None:
            crange['dhh']=np.percentile(data['dhh'][eidx],percentiles)
        else:
            crange['dhh']=np.percentile(data['dhh'],percentiles)
    triax=ax.tripcolor(data['trigrid'], data['dhh'],vmin=crange['dhh'][0],vmax=crange['dhh'][1])
    cb=plt.colorbar(triax)
    cb.set_label('dhh')
    if regionname is not None:
        ax.axis(region['region'])
        f.savefig(filename+'_'+regionname+'_dhh.png',dpi=dpi)
    else:
        f.savefig(filename+'_dhh.png',dpi=dpi)

def llz_click_remove(data,crange=None,s=10,region=None,pretty=False):


    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])

    if isinstance(data,dict):
        if data.has_key('h'):  
            if crange==None:  
                vmin=data['h'].min()
                vmax=data['h'].max()  
            else:
                vmin=crange[0]
                vmax=crange[1]     
            if data.has_key('nodell'):
                px,py,ph=data['nodell'][:,0],data['nodell'][:,1],data['h']
            elif (data.has_key('lon') and data.has_key('lat')):
                px,py,ph=data['lon'],data['lat'],data['h']
            elif (data.has_key('x') and data.has_key('y')):
                px,py,ph=data['x'],data['y'],data['h']
    else:
        if crange==None:  
            vmin=data[:,2].min()
            vmax=data[:,2].max()
        else:
            vmin=crange[0]
            vmax=crange[1]
        px,py,ph=data[:,0],data[:,1],data[:,2]


    scb=ax.scatter(px,py,c=ph,edgecolor='None',s=s,vmin=vmin,vmax=vmax)   

    if region==None:
        region={}
        region['region']=np.array([np.min(px),np.max(px),np.min(py),np.max(py)])
    
    if pretty:
        prettyplot_ll(ax,setregion=region,cb=scb,cblabel='')
    else:
        plt.colorbar(scb)
  
    vec=f.ginput(n=-1,timeout=-1)
    plt.close(f)

    #turn selected points into path
    p=path.Path(vec)
    
    
    #find points in path and remove and return as array
    idx=p.contains_points(np.array([px,py]).T)    
    return np.vstack([px[~idx], py[~idx], ph[~idx]]).T


    
    
    
def plot_idntown(data):
    """
    Plot timeseries of model and data at indian town gauge.
    """

    df=pd.read_csv('/home/mif001/workspace_python/data/01AP005_20150101-20161231_WLp_UVp.csv',header=2)
    times=np.array([t for t in df['Date-Time']])
    time=dates.datestr2num(times)
    lon=-1*(66+5/60.+20/3600.)
    lat=45+16/60.+24/3600.
    aa=(data['lon']-lon)**2+(data['lat']-lat)**2
    idx=np.argmin(aa)
    k=np.argwhere((time>=data['time'].min())&(time<=data['time'].max()))
    zeta=np.array([z for z in df.Value])

    f=plt.figure()
    ax=f.add_axes([.125,.1,.775,.8])
    ax.plot(time[k]+4/24.0,zeta[k]-.7,'r.',lw=2,label='Obs.')	
    ax.plot(data['time'],data['zeta'][:,idx],'b',lw=.5,label='Model')
    
    ax.set_xlim([data['time'].min(),data['time'].max()])

    f.show()
    return f,ax


def select_field(data, field, i, layer=None):
    """
    Helper function to select the correct field and name for the field
    """
    
    fn = {'temp' : r'Temperature ($^{\circ}$)',
          'salinity' : r'Salinity (PSU)',
          'speed' : r'Speed (m/s)',
          'u' : r'U-Velocity (m/s)',
          'v' : r'V-Velocity (m/s)',
          'vorticity' : r'Vorticity',
          'density' : r'Density (kg m$^{3}$)',
          'zeta' : 'Elevation (m)'}    
    
    
    if 'speed' in field:
        if layer=='da':
            fieldout = np.sqrt(data['ua'][i,:]**2 + data['va'][i,:]**2)
        else:
            fieldout = np.sqrt(data['u'][i,layer,:]**2 + data['v'][i,layer,:]**2)
            
    elif 'vorticity' in field:
        if layer=='da':
            dudy = data['a2u'][0,:]*data['ua'][i,:]+data['a2u'][1,:]*data['ua'][i,data['nbe'][:,0]] +\
                   data['a2u'][2,:]*data['ua'][i,data['nbe'][:,1]]+data['a2u'][3,:]*data['ua'][i,data['nbe'][:,2]]
            dvdx = data['a1u'][0,:]*data['va'][i,:]+data['a1u'][1,:]*data['va'][i,data['nbe'][:,0]] +\
                   data['a1u'][2,:]*data['va'][i,data['nbe'][:,1]]+data['a1u'][3,:]*data['va'][i,data['nbe'][:,2]]
        else:
            dudy = data['a2u'][0,:]*data['u'][i,layer,:]+data['a2u'][1,:]*data['u'][i,layer,data['nbe'][:,0]] +\
                   data['a2u'][2,:]*data['u'][i,layer,data['nbe'][:,1]]+data['a2u'][3,:]*data['u'][i,layer,data['nbe'][:,2]]
            dvdx = data['a1u'][0,:]*data['v'][i,layer,:]+data['a1u'][1,:]*data['v'][i,layer,data['nbe'][:,0]] +\
                   data['a1u'][2,:]*data['v'][i,layer,data['nbe'][:,1]]+data['a1u'][3,:]*data['v'][i,layer,data['nbe'][:,2]]
        fieldout = dvdx - dudy   
        
    elif 'density' in field:
        if layer==None:
            print("Can't get density for layer None. Using layer=0.")
            layer = 0
        pres = sw.pres(data['h']+data['zeta'][i,:],data['lat'])
        fieldout = sw.dens(data['salinity'][i,layer,:],data['temp'][i,layer,:],pres)
        
    else:
        if layer==None:
            fieldout = data[field][i,:]
        else:
            fieldout = data[field][i,layer,:]
           
            
    
    try:     
        fieldname = fn[field]
    except KeyError:
        fieldname = field
    
    return fieldout, fieldname



def plot_tsmap(mod,obs,other):
    
    tidx=other['tidx']
    num=other['num']

    
    f=plt.figure(figsize=(8,12))
    axm=f.add_axes([.125,.5,.775,.45])
    axt=f.add_axes([.125,.05,.325,.4])
    axs=f.add_axes([.575,.05,.325,.4])
    
    plotcoast(axm,filename='mid_nwatl6c_sjh_lr.nc', filepath=coastpath, color='k', fill=True)
    axm.plot(obs['Lon'],obs['Lat'],'*r',markersize=10)
    axm.plot(mod['longitue'],mod['latitude'],'.',color='lawngreen',markersize=5)
    axm.axis([-67.5,-65,44.9,45.8])
    
    axt.plot(mod['arrays']['temperature'],mod['arrays']['depth'],'b',lw=.75)
    axt.plot(obs['Temp'],-1*obs['Depth'],'r',lw=2.5)
    axt.plot(mod['arrays']['temperature'][:,tidx],mod['arrays']['depth'][:,tidx],'lawngreen',lw=2.5)
    
    axs.plot(mod['arrays']['salinity'],mod['arrays']['depth'],'b',lw=.75)
    axs.plot(obs['Salinity'],-1*obs['Depth'],'r',lw=2.5)
    axs.plot(mod['arrays']['salinity'][:,tidx],mod['arrays']['depth'][:,tidx],'lawngreen',lw=2.5)

    axm.text(.075,.9,'{}'.format(obs['TimeStamp'].replace('T',' ')),transform=axm.transAxes)
    f.suptitle('{}\n{} - {}'.format(num,other['grid'],other['name']))
    
    axm.set_ylabel('Latitude')
    axm.set_xlabel('Longitude')
    axt.set_ylabel('depth')
    axt.set_xlabel('T')
    axs.set_ylabel('depth')
    axs.set_xlabel('S')
    
    
    f.savefig(other['filename'],dpi=100)
    plt.close(f)
    
    
def plot_tsmap2(ctdm,ctdo,other,Tstats,Sstats,bTstats,bSstats,Tidx,Sidx,ht):
    
    tidx=other['tidx']
    num=other['num']
    zeta=ctdm['zeta']
    
    ctdm['depth']=np.outer(ctdm['siglay'],ctdm['h']+ctdm['zeta'])
    a=''
    ctdo['Time']=np.array([a.join(b) for b in ctdo['timestamp']])
    ctdm['temp']=ctdm['temp'].T
    ctdm['salinity']=ctdm['salinity'].T
    
    f=plt.figure(figsize=(12,8))
    axm=f.add_axes([.1,.3,.35,.6])
    axz=f.add_axes([.1,.075,.35,.15])
    axt=f.add_axes([.55,.4,.15,.5])
    axs=f.add_axes([.8,.4,.15,.5])
    axdfT=f.add_axes([.55+.005,.075,.15,.05])
    axdfS=f.add_axes([.8+.005,.075,.15,.05])
    
    axdfT.xaxis.set_visible(False)  
    axdfT.yaxis.set_visible(False)  
    axdfT.set_frame_on(False)

    axdfS.xaxis.set_visible(False)  
    axdfS.yaxis.set_visible(False)  
    axdfS.set_frame_on(False)
    
    #f.show()
    
    plotcoast(axm,filename='mid_nwatl6c_sjh_lr.nc', filepath=coastpath, color='k', fill=True)
    axm.plot(ctdo['lon'],ctdo['lat'],'*r',markersize=10)
    axm.plot(ctdm['lon'],ctdm['lat'],'.',color='lawngreen',markersize=5)
    axm.axis([-67.5,-65,44.9,45.8])
    
    axz.plot(ctdm['time'],zeta,'k')
    pidx=np.argmin(np.fabs(ctdm['time']-ctdm['time'][0]))
    axz.plot(ctdm['time'][pidx],zeta[pidx],'.b')
    pidx=np.argmin(np.fabs(ctdm['time']-ctdm['time'][-1]))
    axz.plot(ctdm['time'][pidx],zeta[pidx],'.b')
    pidx=np.argmin(np.fabs(ctdm['time']-ctdm['time'][tidx]))
    axz.plot(ctdm['time'][pidx],zeta[pidx],'.',color='lawngreen')
    axz.set_xlim([ctdm['time'][pidx]-18/24.0,ctdm['time'][pidx]+18/24.0])
    axz.set_xticks([ctdm['time'][pidx]-12/24.0,ctdm['time'][pidx]-6/24.0,ctdm['time'][pidx]-3/24.0,ctdm['time'][pidx],ctdm['time'][pidx]+3/24.0,ctdm['time'][pidx]+6/24.0,ctdm['time'][pidx]+12/24.0])
    axz.set_xticklabels([str(a) for a in np.round(24*(axz.get_xticks()-ctdm['time'][pidx]))])

    
    #print(tidx)
    #print(mod['time'][0],mod['time'][tidx],mod['time'][-1])
    
    axt.plot(ctdm['temp'],ctdm['depth'],'b',lw=.75)
    axt.plot(ctdm['temp'][:,Tidx],ctdm['depth'][:,Tidx],color='dodgerblue',lw=.75)
    axt.plot(ctdo['temp'].T,-1*ctdo['depth'].T,'r',lw=2.5)
    axt.plot(ctdm['temp'][:,tidx],ctdm['depth'][:,tidx],'lawngreen',lw=2.5)
    
    axs.plot(ctdm['salinity'],ctdm['depth'],'b',lw=.75)
    axs.plot(ctdm['salinity'][:,Sidx],ctdm['depth'][:,Sidx],color='dodgerblue',lw=.75)
    axs.plot(ctdo['salinity'].T,-1*ctdo['depth'].T,'r',lw=2.5)
    axs.plot(ctdm['salinity'][:,tidx],ctdm['depth'][:,tidx],'lawngreen',lw=2.5)

    axm.text(.075,.9,'{}'.format(ctdo['Time'][0].replace('T',' ')),transform=axm.transAxes)
    f.suptitle('{}\n{} - {}'.format(num,other['grid'],other['name']))
    
    axm.set_ylabel('Latitude')
    axm.set_xlabel('Longitude')
    axt.set_ylabel('depth')
    axt.set_xlabel('T')
    axs.set_ylabel('depth')
    axs.set_xlabel('S')
    
    Tin=OrderedDict()
    Tin[str(num)]=np.append(Tstats[str(num)].values(),ht)
    #print(Tidx)
    #print(ctdm['time'][0,Tidx])
    Tin['Time (m)']=np.append((np.round(24*60*(ctdo['time']-ctdm['time'][Tidx]))).astype(int),ht)
    Tin['Best']=np.append(bTstats[np.arange(7),Tidx],ht)
    
    Sin=OrderedDict()
    Sin[str(num)]=Sstats[str(num)].values()
    Sin['Time (m)']=(np.round(24*60*(ctdo['time']-ctdm['time'][Sidx]))).astype(int)
    Sin['Best']=bSstats[np.arange(7),Sidx]
    
    dfT=pd.DataFrame(Tin,columns=[str(num),'Time (m)','Best']).round(2)
    #dfT=dfT[['meansl','stdsl','rmsesl','relaverr','corsl','skewsl','skill']].T.round(2)
    dfS=pd.DataFrame(Sin,columns=[str(num),'Time (m)','Best']).round(2)
    #dfS=dfS[['meansl','stdsl','rmsesl','relaverr','corsl','skewsl','skill']].T.round(2)
    
    rl=['Bias','Std','RMSE','RAE','Corr','Skew','Skill','ht']
    rs=['Bias','Std','RMSE','RAE','Corr','Skew','Skill']
    tbT=pd.plotting.table(axdfT,dfT, loc='lower left',colWidths=[0.3]*len(dfT.columns),rowLabels=rl)
    tbS=pd.plotting.table(axdfS,dfS, loc='lower left',colWidths=[0.3]*len(dfS.columns),rowLabels=rs)
    
    tbT.scale(1,1.5)
    tbS.scale(1,1.5)
    
    f.savefig(other['filename'],dpi=100)
    plt.close(f)

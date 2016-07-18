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
import os
import inspect
from osgeo import osr, gdal
from matplotlib.colors import LinearSegmentedColormap


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
    ticksout=False
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
            if (key=='ticksout'):
                ticksout=value 
            if (key=='axlabels'):
                axlabels=value
               


    _formatter = mpl.ticker.ScalarFormatter(useOffset=False)
    axin.yaxis.set_major_formatter(_formatter)
    axin.xaxis.set_major_formatter(_formatter)
    axin.set_xticklabels(-1*(axin.get_xticks()))
    if axlabels:
        axin.set_xlabel(r'Longitude ($^{\circ}$W)')
        axin.set_ylabel(r'Latitude ($^{\circ}$N)')
    else:
        axin.xaxis.set_tick_params(labelbottom='off')
        axin.yaxis.set_tick_params(labelleft='off')



    for label in axin.get_xticklabels() +axin.get_yticklabels():
        label.set_fontsize(fontsize)
        
    if ticksout:
        axin.tick_params(direction='out')


    aspect=axin.get_aspect()
    if (aspect!='auto'):
        if (aspect>1.3):
            skinny=True
            #slicer=(np.floor(aspect).astype(int)+1)
            for label in axin.get_xticklabels()[::2]:
                label.set_visible(False)
    
    if (cblabel != None):
        #doesnt really work        
        #divider = make_axes_locatable(axin)
        #cax = divider.append_axes("right", size="5%", pad=0.25)
        #plt.colorbar(cax=cax)
        if skinny==True:
            plt.draw()
            box=axin.get_position()
            cax=axin.get_figure().add_axes([box.xmax + .025, box.ymin, .025, box.height])
            cb=plt.colorbar(colorax,cax=cax)
            cb.set_label(cblabel,fontsize=10)
        else:
            plt.draw()
            box=axin.get_position()
            box.set_points(np.array([[box.xmin,box.ymin],[box.xmax-.1,box.ymax]]))
            axin.set_position(box)
            plt.draw()
            box=axin.get_position()
            cax=axin.get_figure().add_axes([box.xmax + .025, box.ymin, .025, box.height])
            cb=plt.colorbar(colorax,cax=cax)
            cb.set_label(cblabel,fontsize=10)


def get_data_ratio(region):
    """
    Returns the aspect ratio of the region data.
    
    :Parameters:
        region - a region as defined in regions.py
    """

    xsize = np.max(np.fabs(region['region'][1] - region['region'][0]), 1e-30)
    ysize = np.max(np.fabs(region['region'][3] - region['region'][2]), 1e-30)

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

    _base_dir = os.path.realpath(inspect.stack()[0][1])
    idx=_base_dir.rfind('/')
    sl=dt.loadnc(_base_dir[:idx],singlename='/data/shorelines/'+filename)

    idx=np.where(sl['count']!=0)[0]
    sl['count']=sl['count'][idx]
    sl['start']=sl['start'][idx]

    tmparray=[list(zip(sl['lon'][sl['start'][i]:(sl['start'][i]+sl['count'][i])],sl['lat'][sl['start'][i]:(sl['start'][i]+sl['count'][i])])) for i in range(0,len(sl['start']))]

    if fill==True:
        coastseg=PC(tmparray,facecolor = fcolor,edgecolor=color,linewidths=lw)
    else:
        coastseg=LC(tmparray,linewidths = lw,linestyles=ls,color=color)



    

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
    ticksout=False

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
            if (key=='ticksout'):
                ticksout=value 
               
    f=axin[0].get_figure()
    figW, figH = f.get_size_inches()
    fa = figH / figW
    
    if ticksout:
        for ax in axin:
            ax.tick_params(direction='out')
    

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
        plt.draw()
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



def plot_llz(data,show=True,crange=None,s=10,region=None):


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
    
    prettyplot_ll(ax,setregion=region,cb=scb,cblabel='')
  
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


<<<<<<< HEAD
def box2ax(axbox,axregion,region,letter,**kwargs):
=======
def box2ax(axbox,axregion,region,letter,kwargs):
>>>>>>> 909200e9537bc9ef9ea0f899662319af6cd83ce9
    """
    Given two axes and a region draw a box and label with letters.
    """
    defaults={'color' : 'k',
              'lw' : 1,
              'textcolor' : 'k',
<<<<<<< HEAD
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
=======
              'textsize' : 8}
    
    for (option, value) in kwargs:
        defaults[option]=value

    plot_box(axbox,region,color=defaults['color'],lw=defaults['lw'])
    xos=0.0075*(region[0]-region[1])
    yos=0.03*(region[3]-region[2])
    axbox.annotate(letter,xy=(region[0]+xos,region[3]-yos),xycoords='data')
    
    plt.draw()
    axbb=axregion.get_axes().get_position().bounds
    axregion.annotate(letter,xy=(axbb[0]+.0075,axbb[1]+axbb[3]-.03),xycoords='figure fraction')
>>>>>>> 909200e9537bc9ef9ea0f899662319af6cd83ce9
    
    
    






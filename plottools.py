from __future__ import division
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seawater as sw
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
from datatools import *

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
    skinny=False

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
               


    _formatter = mpl.ticker.ScalarFormatter(useOffset=False)
    axin.yaxis.set_major_formatter(_formatter)
    axin.xaxis.set_major_formatter(_formatter)
    axin.set_xticklabels(-1*(axin.get_xticks()))
    axin.set_xlabel(r'Longitude ($^{\circ}$W)')
    axin.set_ylabel(r'Latitude ($^{\circ}$N)')

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




def get_aspectratio(region,LL=1):
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


def plot_box(axin,region,color,lw=1):
    axin.plot([region['region'][0],region['region'][0]],[region['region'][2],region['region'][3]],color,lw=lw)
    axin.plot([region['region'][1],region['region'][1]],[region['region'][2],region['region'][3]],color,lw=lw)
    axin.plot([region['region'][0],region['region'][1]],[region['region'][2],region['region'][2]],color,lw=lw)
    axin.plot([region['region'][0],region['region'][1]],[region['region'][3],region['region'][3]],color,lw=lw)


def fix_osw(axin):
    _formatter = mpl.ticker.ScalarFormatter(useOffset=False)
    axin.yaxis.set_major_formatter(_formatter)
    axin.xaxis.set_major_formatter(_formatter)
    axin.set_xticklabels(-1*(axin.get_xticks()))



def plotcoast(axin,**kwargs):
    
    color='k'
    lw=1
    ls='solid'
    filename='mid_nwatl6b.nc'
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

    sl=loadnc("",singlename='data/shorelines/'+filename)

    idx=np.where(sl['count']!=0)[0]
    sl['count']=sl['count'][idx]
    sl['start']=sl['start'][idx]

    tmparray=[list(zip(sl['lon'][sl['start'][i]:(sl['start'][i]+sl['count'][i])],sl['lat'][sl['start'][i]:(sl['start'][i]+sl['count'][i])])) for i in range(0,len(sl['start']))]

    if fill==True:
        lseg=PC(tmparray,facecolor = fcolor,edgecolor=color,linewidths=lw)
    else:
        lseg=LC(tmparray,linewidths = lw,linestyles=ls,color=color)



    

    axin.add_collection(lseg)




def plotgrid_num(data,size,num,nore):

    if nore=='n':
        region={}
        region['region']=[data['nodexy'][num,0]-size,data['nodexy'][num,0]+size,data['nodexy'][num,1]-size,data['nodexy'][num,1]+size]
        idx=get_nodes_xy(data,region)
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
        idx=get_elements_xy(data,region)
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
        idx=get_nodes_xy(data,region)
        for i in idx:
            axin.text(data['nodell'][i,0],data['nodell'][i,1],("%d"%i),fontsize=10,bbox={'facecolor':'white', 'alpha':.7, 'pad':3})
       
    if nore=='e':
        region={}
        region['region']=[data['uvnode'][num,0]-size,data['uvnode'][num,0]+size,data['uvnode'][num,1]-size,data['uvnode'][num,1]+size]
        idx=get_elements_xy(data,region)
        for i in idx:
            axin.text(data['uvnodell'][i,0],data['uvnodell'][i,1],("%d"%i),fontsize=10,bbox={'facecolor':'white', 'alpha':.7, 'pad':3})
        


def plotgrid_ll(data,size,ll,nore):

    if nore=='n':
        num=closest_node(data,ll)
        region={}
        region['region']=[data['nodexy'][num,0]-size,data['nodexy'][num,0]+size,data['nodexy'][num,1]-size,data['nodexy'][num,1]+size]
        idx=get_nodes_xy(data,region)
        plt.triplot(data['trigridxy'],lw=.5)
        for i in idx:
            plt.text(data['nodexy'][i,0],data['nodexy'][i,1],("%d"%i),fontsize=10,bbox={'facecolor':'white', 'alpha':.7, 'pad':3})
        region2={}
        region2['region']=[data['nodexy'][num,0]-(size*2),data['nodexy'][num,0]+(size*2),data['nodexy'][num,1]-(size*2),data['nodexy'][num,1]+(size*2)]
        plt.axis(region2['region'])
        plt.show()
    if nore=='e':
        num=closest_element(data,ll)
        region={}
        region['region']=[data['uvnode'][num,0]-size,data['uvnode'][num,0]+size,data['uvnode'][num,1]-size,data['uvnode'][num,1]+size]
        idx=get_elements_xy(data,region)
        plt.triplot(data['trigridxy'],lw=.5)
        for i in idx:
            plt.text(data['uvnode'][i,0],data['uvnode'][i,1],("%d"%i),fontsize=10,bbox={'facecolor':'white', 'alpha':.7, 'pad':3})
        region2={}
        region2['region']=[data['uvnode'][num,0]-(size*2),data['uvnode'][num,0]+(size*2),data['uvnode'][num,1]-(size*2),data['uvnode'][num,1]+(size*2)]
        plt.axis(region2['region'])
        plt.show()


def get_data_ratio(region):
    """
    Returns the aspect ratio of the raw data.

    This method is intended to be overridden by new projection
    types.
    """

    xsize = np.max(np.fabs(region['region'][1] - region['region'][0]), 1e-30)
    ysize = np.max(np.fabs(region['region'][3] - region['region'][2]), 1e-30)

    return ysize / xsize


def ax_label_spacer(axin):
    for label in axin.get_xticklabels()[::2] +axin.get_yticklabels()[::2]:
        label.set_visible(False)



def place_axes(region,numplots,cb=False):
    """For placing "subplot" axes when setting aspect ratio. Function starts and returns the figure and axes.

    :Parameters:
    	**region** -- The region being plotted, needed for aspect ratio

    	**numplots** -- The number of axes being define   
    """

    #note to check region orientations this function uses aspect*fa. It is possible it may need to use dr as well. If weird axes orientation are return check into the effect of dr.

    f=plt.figure()
    axarr = np.empty(numplots, dtype=object)

    aspect=get_aspectratio(region)
    dr=get_data_ratio(region)
    figW, figH = f.get_size_inches()
    fa = figH / figW

    space=.8
    if aspect*fa>=1:
        space=.775    

    start=.1
    if cb==True:
        start=start+.125

    spaceper=(space-.025*numplots)/numplots


    axf=np.zeros((numplots,4))

    if aspect*fa>=1:  
        xtarget=spaceper  
        ytarget=np.min([1-.1-start,spaceper*dr*aspect/fa])
        axf[0,:]=[.125,start,1,ytarget]
        for i in range(1,numplots):
            axf[i,:]=[.125+(.025+xtarget)*i,start,1,ytarget]
         

    else:
        ytarget=spaceper
        xtarget=np.min([1-.125-start,spaceper*fa/aspect/dr])    
        axf[0,:]=[.125,.1,xtarget,1]
        for i in range(1,numplots):
            axf[i,:]=[.125,.1+(.025+ytarget)*i,xtarget,1]

        axf=np.flipud(axf)

    for i in range(numplots):
        axarr[i]=f.add_axes(axf[i,:])

    return f,axarr

    

def ppll_sub(axin,**kwargs):

    cblabel=None
    axspacer=True
    cbsize=12

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
            if (key=='cbsize'):
                cbsize=value 
               
    f=axin[0].get_figure()
    figW, figH = f.get_size_inches()
    fa = figH / figW

    aspect=axin[0].get_aspect()
    if (aspect>=1/fa):
        for ax in axin:
            ax.set_xlabel(r'Longitude ($^{\circ}$W)')
            ax.yaxis.set_tick_params(labelleft='off')
        axin[0].yaxis.set_tick_params(labelleft='on')
        axin[0].set_ylabel(r'Latitude ($^{\circ}$N)')
    else:
        for ax in axin:
            ax.set_ylabel(r'Latitude ($^{\circ}$N)')
            ax.xaxis.set_tick_params(labelbottom='off')
        axin[-1].xaxis.set_tick_params(labelbottom='on')
        axin[-1].set_xlabel(r'Longitude ($^{\circ}$W)')
    

    if axspacer==True:
        for ax in axin:
            for label in ax.get_xticklabels()[::2] +ax.get_yticklabels()[::2]:
                label.set_visible(False)


    _formatter = mpl.ticker.ScalarFormatter(useOffset=False)
    for ax in axin:
        ax.yaxis.set_major_formatter(_formatter)
        ax.xaxis.set_major_formatter(_formatter)
        ax.set_xticklabels(-1*(ax.get_xticks()))
    

    
    if (cblabel != None):
        plt.draw()
        axstart=axin[0].get_axes().get_position().bounds
        axend=axin[-1].get_axes().get_position().bounds
        if (aspect>=1/fa):
            #add color at current axis bottom
            ax0ca=f.add_axes([axstart[0],axstart[1]-.125,axend[2]+axend[0]-axstart[0],0.025])
            cb=plt.colorbar(colorax,cax=ax0ca,orientation='horizontal')
            cb.set_label(cblabel,fontsize=cbsize)
        else:
            ax0ca=f.add_axes([axstart[0]+axstart[2]+.025,axend[1],0.025,axstart[1]+axstart[3]-axend[1]])
            cb=plt.colorbar(colorax,cax=ax0ca)
            cb.set_label(cblabel,fontsize=cbsize)



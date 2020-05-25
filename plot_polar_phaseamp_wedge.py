from __future__ import division,print_function
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.tri as mplt
import matplotlib.pyplot as plt
import scipy.io as sio
#from mpl_toolkits.basemap import Basemap
import os as os
import sys
from StringIO import StringIO
from gridtools import *
from datatools import *
from misctools import *
from plottools import *
from regions import makeregions
np.set_printoptions(precision=8,suppress=True,threshold=sys.maxsize)
import glob
import math

import mpl_toolkits.axisartist.floating_axes as floating_axes
from matplotlib.projections import PolarAxes
from mpl_toolkits.axisartist.grid_finder import FixedLocator, MaxNLocator,DictFormatter
import  mpl_toolkits.axisartist.angle_helper as angle_helper

datadir='data/misc/slr_base/'

files = glob.glob(datadir + "*.out")

#this code does not really work.....
#this was the only way I found to generate a polar slice. however the slice has to be increasing to crosszero
#can make it go negative but then the data has to be changed as well
#maybe fix it later.

f = plt.figure()
tr = PolarAxes.PolarTransform()

ax=np.empty((5,),dtype='O')

for i,filename in enumerate(files):
    print i
    #samp, mamp, sphs, mphs = np.genfromtxt( filename, usecols=(0, 1, 4, 5), skip_header=2,skip_footer=1 )
    samp, mamp, sphs, mphs= np.genfromtxt( filename, usecols=(0, 1, 4, 5), skip_header=2,skip_footer=1 ,unpack=True)
    
#    num = 0
#    dtrad = [ 0 ]
#    strad = [ 0 ]
#    nstat = len( mamp )
#    while num < nstat:
#    #  print num, nstat, mphs[num]
#      if num == 0:
#        dtrad[num] = math.radians( mphs[num] )
#        strad[num] = math.radians( sphs[num] )
#      else:
#        dtrad.append( math.radians( mphs[num] ))
#        strad.append( math.radians( sphs[num] ))
#      num = num + 1


    #angle_ticks = [(0, r"$0$"),                  (.25*pi, r"$\frac{1}{4}\pi$"),                   (.5*pi, r"$\frac{1}{2}\pi$")]
    grid_locator1 = angle_helper.LocatorDMS(12)


    tick_formatter1 = angle_helper.FormatterDMS()

    grid_locator2 = MaxNLocator(2)
    
    dtrad=(np.array(mphs))
    strad=(np.array(sphs))

 
    total=np.hstack([dtrad,strad])
    

    checkrange_s=0


    def mod_dist(a,b):
        return np.min([np.mod(a-b,360),np.mod(b-a,360)])

    for a in total:
        for b in total:
            crange=mod_dist(a,b)
            if crange>checkrange_s:
                checkrange_s=crange
                start_s=np.min([a,b])
                end_s=np.max([a,b])

  
         
            
                
    dtrad=np.deg2rad(dtrad)
    strad=np.deg2rad(strad)
    start_s=np.deg2rad(start_s)
    end_s=np.deg2rad(end_s)
    
    print len(np.where((start_s>total)&(end_s<total))[0])
    if (len(np.where((start_s>total)&(end_s<total))[0])<len(total)):
        start_s,end_s=(end_s),start_s
#    else:
#        start_s,end_s=start_s*.95,end_s*1.05

    xmax=np.max([mamp,samp])
    ra0, ra1 = np.pi/2,3*np.pi/4#start_s, end_s
    cz0, cz1 = 0, xmax*1.1
    print ra0, ra1, cz0, cz1
    #grid_helper = floating_axes.GridHelperCurveLinear(tr, extremes=(ra0, ra1, cz0, cz1), grid_locator1=grid_locator1, grid_locator2=grid_locator2,tick_formatter1=tick_formatter1,tick_formatter2=None)
    #grid_helper = floating_axes.GridHelperCurveLinear(tr, extremes=(ra0, ra1, cz0, cz1), grid_locator1=None, grid_locator2=None,tick_formatter1=None,tick_formatter2=None)
    grid_helper = floating_axes.GridHelperCurveLinear(tr, extremes=(ra0, ra1, cz0, cz1), grid_locator1=grid_locator1, grid_locator2=grid_locator2,tick_formatter1=None,tick_formatter2=None)

    ax[i] = floating_axes.FloatingSubplot(f, 321+i, grid_helper=grid_helper)
    f.add_subplot(ax[i])


    # adjust axis
    ax[i].axis["left"].set_axis_direction("bottom")
    ax[i].axis["right"].set_axis_direction("top")

    ax[i].axis["bottom"].set_visible(False)
    ax[i].axis["top"].set_axis_direction("bottom")
    ax[i].axis["top"].toggle(ticklabels=True, label=True)
    ax[i].axis["top"].major_ticklabels.set_axis_direction("top")
    ax[i].axis["top"].label.set_axis_direction("top")

    #ax[i].axis["left"].label.set_text(r"cz [km$^{-1}$]")
    #ax[i].axis["top"].label.set_text(r"$\alpha_{1950}$")


    # create a parasite axes whose transData in RA, cz
    aux_ax = ax[i].get_aux_axes(tr)

    aux_ax.patch = ax[i].patch # for aux_ax to have a clip path as in ax
    ax[i].patch.zorder=0.9


    # Plot the lines from the model points to the observed points
#    num = 0
#    rads = [0.0, 1.0]
#    amps = [0.0, 1.0]
#    while num < nstat:
#      rads[0] = dtrad[num]
#      rads[1] = strad[num]
#      amps[0] = mamp[num]
#      amps[1] = samp[num]
#      #ax[i].plot( rads, amps, color='black' )
#      num = num + 1

    
    # plot the model points with red stars
    ax[i].scatter( dtrad, mamp, c='r', edgecolor='r', marker='*', s=30, label='model' )
    # plot the observed points with blue O's
    ax[i].scatter( strad, samp, c='b',facecolor="none", marker='o', s=20, label='observed' )
    


 
  
#this works where the below does not, get ax position to set legend then delete the axes
bbf=ax[-1].get_position().bounds 
#plt.delaxes(ax[-1])

#get legend info and add to 6th ax space
#handles, labels = ax[0].get_legend_handles_labels()
#legend=plt.legend(handles, labels,scatterpoints=1,prop={'size':16},bbox_to_anchor=(bbf[0]+bbf[2]-.05,bbf[1]+bbf[3]-.03),bbox_transform=f.transFigure)
#ax[-1].legend( bbox_to_anchor=( 0.01, 1.0 ), scatterpoints=1 )


#hide unused 6th ax (this works but then the legend is gone as well... not sure why... maybe how it handles the set_visible....)
#ax[-1].set_visible(False)


f.show()















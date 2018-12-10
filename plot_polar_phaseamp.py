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
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import glob
import math
import pandas as pd


grid='sfm6_musq'

datadir='data/misc/slr_base/'

files = ['M2_comp_mod2.75.out','N2_comp_mod2.75.out','S2_comp_mod2.75.out']

savepath='figures/png/' + grid + '_'  + '/misc/'
if not os.path.exists(savepath): os.makedirs(savepath)

f,ax = plt.subplots(nrows=1,ncols=3, subplot_kw=dict(polar=True))
ax=ax.flatten()



for i,filename in enumerate(files):
    print i
    #samp, mamp, sphs, mphs = np.genfromtxt( filename, usecols=(0, 1, 4, 5), skip_header=2,skip_footer=1 )
    samp, mamp,damp, sphs, mphs,dphs,error= np.genfromtxt( 'data/misc/slr_base/'+filename, usecols=(0, 1,2, 4, 5,6,7), skip_header=2,skip_footer=1 ,unpack=True)
    


    #num = 1
    #dtrad = [ 0 ]
    #dpamp = [ 0 ]
    #strad = [ 0 ]
    #while num <= nstat:
    #  dtrad.append( math.radians( dtphs[near_node[num]] ))
    #  dpamp.append( dtamp[near_node[num]])
    #  strad.append( math.radians( stphs[num] ))
    #  num = num + 1

    num = 0
    dtrad = [ 0 ]
    strad = [ 0 ]
    nstat = len( mamp )
    while num < nstat:
    #  print num, nstat, mphs[num]
      if num == 0:
        dtrad[num] = math.radians( mphs[num] )
        strad[num] = math.radians( sphs[num] )
      else:
        dtrad.append( math.radians( mphs[num] ))
        strad.append( math.radians( sphs[num] ))
      num = num + 1



    # Plot the lines from the model points to the observed points
    num = 0
    rads = [0.0, 1.0]
    amps = [0.0, 1.0]
    while num < nstat:
      rads[0] = dtrad[num]
      rads[1] = strad[num]
      amps[0] = mamp[num]
      amps[1] = samp[num]
      ax[i].plot( rads, amps, color='black',lw=.5 )
      num = num + 1

    
    # plot the model points with red stars
    ax[i].scatter( dtrad, mamp, c='r', edgecolor='r', marker='+', s=10, label='model' )
    # plot the observed points with blue O's
    ax[i].scatter( strad, samp, c='b',facecolor="none", marker='o', s=5, label='observed' )

    for label in ax[i].get_yticklabels()[::2]:
        label.set_visible(False)
    for label in ax[i].get_xticklabels()[1::2]:
        label.set_visible(False)
    for label in ax[i].get_yticklabels():
        label.set_fontsize(8)
    for label in ax[i].get_xticklabels():
        label.set_fontsize(8)


    tgrid=range(0,360,45)
    ax[i].set_thetagrids(tgrid, frac=1.15)  
    ax[i].grid(linestyle='-')
    ax[i].annotate( r''+files[i][0]+'$_'+files[i][1]+'$',xy=(.79,.225), xycoords='axes fraction',fontweight='bold')
    ax[i].set_yticks(ax[i].get_yticks()[::2])
    ax[i].spines['polar'].set_linewidth(1.5)


    print files[i][0:2]


    ain=np.array([samp.mean(), mamp.mean(),damp.mean(), dphs.mean(),error.mean()])
    bin=np.array([np.sqrt(np.mean(samp**2)), np.sqrt(np.mean(mamp**2)),np.sqrt(np.mean(damp**2)), np.sqrt(np.mean(dphs**2)),np.sqrt(np.mean(error**2))])
    df=pd.DataFrame(np.vstack([ain,bin]),['mean','rms'],['obs_amp','model_amp','diff_amp','diff_phase','error'])
    print df



#    print "       obs_amp       model_amp        diff_amp      diff_phase         error"
#    print "mean",samp.mean(), mamp.mean(),damp.mean(), dphs.mean(),error.mean()
#    print "rms",np.sqrt(np.mean(samp**2)), np.sqrt(np.mean(mamp**2)),np.sqrt(np.mean(damp**2)), np.sqrt(np.mean(dphs**2)),np.sqrt(np.mean(error**2))
    



#this works where the below does not, get ax position to set legend then delete the axes
#bbf=ax[-1].get_position().bounds 
#plt.delaxes(ax[-1])

#get legend info and add to 6th ax space
#handles, labels = ax[0].get_legend_handles_labels()
#legend=plt.legend(handles, labels,scatterpoints=1,prop={'size':16},bbox_to_anchor=(bbf[0]+bbf[2]+.05,bbf[1]+bbf[3]-.1),bbox_transform=f.transFigure)
#ax[-1].legend( bbox_to_anchor=( 0.01, 1.0 ), scatterpoints=1 )


#hide unused 6th ax (this works but then the legend is gone as well... not sure why... maybe how it handles the set_visible....)
#ax[-1].set_visible(False)

f.tight_layout()
f.savefig(savepath + grid + '_5con_phaseamp.png',dpi=1200)















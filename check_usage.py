import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from math import pi
from datatools import *
from gridtools import *
from misctools import *
import scipy as sp
import matplotlib as mpl
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import sys
import pandas


#load usage file
usagedata=np.genfromtxt('qstat_history_aug20_2014.dat', dtype=None,skiprows=2)



#create decimal wallhours
cpuhours=np.zeros([len(usagedata),])
for i in range(0,len(usagedata)):
	print i
	temp=usagedata[i][3].split(':')
	if len(temp)==3:
		cpuhours[i]=float(temp[0])+float(temp[0])/60+float(temp[0])/3600
	else:
		cpuhours[i]=0


#create user list
users=np.empty([len(usagedata),],dtype='|S15')
for i in range(0,len(usagedata)):
	print i
	users[i]=usagedata[i][2]


uni_users=np.unique(users)
user_cpuhours=np.zeros([len(uni_users),])

for i in range(0,len(uni_users)):
	idx=np.where(users==uni_users[i])
	user_cpuhours[i]=np.sum(cpuhours[idx])


df=pandas.DataFrame(user_cpuhours,uni_users,['CPU Hours (cores*wall hours)'])

print df.sort(['CPU Hours (cores*wall hours)'],ascending=False)


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



usagedata=np.genfromtxt('qstat_data/qstat_history_aug11_2014.dat', dtype=None,skiprows=2)

#make empty arrays
jid=np.empty([len(usagedata),])
user=np.empty([len(usagedata),],dtype=np.dtype(('S100',1)))
cores=np.empty([len(usagedata),])
walltime=np.empty([len(usagedata),],dtype=np.dtype(('S100',1)))


#load usage file
with open('qstat_data/qstat_history_full_aug11_2014.dat') as f:
    jcnt=0
    for line in f:
        if line.startswith('Job Id: '):
            jid[jcnt] = line[8:-5]
        if line.startswith('    Job_Owner = '):
            user[jcnt] = line[16:-5]
        if line.startswith('    resources_used.ncpus = '):
            cores[jcnt] = line[27:-1]
        if line.startswith('    resources_used.walltime = '):
            walltime[jcnt] = line[30:-1]
        if line.startswith('    job_state = '): 
            if line.endswith('R\n'):
                print 'Running job'
            else:
                jcnt=jcnt+1
       



#create decimal wallhours
cpuhours=np.zeros([len(walltime),])
for i in range(0,len(walltime)):
	print i
	temp=walltime[i].split(':')
	if len(temp)==3:
		cpuhours[i]=float(temp[0])+float(temp[0])/60+float(temp[0])/3600
	else:
		cpuhours[i]=0




uni_users=np.unique(user)
user_cpuhours=np.zeros([len(uni_users),])

for i in range(0,len(uni_users)):
	idx=np.where(user==uni_users[i])
	user_cpuhours[i]=np.sum(np.multiply(cpuhours[idx],cores[idx]))


df=pandas.DataFrame(user_cpuhours,uni_users,['CPU Hours (cores*wall hours)'])

print df.sort(['CPU Hours (cores*wall hours)'],ascending=False)


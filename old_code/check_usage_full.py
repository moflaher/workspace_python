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

pandas.options.display.float_format = '{:,.1f}'.format


usagedata=np.genfromtxt('qstat_data/qstat_history_aug20_2014.dat', dtype=None,skiprows=2)

#make empty arrays
jid=np.empty([len(usagedata),])
user=np.empty([len(usagedata),],dtype=np.dtype(('S100',1)))
cores=np.empty([len(usagedata),])
walltime=np.empty([len(usagedata),],dtype=np.dtype(('S100',1)))
jstate=np.empty([len(usagedata),])
queue=np.empty([len(usagedata),],dtype=np.dtype(('S100',1)))
ctime=np.empty([len(usagedata),],dtype=np.dtype(('S100',1)))
mtime=np.empty([len(usagedata),],dtype=np.dtype(('S100',1)))
qtime=np.empty([len(usagedata),],dtype=np.dtype(('S100',1)))
stime=np.empty([len(usagedata),],dtype=np.dtype(('S100',1)))
qtime_num=np.empty([len(usagedata),])
stime_num=np.empty([len(usagedata),])

#load usage file
f=open('qstat_data/qstat_history_full_aug20_2014.dat')
jcnt=-1
next=False
for line in f:

    if line.startswith('Job Id: '):
        jcnt=jcnt+1
        jid[jcnt] = line[8:-5]
    if line.startswith('    Job_Owner = '):
        user[jcnt] = line[16:-5]
    if line.startswith('    resources_used.ncpus = '):
        cores[jcnt] = line[27:-1]
    if line.startswith('    resources_used.walltime = '):
        walltime[jcnt] = line[30:-1]
    if line.startswith('    job_state = '): 
        if line.endswith('F\n'):
            jstate[jcnt]=True
        else:
            jstate[jcnt]=False
    if line.startswith('    queue = '):
        queue[jcnt]=line[12:-1]
    if line.startswith('    ctime = '):
        ctime[jcnt]=line[12:-1]
    if line.startswith('    mtime = '):
        mtime[jcnt]=line[12:-1]
    if line.startswith('    qtime = '):
        qtime[jcnt]=line[12:-1]
    if line.startswith('    stime = '):
        stime[jcnt]=line[12:-1]




f.close()       




#create decimal wallhours
cpuhours=np.zeros([len(walltime),])
for i in range(0,len(walltime)):
	temp=walltime[i].split(':')
	if len(temp)==3:
		cpuhours[i]=float(temp[0])+float(temp[0])/60+float(temp[0])/3600
	else:
		cpuhours[i]=0

#Compute waittimes
for i in range(0,len(qtime)):
    if qtime[i]=='':
        qtime[i]=stime[i]
    qtime_num[i]=mpl.dates.datestr2num(qtime[i])
    if stime[i]=='':
        stime[i]=qtime[i]
    stime_num[i]=mpl.dates.datestr2num(stime[i])

smin=stime[np.argmin(stime_num)]
smax=stime[np.argmax(stime_num)]

print ''
print '****************************************************************************************'
print 'User Stats from ' + smin + ' to ' +smax
print '****************************************************************************************'
print ''

#Compute usage
uni_users=np.unique(user)
user_cpuhours=np.zeros([len(uni_users),])

for i in range(0,len(uni_users)):
	idx=np.where((user==uni_users[i]) & (jstate==True))
	user_cpuhours[i]=np.sum(np.multiply(cpuhours[idx],cores[idx]))

df=pandas.DataFrame(user_cpuhours,uni_users,['CPU Hours (cores*wall hours)'])
print df.sort(['CPU Hours (cores*wall hours)'],ascending=False)
print ''



waittime=stime_num-qtime_num

user_waittime_mean=np.zeros([len(uni_users),])
for i in range(0,len(uni_users)):
    idx=np.where((user==uni_users[i]) & (waittime>0) & (jstate==True))
    if (idx[0].size!=0):
        user_waittime_mean[i]=np.mean(waittime[idx]*24)

df=pandas.DataFrame(user_waittime_mean,uni_users,['User Average Wait Time (h)'])
print df.sort(['User Average Wait Time (h)'],ascending=False)
print ''

user_waittime_max=np.zeros([len(uni_users),])
for i in range(0,len(uni_users)):
    idx=np.where((user==uni_users[i]) & (waittime>0) & (jstate==True))
    if (idx[0].size!=0):
        user_waittime_max[i]=np.max(waittime[idx]*24)

df=pandas.DataFrame(user_waittime_max,uni_users,['User Max Wait Time (h)'])
print df.sort(['User Max Wait Time (h)'],ascending=False)
print ''


print 'Average cluster wait time (m): ' + ("%d"%np.mean(waittime*24*60))
print 'Max cluster wait time (m): ' + ("%d"%np.max(waittime*24*60))
print 'Min cluster wait time (m): ' + ("%d"%np.min(waittime*24*60))
print ''


print ''
print ''
print ''
print ''
print ''
print ''
print ''
print ''
print '****************************************************************************************'
print 'Queue Stats from ' + smin + ' to ' +smax
print '****************************************************************************************'
print ''

#Compute usage per queue
queue_users=np.unique(queue)
queue_cpuhours=np.zeros([len(queue_users),])

for i in range(0,len(queue_users)):
	idx=np.where((queue==queue_users[i]) & (jstate==True))
	queue_cpuhours[i]=np.sum(np.multiply(cpuhours[idx],cores[idx]))

df=pandas.DataFrame(queue_cpuhours,queue_users,['CPU Hours (cores*wall hours)'])
print df.sort(['CPU Hours (cores*wall hours)'],ascending=False)
print ''


queue_waittime_mean=np.zeros([len(queue_users),])
for i in range(0,len(queue_users)):
    idx=np.where((queue==queue_users[i]) & (waittime>0) & (jstate==True))
    if (idx[0].size!=0):
        queue_waittime_mean[i]=np.mean(waittime[idx]*24)

df=pandas.DataFrame(queue_waittime_mean,queue_users,['Queue Average Wait Time (h)'])
print df.sort(['Queue Average Wait Time (h)'],ascending=False)
print ''

queue_waittime_max=np.zeros([len(queue_users),])
for i in range(0,len(queue_users)):
    idx=np.where((queue==queue_users[i]) & (waittime>0) & (jstate==True))
    if (idx[0].size!=0):
        queue_waittime_max[i]=np.max(waittime[idx]*24)

df=pandas.DataFrame(queue_waittime_max,queue_users,['Queue Max Wait Time (h)'])
print df.sort(['Queue Max Wait Time (h)'],ascending=False)
print ''















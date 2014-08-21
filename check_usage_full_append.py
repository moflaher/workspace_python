import numpy as np
import matplotlib as mpl
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pandas

pandas.options.display.float_format = '{:,.1f}'.format


usagedata=10000

#make empty arrays
qstatdic={}

qstatdic['jid']=np.empty([usagedata,])
qstatdic['user']=np.empty([usagedata,],dtype=np.dtype(('S100',1)))
qstatdic['cores']=np.empty([usagedata,])
qstatdic['walltime']=np.empty([usagedata,],dtype=np.dtype(('S100',1)))
qstatdic['jstate']=np.empty([usagedata,])
qstatdic['queue']=np.empty([usagedata,],dtype=np.dtype(('S100',1)))
qstatdic['ctime']=np.empty([usagedata,],dtype=np.dtype(('S100',1)))
qstatdic['mtime']=np.empty([usagedata,],dtype=np.dtype(('S100',1)))
qstatdic['qtime']=np.empty([usagedata,],dtype=np.dtype(('S100',1)))
qstatdic['stime']=np.empty([usagedata,],dtype=np.dtype(('S100',1)))
qstatdic['qtime_num']=np.empty([usagedata,])
qstatdic['stime_num']=np.empty([usagedata,])

#load usage file
f=open('qstat_data/qstat_history_full.dat')
jcnt=-1
next=False
for line in f:

    if line.startswith('Job Id: '):
        jcnt=jcnt+1
        qstatdic['jid'][jcnt] = line[8:-5]
    if line.startswith('    Job_Owner = '):
        qstatdic['user'][jcnt] = line[16:-5]
    if line.startswith('    resources_used.ncpus = '):
        qstatdic['cores'][jcnt] = line[27:-1]
    if line.startswith('    resources_used.walltime = '):
        qstatdic['walltime'][jcnt] = line[30:-1]
    if line.startswith('    job_state = '): 
        if line.endswith('F\n'):
            qstatdic['jstate'][jcnt]=True
        else:
            qstatdic['jstate'][jcnt]=False
    if line.startswith('    queue = '):
        qstatdic['queue'][jcnt]=line[12:-1]
    if line.startswith('    ctime = '):
        qstatdic['ctime'][jcnt]=line[12:-1]
    if line.startswith('    mtime = '):
        qstatdic['mtime'][jcnt]=line[12:-1]
    if line.startswith('    qtime = '):
        qstatdic['qtime'][jcnt]=line[12:-1]
    if line.startswith('    stime = '):
        qstatdic['stime'][jcnt]=line[12:-1]




f.close()       


jidu,jobididx=np.unique(qstatdic['jid'],return_index=True)


for key in qstatdic.keys():
    qstatdic[key]=qstatdic[key][jobididx]





#create decimal wallhours
cpuhours=np.zeros([len(qstatdic['walltime']),])
for i in range(0,len(qstatdic['walltime'])):
	temp=qstatdic['walltime'][i].split(':')
	if len(temp)==3:
		cpuhours[i]=float(temp[0])+float(temp[0])/60+float(temp[0])/3600
	else:
		cpuhours[i]=0

#Compute waittimes
for i in range(0,len(qstatdic['qtime'])):
    if qstatdic['qtime'][i]=='':
        qstatdic['qtime'][i]=qstatdic['stime'][i]
    qstatdic['qtime_num'][i]=mpl.dates.datestr2num(qstatdic['qtime'][i])
    if qstatdic['stime'][i]=='':
        qstatdic['stime'][i]=qstatdic['qtime'][i]
    qstatdic['stime_num'][i]=mpl.dates.datestr2num(qstatdic['stime'][i])

smin=qstatdic['stime'][np.argmin(qstatdic['stime_num'])]
smax=qstatdic['stime'][np.argmax(qstatdic['stime_num'])]

print ''
print '****************************************************************************************'
print 'user Stats from ' + smin + ' to ' +smax
print '****************************************************************************************'
print ''

#Compute usage
uni_users=np.unique(qstatdic['user'])
user_cpuhours=np.zeros([len(uni_users),])

for i in range(0,len(uni_users)):
	idx=np.where((qstatdic['user']==uni_users[i]) & (qstatdic['jstate']==True))
	user_cpuhours[i]=np.sum(np.multiply(cpuhours[idx],qstatdic['cores'][idx]))

df=pandas.DataFrame(user_cpuhours,uni_users,['CPU Hours (user*wall hours)'])
print df.sort(['CPU Hours (user*wall hours)'],ascending=False)
print ''



waittime=qstatdic['stime_num']-qstatdic['qtime_num']

user_waittime_mean=np.zeros([len(uni_users),])
for i in range(0,len(uni_users)):
    idx=np.where((qstatdic['user']==uni_users[i]) & (waittime>0) & (qstatdic['jstate']==True))
    if (idx[0].size!=0):
        user_waittime_mean[i]=np.mean(waittime[idx]*24)

df=pandas.DataFrame(user_waittime_mean,uni_users,['User Average Wait Time (h)'])
print df.sort(['User Average Wait Time (h)'],ascending=False)
print ''

user_waittime_max=np.zeros([len(uni_users),])
for i in range(0,len(uni_users)):
    idx=np.where((qstatdic['user']==uni_users[i]) & (waittime>0) & (qstatdic['jstate']==True))
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
print 'queue Stats from ' + smin + ' to ' +smax
print '****************************************************************************************'
print ''

#Compute usage per qstatdic['queue']
queue_users=np.unique(qstatdic['queue'])
queue_cpuhours=np.zeros([len(queue_users),])

for i in range(0,len(queue_users)):
	idx=np.where((qstatdic['queue']==queue_users[i]) & (qstatdic['jstate']==True))
	queue_cpuhours[i]=np.sum(np.multiply(cpuhours[idx],qstatdic['cores'][idx]))

df=pandas.DataFrame(queue_cpuhours,queue_users,['CPU Hours (cores*wall hours)'])
print df.sort(['CPU Hours (cores*wall hours)'],ascending=False)
print ''


queue_waittime_mean=np.zeros([len(queue_users),])
for i in range(0,len(queue_users)):
    idx=np.where((qstatdic['queue']==queue_users[i]) & (waittime>0) & (qstatdic['jstate']==True))
    if (idx[0].size!=0):
        queue_waittime_mean[i]=np.mean(waittime[idx]*24)

df=pandas.DataFrame(queue_waittime_mean,queue_users,['Queue Average Wait Time (h)'])
print df.sort(['Queue Average Wait Time (h)'],ascending=False)
print ''

queue_waittime_max=np.zeros([len(queue_users),])
for i in range(0,len(queue_users)):
    idx=np.where((qstatdic['queue']==queue_users[i]) & (waittime>0) & (qstatdic['jstate']==True))
    if (idx[0].size!=0):
        queue_waittime_max[i]=np.max(waittime[idx]*24)

df=pandas.DataFrame(queue_waittime_max,queue_users,['Queue Max Wait Time (h)'])
print df.sort(['Queue Max Wait Time (h)'],ascending=False)
print ''















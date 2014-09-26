import numpy as np
import matplotlib as mpl
np.set_printoptions(precision=8,suppress=True,threshold=np.nan)
import pandas

pandas.options.display.float_format = '{:,.1f}'.format




datetime=np.empty([0,],dtype='|S100')
pressure=np.empty([0,],dtype=np.int16)
temp=np.empty([0,],dtype=np.int16)
dewpoint=np.empty([0,],dtype=np.int16)
winddir=np.empty([0,],dtype=np.int16)
windspeed=np.empty([0,],dtype=np.int16)
windgust=np.empty([0,],dtype=np.int16)
rain=np.empty([0,],dtype=np.float)


#load usage file
f=open('/home/moe46/Desktop/bio/wqs/TEXT_HOURLIES_WQS_20030101-20140915_clean.txt')
f=open('/home/moe46/Desktop/bio/cfki_2003-2014/cpyear/all_cfki_clean.dat')
jcnt=0
next=False
for line in f:
    print jcnt
    jcnt=jcnt+1
    if line.startswith('\r'):
        continue
    else:
        splitline=line.split(' ')
        other=splitline[9].split('/')

    rainnum=True
    for i in range(9,len(splitline)):
        if splitline[i].startswith('PAST'):
            rainnum=i-1
            break
        

    datetime=np.append(datetime,[splitline[0] + '-' + splitline[1]])

    if other[0].startswith('M'):
        pressure=np.append(pressure,np.nan)    
    else:
        pressure=np.append(pressure,other[0])


    if other[1].startswith('M'):
        temp=np.append(temp,np.nan)   
    else:
        temp=np.append(temp,other[1])

   
    if other[2].startswith('M'):
        dewpoint=np.append(dewpoint,np.nan)   
    else:
        dewpoint=np.append(dewpoint,other[1])


    if other[3][0:2].startswith('M'):
        winddir=np.append(winddir,np.nan)
    else:
        winddir=np.append(winddir,int(other[3][0:2])*10)


    if other[3][2:4].startswith('M'):
        windspeed=np.append(windspeed,np.nan)
    else:
        windspeed=np.append(windspeed,int(other[3][2:4]))


    if len(other[3])>4:
        windgust=np.append(windgust,int(other[3][5:7]))
    else:
        windgust=np.append(windgust,0)

    
    if rainnum==True:
        rain=np.append(rain,0.0)
    else:
        rain=np.append(rain,float(splitline[rainnum][0:-2]))


f.close()       


fp=open('cfki_alldata.dat','w')

fp.write('%s\n' % ('time pressure temp(C) dewpoint(C) wind_direction(degree) wind_speed(knots) wind_gust(knots) rain(mm)'))

for i in range(0,len(datetime)):
    fp.write('%s %s %s %s %f %f %d %f\n' % (datetime[i],pressure[i],temp[i],dewpoint[i],winddir[i],windspeed[i],windgust[i],rain[i]) )


fp.close()
































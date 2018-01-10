from gridtools import *
neifile=loadnei('sfm6_musq.nei')
longlat=np.genfromtxt('sfm6_musq.ll')
neifile['llminmax']=np.array([longlat[:,0].max(),longlat[:,1].max(),longlat[:,0].min(),longlat[:,1].min()])
neifile['nodell']=longlat
savenei('sfm6_musq_ll.nei',neifile)

from __future__ import division,print_function
import copy
import numpy as np
cimport numpy as np

def get_nvc(np.ndarray[long, ndim=2] neighbours,long nnodes, long maxnei):

    
    cdef np.ndarray nv=np.empty((2*neighbours.shape[0],3),dtype=np.long) 

    cdef int kk=0
    cdef int i=0
    cdef int ii=0
    cdef int j=0
    cdef int nei_cnt=0
    
    for i in range(nnodes-2):
        nei_cnt=1
        for ii in range(maxnei-1):
            if neighbours[i,ii+1]==0:
                break
            nei_cnt=ii+1    
            if neighbours[i,ii]<=(i+1):
                continue
            if neighbours[i,ii+1]<=(i+1):
                continue   
            for j in range(maxnei):
                if neighbours[neighbours[i,ii]-1,j]!=neighbours[i,ii+1]:
                    continue
                nv[kk,:]=[i+1,neighbours[i,ii],neighbours[i,ii+1]]
                kk=kk+1
                break

        if (nei_cnt>1):
            for j in range(maxnei):
                if neighbours[i,0]<=(i+1):
                    break
                if neighbours[i,nei_cnt]<=(i+1):
                    break
                if neighbours[neighbours[i,0]-1,j] ==0:
                    break    
                if neighbours[neighbours[i,0]-1,j] !=neighbours[i,nei_cnt]:
                    continue
                nv[kk,:]=[i+1,neighbours[i,nei_cnt],neighbours[i,0] ]
                kk=kk+1
                break
                 
    nv=np.delete(nv,np.s_[kk:],axis=0)
    nv=(nv-1).astype(int)      
                
    return nv

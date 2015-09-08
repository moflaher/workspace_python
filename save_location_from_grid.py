from __future__ import division,print_function
from datatools import *
import os, sys
import argparse



def get_location(fileDir,location,filename=None,dim='2D'):
    data = loadnc(fileDir,filename,dim)
    data = ncdatasort(data)
    #lonlat = np.array([location,location])
    cnode = closest_node(data,location)
    cele = closest_element(data,location)

    ua = data['ua'][:,cele]
    va = data['va'][:,cele]
    el = data['zeta'][:,cnode]
    h = data['h'][cnode]
    time = data['time']+678942
    

    return ua,va,el,h,time,cnode,cele


if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument("-lon", help="Longitude of the point at which to extract data.",type=float,required=True)
    parser.add_argument("-lat", help="Latitude of the point at which to extract data.",type=float,required=True)
    parser.add_argument("-path", help="NC-file folder path.",type=str,required=True)
    parser.add_argument("-o", help="Filename of the hdf5 to be saved.",type=str,required=True)
    parser.add_argument("-i", help="NC-file filename (optional).",type=str,default='')
    args = parser.parse_args()
       
 
 
    
   




    location = [args.lon ,args.lat]

    if args.i=='':
        print 'Location is', location
        print 'Output file is', args.o
        print 'File path is', args.path      
        ua,va,el,h,time,cnode,cele = get_location(args.path,location) 
    else:
        print 'Location is', location
        print 'Output file is', args.o
        print 'Input file is', args.path, args.i
        ua,va,el,h,time,cnode,cele = get_location(args.path,location,args.i)





    outfile = h5py.File(args.o,'w')
    outfile.create_dataset("ua", data=ua)
    outfile.create_dataset("va", data=va)
    outfile.create_dataset("el", data=el)
    outfile.create_dataset("h", data=h)
    outfile.create_dataset("time", data=time)
    outfile.create_dataset("cnode", data=cnode)
    outfile.create_dataset("cele", data=cele)

    outfile.close()
    


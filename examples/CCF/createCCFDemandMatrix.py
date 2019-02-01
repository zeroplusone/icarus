#!/usr/bin/python

import sys

if len(sys.argv) != 3:
    print("please enter data size and input filename")
else:
    data_size = int(sys.argv[1])
    filename = sys.argv[2] 
    with open(filename) as f:
        content = f.readlines()
    count=0
    for x in content:
        print(x.strip(), end=' ')
        count+=1
        if count%data_size==0:
            print()

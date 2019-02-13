#!/usr/bin/python

import sys

if len(sys.argv) != 3:
    print("please enter data size and input filename")
else:
    data_size = int(sys.argv[1])
    filename = sys.argv[2] 
    with open(filename) as f:
        content = f.readlines()

    content = [x.strip() for x in content]

    for c in content:
        out_list = list(map(float, c.split()))
        for prob in out_list:
            print(prob)


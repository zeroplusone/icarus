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
        out_set = set(map(int, c.split()))
        remaining_size = len(out_set)
        prob = 1.0/remaining_size
        for j in range(data_size):
            if j in out_set:
                print(prob)
            else:
                print(0)


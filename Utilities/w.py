#!/usr/bin/env python

import sys
import os
import fnmatch

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    start = ''
    if len(args) > 0:
        start = args[0]
        if '*' not in start and '[' not in start and '?' not in start:
            start += '*'
        

    (baseDir, thisExec) = os.path.split(sys.argv[0])
    for f in os.listdir(baseDir):
        if f != thisExec and fnmatch.fnmatch(f, start):
            print f


    return 0



if __name__ == '__main__':
    sys.exit(main())


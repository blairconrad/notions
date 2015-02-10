#!/usr/bin/env "python -u"

import sys
import os
import datetime

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    d = sys.stdin.readline()
    while d:
        print datetime.datetime.now(), d,
        d = sys.stdin.readline()
        
    return 0



if __name__ == '__main__':
    sys.exit(main())


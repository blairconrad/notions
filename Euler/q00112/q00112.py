#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def is_increasing(s):
    last = '0'
    for c in s:
        if c < last:
            return False
        last = c
    return True

def is_decreasing(s):
    last = '9'
    for c in s:
        if c > last:
            return False
        last = c
    return True



def solve(ratio):
    bouncy = 0
    n = 0
    while True:
        n += 1
        s = str(n)
        if not is_decreasing(s) and not is_increasing(s):
            bouncy += 1
            if bouncy >= ratio * n:
                return n
        #print n, bouncy, float(bouncy)/n

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 99
    else:
        n = int(args[0])
    n = float(n)/100

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 1587000 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())


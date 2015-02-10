#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def solve(n):
    t = 0
    for a in range(1,n):
        for b in range(1,n):
            t = max(t, sum(shared.digits(a**b)))
            #print a, b, t
    return t
            

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 100
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 972 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())


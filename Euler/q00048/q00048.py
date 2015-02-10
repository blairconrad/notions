#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def solve(n):
    return sum((i**i for i in xrange(1, n+1))) % 10**10

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 1000
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 9110846700 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())


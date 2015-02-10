#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def solve(n):
    results = set()
    for a in range(2, n+1):
        for b in range(2, n+1):
            results.add(a**b)
    return len(results)

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
    assert 9183 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())


#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def C(n, r):
    return shared.factorial(n)/(shared.factorial(r)*shared.factorial(n-r))

def solve(n):
    count = 0
    for n in range(1,101):
        for r in range(1,n+1):
            if C(n,r) > 1000000:
                count += 1
    return count

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 20
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 4075 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())


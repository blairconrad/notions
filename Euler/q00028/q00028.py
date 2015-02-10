#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def solve(n):
    return 1 + sum((4* l * l - 6 * l + 6 for l in range(3, n+1, 2)))

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 1001
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 669171001 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())


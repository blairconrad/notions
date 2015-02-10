#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared


def partition(smallest_addend, n):
    if smallest_addend > n:
        return 0
    if smallest_addend == n:
        return 1
    return partition(smallest_addend, n-smallest_addend)  + \
           partition(smallest_addend+1, n)
partition = shared.Memoize(partition)

def solve(n):
    return partition(1, n)-1

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
    assert 190569291 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())


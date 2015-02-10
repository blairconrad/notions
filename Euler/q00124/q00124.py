#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared
import operator
import itertools

shared.find_factors = shared.Memoize(shared.find_factors, 1)


def prod(seq):
    r = 1
    for p in seq:
        r *= p
    return r

def solve(n):
    e = []
    for n in range(1, 100000+1):
        factors = set(shared.find_factors(n))
        e.append((reduce(operator.mul, factors, 1), n))
    e.sort()
    return e[10000-1][1]

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
    assert 21417 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())


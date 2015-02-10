#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared
from math import log

def solve(pairs):
    results = []
    for i in range(len(pairs)):
        base, exp = pairs[i]
        results.append((log(base)*exp, i+1))
    results.sort()
    return results[-1][1]

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    pairs = [map(int, line.strip().split(',')) for line in file('base_exp.txt')]
    start = datetime.datetime.now()
    result = solve(pairs)
    end = datetime.datetime.now()
    print result
    assert 709 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())


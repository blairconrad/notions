#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def solve(n):
    allPrimes = {}
    g = shared.PrimeGenerator()
    for p in g:
        if p < n:
            allPrimes[p] = None
        else:
            break

    count = 0
    for p in allPrimes.keys():
        p = str(p)
        all_in = True
        for i in range(len(p)):
            p2 = int(p[i:] + p[:i])
            if p2 not in allPrimes:
                all_in = False
                break
        if all_in:
            count += 1
    return count


def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 1000000
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 55 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())


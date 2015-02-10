#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared
import collections
import pprint

def fourdigitprimes():
    g = shared.PrimeGenerator()
    p = g.next()
    while p < 1000:
        p = g.next()
    while p < 10000:
        yield p
        p = g.next()

def check(primes):
    while len(primes) >= 3:
        p1 = primes.pop(0)
        for i in range(len(primes)-1):
            diff = primes[i] - p1
            #print p1, diff, primes[i:]
            if primes[i] + diff in primes[i+1:]:
                return p1 * 10**8 + primes[i] * 10**4 +  primes[i] + diff
    return 148748178147

def solve(n):
    groups = collections.defaultdict(list)
    for p in fourdigitprimes():
        strp = sorted(str(p))
        groups[''.join(strp)].append(p)

    for group in groups.values():
        result = check(group)
        if result > 148748178147:
            return result
            
            

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
    assert 296962999629 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())


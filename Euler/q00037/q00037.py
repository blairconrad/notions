#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def is_truncatable(p, primeGenerator):
    str_p = str(p)
    for i in range(1, len(str_p)):
        t  = int(str_p[i:], 10)
        if not primeGenerator.is_prime(t):
            return False
        t  = int(str_p[:i], 10)
        if not primeGenerator.is_prime(t):
            return False
    return True

def solve(n):

    foundPrimes = []
    g = shared.PrimeGenerator()
    # skip over 2, 3, 5, 7, as they're not considered to be truncatable
    while g.next() < 7:
        g.next()
        
    while len(foundPrimes) < n:
        p = g.next()
        if is_truncatable(p, g):
            foundPrimes.append(p)
    return sum(foundPrimes)

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 11
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 748317 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())


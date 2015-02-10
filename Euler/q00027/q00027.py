#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import sys
import datetime
sys.path.append('..')
import shared

def number_of_primes(a, b):
    g = shared.PrimeGenerator()
    n = 0
    while True:
        f = n * n + a * n + b
        #print n, a, b, f
        if not g.is_prime(f):
            return n
        n += 1

def solve(max_coeff):
    #n² + an + b, where |a| < max_coeff and |b| < max_coeff

    # -> b must be prime, since the equation evaluates to b when n = 0
    # -> 1 + a + b must be prime, so a is odd
    # -> a = prime - 1 - b
    product = 0
    max_length = 0

    gb = shared.PrimeGenerator()
    for b in gb:
        if b > max_coeff:
            break

        for a in range(1, 1000, 2): # using only the oddness of a, not the prime thing
            for factors in [(a, b), (a, -b), (-a, b), (-a, -b)]:
                count = number_of_primes(*factors)
                if count > max_length:
                    max_length = count
                    product = factors[0] * factors[1]
                    #print factors, max_length
    return product

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
    assert -59231 == result
    
    print 'Elapsed:', end - start

    return 0


if __name__ == '__main__':
    sys.exit(main())


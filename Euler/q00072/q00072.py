#!/usr/bin/env python

import sys
import shared
import itertools


# Consider the fraction, n/d, where n and d are positive integers. If
# n<d and HCF(n,d)=1, it is called a reduced proper fraction.

# If we list the set of reduced proper fractions for d ? 8 in
# ascending order of size, we get:

# 1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5,
# 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

# It can be seen that there are 21 elements in this set.

# How many elements would be contained in the set of reduced proper
# fractions for d <= 1,000,000?


primes = []
shared_factors = []
g = shared.prime_generator()


def find_factors(n, prime_offset=0):
    if n == 1:
        return []
    original_n = n
    while True:
        p = primes[prime_offset]
        if n % p == 0:
            factors = [p]
            n /= p
            while n % p == 0:
                n /= p

            return factors + find_factors(n, prime_offset+1)
        prime_offset += 1

find_factors = shared.Memoize(find_factors, 1)

def prime_primes(n):
    global primes
    global shared_factors
    shared_factors = [None] * (n+1)
    g = shared.prime_generator()
    primes = [p for p in itertools.takewhile(lambda x: x <= n, g)]
    for p in primes:
        find_factors.memo[(p,)] = [p]

expected = 303963552391

def solve():
    n = 1000000
    prime_primes(n)
    count = 0
    g = shared.prime_generator()
    p = g.next()
    for den in xrange(2,n+1):
        if den == p:
            #print den
            count += den-1
            p = g.next()
            continue
        
        factors = find_factors(den)
        #print den, factors
        rn = 1
        rd = 1

        for f in factors:
            rn *= f-1
            rd *= f
        count += den * rn / rd
    return count


if __name__ == '__main__':
    sys.exit(main())


#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import sys
import datetime
sys.path.append('..')
import shared
import itertools

# Euler's Totient function, φ(n) [sometimes called the phi function],
# is used to determine the number of positive numbers less than or
# equal to n which are relatively prime to n.
#
# For example, as 1, 2, 4, # 5, 7, and 8, are all less than nine and
# relatively prime to nine, φ(9)=6.
# The number 1 is considered to be relatively prime to every
# positive number, so φ(1)=1.
#
# Interestingly, φ(87109)=79180, and it can be seen that 87109 is a
# permutation of 79180.
#
# Find the value of n, 1 < n < 10^(7), for which φ(n) is a permutation
# of n and the ratio n/φ(n) produces a minimum.

# -> phi(n)/n is maximal
# -> prod((f-1)/f)/n is maximal
# -> we like lots of fs....
# -> well, high fs....
# -> well, no squares
# hmmm.... prod((f-1)/f)> 1/10
# hey! given the example, we know that prod((f-1)/f)>.908
# - so, if we have a product of 2 primes, p1 and p2, then p1, p2 > 10
# also, we know that n isn't prime, since phi(p) = p-1, and there's no way that's
#   a permutation of p

def solve(max):
    best_ratio = float(79180)/87109
    best_n = 87190
    
    g = shared.PrimeGenerator()
    primes = [p for p in itertools.takewhile(lambda p: p < max * (1-best_ratio), g)]

    high_prime_index = len(primes)-1
    while high_prime_index >= 0:
        high_prime = primes[high_prime_index]

        low_prime_index = 0
        while low_prime_index <= high_prime_index:
            low_prime = primes[low_prime_index]
            low_prime_index += 1
            product = low_prime * high_prime

            if product > max:
                break
            phi = (low_prime-1)*(high_prime-1)

            #print low_prime, high_prime, product, phi
            if sorted(str(product)) == sorted(str(phi)):
                ratio = float(phi)/product
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_n = product
                #    print 'best', best_n, best_ratio
                #print product, phi
                
        high_prime_index -= 1
    return best_n
        
        
    return len(primes)

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 10**7
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 8319823 == result
    


    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())


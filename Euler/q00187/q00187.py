#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared
import sys

# A composite is a number containing at least two prime factors. For example, 15 = 3 × 5; 9 = 3 × 3; 12 = 2 × 2 × 3.
# There are ten composites below thirty containing precisely two, not necessarily distinct, prime factors: 4, 6, 9, 10, 14, 15, 21, 22, 25, 26.
# How many composite integers, n < 10**8, have precisely two, not necessarily distinct, prime factors?

expected = 17427258

def solve():
    max = 10**8
    half_max = max/2
    small_primes = []
    generator = shared.generate_primes(half_max)
    for p in generator:
        if p*p > max: break
        small_primes.append(p)
    count = (len(small_primes)+1) * (len(small_primes)) / 2

    try:
        while len(small_primes) > 0:
            next_small_prime = small_primes[-1]
            while p <= max/next_small_prime:
                count += len(small_primes)
                p = generator.next() 
            small_primes.pop()
    except StopIteration:
        pass
    return count
    

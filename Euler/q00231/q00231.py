#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# The binomial coefficient C(10,3) = 120.
#
# 120 = 2**3 * 3 * 5 = 2 * 2 * 2 * 3 * 5, and 2 + 2 + 2 + 3 + 5 = 14.
#
# So the sum of the terms in the prime factorisation of C(10,3) is 14.
# 
# Find the sum of the terms in the prime factorisation of C(20000000, 15000000).


expected = 7526965179680L

def count_factors(n, p):
    count = 0
    f = p
    while f <= n:
        count += n/f
        f *= p
    return p * count

def solve():
    top = 20000000
    bottom = 15000000
    
    total = 0
    for p in shared.prime_generator(top):
        total -= count_factors(bottom, p)
        total -= count_factors(top-bottom, p)
        total += count_factors(top, p)
            
    return total

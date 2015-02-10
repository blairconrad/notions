#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# Let phi; be Euler's totient function, i.e. for a natural number n,
# phi;(n) is the number of k, 1 <= k <= n, for which gcd(k,n) = 1.
# 
# By iterating phi;, each positive integer generates a decreasing chain of numbers ending in 1.

# E.g. if we start with 5 the sequence 5,4,2,1 is generated.

# Here is a listing of all chains with length 4:
# 
# 5,4,2,1
# 7,6,2,1
# 8,4,2,1
# 9,6,2,1
# 10,4,2,1
# 12,4,2,1
# 14,6,2,1
# 18,6,2,1
# 
# Only two of these chains start with a prime, their sum is 12.
# 
# What is the sum of all primes less than 40000000 which generate a chain of length 25?

expected = 1677366278943


chain_lengths = { 1: 1 }

primes = []

def chain_length(n):
    if n in chain_lengths: return chain_lengths[n]

    l = 1 + chain_length(phi(n))
    chain_lengths[n] = l
    return l

def phi(n):
    factors = shared.find_factors(n, primes)
    for f in set(factors):
        n = n * (f-1) / f
    return n

def solve():
    total = 0
    g = shared.prime_generator(40000000)
    for p in g:
        primes.append(p)
    
        if 24 == chain_length(p-1): # plus one for p
            total += p
    
    return total


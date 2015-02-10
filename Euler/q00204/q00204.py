#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared
import math
import itertools

# A Hamming number is a positive number which has no prime factor larger than 5.<br/>
# So the first few Hamming numbers are 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15.<br/>
# There are 1105 Hamming numbers not exceeding 10**8.
# 
# We will call a positive number a generalised Hamming number of type <var>n</var>, if it has no prime factor larger than <var>n</var>.<br/>
# Hence the Hamming numbers are the generalised Hamming numbers of type 5.
# 
# How many generalised Hamming numbers of type 100 are there which don't exceed 10**9?

expected = 2944730

def count_hamming(primes, max):
    if not primes:
        return 1

    total = 0
    first_prime = primes[0]
    for exp in range(int(math.log(max, first_prime))+1):
        total += count_hamming(primes[1:], max/(first_prime**exp))
    return total

def solve():
    max = 10**9

    count = 0

    primes = list(itertools.takewhile(lambda p: p < 100, shared.prime_generator(100)))
    return count_hamming(primes, max)
    

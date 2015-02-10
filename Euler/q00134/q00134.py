#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared
import math

# Consider the consecutive primes p_1 = 19 and p_2 = 23.
# It can be verified that 1219 is the smallest number such that the
# last digits are formed by p_1 whilst also being divisible by p_2.
# In fact, with the exception of p_1 = 3 and p_2 = 5, for every pair
# of consecutive primes, p_2 > p_1, there exist values of n for which
# the last digits are formed by p_1 and n is divisible by p_2. Let S
# be the smallest of these values of n.
# Find Sum(S) for every pair of consecutive primes with 5 <= p_1 <= 1000000.


expected = 18613426663617118L

import pprint

def first(p1, p2):
    num_digits = int(math.log(p1, 10))

    S = 0
    this_digit = 0

    while this_digit <= num_digits:
        addition = p2 * 10 ** this_digit
        mod = 10 ** (this_digit + 1)
        p1_mod = p1 % mod

        while S % mod != p1_mod:
            S += addition

        this_digit += 1

    return S

def solve():
    top = 1000000

    g = shared.prime_generator()
    g.next() # 2
    g.next() # 3 

    total = 0
    p1 = g.next() # 5

    for p2 in g:
        if p1 > top: break
        total += first(p1, p2)
        p1 = p2
        
    return total


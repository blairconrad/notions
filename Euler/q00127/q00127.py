#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared
from fractions import gcd

# The radical of n, rad(n), is the product of distinct prime factors of n. For example, 504 = 2³ × 3² × 7, so rad(504) = 2 × 3 × 7 = 42.
# We shall define the triplet of positive integers (a, b, c) to be an abc-hit if:
# 
# * GCD(a, b) = GCD(a, c) = GCD(b, c) = 1
# * a < b
# * a + b = c
# * rad(abc) < c
# 
# For example, (5, 27, 32) is an abc-hit, because:
# 
# * GCD(5, 27) = GCD(5, 32) = GCD(27, 32) = 1
# * 5 < 27
# * 5 + 27 = 32
# * rad(4320) = 30 < 32
# 
# It turns out that abc-hits are quite rare and there are only thirty-one abc-hits for c < 1000, with ∑c = 12523.
# Find ∑c for c < 120000.
# 

expected = 18407904

find_factors = shared.Memoize(shared.find_factors, 1)

def distinct_factors(n):
    global known_primes
    return set(find_factors(n, known_primes))
    

@shared.Memoize
def rad(n):
    global known_primes
    #print a, b, c
    product = 1
    for f in distinct_factors(n):
        product *= f
    return product

def are_relatively_prime(a, b, c):
    return gcd(a, b) == 1 and gcd(a, c) == 1
           

def solve():

    max_c = 120000 #120000

    global known_primes
    known_primes = list(shared.prime_generator(max_c))


    rad_n_to_n_map = dict()

    for n in range(1,max_c+1):
        rad_n = rad(n)
        if rad_n_to_n_map.has_key(rad_n):
            rad_n_to_n_map[rad_n].append(n)
        else:
            rad_n_to_n_map[rad_n] = [n]

    total = 0
    for c in range(2, max_c+1):
        rad_c=rad(c)

        c_over_rad_c = c/rad_c
        if c_over_rad_c == 1:
            continue

        for rad_a in range(1, c_over_rad_c+1):
            for a in rad_n_to_n_map.get(rad_a, []):
                b = c - a
                if a >= b:
                    break

                if rad(b) * rad_a < c_over_rad_c and are_relatively_prime(a, b, c):
                    total += c
    return total


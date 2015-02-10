#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# There are some prime values, p, for which there exists a positive
# integer, n, such that the expression n**3 + n**2 * p is a perfect cube.
#
# For example, when p = 19, 8**3 + 8**2*19 = 12**3.
#
# What is perhaps most surprising is that for each prime with this
# property the value of n is unique, and there are only four such
# primes below one-hundred.
#
# How many primes below one million have this remarkable property?
# 

expected = 173

def solve():
    limit = 10**6

    primes = list(shared.prime_generator(limit))

    count = 0
    cube = 1
    k = 2
    while True:
        old_cube, cube = cube, k**3
        diff = cube - old_cube
        if diff > limit: break
        if diff in primes: count += 1

        k += 1
    
    return count



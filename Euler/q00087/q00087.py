#!/usr/bin/env python

import shared

expected = 1097343

def solve(n=50000000):
    g = shared.prime_generator()
    primes = []
    for p in g:
        if p**2 > n:
            break
        primes.append(p)

    nums = set()
    for p4 in primes:
        target4 = n - p4**4
        if target4 <= 0:
            break
        for p3 in primes:
            target3 = target4 - p3**3
            if target3 <= 0:
                break
            for p2 in primes:
                target2 = target3 - p2**2
                if target2 <= 0:
                    break
                else:
                    nums.add(n-target2)
    return len(nums)
    

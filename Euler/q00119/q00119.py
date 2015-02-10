#!/usr/bin/env python
# -*- coding: utf-8 -*-

import heapq

# The number 512 is interesting because it is equal to the sum of its
# digits raised to some power: 5 + 1 + 2 = 8, and 8**3 = 512. Another
# example of a number with this property is 614656 = 28**4.

# We shall define an to be the nth term of this sequence and insist
# that a number must contain at least two digits to have a sum.

# You are given that a2 = 512 and a10 = 614656.

# Find a30.

expected = 248155780267521

def sum_of_digits(n):
    result = 0
    while n > 0:
        n, digit = divmod(n, 10)
        result += digit
    return result

def is_power_of(n, base):
    exp = 1
    prospective_n = base
    while prospective_n < n:
        prospective_n *= base
        exp += 1
    if prospective_n == n:
        #print n, base, exp
        return True
    return False
    

def solve():
    winners = set()
    candidates = [(16,2,4),(27,3,3)]
    heapq.heapify(candidates)
    
    num_found = 0
    
    while len(winners) < 30:
        number, base, power = heapq.heappop(candidates)
        if power == 3:
            # we'll need a new candidate, and no answers are a power less than 3
            # (and there are only 3 of those or so....)
            heapq.heappush(candidates, ((base+1)**power, base+1, power))
        heapq.heappush(candidates, (number * base, base, power+1))

        s_d = sum_of_digits(number)
        if s_d == 1: continue
        if is_power_of(number, s_d):
            winners.add(number)

    return max(winners)

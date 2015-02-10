#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Find the number of integers 1 < n < 10^(7), for which n and n + 1 have
# the same number of positive divisors. For example, 14 has the positive
# divisors 1, 2, 7, 14 while 15 has 1, 3, 5, 15

import math

expected = 986262

def solve():
    min =  2
    max = 10**7

    divisors = [2] * (max+1)
    limit = int(math.sqrt(max))
    for step in range(2, limit+1):
        index = step*step
        divisors[index] -= 1 # only add one for the square
        while index < len(divisors):
            divisors[index] += 2
            index += step
    
    return sum((divisors[i] == divisors[i+1] for i in xrange(2, max)))


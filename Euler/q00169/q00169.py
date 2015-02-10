#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared
import math

# Define f(0)=1 and f(n) to be the number of different ways n can be expressed as a sum of integer powers of 2 using each power no more than twice.
# For example, f(10)=5 since there are five different ways to express 10:
# <p style="margin-left:50px;">1 + 1 + 8

# 1 + 1 + 4 + 4
1 + 1 + 2 + 2 + 4

# 2 + 4 + 4

# 2 + 8
# What is f(10**25)?
# 


expected = 178653872807L

@shared.Memoize
def f(n, power_of_two, reps):
    if (2+reps) * power_of_two - 2 < n: return 0
    if reps * power_of_two > n: return 0
    if n == power_of_two *reps: return 1
    n -= reps * power_of_two
    power_of_two /= 2
    r= f(n, power_of_two, 2) + \
           f(n, power_of_two, 1) + \
           f(n, power_of_two, 0)
    return r

def solve():
    n = 10**25
    power_of_two = 2**(int(math.log(n,2)))
    return f(n, power_of_two, 2) + f(n, power_of_two, 1) + f(n, power_of_two, 0)



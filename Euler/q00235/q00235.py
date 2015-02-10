#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# 
# Given is the arithmetic-geometric sequence u(k) = (900-3k)r**k-1.

# Let s(n) = Sum(k=1...n)u(k).
# 
# Find the value of r for which s(5000) = -600,000,000,000.
# 
# Give your answer rounded to 12 places behind the decimal point.

expected = '1.002322108633'

TOO_LOW = 0
TOO_HIGH = 1

def s(n, r):
    result = 0
    k = 1
    while k <= n:
        result += (900 - 3*k) * r**(k-1)
        if result < -6 * 10**11:
            return TOO_HIGH
        k += 1
    return TOO_LOW

def solve():

    r_max = 10**14
    r_min = 0

    while r_max - r_min > 1:
        r = 1 + float(r_max + r_min)/2/10**15
        result =  s(5000, r)
        if result == TOO_HIGH:
            r_max = (r_max + r_min)/2
        else:
            r_min = (r_max + r_min)/2

    return '%.12f' % r

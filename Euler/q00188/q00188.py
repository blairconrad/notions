#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# The hyperexponentiation or tetration of a number a by a positive
# integer b, denoted by a^^b or **ba, is recursively defined by:
# a^^1 = a,
# a^^(k+1) = a**(a^^k).
# 
# Thus we have e.g. 3^^2 = 3**3 = 27, hence 3^^3 = 3**27 = 7625597484987 and 3^^4 is roughly 10**3.6383346400240996*10^12.
# Find the last 8 digits of 1777^^1855.

expected = 95962097

def solve():
    bound = 10**8
    a = 1777
    b = 1855
    answer = 1
    while b > 0:
        answer = pow(a, answer, bound)
        b -= 1
    return answer


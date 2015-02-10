#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# In the hexadecimal number system numbers are represented using 16
# different digits: The hexadecimal number AF when written in the
# decimal number system equals 10x16+15=175.  In the 3-digit
# hexadecimal numbers 10A, 1A0, A10, and A01 the digits 0,1 and A are
# all present.

# Like numbers written in base ten we write hexadecimal numbers
# without leading zeroes.  How many hexadecimal numbers containing at
# most sixteen hexadecimal digits exist with all of the digits 0,1,
# and A present at least once?

# Give your answer as a hexadecimal number.  (A,B,C,D,E and F in upper
# case, without any leading or trailing code that marks the number as
# hexadecimal and without leading zeroes , e.g. 1A3F and not: 1a3f and
# not 0x1a3f and not $1A3F and not #1A3F and not 0000001A3F)

expected = '3D58725572C62302'

def f(k, n):
    if n < k: return 0
    if n == k: return shared.factorial(k)
    if k == 0: return 16**n
    return k * f(k-1, n-1) + (16-k) * f(k, n-1)

def solve():
    n = 16
    # disallow starting with by saying we can start with 1, A, or 13 others
    return '%X' % sum((2 * f(2, n-1) + 13 * f(3, n-1) for n in range(3,n+1)))
               


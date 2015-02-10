#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

expected = 2906969179

def is_palindrome(n):
    s = str(n)
    return s == s[::-1]

def solve():
    max_length = 8
    max_n = 10**max_length
    
    palindromes = set()
    max_m = int(math.sqrt(max_n))
    for m in xrange(1, max_m):
        total = m*m
        n = m
        while True:
            n += 1
            total += n*n
            if total > max_n: break
            if is_palindrome(total):
                palindromes.add(total)
    return sum(palindromes)

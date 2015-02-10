#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# How many 20 digit numbers n (without any leading zero) exist such
# that no three consecutive digits of n have a sum greater than 9?

expected = 378158756814587


@shared.Memoize
def f(two_ago, one_ago, num_digits):
    if num_digits == 0: return 1
    if num_digits == 1: return 9 - two_ago - one_ago + 1
    count = 0
    for next_digit in range(9 - two_ago - one_ago + 1):
        count += f(one_ago, next_digit, num_digits - 1)
    return count

def solve():
    n = 20
    return  sum((f(0, k, 19) for k in range(1, 10)))


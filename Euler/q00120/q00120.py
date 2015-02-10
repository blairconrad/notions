#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Let r be the remainder when (a-1)ⁿ + (a+1)ⁿ is divided by a².
#
# For example, if a = 7 and n = 3, then r = 42: 6³ + 8³ = 728 ≡ 42 mod 49. And as n varies, so too will r, but for a = 7 it turns out that r_max = 42.
#
# For 3 ≤ a  ≤ 1000, find  ∑r_max.

import shared

expected = 333082500

def solve():
    # using math, the sum (mod a²) is either 2an, when n is odd, or 2 when n is even
    # in all cases, there is at least one 2an that's bigger than 2
    return sum((max(((2 * a * n) % (a*a) for n in range(1, a))) for a in range(3, 1001)))


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# If a box contains twenty-one coloured discs, composed of fifteen
# blue discs and six red discs, and two discs were taken at random, it
# can be seen that the probability of taking two blue discs, P(BB) =
# (15/21)×(14/20) = 1/2.
#
# The next such arrangement, for which there is exactly 50% chance of
# taking two blue discs at random, is a box containing eighty-five
# blue discs and thirty-five red discs.
#
# By finding the first arrangement to contain over 10^(12) =
# 1,000,000,000,000 discs in total, determine the number of blue discs
# that the box would contain.

expected = 756872327473L

# Farey primes to bind 0.5**0.5
# We can un-lowest-form the fractions by multiplying the big one by the difference
# between the low fraction's numerator and denominator
#
# This solution takes like 12 steps.... very satisfying

def solve():
    min = 10**12
    low_num = 0
    low_denom = 1
    high_num = 1
    high_denom = 1

    i = 0
    while i < True:
        mediant_num = low_num + high_num
        mediant_denom = low_denom + high_denom
        if mediant_num * mediant_num * 2 > mediant_denom * mediant_denom:
            high_num, high_denom = mediant_num, mediant_denom
        else:
            low_num, low_denom = mediant_num, mediant_denom

        if low_num * high_num * 2 == low_denom * high_denom:
            total = high_denom * (low_denom - low_num)
            if total >= min and total == 1 +  low_denom * (high_denom - high_num):
                return high_num * (low_denom - low_num)


#!/usr/bin/env python

import sys
import datetime
import shared
import pprint

# Some positive integers n have the property that the sum [ n +
# reverse(n) ] consists entirely of odd (decimal) digits. For
# instance, 36 + 63 = 99 and 409 + 904 = 1313. We will call such
# numbers reversible; so 36, 63, 409, and 904 are reversible. Leading
# zeroes are not allowed in either n or reverse(n).

# There are 120 reversible numbers below 10^3

# How many reversible numbers are there below 10^9

expected = 608720


def solve():
    max_length = 9

    def num_reversible_no_carry(n):
        if n % 2: return 0
        return 20 * 30 ** (n/2)

    def num_reversible_carry(n):
        # if this exists, it's a single digit in the middle, less than 5 so there's no carry
        # then next to it, a pair whose sum is odd and has a carry
        # if there are more digits, the next two rings are
        # a pair that sum to be even, no carry and a pair that sum to be odd, with carry
        # the last two rings repeat outward and have 25 and 20 possibilities, respectively
        if n % 4 == 3:
            return 100 * (25*20)**((n-3)/4)
        return 0

    count = 0 
    for length in range(2, max_length+1):
        reversible_with_no_carry = num_reversible_no_carry(length-2)
        reversible_with_carry = num_reversible_carry(length)
        count += reversible_with_no_carry + reversible_with_carry

    return count

# why is num_reversible_no_carry for length 4 600?
# why?

# totals by length (cumulative)
# 2 20
# 3 120
# 4 720
# 5 720
# 6 18720
# 7 68720
# 8 608720
# 9 608720

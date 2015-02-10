#!/usr/bin/env python

import shared

# We shall say that an n-digit number is pandigital if it makes use of
# all the digits 1 to n exactly once. For example, 2143 is a 4-digit
# pandigital and is also prime.
#
# What is the largest n-digit pandigital prime that exists?

# can't be 8 or 9 digits, as would be a multiple of 9

expected = '7652413'

def solve():
    for num in shared.pick_without_replacement('7654321', 7):
        if shared.is_prime(int(num)):
            return num

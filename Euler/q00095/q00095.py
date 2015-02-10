#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared
import itertools

# The proper divisors of a number are all the divisors excluding the
# number itself. For example, the proper divisors of 28 are 1, 2, 4,
# 7, and 14. As the sum of these divisors is equal to 28, we call it a
# perfect number.

# Interestingly the sum of the proper divisors of 220 is 284 and the
# sum of the proper divisors of 284 is 220, forming a chain of two
# numbers. For this reason, 220 and 284 are called an amicable pair.

# Perhaps less well known are longer chains. For example, starting
# with 12496, we form a chain of five numbers:

# 12496 -> 14288 -> 15472 -> 14536 -> 14264 (-> 12496 -> ...)

# Since this chain returns to its starting point, it is called an
# amicable chain.

# Find the smallest member of the longest amicable chain with no
# element exceeding one million.


expected = 14316


def sum_divisors(n, primes):
    sum = 1
    for p in primes:
        if p*p > n: break
        quot, rem = divmod(n, p)
        
        if rem == 0:
            last_sum = sum
            while rem == 0:
                last_sum *= p
                sum += last_sum
                n = quot
                quot, rem = divmod(n, p)
            if n == 1: return sum
            return sum * sum_divisors(n, primes)

    return sum * (n+1)
            

sum_divisors = shared.Memoize(sum_divisors, 1)

def solve():
    n = 10**6
    primes = []
    for p in shared.prime_generator(n**0.5):
        primes.append(p)
    longest = 0
    smallest = n

    for i in xrange(2, n+1):
        friends = [i]
        s_o_f = sum_divisors(i, primes) - i

        while 1 < s_o_f <= n and s_o_f not in friends:
            friends.append(s_o_f)
            s_o_f = sum_divisors(s_o_f, primes) - s_o_f

        if s_o_f == i:
            if len(friends) > longest:
                longest = len(friends)
                smallest = min(friends)
            elif len(friends) == longest:
                smallest = min(min(friends), smallest)
    return smallest


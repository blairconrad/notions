#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# Considering 4-digit primes containing repeated digits it is clear
# that they cannot all be the same: 1111 is divisible by 11, 2222 is
# divisible by 22, and so on. But there are nine 4-digit primes
# containing three ones:
#
# 1117, 1151, 1171, 1181, 1511, 1811, 2111, 4111, 8111
#
# We shall say that M(n, d) represents the maximum number of repeated
# digits for an n-digit prime where d is the repeated digit, N(n, d)
# represents the number of such primes, and S(n, d) represents the sum
# of these primes.
#
# So M(4, 1) = 3 is the maximum number of repeated digits for a
# 4-digit prime where one is the repeated digit, there are N(4, 1) = 9
# such primes, and the sum of these primes is S(4, 1) = 22275. It
# turns out that for d = 0, it is only possible to have M(4, 0) = 2
# repeated digits, but there are N(4, 0) = 13 such cases.

# In the same way we obtain the following results for 4-digit primes.

# |Digit, d |M(4, d) |N(4, d) |S(4, d) 
#	|0	|2	|13	|67061 
#	|1	|3	|9	|22275 
#	|2	|3	|1	|2221 
#	|3	|3	|12	|46214 
#	|4	|3	|2	|8888 
#	|5	|3	|1	|5557 
#	|6	|3	|1	|6661 
#	|7	|3	|9	|57863 
#	|8	|3	|1	|8887 
#	|9	|3	|7	|48073 
# For d = 0 to 9, the sum of all S(4, d) is 273700.
# Find the sum of all S(10, d).
# 

expected = 612407567715

def take_away_digit(inputs, digit):
    replacement_digits = range(10)[:digit] + range(10)[digit+1:]
    digit = str(digit)
    result = []
    for n in inputs:
        for i in range(len(n)):
            if n[i] == digit:
                for d in replacement_digits:
                    new_n = n[:i] + str(d) + n[i+1:]
                    if not new_n.startswith('0'):
                        result.append(new_n)
    return result

def solve():
    num_digits = 10
    max_prime = 10 ** (num_digits+1)
    primes = list(shared.prime_generator(int(max_prime**0.5)))
    

    big_sum = 0
    for digit in range(10):
        seed = str(digit)*num_digits
        best = [seed]
        while True:
            total = 0
            for n in best:
                n = int(n)
                if shared.is_prime(n, primes):
                    total += n
            if total > 0:
                big_sum += total
                break
            new_best = []
            for b in best:
                new_best.extend(take_away_digit(best, digit))
            best = set(new_best)

    return big_sum


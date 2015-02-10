#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared
import math
import itertools

# Using all of the digits 1 through 9 and concatenating them freely to
# form decimal integers, different sets can be formed. Interestingly
# with the set {2,5,47,89,631}, all of the elements belonging to it
# are prime.  How many distinct sets containing each of the digits one
# through nine exactly once contain only prime elements?

expected = 'hippo'

global known_primes

def combine_digits(digits):
    result = 0
    for digit in digits:
        result = result * 10 + digit
    return result

def group_into_primes(digits, last_prime):
    global known_primes

    if not digits:
        return 1
    
    count = 0
    for first_group_length in range(1, len(digits)+1):
        number = combine_digits(digits[:first_group_length])
        if number > last_prime and shared.is_prime(number, known_primes):
            count += group_into_primes(digits[first_group_length:], number)

    return count

def solve():
    global known_primes
    
    top_digit = 9
    known_primes= list(shared.prime_generator(int(math.sqrt(10**top_digit))))
    digits = range(1, top_digit+1)

    all_sets = set()

    total = 0
    for d in itertools.permutations(digits, len(digits)):
        total += group_into_primes(d, 1)

    return total

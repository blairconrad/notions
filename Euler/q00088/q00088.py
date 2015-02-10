#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# A natural number, N, that can be written as the sum and product of
# a given set of at least two natural numbers, {a_1, a_2, ... , a_k}
# is called a product-sum number: N = a_1 + a_2 + ... + a_k = a_1 *
# a_2 * ... * a_k.
#
# For example, 6 = 1 + 2 + 3 = 1 * 2 * 3.

# For a given set of size, k, we shall call the smallest N with this
# property a minimal product-sum number. The minimal product-sum
# numbers for sets of size, k = 2, 3, 4, 5, and 6 are as follows.
# k=2: 4 = 2 * 2 = 2 + 2
# k=3: 6 = 1 * 2 * 3 = 1 + 2 + 3
# k=4: 8 = 1 * 1 * 2 * 4 = 1 + 1 + 2 + 4
# k=5: 8 = 1 * 1 * 2 * 2 * 2  = 1 + 1 + 2 + 2 + 2
# k=6: 12 = 1 * 1 * 1 * 1 * 2 * 6 = 1 + 1 + 1 + 1 + 2 + 6

# Hence for 2<=k<=6, the sum of all the minimal product-sum numbers is 4+6+8+12 = 30; note that 8 is only counted once in the sum.
# In fact, as the complete set of minimal product-sum numbers for 2<=k<=12 is {4, 6, 8, 12, 15, 16}, the sum is 61.
# What is the sum of all the minimal product-sum numbers for 2<=k<=12000?
# 

expected = 7587457



def make_shortest_sets(n):
    divisors = shared.find_divisors(n)
    results = []
    for i in range(1, (len(divisors)+1)/2):
        results .append(
            [1] * (n - divisors[i] - divisors[-i-1]) + [divisors[i], divisors[-i-1]])
    return results
    
def solve():
    minimal_set_sizes = {}

    translations = {}

    top = 12000
    done = False
    n = 2
    while not done:
        short_sets = make_shortest_sets(n)
        if short_sets:
            translations_for_n = set()
            for short_set in short_sets:
                translations_for_n.add(len(short_set))
                for factor in short_set:
                    if factor > 1:
                        expansions = translations.get(factor, [])
                        for expansion in expansions:
                            translations_for_n.add(len(short_set) - 1 + expansion)
            translations[n] = translations_for_n
            for k in translations_for_n:
                minimal_set_sizes[k] = min(n, minimal_set_sizes.get(k, n))

        if len(minimal_set_sizes) >= top-1:
            done = True
            for i in range(top, 1, -1):
                if i not in minimal_set_sizes:
                    done = False
                    break
        n += 1
    
    return sum(set((minimal_set_sizes[i] for i in range(2, top+1))))

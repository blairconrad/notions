#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import shared
import itertools

# Let S(A) represent the sum of elements in set A of size n. We shall call it a special sum set if for any two non-empty disjoint subsets, B and C, the following properties are true:
# # S(B) != S(C); that is, sums of subsets cannot be equal.
# # If B contains more elements than C then S(B) > S(C).
# If S(A) is minimised for a given n, we shall call it an optimum special sum set. The first five optimum special sum sets are given below.
# n = 1: {1}

# n = 2: {1, 2}

# n = 3: {2, 3, 4}

# n = 4: {3, 5, 6, 7}

# n = 5: {6, 9, 11, 12, 13} = 51

# n = 6: {11, 18, 19, 20, 22, 25}
              
# It seems that for a given optimum set, A = {a_1, a_2, ... , a_n},
# the next optimum set is of the form B = {b, a_1+b, a_2+b,
# ... ,a_n+b}, where b is the "middle" element on the previous row.
# By applying this "rule" we would expect the optimum set for n = 6 to
# be A = {11, 17, 20, 22, 23, 24}, with S(A) = 117. However, this is
# not the optimum set, as we have merely applied an algorithm to
# provide a near optimum set. The optimum set for n = 6 is A = {11,
# 18, 19, 20, 22, 25}, with S(A) = 115 and corresponding set string:
# 111819202225.  Given that A is an optimum special sum set for n = 7,
# find its set string.

expected = '20313839404245'

# S(B) != S(C) for any subset
# S(B) > S(C> if |B| > |C|
# so, the 0th and 1st elements sum to more than the last one. Good to know
# so again, the 1st element > last/2


def is_special_sum_set(A):
    len_a = len(A)
    if len_a < 3:
        return True
    A=set(A)
    
    for n in range(2, len(A)):
        for base_set in itertools.combinations(A, n):
            base_sum = sum(base_set)
            #print base_set, base_sum

            remainder = A - set(base_set)
            #print 'remainder', remainder
            for smaller_set_size in range(1, n):
                for smaller_set in itertools.combinations(remainder, smaller_set_size):
                    if sum(smaller_set) >= base_sum:
                        return False
            for equal_set in itertools.combinations(remainder, n):
                if sum(equal_set) == base_sum:
                    return False
                    
    return True     

@shared.Memoize
def find_special_sum_set(total, size, highest):
    #print total, size, highest
    if size == 1:
        if highest == total:
            return [[total]]
        return []

    sets = []

    remaining = total - highest
    if remaining <= 0: return sets
    next_highest = highest - 1
    next_size = size-1

    lower_bound = 0
    if next_size >= 2:
        lower_bound = highest/2
    while next_highest > lower_bound and next_size * next_highest - (next_size)*(next_size-1)/2 >= remaining:

        for special_set in find_special_sum_set(remaining, next_size, next_highest):
            candidate = special_set + [highest]
            if is_special_sum_set(candidate):
                #print candidate
                sets.append(candidate)
                
        next_highest -= 1
    return sets

def solve():
    size  = 7

    
    total = size*(size+1)/2 # could be a lot higher, I'm thinking. This is probably no better than 0.

    best =[]
    
    while True:
        best = []
        for highest in range(1, total):
            for special_sum_set in find_special_sum_set(total, size, highest):
                if not best or (sum(best) > sum(special_sum_set)):
                    best = special_sum_set
        if best:
            return ''.join(map(str,best))
        total += 1


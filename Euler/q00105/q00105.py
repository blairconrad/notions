#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared
import itertools

# Let S(A) represent the sum of elements in set A of size n. We shall
# call it a special sum set if for any two non-empty disjoint subsets,
# B and C, the following properties are true:
# * S(B) != S(C); that is, sums of subsets cannot be equal.
# * If B contains more elements than C then S(B) > S(C).

# For example, {81, 88, 75, 42, 87, 84, 86, 65} is not a special sum
# set because 65 + 87 + 88 = 75 + 81 + 84, whereas {157, 150, 164,
# 119, 79, 159, 161, 1 39, 158} satisfies both rules for all possible
# subset pair combinations and S(A) = 1286.

# Using sets.txt, a 4K text file with one-hundred sets containing
# seven to twelve elements (the two examples given above are the first
# two sets in the file), identify all the special sum sets, A_1, A_2,
# ..., A_k, and find the value of S(A_1) + S(A_2) + ... + S(A_k).
# NOTE: This problem is related to problems 103 and 106.

expected = 73702

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

def solve():
    print
    total = 0
    for line in file('sets.txt'):
        candidate = map(int, line.strip().split(','))
        if is_special_sum_set(candidate):
            total += sum(candidate)
    return total



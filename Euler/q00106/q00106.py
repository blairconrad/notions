#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared
import itertools

# Let S(A) represent the sum of elements in set A of size n. We shall call it a special sum set if for any two non-empty disjoint subsets, B and C, the following properties are true:
# <ol style="list-style-type:lower-roman;">
# <li>S(B) != S(C); that is, sums of subsets cannot be equal.</li>
# <li>If B contains more elements than C then S(B) > S(C).</li>
# </ol>
# For this problem we shall assume that a given set contains n strictly increasing elements and it already satisfies the second rule.
# Surprisingly, out of the 25 possible subset pairs that can be obtained from a set for which n = 4, only 1 of these pairs need to be tested for equality (first rule). Similarly, when n = 7, only 70 out of the 966 subset pairs need to be tested.
# For n = 12, how many of the 261625 subset pairs that can be obtained need to be tested for equality?
# <p class="info">NOTE: This problem is related to problems <a href="index.php?section=problems&amp;id=103">103</a> and <a href="index.php?section=problems&amp;id=105">105</a>.

expected = 21384

def solve():
    print

    n = 12
    
    have_to_check_count = 0 

    for subset_size in range(2, n/2+1):
        for lowest in range(n-2*subset_size+1):
            items = set(range(lowest+1,n))
            large_sets = itertools.combinations(items, subset_size)

            for large_set in large_sets:
                small_sets = itertools.combinations(items-set(large_set), subset_size-1)
                large_set = list(large_set)
                large_set.sort()

                for small_set in small_sets:
                    small_set = [lowest,] + list(small_set)
                    small_set.sort()

                    for i in range(subset_size):

                        if small_set[i] > large_set[i]:
                            have_to_check_count += 1
                            break

    return have_to_check_count


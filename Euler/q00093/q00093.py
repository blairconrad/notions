#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator
import itertools

# By using each of the digits from the set, {1, 2, 3, 4}, exactly
# once, and making use of the four arithmetic operations (+, , *, /)
# and brackets/parentheses, it is possible to form different positive
# integer targets.

# For example,

# 8 = (4 * (1 + 3)) / 2
# 14 = 4 * (3 + 1 / 2)
# 19 = 4 * (2 + 3)  1
# 36 = 3 * 4 * (2 + 1)

# Note that concatenations of the digits, like 12 + 34, are not
# allowed.

# Using the set, {1, 2, 3, 4}, it is possible to obtain thirty-one
# different target numbers of which 36 is the maximum, and each of the
# numbers 1 to 28 can be obtained before encountering the first
# non-expressible number.

# Find the set of four distinct digits, a < b < c < d, for which the
# longest set of consecutive positive integers, 1 to n, can be
# obtained, giving your answer as a string: abcd.

expected = 1258


def expand(equations):
    operators = [operator.add, operator.sub, operator.mul, operator.div]
    while equations:
        equation = equations.pop()
        for op in operators:
            #print op, equation
            for pos in range(len(equation)-1):
                new_equation = equation[:]
                try:
                    result = apply(op, [float(new_equation[pos]), float(new_equation[pos+1])])
                except ZeroDivisionError:
                    continue

                # evaluating the operator here has the effect of
                # parenthesising the arguments 
                new_equation[pos:pos+2] = [result]
                if len(new_equation) > 1:
                    equations.append(new_equation)
                else:
                    if int(new_equation[0]) == new_equation[0] and new_equation[0] > 0:
                        yield new_equation[0]


def solve():
    max_n = 0
    best_subset = []
    
    digits = range(10)

    for subset in itertools.combinations(digits, 4):
        #print subset

        equations = []
        for i in itertools.permutations(subset, 4):
            equations.append(list(i))


        results = set()
        for result in expand(equations):
            results.add(result)


        n = 1
        while n in results:
            if n > max_n:
                max_n = n
                best_subset = subset
            n += 1

    result = 0
    for i in best_subset:
        result = result * 10 + i
    return result







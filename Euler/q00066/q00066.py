#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import fractions
import math

# Consider quadratic Diophantine equations of the form:

# x² - D*y² = 1

# For example, when D=13, the minimal solution in x is 649² - 13 * 1802 = 1.

# It can be assumed that there are no solutions in positive integers when D is square.

# By finding minimal solutions in x for D = {2, 3, 5, 6, 7}, we obtain the following:

# 3² - 2 * 2² = 1
# 2² - 3 * 1² = 1
# 9² - 5 * 4² = 1
# 5² - 6 * 2² = 1
# 8² - 7 * 3² = 1

# Hence, by considering minimal solutions in x for D ≤ 7, the largest x is obtained when D=5.

# Find the value of D ≤ 1000 in minimal solutions of x for which the largest value of x is obtained.

expected = 661

global primes

def is_square(n):
    s = math.sqrt(n)
    return int(s) == s

def find_continued_fraction_parts_of_square_root(base):

    root = math.sqrt(base)
    
    # calculate the first term, which won't be part of the cycle
    denominator = 1
    numerator = int(math.floor(root))

    yield numerator
    
    plus = -numerator

    i = 0
    while True:
        new_denom = base - plus*plus
        common = fractions.gcd(new_denom, denominator)

        top = (denominator * (root - plus))/common
        denominator = new_denom/common    

        numerator = int(math.floor(top/denominator))
        plus = -plus - denominator * numerator

        yield numerator

def solve(maxD=1000):

    best_x = 0
    best_d = 0

    for d in range(2, maxD+1):
        if is_square(d): continue
        
        all_bs = find_continued_fraction_parts_of_square_root(d)

        b = all_bs.next()
        xs = [b]
        ys = [1]

        if xs[-1]*xs[-1] - d * ys[-1]*ys[-1] != 1:
            b = all_bs.next()
            xs.append(b * xs[0]+1)
            ys = [1, b]

            if xs[-1]*xs[-1] - d * ys[-1]*ys[-1] != 1:
                i = 2
                while True:
                    b = all_bs.next()
                    xs.append(b * xs[-1] + xs[-2])
                    ys.append(b * ys[-1] + ys[-2])

                    if xs[-1]*xs[-1] - d * ys[-1]*ys[-1] == 1:
                            break
                    i += 1

        if xs[-1] > best_x:
            best_x = xs[-1]
            best_d = d

    return best_d

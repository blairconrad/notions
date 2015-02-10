#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared
import math
# The binomial coefficients nCk can be arranged in triangular form, Pascal's triangle, like this:

# 1	
# 1	1	
# 1	2	1	
# 1	3	3	1	
# 1	4	6	4	1	
# 1	5	10	10	5	1	
# 1	6	15	20	15	6	1	
# 1	7	21	35	35	21	7	1
# .........

# It can be seen that the first eight rows of Pascal's triangle
# contain twelve distinct numbers: 1, 2, 3, 4, 5, 6, 7, 10, 15, 20, 21
# and 35.

# A positive integer n is called squarefree if no square of a prime
# divides n. Of the twelve distinct numbers in the first eight rows of
# Pascal's triangle, all except 4 and 20 are squarefree. The sum of
# the distinct squarefree numbers in the first eight rows is 105.

# Find the sum of the distinct squarefree numbers in the first 51 rows
# of Pascal's triangle.

expected = 34029210557338

def solve():
    num_rows = 51

    distinct = set()
    row = 1
    p_triangle = [1]
    while row < num_rows:

        p_triangle.append(0)

        for i in range(len(p_triangle)-1, 0, -1):
            p_triangle[i] = p_triangle[i] + p_triangle[i-1]
            distinct.add(p_triangle[i])
        row += 1


    square_primes = []
    total = sum(distinct)
    m = max(distinct)
    for p in shared.prime_generator(math.sqrt(m)):
        if p*p > m: break
        square_primes.append(p*p)

    distinct = list(distinct)
    distinct.sort()
    
    for d in distinct:
        for s in square_primes:
            if not d % s:
                total -= d
                break
    return total
                

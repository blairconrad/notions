#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared
import math

def frac(n,d):
    return float(n)/d

# If we list the set of reduced proper fractions for d <= 8 in
# ascending order of size, we get:

# 1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5,
# 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

# It can be seen that there are 3 fractions between 1/3 and 1/2.

# How many fractions lie between 1/3 and 1/2 in the sorted set of
# reduced proper fractions for d <= 10,000?

def solve(n):
    count = 0
    one_third = frac(1,3)
    one_half = frac(1,2)
    for denom in range(5,n+1):
        for num in range(int(math.ceil(frac(denom,3))), (denom+1)/2):
            if shared.gcd(num,denom) == 1:
                count += 1
    return count

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 10000
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 5066251 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())


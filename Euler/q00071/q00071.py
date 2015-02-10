#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared
import bisect
import math

# Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1, it is called a reduced proper fraction.
# If we list the set of reduced proper fractions for d <= 8 in ascending order of size, we get:
# 1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8
# It can be seen that 2/5 is the fraction immediately to the left of 3/7.
# By listing the set of reduced proper fractions for d <= 1,000,000 in ascending order of size, find the numerator of the fraction immediately to the left of 3/7.

def frac(n,d):
    return (float(n)/d, (n,d))

def solve(n):
    three_sevenths = frac(3,7)
    fractions = [frac(2,5), three_sevenths]

    for d in range(9,n+1):
        three_seven_index = bisect.bisect_left(fractions, three_sevenths)
        prev_frac = fractions[three_seven_index-1]
        #print prev_frac

        for n in range(int(math.ceil(prev_frac[0] * d))-1, int(math.ceil(three_sevenths[0] * d))+1):
            #print 'n =', n
            if shared.gcd(n,d) == 1:
                new_frac = frac(n,d)
                if prev_frac < new_frac < three_sevenths:
                    #print n,d
                    bisect.insort(fractions, new_frac)
    index = bisect.bisect_left(fractions, three_sevenths)
    return fractions[index-1][1][0]


def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 1000000
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 428570 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())


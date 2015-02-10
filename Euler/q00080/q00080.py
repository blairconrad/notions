#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared




# It is well known that if the square root of a natural number is not
# an integer, then it is irrational. The decimal expansion of such
# square roots is infinite without any repeating pattern at all.
#
# The square root of two is 1.41421356237309504880..., and the digital
# sum of the first one hundred decimal digits is 475.
#
# For the first one hundred natural numbers, find the total of the
# digital sums of the first one hundred decimal digits for all the
# irrational square roots.

def sqrt(n):
    n *= 10**202
    best_guess = 0
    for i in range(101,-0,-1):
        for d in range(1,10):
            guess = best_guess + 10**i
            if guess ** 2 <= n:
                best_guess = guess
            else:
                break
    return best_guess

def solve(max):
    total = 0
    for i in range(2, max+1):
        if i in [x*x for x in range(2,11)]:
            continue
        si = str(sqrt(i))[:100]
        total += sum((ord(c) for c in si)) - 100*ord('0')
    return total
        
def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 100
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 40886 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())


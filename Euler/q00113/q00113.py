#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

# Working from left-to-right if no digit is exceeded by the digit to
# its left it is called an increasing number; for example, 134468.

# Similarly if no digit is exceeded by the digit to its right it is
# called a decreasing number; for example, 66420.

# We shall call a positive integer that is neither increasing nor
# decreasing a "bouncy" number; for example, 155349.

# As n increases, the proportion of bouncy numbers below n increases
# such that there are only 12951 numbers below one-million that are
# not bouncy and only 277032 non-bouncy numbers below 10^(10).

# How many numbers below a googol (10^(100)) are not bouncy?

def num_flat(num_digits):
    return 9

def num_increasing(min_digit, num_digits):
    #print min_digit, num_digits
    if num_digits == 1:
        return 10-min_digit

    return sum((num_increasing(d, num_digits-1) for d in range(min_digit, 10)))
num_increasing = shared.Memoize(num_increasing)

def num_decreasing(max_digit, num_digits):
    if num_digits == 1:
        return max_digit+1

    return sum((num_decreasing(d, num_digits-1) for d in range(max_digit+1)))
num_decreasing = shared.Memoize(num_decreasing)

def solve(num_digits):
    t = 9 # 1 digit
    for n in range(2, num_digits+1):
        t += sum((num_increasing(d, n-1) for d in range(1,10)))
        t += sum((num_decreasing(d, n-1) for d in range(1,10)))
        t -= 9
    return t

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
    assert 51161058134250 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())


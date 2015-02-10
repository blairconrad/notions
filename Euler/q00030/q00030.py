#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def sum_digit_power(num, power):
    total = 0
    while num > 0:
        num, rem = divmod(num, 10)
        total += rem ** power
    return total

def solve(n):
    total = 0
    
    for i in xrange(2, 1000000):
        if i == sum_digit_power(i, n):
            total += i
    return total
            
        

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 5
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 443839 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

